# MIT License - Copyright (c) fintonlabs.com
from rundeck_mcp.context import ContextResolver
from rundeck_mcp.models import Job, JobImportResult, JobQuery, ListResponseModel


def list_jobs(project_name: str, query: JobQuery | None = None) -> ListResponseModel[Job]:
    """List jobs in a Rundeck project.

    Args:
        project_name: The project to list jobs from.
        query: Optional filtering and pagination parameters.

    Returns:
        List of jobs matching the query.
    """
    if query is None:
        query = JobQuery()
    client = ContextResolver.get_client()
    data = client.rget(f"/project/{project_name}/jobs", params=query.to_params())
    jobs = [Job.model_validate(j) for j in data]
    return ListResponseModel[Job](response=jobs)


def get_job(job_id: str) -> Job:
    """Get the full definition of a job, including its options and steps.

    Use this before running a job to discover available options, their defaults,
    required flags, and allowed values.

    Args:
        job_id: The UUID of the job.

    Returns:
        The complete job definition with options and sequence.
    """
    client = ContextResolver.get_client()
    data = client.rget(f"/job/{job_id}")
    return Job.model_validate(data)


def import_job_yaml(project_name: str, yaml_definition: str, dupe_option: str = "create") -> JobImportResult:
    """Import a job into a project from a YAML definition.

    Args:
        project_name: The project to import the job into.
        yaml_definition: The job definition in Rundeck YAML format. Must be a complete
            job list starting with '- name:'.
        dupe_option: How to handle duplicate jobs: 'create' (new), 'update' (overwrite),
            or 'skip' (ignore). Defaults to 'create'.

    Returns:
        Import result showing succeeded, failed, and skipped jobs.
    """
    client = ContextResolver.get_client()
    response = client._client.post(
        f"/project/{project_name}/jobs/import",
        content=yaml_definition,
        headers={"Content-Type": "application/yaml"},
        params={"fileformat": "yaml", "dupeOption": dupe_option},
    )
    response.raise_for_status()
    return JobImportResult.model_validate(response.json())


def delete_job(job_id: str) -> str:
    """Delete a job from Rundeck.

    Args:
        job_id: The UUID of the job to delete.

    Returns:
        Confirmation message.
    """
    client = ContextResolver.get_client()
    client.rdelete(f"/job/{job_id}")
    return f"Job {job_id} deleted successfully."
