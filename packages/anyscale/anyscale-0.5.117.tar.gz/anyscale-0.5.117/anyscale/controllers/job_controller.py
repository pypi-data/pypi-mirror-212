from abc import ABC, abstractmethod
import asyncio
import contextlib
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import random
import string
import time
import traceback
from typing import Any, Callable, cast, Dict, List, Optional, Tuple, Type, Union
from urllib.parse import urlparse

import click
from pydantic import BaseModel, Extra, Field, root_validator
import requests
from requests.adapters import HTTPAdapter
import tabulate
from urllib3 import Retry
import yaml

from anyscale.api_utils.exceptions.log_retrieval_errors import (
    ExpectedLogRetrievalError,
    UnsupportedLogRetrievalMethodError,
    wrap_as_unsupported_log_retrieval_method_error,
    wrap_job_run_log_not_retrievable_on_active_cluster_error,
)
from anyscale.api_utils.job_logs_util import (
    _get_job_logs_from_storage_bucket,
    _get_logs_from_active_job_run,
)
from anyscale.api_utils.job_util import _is_production_job_on_v2_cloud
from anyscale.api_utils.logs_util import _stream_log_from_ray_websocket
from anyscale.cli_logger import LogsLogger
from anyscale.client.openapi_client import (
    ComputeTemplate,
    JobsLogsQueryInfo,
    ProductionJob,
    ProductionJobConfig,
)
from anyscale.client.openapi_client.models.create_internal_production_job import (
    CreateInternalProductionJob,
)
from anyscale.client.openapi_client.models.decorated_production_job import (
    DecoratedProductionJob,
)
from anyscale.client.openapi_client.models.ha_job_states import HaJobStates
from anyscale.cluster_compute import (
    get_cluster_compute_from_name,
    get_default_cluster_compute,
    register_compute_template,
)
from anyscale.cluster_env import (
    get_build_from_cluster_env_identifier,
    get_default_cluster_env_build,
    validate_successful_build,
)
from anyscale.controllers.base_controller import BaseController
from anyscale.project import (
    get_parent_cloud_id_and_name_of_project,
    get_proj_id_from_name,
    infer_project_id,
)
from anyscale.sdk.anyscale_client.models.job import Job
from anyscale.sdk.anyscale_client.models.jobs_query import JobsQuery
from anyscale.sdk.anyscale_client.models.jobs_sort_field import JobsSortField
from anyscale.sdk.anyscale_client.models.page_query import PageQuery
from anyscale.sdk.anyscale_client.models.sort_by_clause_jobs_sort_field import (
    SortByClauseJobsSortField,
)
from anyscale.sdk.anyscale_client.models.sort_order import SortOrder
from anyscale.shared_anyscale_utils.utils.byod import BYODInfo
from anyscale.util import (
    extract_versions_from_image_name,
    get_endpoint,
    handle_and_log_lines_in_click_exception,
    is_anyscale_workspace,
    poll,
    populate_dict_with_workspace_config_if_exists,
    PROJECT_NAME_ENV_VAR,
    validate_job_config_dict,
)
from anyscale.utils.connect_helpers import search_entities
from anyscale.utils.runtime_env import override_runtime_env_config
from anyscale.utils.workload_types import Workload


log = LogsLogger()

_TERMINAL_STATES = {
    HaJobStates.SUCCESS,
    HaJobStates.TERMINATED,
    HaJobStates.BROKEN,
    HaJobStates.OUT_OF_RETRIES,
}
_PENDING_STATES = {
    HaJobStates.PENDING,
    HaJobStates.AWAITING_CLUSTER_START,
    HaJobStates.ERRORED,
    HaJobStates.RESTARTING,
}


class MiniJobRun(BaseModel):
    last_job_run_id: str
    job_state: str
    error: Optional[str]


def _validate_conda_option(conda_option: Union[str, Dict]) -> Union[str, Dict]:
    """Parses and validates a user-provided 'conda' option.

    Can be one of three cases:
        1) A str that's the name of a pre-installed conda environment.
        2) A string pointing to a local conda environment YAML. In this case,
           the file contents will be read into a dict.
        3) A dict that defines a conda environment. This is passed through.
    """
    result = None
    if isinstance(conda_option, str):
        yaml_file = Path(conda_option)
        if yaml_file.suffix in (".yaml", ".yml"):
            if not yaml_file.is_file():
                raise click.ClickException(f"Can't find conda YAML file {yaml_file}.")
            try:
                result = yaml.safe_load(yaml_file.read_text())
            except Exception as e:  # noqa: BLE001
                raise click.ClickException(
                    f"Failed to read conda file {yaml_file}: {e}."
                )
        else:
            # Assume it's a pre-existing conda environment name.
            result = conda_option
    elif isinstance(conda_option, dict):
        result = conda_option

    return result


def _validate_pip_option(pip_option: Union[str, List[str]]) -> Optional[List[str]]:
    """Parses and validates a user-provided 'pip' option.

    Can be one of two cases:
        1) A List[str] describing the requirements. This is passed through.
        2) A string pointing to a local requirements file. In this case, the
           file contents will be read split into a list.
    """
    result = None
    if isinstance(pip_option, str):
        # We have been given a path to a requirements.txt file.
        pip_file = Path(pip_option)
        if not pip_file.is_file():
            raise click.ClickException(f"{pip_file} is not a valid file.")
        result = pip_file.read_text().strip().split("\n")
    elif isinstance(pip_option, list) and all(
        isinstance(dep, str) for dep in pip_option
    ):
        if len(pip_option) == 0:
            result = None
        else:
            result = pip_option

    return result


