"""Schemas for Work Order related operations."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class WorkOrderTagBase(BaseModel):
    """Base schema for work order tag."""
    tag_text: str = Field(..., description="Tag text, e.g., #1_analysis_required")
    weight: int = Field(..., ge=1, le=5, description="Priority weight")
    category: str = Field(..., description="Tag category: functional, behavioral, process, context")
    description: Optional[str] = None


class WorkOrderTagCreate(WorkOrderTagBase):
    """Schema for creating a work order tag."""
    pass


class WorkOrderTagResponse(WorkOrderTagBase):
    """Schema for responding with a work order tag."""
    tag_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class WorkOrderBase(BaseModel):
    """Base schema for Work Order."""
    title: str = Field(..., description="Work order title")
    description: str = Field(..., description="Detailed description")
    priority_level: int = Field(3, ge=1, le=5, description="1=highest, 5=lowest")
    estimated_complexity: Optional[float] = Field(None, ge=0, le=100)
    max_relay_depth: int = 10


class WorkOrderCreate(WorkOrderBase):
    """Schema for creating a Work Order."""
    issuer_agent_id: str = Field(..., description="ID of the AI agent issuing the order")
    tags: List[str] = Field([], description="List of tag texts")
    acceptance_criteria: Optional[List[str]] = []
    ai_readable_requirements: Optional[str] = None
    context_data: Optional[Dict[str, Any]] = {}
    dependency_ids: Optional[List[str]] = []


class WorkOrderUpdate(BaseModel):
    """Schema for updating a Work Order."""
    title: Optional[str] = None
    description: Optional[str] = None
    priority_level: Optional[int] = None
    status: Optional[str] = None
    acceptance_criteria: Optional[List[str]] = None
    ai_readable_requirements: Optional[str] = None


class WorkOrderClaimRequest(BaseModel):
    """Schema for claiming a work order."""
    agent_id: str = Field(..., description="AI agent claiming the work order")


class WorkOrderRejectRequest(BaseModel):
    """Schema for rejecting a work order."""
    agent_id: str
    reason: str


class WorkOrderResponse(WorkOrderBase):
    """Schema for responding with Work Order details."""
    work_order_id: str
    issuer_agent_id: str
    claiming_agent_id: Optional[str] = None
    status: str
    relay_chain_depth: int
    current_relay_step: int
    tags: List[WorkOrderTagResponse]
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class WorkOrderListResponse(BaseModel):
    """Schema for listing work orders."""
    total: int
    work_orders: List[WorkOrderResponse]


class WorkOrderDetailResponse(WorkOrderResponse):
    """Detailed work order response with relay history."""
    relay_history: List[Dict[str, Any]] = []
    result_packages: List[Dict[str, Any]] = []
