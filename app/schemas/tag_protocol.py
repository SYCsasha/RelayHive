"""Tag protocol schema.

Tag format (v1):
    #<weight>_<name>[.<suffix>]

Examples:
    #1_需要设计
    #2_需要编程.blocked
    #3_等待验收.ready
"""

from __future__ import annotations

from enum import Enum
import re

from pydantic import BaseModel, Field, field_validator

TAG_PATTERN = re.compile(r"^#(?P<weight>\d+?)_(?P<name>[\w\u4e00-\u9fa5-]+?)(?:\.(?P<suffix>[\w-]+))?$")


class TagCategory(str, Enum):
    """High-level categories for script routing and policy checks."""

    FUNCTION = "function"
    LIFECYCLE = "lifecycle"
    BEHAVIOR = "behavior"
    CONTEXT = "context"


class TagProtocol(BaseModel):
    """Normalized protocol object used by rule engines and task handover."""

    raw: str = Field(..., description="Original protocol text such as #1_需要设计")
    category: TagCategory = Field(..., description="Tag category")
    weight: int = Field(..., ge=1, le=99, description="Priority weight, smaller is stronger")
    name: str = Field(..., min_length=1, description="Semantic tag label")
    suffix: str | None = Field(default=None, description="Optional phase marker (e.g., blocked, ready)")
    notes: str | None = Field(default=None, description="Human explanation for this tag intent")

    @field_validator("raw")
    @classmethod
    def validate_raw(cls, value: str) -> str:
        if not TAG_PATTERN.match(value):
            raise ValueError("tag must match #<weight>_<name>[.<suffix>]")
        return value

    @classmethod
    def from_raw(cls, raw: str, category: TagCategory, notes: str | None = None) -> "TagProtocol":
        """Parse a raw tag string into a typed protocol object."""
        match = TAG_PATTERN.match(raw)
        if not match:
            raise ValueError("invalid tag format")
        return cls(
            raw=raw,
            category=category,
            weight=int(match.group("weight")),
            name=match.group("name"),
            suffix=match.group("suffix"),
            notes=notes,
        )


# Canonical examples to guide new profession-AI integrations.
TAG_PROTOCOL_EXAMPLES: list[TagProtocol] = [
    TagProtocol.from_raw("#1_需要设计", category=TagCategory.FUNCTION, notes="先出设计，再进入编程链"),
    TagProtocol.from_raw("#2_需要编程", category=TagCategory.FUNCTION, notes="触发编程职业AI接单"),
    TagProtocol.from_raw("#2_禁止联网", category=TagCategory.BEHAVIOR, notes="限制执行环境联网能力"),
    TagProtocol.from_raw("#3_等待验收.ready", category=TagCategory.LIFECYCLE, notes="进入验收阶段，可被QA脚本命中"),
    TagProtocol.from_raw("#4_仅当前任务", category=TagCategory.CONTEXT, notes="上下文读取范围限制为当前任务包裹"),
]
