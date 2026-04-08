# MIT License - Copyright (c) fintonlabs.com
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from rundeck_mcp.models.base import DEFAULT_PAGINATION_LIMIT, MAXIMUM_PAGINATION_LIMIT


class JobOption(BaseModel):
    """A single option defined on a Rundeck job."""

    name: str = Field(description="Option name")
    description: str | None = Field(default=None, description="Human-readable description")
    required: bool = Field(default=False, description="Whether this option is required")
    value: str | None = Field(default=None, description="Default value")
    values: list[str] | None = Field(default=None, description="List of allowed values")
    enforced: bool = Field(default=False, description="If true, only listed values are accepted")
    regex: str | None = Field(default=None, description="Validation regex pattern")
    secure: bool = Field(default=False, description="If true, value is not logged or stored in history")
    multivalued: bool = Field(default=False, description="If true, accepts multiple values")
    delimiter: str | None = Field(default=None, description="Separator for multivalued options")
    type: str | None = Field(default=None, description="Option type (text or file)")


class Job(BaseModel):
    """A Rundeck job definition."""

    id: str = Field(description="Unique job identifier (UUID)")
    name: str = Field(description="Job name")
    group: str | None = Field(default=None, description="Job group path (e.g. 'deploy/web')")
    project: str = Field(description="Project this job belongs to")
    description: str | None = Field(default=None, description="Job description")
    href: str | None = Field(default=None, description="API URL for this job")
    permalink: str | None = Field(default=None, description="Web UI URL for this job")
    scheduled: bool | None = Field(default=None, description="Whether this job has a schedule")
    enabled: bool | None = Field(default=None, description="Whether this job is enabled")
    schedule_enabled: bool | None = Field(
        default=None, alias="scheduleEnabled", description="Whether schedule is enabled"
    )
    average_duration: int | None = Field(
        default=None, alias="averageDuration", description="Average run duration in ms"
    )
    options: list[JobOption] | None = Field(default=None, description="Job options/parameters")
    sequence: dict[str, Any] | None = Field(default=None, description="Job step sequence definition")

    model_config = {"populate_by_name": True}


class JobQuery(BaseModel):
    """Query parameters for listing jobs."""

    job_filter: str | None = Field(default=None, description="Filter by job name (substring match)")
    job_exact_filter: str | None = Field(default=None, description="Filter by exact job name")
    group_path: str | None = Field(default=None, description="Filter by group path")
    group_path_exact: str | None = Field(default=None, description="Exact group path match")
    scheduled_filter: bool | None = Field(default=None, description="Filter by scheduled status")
    execution_enabled_filter: bool | None = Field(default=None, description="Filter by execution enabled")
    max: int = Field(default=DEFAULT_PAGINATION_LIMIT, ge=1, le=MAXIMUM_PAGINATION_LIMIT, description="Max results")
    offset: int = Field(default=0, ge=0, description="Pagination offset")

    def to_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {"max": self.max, "offset": self.offset}
        if self.job_filter:
            params["jobFilter"] = self.job_filter
        if self.job_exact_filter:
            params["jobExactFilter"] = self.job_exact_filter
        if self.group_path:
            params["groupPath"] = self.group_path
        if self.group_path_exact:
            params["groupPathExact"] = self.group_path_exact
        if self.scheduled_filter is not None:
            params["scheduledFilter"] = str(self.scheduled_filter).lower()
        if self.execution_enabled_filter is not None:
            params["executionEnabledFilter"] = str(self.execution_enabled_filter).lower()
        return params


class JobImportResult(BaseModel):
    """Result of a job import operation."""

    succeeded: list[dict[str, Any]] = Field(default_factory=list, description="Successfully imported jobs")
    failed: list[dict[str, Any]] = Field(default_factory=list, description="Jobs that failed to import")
    skipped: list[dict[str, Any]] = Field(default_factory=list, description="Jobs that were skipped")
