# MIT License - Copyright (c) fintonlabs.com
from rundeck_mcp.tools.executions import (
    abort_execution,
    get_execution,
    get_execution_output,
    list_executions_for_job,
    run_job,
)
from rundeck_mcp.tools.jobs import (
    delete_job,
    get_job,
    import_job_yaml,
    list_jobs,
)
from rundeck_mcp.tools.projects import (
    create_project,
    get_project,
    list_projects,
)

read_tools = [
    list_projects,
    get_project,
    list_jobs,
    get_job,
    get_execution,
    list_executions_for_job,
    get_execution_output,
]

write_tools = [
    create_project,
    import_job_yaml,
    delete_job,
    run_job,
    abort_execution,
]