def _validate_py_modules(py_modules_option: List[str]) -> List[str]:
    for entry in py_modules_option:
        if "://" not in entry:
            raise click.ClickException(
                "Only remote URIs are currently supported for py_modules in the job "
                "config (not local directories). Please see "
                "https://docs.ray.io/en/master/handling-dependencies.html#remote-uris for supported options."
            )

    return py_modules_option


def _working_dir_is_remote_uri(working_dir: str) -> bool:
    return "://" in working_dir


def _validate_working_dir(working_dir_option: str) -> str:
    """If working_dir is a local directory, check that it exists."""
    # We have been given a path to a local directory.
    if (
        not _working_dir_is_remote_uri(working_dir_option)
        and not Path(working_dir_option).is_dir()
    ):
        raise click.ClickException(
            f"working_dir {working_dir_option} is not a valid local directory or remote URI."
        )

    return working_dir_option


def _validate_working_dir_and_upload_path(
    working_dir: Optional[str], upload_path: Optional[str]
):
    """Check that the combination of working_dir and upload_path is valid.

    Exception should be thrown if both working dir is a remote uri and upload path is defined
    Otherwise, all other permutations are valid
    """
    if (
        upload_path is not None
        and working_dir
        and _working_dir_is_remote_uri(working_dir)
    ):
        raise click.ClickException(
            f"`upload_path` was specified, but `working_dir` is not a local directory.  Recieved `upload_path`: {upload_path} and `working_dir`: {working_dir}."
        )
    elif upload_path is not None and not working_dir:
        raise click.ClickException(
            f"`upload_path` was specified, but no `working_dir` is defined. Recieved `upload_path`: {upload_path} and `working_dir`: None."
        )


def _validate_upload_path(upload_path: str) -> str:
    """Check that the upload path is a valid S3 or GS remote URI."""
    try:
        parsed_upload_path = urlparse(upload_path)
    except Exception as e:  # noqa: BLE001
        raise click.ClickException(
            f"Failed to parse `upload_path` {upload_path} as a URI (e.g. 's3://my_bucket/my_dir'): {e}"
        )
    if parsed_upload_path.scheme not in ["s3", "gs"]:
        raise click.ClickException(
            f"Only Amazon S3 (e.g. 's3://bucket', 's3://bucket/path') and Google Storage URIs (e.g. 'gs://bucket', 'gs://bucket/path') are supported. Received {upload_path}."
        )
    return upload_path


def _validate_env_vars(env_vars: Dict[str, str]) -> Dict[str, str]:
    for key, value in env_vars.items():
        if not isinstance(key, str):
            raise click.ClickException(
                f"env_vars key {key} is not a string. Please check the formatting."
            )
        if not isinstance(value, str):
            raise click.ClickException(
                f"env_vars value {value} is not a string. Please check the formatting."
            )

    return env_vars


def _validate_and_modify_runtime_env(runtime_env: Dict):
    """Validates, then modifies runtime_env in place.

    Raises: click.ClickException if the runtime env doesn't pass validation.
    """

    if "conda" in runtime_env:
        conda_option = runtime_env["conda"]
        if not isinstance(conda_option, (str, dict)):
            raise click.ClickException(
                f"runtime_env['conda'] must be str or dict, got type({conda_option})."
            )
        runtime_env["conda"] = _validate_conda_option(conda_option)
    if "pip" in runtime_env:
        pip_option = runtime_env["pip"]
        if not isinstance(pip_option, (str, list)):
            raise click.ClickException(
                f"runtime_env['pip'] must be str or list, got type({pip_option})."
            )
        runtime_env["pip"] = _validate_pip_option(runtime_env["pip"])
    if "py_modules" in runtime_env:
        py_modules_option = runtime_env["py_modules"]
        if not isinstance(py_modules_option, list):
            raise click.ClickException(
                f"runtime_env['py_modules'] must be list, got type({py_modules_option})."
            )
        runtime_env["py_modules"] = _validate_py_modules(py_modules_option)
    if "upload_path" in runtime_env:
        upload_path_option = runtime_env["upload_path"]
        if not isinstance(upload_path_option, str):
            raise click.ClickException(
                f"runtime_env['upload_path'] must be str, got type({upload_path_option})."
            )
        runtime_env["upload_path"] = _validate_upload_path(upload_path_option)
    if "working_dir" in runtime_env:
        working_dir_option = runtime_env["working_dir"]
        if not isinstance(working_dir_option, str):
            raise click.ClickException(
                f"runtime_env['working_dir'] must be str, got type({working_dir_option})."
            )
        runtime_env["working_dir"] = _validate_working_dir(working_dir_option)
    _validate_working_dir_and_upload_path(
        runtime_env.get("working_dir"), runtime_env.get("upload_path")
    )
    if "env_vars" in runtime_env:
        env_vars_option = runtime_env["env_vars"]
        if not isinstance(env_vars_option, dict):
            raise click.ClickException(
                f"runtime_env['env_vars'] must be dict, got type({env_vars_option})."
            )
        runtime_env["env_vars"] = _validate_env_vars(env_vars_option)


def _get_project_id_from_id_or_name(
    project_id: Optional[str] = None, project_name: Optional[str] = None
) -> Optional[str]:
    """
    Get project id from PROJECT_NAME_ENV_VAR or `project_id` or `project_name`
    fields in the job config. Return None if no project was specified by the user,
    and the default project will selected later in the job submit code.
    """
    if project_id and project_name:
        raise click.ClickException(
            "Only one of `project_id` or `project` can be provided in the config file. "
        )
    project_name_env_var = os.environ.get(PROJECT_NAME_ENV_VAR)
    if project_name_env_var:
        # Get project from environment variable regardless of if is provided in config
        project_id = get_proj_id_from_name(project_name_env_var)
    elif project_name:
        project_id = get_proj_id_from_name(project_name)
    return project_id


