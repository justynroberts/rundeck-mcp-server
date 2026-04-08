# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Rundeck MCP server -- a Python MCP (Model Context Protocol) server that exposes Rundeck project, job, and execution management as tools for AI assistants. Follows the same architecture as the PagerDuty MCP server.

## Commands

```bash
# Install dependencies
uv sync --group dev

# Run tests
uv run pytest

# Run a single test
uv run pytest tests/test_models.py::TestJobModels::test_job_with_options

# Lint
uv run ruff check .

# Type check
uv run pyright

# Run server locally
RUNDECK_API_TOKEN=<token> RUNDECK_URL=http://localhost:4440 uv run rundeck-mcp --enable-write-tools
```

## Architecture

The server uses `FastMCP` from the `mcp` SDK. Tools are plain Python functions (no decorators) registered via `mcp.add_tool()` with `ToolAnnotations` marking them as read-only or destructive.

```
rundeck_mcp/
  __main__.py          # Entry point -> server.app() (Typer CLI)
  server.py            # FastMCP setup, tool registration, --enable-write-tools flag
  client.py            # RundeckClient (httpx-based REST client with pagination)
  context/             # Strategy pattern for client resolution
    context_strategy.py          # Protocol definition
    application_context_strategy.py  # Single-tenant (env var based)
  models/              # Pydantic models for API requests/responses
    base.py            # ListResponseModel[T], pagination constants
    projects.py        # Project, ProjectCreateRequest
    jobs.py            # Job, JobOption, JobQuery, JobImportResult
    executions.py      # Execution, ExecutionOutput, ExecutionQuery, JobRunRequest
  tools/               # Tool functions grouped by domain
    __init__.py        # read_tools[] and write_tools[] lists
    projects.py        # list_projects, get_project, create_project
    jobs.py            # list_jobs, get_job, import_job_yaml, delete_job
    executions.py      # run_job, get_execution, list_executions_for_job, get_execution_output, abort_execution
```

## Key Patterns

- **Tool functions** are plain functions with type-annotated params (Pydantic models for complex inputs). FastMCP auto-generates JSON schemas from the function signature and docstring.
- **Read/write split**: `read_tools` are always registered; `write_tools` require `--enable-write-tools` CLI flag.
- **Client access**: Always use `ContextResolver.get_client()` inside tools, never instantiate directly.
- **Rundeck API**: Uses httpx against `/api/{version}/` endpoints with `X-Rundeck-Auth-Token` header. Job import uses YAML content type directly.
- **Pagination**: Rundeck uses `offset`/`max` query params. `RundeckClient.paginate()` handles this. List endpoints like `/projects` and `/jobs` return plain arrays; `/executions` returns a wrapper with `paging` metadata.

## Environment Variables

- `RUNDECK_API_TOKEN` (required) -- API auth token
- `RUNDECK_URL` (default: `http://localhost:4440`) -- Rundeck base URL
- `RUNDECK_API_VERSION` (default: `41`) -- API version number
