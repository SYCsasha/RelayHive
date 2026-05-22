"""Schemas for AI Agent related operations."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class AIAgentCapabilityBase(BaseModel):
    """Base schema for AI agent capability."""
    capability: str
    proficiency_level: int = Field(1, ge=1, le=5)
    notes: Optional[str] = None


class AIAgentCapabilityCreate(AIAgentCapabilityBase):
    """Schema for creating AI agent capability."""
    pass


class AIAgentCapabilityResponse(AIAgentCapabilityBase):
    """Schema for responding with AI agent capability."""
    id: int
    
    class Config:
        from_attributes = True


class AIAgentBase(BaseModel):
    """Base schema for AI Agent."""
    agent_id: str = Field(..., description="Unique identifier for the AI agent")
    agent_name: str = Field(..., description="Human-readable name")
    description: Optional[str] = None
    api_endpoint: Optional[str] = None
    max_concurrent_tasks: int = 5
    supports_relay_handoff: bool = True
    requires_context_history: bool = False


class AIAgentCreate(AIAgentBase):
    """Schema for creating an AI Agent."""
    capabilities: List[AIAgentCapabilityCreate] = []
    config: Optional[Dict[str, Any]] = {}


class AIAgentUpdate(BaseModel):
    """Schema for updating an AI Agent."""
    agent_name: Optional[str] = None
    description: Optional[str] = None
    api_endpoint: Optional[str] = None
    max_concurrent_tasks: Optional[int] = None
    supports_relay_handoff: Optional[bool] = None
    requires_context_history: Optional[bool] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None


class AIAgentResponse(AIAgentBase):
    """Schema for responding with AI Agent details."""
    capabilities: List[AIAgentCapabilityResponse]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AIAgentListResponse(BaseModel):
    """Schema for listing AI agents."""
    total: int
    agents: List[AIAgentResponse]
