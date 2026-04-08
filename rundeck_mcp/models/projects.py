# MIT License - Copyright (c) fintonlabs.com
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Project(BaseModel):
    """A Rundeck project."""

    name: str = Field(description="The project name (unique identifier)")
    description: str | None = Field(default=None, description="Project description")
    label: str | None = Field(default=None, description="Display label for the project")
    url: str | None = Field(default=None, description="API URL for this project")
    config: dict[str, Any] | None = Field(default=None, description="Project configuration properties")


class ProjectCreateRequest(BaseModel):
    """Request to create a new Rundeck project."""

    name: str = Field(description="The project name (must be unique, no spaces)")
    description: str | None = Field(default=None, description="Project description")
    label: str | None = Field(default=None, description="Display label")

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"name": self.name}
        config: dict[str, str] = {}
        if self.description:
            payload["description"] = self.description
            config["project.description"] = self.description
        if self.label:
            config["project.label"] = self.label
        if config:
            payload["config"] = config
        return payload
