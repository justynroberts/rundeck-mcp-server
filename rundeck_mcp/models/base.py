# MIT License - Copyright (c) fintonlabs.com
from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, computed_field

MAX_RESULTS = 200
DEFAULT_PAGINATION_LIMIT = 20
MAXIMUM_PAGINATION_LIMIT = 100

T = TypeVar("T", bound=BaseModel)


class ListResponseModel(BaseModel, Generic[T]):
    """Generic wrapper for list responses with a summary."""

    response: list[T]

    @computed_field
    @property
    def response_summary(self) -> str:
        count = len(self.response)
        type_name = self.response[0].__class__.__name__ if self.response else "unknown"
        summary = f"ListResponseModel<{type_name}>: Returned {count} record(s)"
        if count >= MAX_RESULTS:
            summary += " (result limit reached, there may be more records)"
        return summary
