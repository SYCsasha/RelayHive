"""Relay step history tracking."""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from app.db.base import Base


class RelayStepHistory(Base):
    """Track each step in the relay chain."""
    
    __tablename__ = "relay_step_history"
    
    step_id = Column(String, primary_key=True, index=True)
    work_order_id = Column(String, ForeignKey('work_order.work_order_id', ondelete='CASCADE'), nullable=False, index=True)
    agent_id = Column(String, ForeignKey('ai_agent.agent_id'), nullable=False, index=True)
    
    # Step sequence
    step_number = Column(Integer, nullable=False)  # 0, 1, 2, ...
    status = Column(String, nullable=False, default="pending")  # pending, claimed, in_progress, completed, failed, rejected, escalated
    
    # Execution details
    claimed_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Execution metadata
    execution_log = Column(Text, nullable=True)
    api_calls_made = Column(JSON, nullable=True, default=[])
    error_message = Column(Text, nullable=True)
    
    # Relationships
    work_order = relationship("WorkOrder", back_populates="relay_history", foreign_keys=[work_order_id])
    agent = relationship("AIAgent", back_populates="relay_steps", foreign_keys=[agent_id])
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<RelayStep(work_order={self.work_order_id}, step={self.step_number}, agent={self.agent_id})>"
