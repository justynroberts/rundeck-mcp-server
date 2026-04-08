# MIT License - Copyright (c) fintonlabs.com
FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml .
RUN uv pip install --system .

COPY rundeck_mcp/ rundeck_mcp/

ENTRYPOINT ["rundeck-mcp"]