class BaseHAJobConfig(BaseModel):
    """
    Base job configuration for both Production Jobs and Services.
    """

    name: Optional[str] = Field(
        None,
        description="Name of job to be submitted. Default will be used if not provided.",
    )
    description: Optional[str] = Field(
        None,
        description="Description of job to be submitted. Default will be used if not provided.",
    )
    runtime_env: Optional[Dict[str, Any]] = Field(
        None,
        description="A ray runtime env json. Your entrypoint will be run in the environment specified by this runtime env.",
    )
    build_id: Optional[str] = Field(
        None,
        description="The id of the cluster env build. This id will determine the docker image your job is run on.",
    )
    cluster_env: Optional[str] = Field(
        None,
        description="The name of the cluster environment and build revision in format `my_cluster_env:1`.",
    )
    docker: Optional[str] = Field(None, description="Custom docker image name.")
    python_version: Optional[str] = Field(
        None, description="Python version for the custom docker image."
    )
    ray_version: Optional[str] = Field(
        None, description="Ray version for the custom docker image."
    )
    compute_config_id: Optional[str] = Field(
        None,
        description="The id of the compute configuration that you want to use. This id will specify the resources required for your job",
    )
    project_id: Optional[str] = Field(
        None,
        description="The id of the project you want to use. If not specified, and no project is inferred from the directory, no project will be used.",
    )
    workspace_id: Optional[str] = Field(
        None, description="The id of the workspace that this job is submitted from.",
    )
    project: Optional[str] = Field(
        None,
        description="The name of the project you want to use. If not specified, and no project is inferred from the directory, no project will be used.",
    )
    compute_config: Optional[Union[str, Dict[str, Any]]] = Field(
        None,
        description="The name of the compute configuration that you want to use. This will specify the resources required for your job."
        "This field also accepts a one-off config as a dictionary.",
    )
    cloud: Optional[str] = Field(
        None,
        description="The cloud name to specify a default compute configuration with. This will specify the resources required for your job",
    )
    max_retries: Optional[int] = Field(
        5,
        description="The number of retries this job will attempt on failure. Set to None to set infinite retries",
    )

    class Config:
        extra = Extra.forbid

    @root_validator
    def fill_project_id(cls: Any, values: Any) -> Any:
        project_id, project_name = (
            values.get("project_id"),
            values.get("project"),
        )
        values["project_id"] = _get_project_id_from_id_or_name(project_id, project_name)
        return values

    @root_validator
    def fill_cluster_env_from_custom_docker(cls: Any, values: Any) -> Any:
        docker, python_version, ray_version, cluster_env, build_id = (
            values.get("docker"),
            values.get("python_version"),
            values.get("ray_version"),
            values.get("cluster_env"),
            values.get("build_id"),
        )
        if docker is not None:
            if cluster_env is not None:
                raise click.ClickException(
                    "`cluster_env` and `docker` cannot both be specified. Please only provide one"
                    "of these in the job config file."
                )
            if build_id is not None:
                raise click.ClickException(
                    "`build_id` and `docker` cannot both be specified. Please only provide one"
                    "of these in the job config file."
                )
            if python_version is None and ray_version is None:
                python_version, ray_version = extract_versions_from_image_name(docker)

            if python_version is None:
                raise click.ClickException(
                    "`python_version` should be specified when `docker` is used."
                )
            if ray_version is None:
                raise click.ClickException(
                    "`ray_version` should be specified when `docker` is used."
                )
            values["cluster_env"] = BYODInfo(
                docker_image_name=docker,
                python_version=python_version,
                ray_version=ray_version,
            ).encode()
        return values

    @root_validator
    def fill_build_id(cls: Any, values: Any) -> Any:
        build_id, cluster_env = (
            values.get("build_id"),
            values.get("cluster_env"),
        )
        if cluster_env and build_id:
            raise click.ClickException(
                "Only one of `cluster_env` or `build_id` can be provided in the config file. "
            )
        if cluster_env:
            build_id = get_build_from_cluster_env_identifier(cluster_env).id
            values["build_id"] = build_id
        elif not build_id:
            log.info(
                "No cluster environment provided, setting default based on local Python and Ray versions."
            )
            build_id = get_default_cluster_env_build().id
            values["build_id"] = build_id
        validate_successful_build(values["build_id"])
        return values

    @root_validator
    def fill_compute_config_id(cls: Any, values: Any) -> Any:
        compute_config_id, compute_config, cloud = (
            values.get("compute_config_id"),
            values.get("compute_config"),
            values.get("cloud"),
        )
        project_id = values.get("project_id")
        if not project_id:
            project_id = _get_project_id_from_id_or_name(
                values.get("project_id"), values.get("project")
            )
        if bool(compute_config_id) + bool(compute_config) + bool(cloud) > 1:
            raise click.ClickException(
                "Only one of `compute_config_id`, `compute_config`, or `cloud` can be provided in the config file."
            )
        if compute_config and isinstance(compute_config, str):
            compute_config_id = get_cluster_compute_from_name(compute_config).id
        elif compute_config and isinstance(compute_config, dict):
            compute_config_id = register_compute_template(compute_config).id
        elif cloud:
            # Get default cluster compute for the specified cloud.
            compute_config_id = get_default_cluster_compute(
                cloud_name=cloud, project_id=None
            ).id
            log.info(
                f"Using default compute config for specified cloud {cloud}: {compute_config_id}."
            )
        elif not compute_config_id:
            parent_cloud_name = None
            if project_id:
                parent_cloud_id_and_name = get_parent_cloud_id_and_name_of_project(
                    project_id
                )
                if parent_cloud_id_and_name:
                    _, parent_cloud_name = parent_cloud_id_and_name
            # Get default cluster compute for the parent cloud if it exists or the default cloud default cloud.
            compute_config_id = get_default_cluster_compute(
                cloud_name=parent_cloud_name, project_id=None
            ).id
            msg_about_cloud = (
                f" for cloud {parent_cloud_name}" if parent_cloud_name else ""
            )
            log.info(
                f"No cloud or compute config specified, using the default{msg_about_cloud}: {compute_config_id}."
            )
        values["compute_config_id"] = compute_config_id

        return values

    @root_validator
    def validate_runtime_env(cls: Any, values: Any) -> Any:  # noqa: PLR0912
        runtime_env = values.get("runtime_env")
        if runtime_env is not None:
            _validate_and_modify_runtime_env(runtime_env)
        return values


