# MIT License - Copyright (c) fintonlabs.com
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from rundeck_mcp.client import RundeckClient


@runtime_checkable
class ContextStrategy(Protocol):
    """Protocol for resolving the Rundeck client."""

    def get_client(self) -> RundeckClient: ...
