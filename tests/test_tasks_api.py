from fastapi.testclient import TestClient

from app.main import app
from app.services.task_center import task_center

client = TestClient(app)


def setup_function() -> None:
    task_center.reset()


def test_create_and_list_task() -> None:
    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Build coding task",
            "description": "Relay-ready coding task",
            "tags": ["#1_需要编程", "#2_禁止联网"],
            "status": "ready",
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "Build coding task"
    assert created["event_log"][0]["event_type"] == "TASK_CREATED"

    list_response = client.get("/api/v1/tasks")
    assert list_response.status_code == 200
    tasks = list_response.json()
    assert len(tasks) == 1
    assert tasks[0]["task_id"] == created["task_id"]


def test_parent_child_task_linking() -> None:
    parent_resp = client.post(
        "/api/v1/tasks",
        json={
            "title": "Parent task",
            "description": "Top-level relay task",
            "tags": ["#1_需要调研"],
        },
    )
    assert parent_resp.status_code == 201
    parent_task_id = parent_resp.json()["task_id"]

    child_resp = client.post(
        "/api/v1/tasks",
        json={
            "title": "Child task",
            "description": "Sub-step execution",
            "parent_task_id": parent_task_id,
            "tags": ["#2_需要编程"],
        },
    )
    assert child_resp.status_code == 201
    child_task_id = child_resp.json()["task_id"]

    tasks = client.get("/api/v1/tasks").json()
    parent = next(task for task in tasks if task["task_id"] == parent_task_id)
    assert child_task_id in parent["child_task_ids"]


def test_create_task_with_missing_parent_fails() -> None:
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Broken child",
            "description": "Should fail",
            "parent_task_id": "task_not_found",
        },
    )
    assert response.status_code == 400
    assert "parent_task_id does not exist" in response.json()["detail"]
