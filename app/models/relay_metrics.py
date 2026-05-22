"""Relay chain performance metrics."""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from app.db.base import Base


class RelayMetrics(Base):
    """Performance metrics for work order relay chain."""
    
    __tablename__ = "relay_metrics"
    
    metric_id = Column(String, primary_key=True, index=True)
    work_order_id = Column(String, ForeignKey('work_order.work_order_id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    
    # Timing metrics (in seconds)
    total_execution_time = Column(Float, nullable=True)
    total_wait_time = Column(Float, nullable=True)
    avg_step_duration = Column(Float, nullable=True)
    
    # Cost metrics
    total_tokens_used = Column(Integer, nullable=True)
    total_cost = Column(Float, nullable=True)  # In USD
    
    # Relay statistics
    total_steps = Column(Integer, default=0)
    successful_steps = Column(Integer, default=0)
    failed_steps = Column(Integer, default=0)
    rejected_steps = Column(Integer, default=0)
    escalated_steps = Column(Integer, default=0)
    
    # Efficiency metrics
    success_rate = Column(Float, nullable=True)  # 0-1.0
    retry_count = Column(Integer, default=0)
    
    # Performance details (per-step breakdown)
    step_metrics = Column(JSON, nullable=True, default=[])  # List of per-step metrics
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    work_order = relationship("WorkOrder", back_populates="metrics", foreign_keys=[work_order_id])
    
    def __repr__(self):
        return f"<RelayMetrics(work_order={self.work_order_id}, success_rate={self.success_rate})>"