class JobConfig(BaseHAJobConfig):
    """
    Job Config model for CLI. Validate and preprocess so `entrypoint`, `runtime_env_config`,
    `build_id`, `compute_config_id`, `max_retries` have the correct values to call
    `/api/v2/decorated_ha_jobs/create`.
    """

    entrypoint: str = Field(
        ...,
        description="A script that will be run to start your job. This command will be run in the root directory of the specified runtime env. Eg. 'python script.py'",
    )


class LogProvider(ABC):
    @abstractmethod
    def __init__(self, dns_name: str, anyscale_token: str, query: str) -> None:
        pass

    @abstractmethod
    def query(
        self, start_timestamp_ns: int, end_timestamp_ns: int
    ) -> List[Tuple[int, str]]:
        """Query logs for a time range, return list of (timestamp_ns, log_line)."""

    @abstractmethod
    def close(self) -> None:
        """Close any connection this log provider uses"""

    def __enter__(self, *args, **kwargs):  # noqa: B027
        pass

    def __exit__(self, *args, **kwargs):
        self.close()


class LokiLogProvider(LogProvider):
    def __init__(self, dns_name: str, anyscale_token: str, query: str) -> None:
        # https://grafana.com/docs/loki/latest/api/#get-lokiapiv1query_range
        self.url = f"https://{dns_name}/loki/api/v1/query_range"
        self.params: Dict[str, Union[str, int]] = {
            "token": anyscale_token,
            "query": query,
            "limit": 1000,
            "start": 0,
            "end": int(time.time() * 1e9),
            "direction": "forward",
        }

    def __enter__(self, *args, **kwargs):
        self.session = requests.Session()
        self.session.mount(
            "https://",
            HTTPAdapter(
                max_retries=Retry(total=10, backoff_factor=0.1, allowed_methods=["GET"])
            ),
        )
        return self

    def close(self) -> None:
        self.session.close()

    def __exit__(self, *args, **kwargs):
        self.close()

    def query(
        self, start_timestamp_ns: int, end_timestamp_ns: int
    ) -> List[Tuple[int, str]]:
        if start_timestamp_ns == 0:
            # 10^9 nanoseconds in a second
            start_timestamp_ns = int(
                (datetime.now() - timedelta(days=7)).timestamp() * (10 ** 9)
            )
        self.params["start"] = start_timestamp_ns
        self.params["end"] = end_timestamp_ns

        resp = self.session.get(self.url, params=self.params)
        resp.raise_for_status()

        resp_data = resp.json()
        if resp_data["status"] != "success":
            raise click.ClickException("Querying Anyscale log endpoint failed.")
        if resp_data["data"]["resultType"] != "streams":
            raise click.ClickException("Invalid metrics type.")

        lines = []
        for log_chunk in resp_data["data"]["result"]:
            # TODO(simon): potentially annotate the log with the log_chunk["stream"] metadata
            for timestamp, line in log_chunk["values"]:
                lines.append((int(timestamp), line))

        return lines


