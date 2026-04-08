# Rundeck MCP Server

A Model Context Protocol (MCP) server for [Rundeck](https://www.rundeck.com/), enabling AI assistants to manage projects, jobs, and executions through a standardized interface.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- A Rundeck instance with API access
- A Rundeck API Token (generate under **User Profile > API Tokens** in the Rundeck UI)

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RUNDECK_API_TOKEN` | Yes | - | Rundeck API authentication token |
| `RUNDECK_URL` | No | `http://localhost:4440` | Rundeck server base URL |
| `RUNDECK_API_VERSION` | No | `41` | Rundeck API version |

## MCP Client Configuration

### Claude Desktop / Claude Code

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "rundeck": {
      "command": "uvx",
      "args": ["rundeck-mcp"],
      "env": {
        "RUNDECK_API_TOKEN": "<your-api-token>"
      }
    }
  }
}
```

To enable write tools (create projects, import jobs, run jobs):

```json
{
  "mcpServers": {
    "rundeck": {
      "command": "uvx",
      "args": ["rundeck-mcp", "--enable-write-tools"],
      "env": {
        "RUNDECK_API_TOKEN": "<your-api-token>",
        "RUNDECK_URL": "http://your-rundeck-server:4440"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "rundeck": {
      "command": "uvx",
      "args": ["rundeck-mcp", "--enable-write-tools"],
      "env": {
        "RUNDECK_API_TOKEN": "<your-api-token>",
        "RUNDECK_URL": "http://your-rundeck-server:4440"
      }
    }
  }
}
```

### VS Code

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "rundeck": {
      "command": "uvx",
      "args": ["rundeck-mcp", "--enable-write-tools"],
      "env": {
        "RUNDECK_API_TOKEN": "<your-api-token>",
        "RUNDECK_URL": "http://your-rundeck-server:4440"
      }
    }
  }
}
```

## Docker

### Build

```bash
docker build -t rundeck-mcp .
```

### Run (read-only)

```bash
docker run -e RUNDECK_API_TOKEN=<token> -e RUNDECK_URL=http://your-rundeck:4440 rundeck-mcp
```

### Run (with write tools)

```bash
docker run -e RUNDECK_API_TOKEN=<token> -e RUNDECK_URL=http://your-rundeck:4440 rundeck-mcp --enable-write-tools
```

## Local Development

```bash
git clone https://github.com/your-org/rundeck-mcp-server.git
cd rundeck-mcp-server
uv sync --group dev
```

### Run tests

```bash
uv run pytest
```

### Lint and type check

```bash
uv run ruff check .
uv run pyright
```

### Run locally

```bash
export RUNDECK_API_TOKEN=<your-token>
export RUNDECK_URL=http://localhost:4440
uv run rundeck-mcp --enable-write-tools
```

## Available Tools

### Read Tools (always available)

| Tool | Description |
|------|-------------|
| `list_projects` | List all Rundeck projects |
| `get_project` | Get details for a specific project |
| `list_jobs` | List jobs in a project with optional filtering |
| `get_job` | Get full job definition including options and steps |
| `get_execution` | Get current status of a job execution |
| `list_executions_for_job` | List recent executions for a job |
| `get_execution_output` | Get log output from an execution |

### Write Tools (require `--enable-write-tools`)

| Tool | Description |
|------|-------------|
| `create_project` | Create a new Rundeck project |
| `import_job_yaml` | Import a job from YAML definition |
| `delete_job` | Delete a job |
| `run_job` | Execute a job with optional parameters |
| `abort_execution` | Abort a running execution |

### Job Execution Workflow

The server enforces a safe execution pattern:

1. **Discover**: Use `get_job` to retrieve the job definition and its options
2. **Present**: The AI presents option names, descriptions, defaults, required flags, and allowed values to the user
3. **Collect**: The user provides values for required and desired optional parameters
4. **Execute**: `run_job` is called with the collected option values
5. **Monitor**: Use `get_execution` and `get_execution_output` to track progress

## License

MIT License - Copyright (c) fintonlabs.com
