"""In-memory Task Center service for MVP bootstrap."""

from __future__ import annotations

from typing import Dict, List

from app.schemas.task import Task, TaskCreate, TaskEventLogEntry


class TaskCenter:
    def __init__(self) -> None:
        self._tasks: Dict[str, Task] = {}

    def create_task(self, payload: TaskCreate) -> Task:
        if payload.parent_task_id and payload.parent_task_id not in self._tasks:
            raise ValueError("parent_task_id does not exist")

        task = Task(**payload.model_dump())
        if not task.event_log:
            task.event_log.append(
                TaskEventLogEntry(
                    event_type="TASK_CREATED",
                    message="Task created in Task Center",
                )
            )

        self._tasks[task.task_id] = task

        if task.parent_task_id:
            parent = self._tasks[task.parent_task_id]
            if task.task_id not in parent.child_task_ids:
                parent.child_task_ids.append(task.task_id)
                parent.event_log.append(
                    TaskEventLogEntry(
                        event_type="TASK_CHILD_LINKED",
                        message=f"Child task linked: {task.task_id}",
                    )
                )

        return task

    def list_tasks(self) -> List[Task]:
        return list(self._tasks.values())

    def reset(self) -> None:
        self._tasks.clear()


task_center = TaskCenter()
