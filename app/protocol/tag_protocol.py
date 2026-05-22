"""Tag Protocol v1 data structures.

Philosophy:
- AI agents coordinate by explicit tags, not by implicit natural-language guessing.
- Weight prefix controls priority; suffix can carry stage/tool hints.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TagCategory(str, Enum):
    capability = "capability"
    lifecycle = "lifecycle"
    behavior = "behavior"
    context = "context"


class TagRule(BaseModel):
    category: TagCategory
    value: str = Field(description="Semantic label, e.g. 需要编程/禁止联网/等待验收.")
    weight: int = Field(default=5, ge=1, le=99)
    suffix: Optional[str] = Field(
        default=None,
        description="Optional marker for phase, profile, or version.",
    )

    @property
    def token(self) -> str:
        suffix = f".{self.suffix}" if self.suffix else ""
        return f"#{self.weight}_{self.value}{suffix}"
