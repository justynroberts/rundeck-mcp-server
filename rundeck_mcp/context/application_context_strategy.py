# MIT License - Copyright (c) fintonlabs.com
from __future__ import annotations

from rundeck_mcp.client import RundeckClient, create_rundeck_client


class ApplicationContextStrategy:
    """Single-tenant strategy that creates a client once from environment variables."""

    def __init__(self) -> None:
        self._client: RundeckClient | None = None

    def get_client(self) -> RundeckClient:
        if self._client is None:
            self._client = create_rundeck_client()
        return self._client
