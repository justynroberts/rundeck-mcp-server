# MIT License - Copyright (c) fintonlabs.com
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from rundeck_mcp.models.base import DEFAULT_PAGINATION_LIMIT, MAXIMUM_PAGINATION_LIMIT


class Execution(BaseModel):
    """A Rundeck job execution."""

    id: int = Field(description="Execution ID")
    href: str | None = Field(default=None, description="API URL for this execution")
    permalink: str | None = Field(default=None, description="Web UI URL for this execution")
    status: str = Field(description="Execution status: running, succeeded, failed, aborted, timedout")
    project: str = Field(description="Project name")
    user: str | None = Field(default=None, description="User who started the execution")
    date_started: dict[str, Any] | None = Field(default=None, alias="date-started", description="Start time")
    date_ended: dict[str, Any] | None = Field(default=None, alias="date-ended", description="End time")
    job: dict[str, Any] | None = Field(default=None, description="Job reference")
    description: str | None = Field(default=None, description="Execution description")
    argstring: str | None = Field(default=None, description="Argument string used")
    successful_nodes: list[str] | None = Field(
        default=None, alias="successfulNodes", description="Nodes that succeeded"
    )
    failed_nodes: list[str] | None = Field(default=None, alias="failedNodes", description="Nodes that failed")

    model_config = {"populate_by_name": True}


class ExecutionList(BaseModel):
    """Paginated list of executions."""

    paging: dict[str, int] = Field(description="Pagination info (count, total, offset, max)")
    executions: list[Execution] = Field(description="List of executions")


class ExecutionOutputEntry(BaseModel):
    """A single log entry from execution output."""

    time: str | None = Field(default=None, description="Relative timestamp")
    absolute_time: str | None = Field(default=None, description="Absolute ISO timestamp")
    log: str = Field(description="Log message content")
    level: str | None = Field(default=None, description="Log level (NORMAL, ERROR, WARNING, etc)")
    stepctx: str | None = Field(default=None, description="Step context identifier")
    node: str | None = Field(default=None, description="Node name")


class ExecutionOutput(BaseModel):
    """Output/log from a Rundeck execution."""

    id: int = Field(description="Execution ID")
    offset: str | None = Field(default=None, description="Byte offset for incremental retrieval")
    completed: bool = Field(description="Whether the output is complete")
    exec_completed: bool = Field(default=False, alias="execCompleted", description="Whether execution is finished")
    exec_state: str | None = Field(default=None, alias="execState", description="Current execution state")
    entries: list[ExecutionOutputEntry] = Field(default_factory=list, description="Log entries")
    total_size: int | None = Field(default=None, alias="totalSize", description="Total log size in bytes")

    model_config = {"populate_by_name": True}


class ExecutionQuery(BaseModel):
    """Query parameters for listing executions."""

    status: str | None = Field(default=None, description="Filter by status: running, succeeded, failed, aborted")
    max: int = Field(default=DEFAULT_PAGINATION_LIMIT, ge=1, le=MAXIMUM_PAGINATION_LIMIT, description="Max results")
    offset: int = Field(default=0, ge=0, description="Pagination offset")

    def to_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {"max": self.max, "offset": self.offset}
        if self.status:
            params["status"] = self.status
        return params


class JobRunRequest(BaseModel):
    """Request to run a Rundeck job."""

    options: dict[str, str] | None = Field(default=None, description="Job option values as key-value pairs")
    log_level: str | None = Field(default=None, description="Log level: DEBUG, VERBOSE, INFO, WARNING, ERROR")
    filter: str | None = Field(default=None, description="Node filter override")
    run_at_time: str | None = Field(default=None, description="Schedule for future execution (ISO 8601)")

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.options:
            payload["options"] = self.options
        if self.log_level:
            payload["loglevel"] = self.log_level
        if self.filter:
            payload["filter"] = self.filter
        if self.run_at_time:
            payload["runAtTime"] = self.run_at_time
        return payload
