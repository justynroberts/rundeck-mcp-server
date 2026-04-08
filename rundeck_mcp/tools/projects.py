# MIT License - Copyright (c) fintonlabs.com
from rundeck_mcp.context import ContextResolver
from rundeck_mcp.models import ListResponseModel, Project, ProjectCreateRequest


def list_projects() -> ListResponseModel[Project]:
    """List all Rundeck projects.

    Returns:
        List of all projects accessible to the current API token.
    """
    client = ContextResolver.get_client()
    data = client.rget("/projects")
    projects = [Project.model_validate(p) for p in data]
    return ListResponseModel[Project](response=projects)


def get_project(project_name: str) -> Project:
    """Get details for a specific project.

    Args:
        project_name: The name of the project to retrieve.

    Returns:
        The project details including configuration.
    """
    client = ContextResolver.get_client()
    data = client.rget(f"/project/{project_name}")
    return Project.model_validate(data)


def create_project(request: ProjectCreateRequest) -> Project:
    """Create a new Rundeck project.

    Args:
        request: Project creation parameters including name, description, and label.

    Returns:
        The newly created project.
    """
    client = ContextResolver.get_client()
    data = client.rpost("/projects", json=request.to_payload())
    return Project.model_validate(data)
