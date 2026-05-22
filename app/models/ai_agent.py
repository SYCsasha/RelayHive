"""AI Agent model and registry."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from app.db.base import Base
from app.core.enums import AIAgentCapability


# Association table for many-to-many relationship between AIAgent and Capabilities
ai_agent_capability_association = Table(
    'ai_agent_capability',
    Base.metadata,
    Column('agent_id', String, ForeignKey('ai_agent.agent_id', ondelete='CASCADE')),
    Column('capability', String, nullable=False),
)


class AIAgent(Base):
    """Registry of AI agents and their capabilities."""
    
    __tablename__ = "ai_agent"
    
    agent_id = Column(String, primary_key=True, index=True)
    agent_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    # Capabilities this agent can handle
    capabilities = relationship(
        "AIAgentCapabilityAssociation",
        back_populates="agent",
        cascade="all, delete-orphan",
        foreign_keys="AIAgentCapabilityAssociation.agent_id"
    )
    
    # Constraints and configuration
    max_concurrent_tasks = Column(Integer, default=5)
    supports_relay_handoff = Column(Boolean, default=True)
    requires_context_history = Column(Boolean, default=False)
    api_endpoint = Column(String, nullable=True)
    api_key_ref = Column(String, nullable=True)  # Reference to secure key storage
    
    # Configuration JSON
    config = Column(JSON, nullable=True, default={})
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    claimed_work_orders = relationship(
        "WorkOrder",
        back_populates="claiming_agent",
        foreign_keys="WorkOrder.claiming_agent_id"
    )
    relay_steps = relationship(
        "RelayStepHistory",
        back_populates="agent",
        foreign_keys="RelayStepHistory.agent_id"
    )
    
    def __repr__(self):
        return f"<AIAgent(agent_id={self.agent_id}, name={self.agent_name})>"


class AIAgentCapabilityAssociation(Base):
    """Association between AI agents and their capabilities."""
    
    __tablename__ = "ai_agent_capability_association"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_id = Column(String, ForeignKey('ai_agent.agent_id', ondelete='CASCADE'), nullable=False)
    capability = Column(String, nullable=False, index=True)
    proficiency_level = Column(Integer, default=1)  # 1-5 scale
    notes = Column(String, nullable=True)
    
    # Relationships
    agent = relationship("AIAgent", back_populates="capabilities")
    
    def __repr__(self):
        return f"<Capability(agent={self.agent_id}, capability={self.capability})>"
