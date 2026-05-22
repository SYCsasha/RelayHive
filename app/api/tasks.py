"""Task Center API: minimal create/list endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.task import Task, TaskCreate
from app.services.task_center import task_center

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    try:
        return task_center.create_task(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("", response_model=list[Task], status_code=status.HTTP_200_OK)
def list_tasks() -> list[Task]:
    return task_center.list_tasks()
