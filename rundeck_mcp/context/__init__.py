# MIT License - Copyright (c) fintonlabs.com
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rundeck_mcp.client import RundeckClient
    from rundeck_mcp.context.context_strategy import ContextStrategy


class ContextResolver:
    """Resolves the current Rundeck client using a pluggable strategy."""

    _strategy: ContextStrategy | None = None

    @classmethod
    def set_strategy(cls, strategy: ContextStrategy) -> None:
        cls._strategy = strategy

    @classmethod
    def get_client(cls) -> RundeckClient:
        if cls._strategy is None:
            raise RuntimeError("Context strategy has not been set. Call ContextResolver.set_strategy() first.")
        return cls._strategy.get_client()