class JobController(BaseController):
    def __init__(
        self,
        log: Optional[LogsLogger] = None,
        initialize_auth_api_client: bool = True,
        raise_structured_exception: bool = False,
    ):
        if log is None:
            log = LogsLogger()

        super().__init__(initialize_auth_api_client, raise_structured_exception)
        self.log = log
        self.log.open_block("Output")

    def submit(
        self,
        job_config_file: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_entrypoint_cmd: Optional[bool] = False,
        entrypoint: Optional[List[str]] = None,
    ) -> str:
        entrypoint = entrypoint or []
        workspace_id = os.environ.get("ANYSCALE_EXPERIMENTAL_WORKSPACE_ID", None)
        if is_anyscale_workspace() and is_entrypoint_cmd:
            entrypoint = [job_config_file, *entrypoint]
            config = self.generate_config_from_entrypoint(
                entrypoint, name, description, workspace_id
            )
            id = self.submit_from_config(config)  # noqa: A001
        elif len(entrypoint) == 0:
            # Assume that job_config_file is a file and submit it.
            config = self.generate_config_from_file(
                job_config_file,
                name=name,
                description=description,
                workspace_id=workspace_id,
            )
            id = self.submit_from_config(config)  # noqa: A001
        elif len(entrypoint) != 0:
            msg = (
                "Within an Anyscale Workspace, `anyscale job submit` takes either a file, or a command. To submit a command, use `anyscale job submit -- my command`."
                if is_anyscale_workspace()
                else "`anyscale job submit` takes one argument, a YAML file configuration. Please use `anyscale job submit my_file`."
            )
            raise click.ClickException(msg)
        return id

    def generate_config_from_entrypoint(
        self,
        entrypoint: List[str],
        name: Optional[str],
        description: Optional[str],
        workspace_id: Optional[str] = None,
    ) -> JobConfig:
        config_dict = {
            "entrypoint": " ".join(entrypoint),
            "name": name,
            "description": description,
            "workspace_id": workspace_id,
        }
        config_dict = populate_dict_with_workspace_config_if_exists(
            config_dict, self.anyscale_api_client
        )
        job_config = JobConfig.parse_obj(config_dict)
        return job_config

    def generate_config_from_file(
        self,
        job_config_file: str,
        name: Optional[str],
        description: Optional[str],
        workspace_id: Optional[str] = None,
    ) -> JobConfig:
        config_dict = self._load_config_dict_from_file(job_config_file)
        config_dict["workspace_id"] = workspace_id
        validate_job_config_dict(config_dict, self.api_client)
        config_dict = populate_dict_with_workspace_config_if_exists(
            config_dict, self.anyscale_api_client
        )
        job_config = JobConfig.parse_obj(config_dict)

        if name:
            job_config.name = name

        if description:
            job_config.description = description

        return job_config

    def submit_from_config(self, job_config: JobConfig):
        # If project id is not specified, try to infer it
        project_id = infer_project_id(
            self.anyscale_api_client,
            self.api_client,
            self.log,
            project_id=job_config.project_id,
            cluster_compute_id=job_config.compute_config_id,
            cluster_compute=job_config.compute_config,
            cloud=job_config.cloud,
        )

        job_config.runtime_env = override_runtime_env_config(
            runtime_env=job_config.runtime_env,
            anyscale_api_client=self.anyscale_api_client,
            api_client=self.api_client,
            workload_type=Workload.JOBS,
            compute_config_id=job_config.compute_config_id,
            log=self.log,
        )
        config_object = ProductionJobConfig(
            entrypoint=job_config.entrypoint,
            runtime_env=job_config.runtime_env,
            build_id=job_config.build_id,
            compute_config_id=job_config.compute_config_id,
            max_retries=job_config.max_retries,
        )

        job = self.api_client.create_job_api_v2_decorated_ha_jobs_create_post(
            CreateInternalProductionJob(
                name=job_config.name or self._generate_random_job_name(),
                description=job_config.description or "Job submitted from CLI",
                project_id=project_id,
                workspace_id=job_config.workspace_id,
                config=config_object,
            )
        ).result
        self.log.info(
            f"Maximum uptime is {self._get_maximum_uptime_output(job)} for clusters launched by this job."
        )
        self.log.info(
            f"Job {job.id} has been successfully submitted. Current state of job: {job.state.current_state}."
        )
        self.log.info(
            f"Query the status of the job with `anyscale job list --job-id {job.id}`."
        )
        self.log.info(
            f"Get the logs for the job with `anyscale job logs --job-id {job.id} --follow`."
        )
        self.log.info(f'View the job in the UI at {get_endpoint(f"/jobs/{job.id}")}')
        return job.id

    def _get_maximum_uptime_output(self, job: ProductionJob) -> str:
        compute_config: ComputeTemplate = self.api_client.get_compute_template_api_v2_compute_templates_template_id_get(
            job.config.compute_config_id
        ).result
        maximum_uptime_minutes = compute_config.config.maximum_uptime_minutes
        if maximum_uptime_minutes and maximum_uptime_minutes > 0:
            return f"set to {maximum_uptime_minutes} minutes"
        return "disabled"

    def _load_config_dict_from_file(self, job_config_file: str) -> Dict[str, Any]:
        if not os.path.exists(job_config_file):
            raise click.ClickException(f"Config file {job_config_file} not found.")

        with open(job_config_file) as f:
            config_dict = yaml.safe_load(f)
        return config_dict

    def wait(
        self,
        job_name: Optional[str] = None,
        job_id: Optional[str] = None,
        is_service: bool = False,
        target_state: str = HaJobStates.SUCCESS,
        interval_secs: float = 10.0,
        timeout_secs=None,
    ):
        if target_state not in HaJobStates.allowable_values:
            raise click.ClickException(
                f"`{target_state}` is not a valid Job state. Allowed states are {HaJobStates.allowable_values}"
            )
        job_id_or_name = job_name or job_id
        job_id = cast(
            str,
            self._resolve_job_object(
                job_id, job_name, entity_type="service" if is_service else "job"
            ).id,
        )
        with self.log.spinner(f"Waiting for Job `{job_id_or_name}`...") as spinner:
            state = None
            for _ in poll(interval_secs=interval_secs, timeout_secs=timeout_secs):
                state = self._get_job_state(job_id)
                spinner.text = f"Job `{job_id_or_name}` is in state `{state}`. Waiting to reach state `{target_state}`."

                if state == target_state:
                    spinner.succeed(
                        f"Job `{job_id_or_name}` reached state `{target_state}`."
                    )
                    return job_id

                if state in _TERMINAL_STATES:
                    msg = f"Job `{job_id_or_name}` reached terminal state `{state}`, and will not reach `{target_state}`."
                    spinner.fail(msg)
                    raise click.ClickException(msg)

            msg = f"Timed out after waiting for {timeout_secs} seconds. The current state is {state}."
            spinner.fail(msg)
            raise click.ClickException(msg)

    def _get_job_state(self, job_id: str):
        job = self.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get(
            job_id
        ).result
        return job.state.current_state

    def list(  # noqa: PLR0913
        self,
        include_all_users: bool,
        name: Optional[str],
        job_id: Optional[str],
        project_id: Optional[str],
        include_archived: bool,
        max_items: int,
        is_service: bool = False,
    ) -> None:
        """
        This function will either list jobs or services based on the value of `is_service`.
        Both functionalities are combined in one function because the API to list both these
        entities is currently the same.
        """
        entity_type = "services" if is_service else "jobs"
        print(f'View your {entity_type} in the UI at {get_endpoint(f"/{entity_type}")}')

        jobs_list = []
        if job_id:
            job = self.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get(
                job_id
            ).result
            if not is_service and job.is_service:
                # `job_id` belongs to a service, but this function should list jobs.
                raise click.ClickException(
                    f"ID {job_id} belongs to a Anyscale service. Please get information about "
                    f"this service with `anyscale service list --service-id {job_id}`."
                )
            elif is_service and not job.is_service:
                # `job_id` belongs to a job, but this function should list services.
                raise click.ClickException(
                    f"ID {job_id} belongs to a Anyscale job. Please get information about "
                    f"this job with `anyscale job list --job-id {job_id}`."
                )
            output_map = {
                "Name": job.name,
                "Id": job.id,
                "Cost (dollars)": job.cost_dollars,
                "Project name": job.project.name,
                "Cluster name": job.last_job_run.cluster.name
                if job.last_job_run and job.last_job_run.cluster
                else None,
                "Current state": job.state.current_state,
                "Creator": job.creator.email,
                "Entrypoint": job.config.entrypoint
                if len(job.config.entrypoint) < 100
                else job.config.entrypoint[:100] + " ...",
            }
            if is_service:
                output_map["Access"] = job.access
                output_map["URL"] = job.url
                output_map["Token"] = job.token

            output_str = "\n".join(
                [f"\t{key}: {output_map[key]}" for key in output_map]
            )
            print(output_str)
            return
        else:
            if not include_all_users:
                creator_id = (
                    self.api_client.get_user_info_api_v2_userinfo_get().result.id
                )
            else:
                creator_id = None
            resp = self.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get(
                project_id=project_id,
                name=name,
                creator_id=creator_id,
                type_filter="SERVICE" if is_service else "BATCH_JOB",
                archive_status="ALL" if include_archived else "NOT_ARCHIVED",
                count=10,
            )
            jobs_list.extend(resp.results)
            paging_token = resp.metadata.next_paging_token
            has_more = (paging_token is not None) and (len(jobs_list) < max_items)
            while has_more:
                resp = self.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get(
                    project_id=project_id,
                    name=name,
                    creator_id=creator_id,
                    type_filter="SERVICE" if is_service else "BATCH_JOB",
                    archive_status="ALL" if include_archived else "NOT_ARCHIVED",
                    count=10,
                    paging_token=paging_token,
                )
                jobs_list.extend(resp.results)
                paging_token = resp.metadata.next_paging_token
                has_more = (paging_token is not None) and (len(jobs_list) < max_items)
            jobs_list = jobs_list[:max_items]

        jobs_table = [
            [
                job.name,
                job.id,
                job.cost_dollars,
                job.project.name,
                job.last_job_run.cluster.name
                if job.last_job_run and job.last_job_run.cluster
                else None,
                job.state.current_state,
                job.creator.email,
                job.config.entrypoint
                if len(job.config.entrypoint) < 50
                else job.config.entrypoint[:50] + " ...",
            ]
            for job in jobs_list
        ]

        table = tabulate.tabulate(
            jobs_table,
            headers=[
                "NAME",
                "ID",
                "COST",
                "PROJECT NAME",
                "CLUSTER NAME",
                "CURRENT STATE",
                "CREATOR",
                "ENTRYPOINT",
            ],
            tablefmt="plain",
        )
        print(f"{entity_type.capitalize()}:\n{table}")

    def archive(
        self, job_id: Optional[str], job_name: Optional[str], is_service: bool = False,
    ) -> None:
        """
        This function will either archive jobs or services based on the value of `is_service`.
        Both functionalities are combined in one function because the API to archive both these
        entities is currently the same.
        """
        entity_type = "service" if is_service else "job"
        job_resp: DecoratedProductionJob = self._resolve_job_object(
            job_id, job_name, entity_type
        )
        self.api_client.archive_job_api_v2_decorated_ha_jobs_production_job_id_archive_post(
            job_resp.id
        )
        self.log.info(
            f"{entity_type.capitalize()} {job_resp.id} is successfully archived."
        )

    def terminate(
        self, job_id: Optional[str], job_name: Optional[str], is_service: bool = False,
    ) -> None:
        """
        This function will either terminate jobs or services based on the value of `is_service`.
        Both functionalities are combined in one function because the API to terminate both these
        entities is currently the same.
        """
        entity_type = "service" if is_service else "job"
        job_resp: DecoratedProductionJob = self._resolve_job_object(
            job_id, job_name, entity_type
        )
        job = self.api_client.terminate_job_api_v2_decorated_ha_jobs_production_job_id_terminate_post(
            job_resp.id
        ).result
        self.log.info(f"{entity_type.capitalize()} {job.id} has begun terminating...")
        self.log.info(
            f" Current state of {entity_type}: {job.state.current_state}. Goal state of {entity_type}: {job.state.goal_state}"
        )
        self.log.info(
            f"Query the status of the {entity_type} with `anyscale {entity_type} list --{entity_type}-id {job.id}`."
        )

    def _resolve_job_object(
        self, job_id: Optional[str], job_name: Optional[str], entity_type: str = "job"
    ) -> DecoratedProductionJob:
        """Given job_id or job_name, retrieve decorated ha job spec"""
        if job_id is None and job_name is None:
            raise click.ClickException(
                f"Either `--id` or `--name` must be passed in for {entity_type}."
            )
        if job_id:
            return self._get_job(job_id)

        jobs_list_resp: List[
            DecoratedProductionJob
        ] = self.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get(
            name=job_name,
            type_filter="BATCH_JOB" if entity_type == "job" else "SERVICE",
        ).results
        if len(jobs_list_resp) == 0:
            raise click.ClickException(
                f"No {entity_type} found with name {job_name}. Please either pass `--id` or list the "
                f"available {entity_type}s with `anyscale {entity_type} list`."
            )
        if len(jobs_list_resp) > 1:
            raise click.ClickException(
                f"Multiple {entity_type}s found with name {job_name}. Please specify the `--id` instead."
            )
        return jobs_list_resp[0]

    def _get_job(self, job_id: str) -> DecoratedProductionJob:
        job_object = self.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get(
            production_job_id=job_id
        ).result
        return job_object

    def _get_formatted_latest_job_run(
        self, job: DecoratedProductionJob
    ) -> Optional[MiniJobRun]:
        job_state = job.state.current_state
        last_job_run_id = job.last_job_run_id
        if job_state in _TERMINAL_STATES and last_job_run_id is None:
            raise click.ClickException(
                f"Can't find latest job run for {job_state} job."
            )
        if not last_job_run_id:
            return None
        return MiniJobRun(
            last_job_run_id=last_job_run_id, job_state=job_state, error=job.state.error
        )

    def _wait_for_a_job_run(
        self, job_id: Optional[str], job_name: Optional[str]
    ) -> DecoratedProductionJob:
        """Waits until the job has a job run and is in a non-pending state
        (encountered when initially submitting).

        Returns the job."""
        job = self._resolve_job_object(job_id, job_name)
        last_job_run_id: str = job.last_job_run_id
        job_state = job.state.current_state
        with self.log.spinner("Waiting for job run...") as spinner:
            while last_job_run_id is None or job_state in _PENDING_STATES:
                if job_state in _TERMINAL_STATES:
                    raise click.ClickException(
                        f"Can't find latest job run for {job_state} job."
                    )
                spinner.text = f"Waiting for a job run, current state is {job_state}..."
                time.sleep(5)
                job = self._get_job(job.id)
                last_job_run_id = job.last_job_run_id
                job_state = job.state.current_state
        return job

    def _wait_for_job_running(self, job_id: str) -> None:
        with self.log.spinner("Waiting for job to retry...") as spinner:
            for _ in poll():
                job_object = self._get_job(job_id)
                job_state = job_object.state.current_state
                if job_state in _PENDING_STATES:
                    spinner.text = (
                        f"Waiting for job to retry, current state is {job_state}..."
                    )
                else:
                    return

    def _print_logs_for_active_job_run(
        self, job_run_id: str, should_follow: bool
    ) -> None:
        """
        Prints logs from the active cluster the job is run on.
        """
        with handle_and_log_lines_in_click_exception(log_callback=self.log.error):
            if should_follow:
                # Use websockets (to continuously poll logs)
                with wrap_as_unsupported_log_retrieval_method_error():
                    websocket_url: str = (
                        self.api_client.get_job_logs_stream_api_v2_logs_job_logs_stream_job_id_get(
                            job_id=job_run_id
                        ).result.stream_url
                    )

                with wrap_job_run_log_not_retrievable_on_active_cluster_error(
                    job_run_id, raise_connection_issue_as_cli_error=True
                ):
                    # (run_until_complete() is used here b/c the KeyboardInterrupt exception is
                    # not propogated all the way up (and likely being handled by internals of asyncio.run()))
                    asyncio.get_event_loop().run_until_complete(
                        _stream_log_from_ray_websocket(
                            websocket_url,
                            log_callback=self.log.log,
                            remove_escape_chars=False,
                        )
                    )
            else:
                # Make a one-time request to get logs
                logs = asyncio.run(
                    _get_logs_from_active_job_run(
                        self.anyscale_api_client,
                        job_run_id,
                        raise_connection_issue_as_cli_error=True,
                        remove_escape_chars=False,
                    )
                )
                for line in logs.splitlines():
                    self.log.log(line)

    def _print_logs_for_inactive_job_run(self, job_run_id: str) -> None:
        """Retrieves logs from the cloud storage bucket for a job run in terminal state"""
        logs = ""
        with self.log.spinner("Retrieving logs..."):
            # For jobs on a cluster that is terminating, the logs are in-flight between cluster and storage bucket
            # of the cloud. In that case, wait for a bit and try again.
            for _ in poll(interval_secs=5, max_iter=10):
                logs = asyncio.run(
                    _get_job_logs_from_storage_bucket(
                        self.anyscale_api_client,
                        job_run_id=job_run_id,
                        remove_escape_chars=False,
                    )
                )
                if logs:
                    break
        if not logs:
            self.log.error("Logs are not available for this job run.")
            return
        for line in logs.splitlines():
            self.log.log(line)

    def logs(
        self,
        job_id: Optional[str] = None,
        job_name: Optional[str] = None,
        should_follow: bool = False,
        all_attempts: bool = False,
    ) -> None:
        """Uses fallback logic to print logs for a (production) job to terminal output.

        * If the job is running, it will retrieve logs from the cluster the job is run on.
        * If the job is not running, it will retrieve logs from Anyscale's backend cache.
        * If the logs no longer live in the cache, or the cloud the job is on is using Anyscale V2,
            it falls back to retrieving logs from the storage bucket of the cloud.
        """
        # This logic will be simplified once the migration to Anyscale V2 is complete.
        job = self._wait_for_a_job_run(job_id, job_name)
        last_job_run_id: str = job.last_job_run_id
        job_state: HaJobStates = job.state.current_state
        job_run_ids: List[str] = [last_job_run_id] if not all_attempts else [
            job_run.id for job_run in self._get_all_job_runs(job.id)
        ]  # type: ignore
        for job_run_id in job_run_ids:
            self.log.open_block(
                job_run_id, f"Job Run Id: {job_run_id}", auto_close=True,
            )
            # 1. Last job run, and 2. job is RUNNING implies (==) job run is RUNNING
            is_last_job_run_and_active = (
                job_run_id == last_job_run_id and job_state == HaJobStates.RUNNING
            )
            get_logs_fns: List[Callable[[], None]] = [
                *(
                    # If the job run is RUNNING, retrieve logs from the active cluster
                    []
                    if not is_last_job_run_and_active
                    else [
                        lambda: self._print_logs_for_active_job_run(
                            job_run_id, should_follow  # noqa: B023
                        )
                    ]
                ),
                # Else (job run is done) or if the previous retrieval method failed,
                # retrieve logs from Anyscale's cache
                lambda: self._print_logs_legacy(job, should_follow),  # noqa: B023
                # Else (job run not in v1 cloud, logs expired from cache) or if the previous retrieval method failed,
                # retrieve logs from Anyscale's cache
                lambda: self._print_logs_for_inactive_job_run(job_run_id),  # noqa: B023
            ]
            for fn in get_logs_fns:
                with contextlib.suppress(ExpectedLogRetrievalError):
                    fn()
                    # If `fn` didn't raise `ExpectedLogRetrievalError`, we assume logs were successfully printed.
                    # In this case, break out of this loop and log for the next `job_run_id`
                    break

    def _print_logs_legacy(
        self,
        job: DecoratedProductionJob,
        should_follow: bool = False,
        log_provider_cls: Type[LogProvider] = LokiLogProvider,
    ) -> None:
        """Retrieves logs from Anyscale's backend cache. Not supported for Anyscale v2 clouds."""
        job_id: str = job.id
        if _is_production_job_on_v2_cloud(self.anyscale_api_client, job_id):
            raise UnsupportedLogRetrievalMethodError(
                "Logs are not stored Anyscale-side on clouds set up with Anyscale v2."
            )

        start_timestamp_ns = 0
        max_iter = 1 if not should_follow else None
        log_provider_map: Dict[str, LogProvider] = {}

        num_times_logged = 0
        for _ in poll(1, max_iter=max_iter):
            # Fetch the latest job run
            jr = self._get_formatted_latest_job_run(job)

            # This shouldn't happen because we are waiting for it above
            assert jr, "Could not find the latest job run"

            log_provider = log_provider_map.get(jr.last_job_run_id)
            if not log_provider:
                # Open a new CLI block
                # This is to ensure the logs for each job are nicely formatted

                # We have not seen this job run id before. We need to construct a new log provider
                log_info: JobsLogsQueryInfo = self.api_client.get_job_logs_query_info_api_v2_decorated_ha_jobs_production_job_id_logs_query_get(
                    production_job_id=job_id
                ).result

                log_provider = log_provider_cls(
                    dns_name=log_info.loki_dns_name,
                    anyscale_token=log_info.access_token,
                    query=log_info.loki_query,
                )

                # Add to the cache
                log_provider_map[jr.last_job_run_id] = log_provider

            # Make sure we only have 1 open request session at a time
            with log_provider:

                # Flush all logs in the loki endpoint
                last_received_logs_iteration = 0
                for iteration in poll(interval_secs=1):
                    # Fetch logs in the time range
                    end_timestamp_ns = int(time.time() * 1e9)
                    lines = log_provider.query(start_timestamp_ns, end_timestamp_ns)

                    # Print the results
                    for time_stamp, line in lines:
                        # Update the start timestamp in case we are following or paginated.
                        start_timestamp_ns = time_stamp + 1
                        self.log.log(line)
                        num_times_logged += 1
                    if len(lines) > 0:
                        # Record the last iteration at which we received logs
                        last_received_logs_iteration = iteration

                    # If we are following, threshold is 30 iterations (or 30 seconds)
                    threshold = 30 if should_follow else 0
                    if iteration - last_received_logs_iteration > threshold:
                        # If we haven't received logs after threshold iterations, assume existing logs have been flushed
                        break

                # We have already flushed existing logs for this job run
                # If the job is in a terminal state, exit
                if jr.job_state in _TERMINAL_STATES:
                    # If the state is terminal, exit
                    if num_times_logged == 0:
                        raise ExpectedLogRetrievalError(
                            "Logs have expired from Anyscale's backend cache layer."
                        )
                    self.log.info(f"Job entered terminal state {jr.job_state}.")
                    if jr.error:
                        self.log.error(f"Job exited with error: {jr.error}")
                    return

                # If the job is in a pending state, wait for it to start running
                # before fetching more logs
                if jr.job_state in _PENDING_STATES:
                    self._wait_for_job_running(job_id)

    def retrieve_output(
        self, job_name: Optional[str] = None, job_id: Optional[str] = None,
    ) -> None:
        if not job_id:
            job = self._resolve_job_object(job_id, job_name)
            job_id = job.id

        try:
            output = self.api_client.find_structured_job_output_api_v2_structured_outputs_ha_job_output_ha_job_id_get(
                ha_job_id=job_id
            )
            self.log.log(json.dumps(output.result.output, indent=2))
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            # Swallow if pretty print logic fails
            with contextlib.suppress(Exception):
                j = json.loads(e.body)  # type: ignore
                detail = j.get("error", {}).get("detail")
                self.log.error(detail)

    def _generate_random_job_name(self) -> str:
        """Generates a random job name
        Format:
            cli-job-{10 random characters}
        """
        random_chars = "".join(random.choices(string.ascii_letters, k=10)).lower()
        return "cli-job-" + random_chars

    def _get_all_job_runs(self, job_id: str) -> List[Job]:
        """Returns all job runs for a given job id.
        Returned in ascending order by creation time."""
        job_runs: List[Job] = search_entities(
            self.anyscale_api_client.search_jobs,
            JobsQuery(
                ha_job_id=job_id,
                show_ray_client_runs_only=False,
                sort_by_clauses=[
                    SortByClauseJobsSortField(
                        sort_field=JobsSortField.CREATED_AT, sort_order=SortOrder.ASC,
                    )
                ],
                paging=PageQuery(),
            ),
        )
        return job_runs
