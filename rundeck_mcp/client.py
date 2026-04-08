# MIT License - Copyright (c) fintonlabs.com
from __future__ import annotations

import os
from importlib import metadata
from typing import Any

import httpx

from rundeck_mcp import DIST_NAME


class RundeckClient:
    """HTTP client for the Rundeck API."""

    def __init__(self, base_url: str, api_token: str, api_version: int = 41) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_version = api_version
        self._token = api_token
        try:
            version = metadata.version(DIST_NAME)
        except metadata.PackageNotFoundError:
            version = "dev"
        self._client = httpx.Client(
            base_url=f"{self.base_url}/api/{self.api_version}",
            headers={
                "X-Rundeck-Auth-Token": self._token,
                "Accept": "application/json",
                "User-Agent": f"{DIST_NAME}/{version}",
            },
            timeout=30.0,
        )

    def rget(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """GET request returning parsed JSON."""
        response = self._client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    def rpost(self, path: str, json: dict[str, Any] | None = None, content: str | None = None,
              content_type: str | None = None) -> Any:
        """POST request returning parsed JSON."""
        headers = {}
        if content_type:
            headers["Content-Type"] = content_type
        if content is not None:
            response = self._client.post(path, content=content, headers=headers)
        else:
            headers["Content-Type"] = "application/json"
            response = self._client.post(path, json=json, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return None
        return response.json()

    def rdelete(self, path: str) -> None:
        """DELETE request."""
        response = self._client.delete(path)
        response.raise_for_status()

    def paginate(self, path: str, result_key: str, params: dict[str, Any] | None = None,
                 max_results: int = 200) -> list[dict[str, Any]]:
        """Paginate through results using offset/max pattern."""
        params = dict(params) if params else {}
        page_size = min(max_results, 100)
        params["max"] = page_size
        params["offset"] = 0
        results: list[dict[str, Any]] = []

        while len(results) < max_results:
            data = self.rget(path, params=params)

            # Some endpoints return a list directly (e.g. /projects, /jobs)
            if isinstance(data, list):
                results.extend(data)
                break

            # Others return a paging wrapper (e.g. executions)
            items = data.get(result_key, [])
            results.extend(items)
            paging = data.get("paging", {})
            total = paging.get("total", len(items))
            if len(results) >= total or len(items) < page_size:
                break
            params["offset"] = len(results)

        return results[:max_results]


def create_rundeck_client() -> RundeckClient:
    """Create a RundeckClient from environment variables."""
    api_token = os.getenv("RUNDECK_API_TOKEN")
    if not api_token:
        raise RuntimeError(
            "RUNDECK_API_TOKEN environment variable is required. "
            "Generate a token in Rundeck under User Profile > API Tokens."
        )
    base_url = os.getenv("RUNDECK_URL", "http://localhost:4440")
    api_version = int(os.getenv("RUNDECK_API_VERSION", "41"))
    return RundeckClient(base_url, api_token, api_version)
