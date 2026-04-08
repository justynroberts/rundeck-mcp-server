# MIT License - Copyright (c) fintonlabs.com
from collections.abc import Callable

import typer
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from rundeck_mcp.context import ContextResolver
from rundeck_mcp.context.application_context_strategy import ApplicationContextStrategy
from rundeck_mcp.tools import read_tools, write_tools

app = typer.Typer()

MCP_SERVER_INSTRUCTIONS = """
When the user asks about their Rundeck environment, use the available tools to query
projects, jobs, and executions.

READ operations are safe to use. WRITE operations (creating projects, importing jobs,
running jobs) can modify the live Rundeck environment. Always confirm with the user
before using any tool marked as destructive.

When running a job that has options, first retrieve the job definition to discover
available options, their defaults, required flags, and allowed values. Present these
to the user and collect values before executing.
"""


def add_read_only_tool(mcp_instance: FastMCP, tool: Callable) -> None:
    mcp_instance.add_tool(
        tool,
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True),
    )


def add_write_tool(mcp_instance: FastMCP, tool: Callable) -> None:
    mcp_instance.add_tool(
        tool,
        annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True, idempotentHint=False),
    )


@app.command()
def run(*, enable_write_tools: bool = False) -> None:
    """Start the Rundeck MCP server."""
    ContextResolver.set_strategy(ApplicationContextStrategy())
    mcp = FastMCP("Rundeck MCP Server", instructions=MCP_SERVER_INSTRUCTIONS)
    for tool in read_tools:
        add_read_only_tool(mcp, tool)
    if enable_write_tools:
        for tool in write_tools:
            add_write_tool(mcp, tool)
    mcp.run()
