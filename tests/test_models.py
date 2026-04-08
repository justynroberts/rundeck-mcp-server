# MIT License - Copyright (c) fintonlabs.com
from rundeck_mcp.models import (
    Execution,
    ExecutionOutput,
    ExecutionQuery,
    Job,
    JobQuery,
    JobRunRequest,
    ListResponseModel,
    Project,
    ProjectCreateRequest,
)


class TestProjectModels:
    def test_project_from_api(self):
        data = {"name": "MyProject", "description": "Test project", "url": "http://host/api/41/project/MyProject"}
        project = Project.model_validate(data)
        assert project.name == "MyProject"
        assert project.description == "Test project"

    def test_project_create_payload(self):
        req = ProjectCreateRequest(name="NewProject", description="A project", label="New")
        payload = req.to_payload()
        assert payload["name"] == "NewProject"
        assert payload["config"]["project.description"] == "A project"
        assert payload["config"]["project.label"] == "New"

    def test_project_create_minimal(self):
        req = ProjectCreateRequest(name="Minimal")
        payload = req.to_payload()
        assert payload == {"name": "Minimal"}


class TestJobModels:
    def test_job_from_api(self):
        data = {
            "id": "abc-123",
            "name": "Deploy",
            "group": "ops",
            "project": "MyProject",
            "description": "Deploy app",
            "scheduled": True,
            "enabled": True,
            "scheduleEnabled": True,
            "averageDuration": 5000,
        }
        job = Job.model_validate(data)
        assert job.id == "abc-123"
        assert job.schedule_enabled is True
        assert job.average_duration == 5000

    def test_job_with_options(self):
        data = {
            "id": "abc-123",
            "name": "Deploy",
            "project": "MyProject",
            "options": [
                {"name": "env", "required": True, "values": ["dev", "prod"], "enforced": True},
                {"name": "version", "required": False, "secure": False},
            ],
        }
        job = Job.model_validate(data)
        assert job.options is not None
        assert len(job.options) == 2
        assert job.options[0].name == "env"
        assert job.options[0].enforced is True

    def test_job_query_params(self):
        query = JobQuery(job_filter="deploy", group_path="ops", max=50)
        params = query.to_params()
        assert params["jobFilter"] == "deploy"
        assert params["groupPath"] == "ops"
        assert params["max"] == 50

    def test_job_query_defaults(self):
        query = JobQuery()
        params = query.to_params()
        assert params["max"] == 20
        assert params["offset"] == 0
        assert "jobFilter" not in params


class TestExecutionModels:
    def test_execution_from_api(self):
        data = {
            "id": 12345,
            "status": "succeeded",
            "project": "MyProject",
            "user": "admin",
            "date-started": {"unixtime": 1712592000000, "date": "2026-04-08T16:00:00Z"},
            "date-ended": {"unixtime": 1712592060000, "date": "2026-04-08T16:01:00Z"},
            "successfulNodes": ["node1"],
            "failedNodes": [],
        }
        execution = Execution.model_validate(data)
        assert execution.id == 12345
        assert execution.status == "succeeded"
        assert execution.successful_nodes == ["node1"]

    def test_execution_query_params(self):
        query = ExecutionQuery(status="running", max=10)
        params = query.to_params()
        assert params["status"] == "running"
        assert params["max"] == 10

    def test_job_run_request_payload(self):
        req = JobRunRequest(options={"env": "prod", "version": "1.0"}, log_level="DEBUG")
        payload = req.to_payload()
        assert payload["options"] == {"env": "prod", "version": "1.0"}
        assert payload["loglevel"] == "DEBUG"

    def test_job_run_request_empty(self):
        req = JobRunRequest()
        assert req.to_payload() == {}

    def test_execution_output(self):
        data = {
            "id": 12345,
            "completed": True,
            "execCompleted": True,
            "execState": "succeeded",
            "entries": [
                {"time": "16:00:01", "log": "Hello", "level": "NORMAL", "node": "localhost"},
            ],
        }
        output = ExecutionOutput.model_validate(data)
        assert output.completed is True
        assert len(output.entries) == 1
        assert output.entries[0].log == "Hello"


class TestListResponseModel:
    def test_summary(self):
        projects = [Project(name="A"), Project(name="B")]
        result = ListResponseModel[Project](response=projects)
        assert "2 record(s)" in result.response_summary
        assert "Project" in result.response_summary

    def test_empty(self):
        result = ListResponseModel[Project](response=[])
        assert "0 record(s)" in result.response_summary
