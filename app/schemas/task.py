"""Task Center core data structures.

RelayHive uses task relay (not long chat context) as the core operating unit.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def generate_task_id() -> str:
    return f"task_{uuid4().hex[:12]}"


class TaskStatus(str, Enum):
    created = "created"
    ready = "ready"
    claimed = "claimed"
    in_progress = "in_progress"
    handover = "handover"
    review = "review"
    done = "done"
    blocked = "blocked"
    failed = "failed"


class TaskEventLogEntry(BaseModel):
    event_type: str = Field(description="Event type for relay timeline audit.")
    message: str = Field(description="Readable event summary.")
    timestamp: datetime = Field(default_factory=utc_now)


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=5000)
    tags: List[str] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.created
    parent_task_id: Optional[str] = None


class TaskCreate(TaskBase):
    event_log: List[TaskEventLogEntry] = Field(default_factory=list)


class Task(TaskBase):
    task_id: str = Field(default_factory=generate_task_id)
    child_task_ids: List[str] = Field(default_factory=list)
    event_log: List[TaskEventLogEntry] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
