"""Schemas for Result Package related operations."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ResultPackageOutputBase(BaseModel):
    """Base schema for result package output."""
    file_path: str
    file_type: Optional[str] = None
    description: Optional[str] = None
    is_artifact: bool = False


class ResultPackageOutputCreate(ResultPackageOutputBase):
    """Schema for creating result package output."""
    pass


class ResultPackageOutputResponse(ResultPackageOutputBase):
    """Schema for responding with result package output."""
    output_id: str
    file_size: Optional[int] = None
    sha256_hash: Optional[str] = None
    storage_location: Optional[str] = None
    storage_path: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ResultPackageBase(BaseModel):
    """Base schema for Result Package."""
    version: int
    qa_summary: Optional[Dict[str, Any]] = {}
    confidence_score: Optional[float] = Field(None, ge=0, le=1)
    next_tags: List[str] = []
    next_agent_recommendation: Optional[str] = None


class ResultPackageCreate(ResultPackageBase):
    """Schema for creating a Result Package."""
    work_order_id: str
    producer_agent_id: str
    input_refs: List[str] = []
    execution_log: Optional[str] = None
    api_calls_made: List[Dict[str, Any]] = []
    outputs: List[ResultPackageOutputCreate] = []
    output_manifest: List[Dict[str, Any]] = []


class ResultPackageResponse(ResultPackageBase):
    """Schema for responding with Result Package."""
    package_id: str
    work_order_id: str
    producer_agent_id: str
    input_refs: List[str]
    checksum: Optional[str] = None
    is_final: bool
    outputs: List[ResultPackageOutputResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ResultPackagePublishRequest(BaseModel):
    """Schema for publishing a result package."""
    producer_agent_id: str
    qa_summary: Optional[Dict[str, Any]] = {}
    confidence_score: Optional[float] = None
    next_tags: List[str] = []
    next_agent_recommendation: Optional[str] = None
    execution_log: Optional[str] = None
    api_calls_made: List[Dict[str, Any]] = []
    outputs: List[ResultPackageOutputCreate] = []
    is_final: bool = False
