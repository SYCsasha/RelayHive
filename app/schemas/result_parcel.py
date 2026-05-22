"""Result parcel schema.

Result parcels are the only long-term assets in RelayHive relay flow.
Each parcel forms a version chain by (task_id, iteration).
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from enum import Enum

from pydantic import BaseModel, Field


class AssetType(str, Enum):
    """Supported output asset types for parcel manifest."""

    CODE = "code"
    DOCUMENT = "document"
    IMAGE = "image"
    DATA = "data"
    BINARY = "binary"
    OTHER = "other"


class ParcelAsset(BaseModel):
    """Single output asset attached to a result parcel."""

    path: str = Field(..., description="Relative or absolute storage path")
    asset_type: AssetType = Field(..., description="Output asset type")
    checksum: str | None = Field(default=None, description="Optional file checksum")
    description: str | None = Field(default=None, description="Asset business meaning")


class IterationMeta(BaseModel):
    """Producer and relay context for one parcel iteration."""

    producer_agent: str = Field(..., description="Agent that generated this parcel")
    source_task_id: str = Field(..., description="Task ID owning the parcel chain")
    parent_parcel_id: str | None = Field(default=None, description="Previous parcel in chain")
    iteration: int = Field(..., ge=1, description="Monotonic iteration number")


class ResultParcel(BaseModel):
    """Standard handover payload across profession-AI relays."""

    parcel_id: str = Field(..., description="Unique parcel id, e.g. parcel_task_1001_v2")
    task_id: str = Field(..., description="Task identity used by parcel registry")
    iteration_meta: IterationMeta
    content_summary: str = Field(..., min_length=1, description="Readable summary for next relay")
    assets: list[ParcelAsset] = Field(default_factory=list, description="Output assets of this iteration")
    referenced_tags: list[str] = Field(default_factory=list, description="Tag protocol references for next relay")
    retention_until: datetime = Field(..., description="Retention deadline, minimum now+7d")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="Creation timestamp")

    @classmethod
    def create_with_min_retention(
        cls,
        *,
        parcel_id: str,
        task_id: str,
        iteration_meta: IterationMeta,
        content_summary: str,
        assets: list[ParcelAsset] | None = None,
        referenced_tags: list[str] | None = None,
        minimum_days: int = 7,
    ) -> "ResultParcel":
        """Factory ensuring retention follows the at-least-7-days policy."""
        now = datetime.now(UTC)
        return cls(
            parcel_id=parcel_id,
            task_id=task_id,
            iteration_meta=iteration_meta,
            content_summary=content_summary,
            assets=assets or [],
            referenced_tags=referenced_tags or [],
            retention_until=now + timedelta(days=max(minimum_days, 7)),
            created_at=now,
        )


# Standard example: design parcel -> coding parcel -> QA parcel.
RESULT_PARCEL_EXAMPLE = ResultParcel.create_with_min_retention(
    parcel_id="parcel_task_1001_v2",
    task_id="task_1001",
    iteration_meta=IterationMeta(
        producer_agent="CodingAgent",
        source_task_id="task_1001",
        parent_parcel_id="parcel_task_1001_v1",
        iteration=2,
    ),
    content_summary="完成登录模块接口与基础鉴权，等待QA验收。",
    assets=[
        ParcelAsset(path="outputs/app/auth.py", asset_type=AssetType.CODE, description="认证逻辑实现"),
        ParcelAsset(path="outputs/docs/auth_api.md", asset_type=AssetType.DOCUMENT, description="接口说明文档"),
    ],
    referenced_tags=["#3_等待验收.ready", "#2_禁止联网"],
)
