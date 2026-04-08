# MIT License - Copyright (c) fintonlabs.com
from rundeck_mcp.context import ContextResolver
from rundeck_mcp.models import (
    Execution,
    ExecutionOutput,
    ExecutionQuery,
    JobRunRequest,
    ListResponseModel,
)


def run_job(job_id: str, run_request: JobRunRequest | None = None) -> Execution:
    """Execute a Rundeck job.

    Before running, use get_job to discover the job's options. If the job has
    required options, they must be provided in run_request.options.

    Args:
        job_id: The UUID of the job to run.
        run_request: Optional execution parameters including option values,
            log level, node filter override, and scheduled time.

    Returns:
        The execution record with its ID and initial status.
    """
    client = ContextResolver.get_client()
    payload = run_request.to_payload() if run_request else {}
    data = client.rpost(f"/job/{job_id}/run", json=payload)
    return Execution.model_validate(data)


def get_execution(execution_id: int) -> Execution:
    """Get the current status of a job execution.

    Args:
        execution_id: The numeric execution ID.

    Returns:
        The execution details including status, timing, and node results.
    """
    client = ContextResolver.get_client()
    data = client.rget(f"/execution/{execution_id}")
    return Execution.model_validate(data)


def list_executions_for_job(job_id: str, query: ExecutionQuery | None = None) -> ListResponseModel[Execution]:
    """List recent executions for a specific job.

    Args:
        job_id: The UUID of the job.
        query: Optional filtering by status and pagination.

    Returns:
        List of executions for this job.
    """
    if query is None:
        query = ExecutionQuery()
    client = ContextResolver.get_client()
    data = client.rget(f"/job/{job_id}/executions", params=query.to_params())
    executions = [Execution.model_validate(e) for e in data.get("executions", [])]
    return ListResponseModel[Execution](response=executions)


def get_execution_output(execution_id: int, max_lines: int = 200, last_lines: int | None = None) -> ExecutionOutput:
    """Get the log output from a job execution.

    Args:
        execution_id: The numeric execution ID.
        max_lines: Maximum number of log lines to return (default 200).
        last_lines: If set, return only the last N lines from the end.

    Returns:
        The execution output including log entries and completion status.
    """
    client = ContextResolver.get_client()
    params: dict[str, int] = {"maxlines": max_lines}
    if last_lines is not None:
        params["lastlines"] = last_lines
    data = client.rget(f"/execution/{execution_id}/output", params=params)
    return ExecutionOutput.model_validate(data)


def abort_execution(execution_id: int) -> str:
    """Abort a running execution.

    Args:
        execution_id: The numeric execution ID to abort.

    Returns:
        Abort status message.
    """
    client = ContextResolver.get_client()
    data = client.rpost(f"/execution/{execution_id}/abort")
    abort_status = data.get("abort", {}).get("status", "unknown")
    return f"Execution {execution_id} abort status: {abort_status}"
