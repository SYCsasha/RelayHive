"""Work Order model - core task unit for AI relay."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text, Boolean, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from app.db.base import Base
from app.core.enums import WorkOrderStatus


# Association table for many-to-many relationship between WorkOrder and Tags
work_order_tag_association = Table(
    'work_order_tag_association',
    Base.metadata,
    Column('work_order_id', String, ForeignKey('work_order.work_order_id', ondelete='CASCADE')),
    Column('tag_id', Integer, ForeignKey('work_order_tag_model.tag_id', ondelete='CASCADE')),
)


class WorkOrder(Base):
    """Work Order model - extends Task for AI-native execution."""
    
    __tablename__ = "work_order"
    
    work_order_id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    # AI-specific fields
    issuer_agent_id = Column(String, ForeignKey('ai_agent.agent_id'), nullable=False, index=True)
    claiming_agent_id = Column(String, ForeignKey('ai_agent.agent_id'), nullable=True, index=True)
    
    # Status and lifecycle
    status = Column(String, default=WorkOrderStatus.CREATED, nullable=False, index=True)
    priority_level = Column(Integer, default=3)  # 1=highest, 5=lowest
    
    # Relay management
    relay_chain_depth = Column(Integer, default=0)
    max_relay_depth = Column(Integer, default=10)
    current_relay_step = Column(Integer, default=0)
    
    # Complexity estimation
    estimated_complexity = Column(Float, nullable=True)  # 0-100 scale
    
    # Execution requirements
    acceptance_criteria = Column(JSON, nullable=True, default=[])
    ai_readable_requirements = Column(Text, nullable=True)
    
    # Tags and routing
    tags = relationship(
        "WorkOrderTag",
        secondary=work_order_tag_association,
        back_populates="work_orders",
        cascade="all, delete"
    )
    
    # Context and dependencies
    context_data = Column(JSON, nullable=True, default={})
    dependency_ids = Column(JSON, nullable=True, default=[])
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    issuer = relationship(
        "AIAgent",
        foreign_keys=[issuer_agent_id],
        backref="issued_work_orders"
    )
    claiming_agent = relationship(
        "AIAgent",
        foreign_keys=[claiming_agent_id],
        back_populates="claimed_work_orders"
    )
    
    relay_history = relationship(
        "RelayStepHistory",
        back_populates="work_order",
        cascade="all, delete-orphan",
        foreign_keys="RelayStepHistory.work_order_id"
    )
    
    result_packages = relationship(
        "ResultPackage",
        back_populates="work_order",
        cascade="all, delete-orphan",
        foreign_keys="ResultPackage.work_order_id"
    )
    
    metrics = relationship(
        "RelayMetrics",
        back_populates="work_order",
        cascade="all, delete-orphan",
        uselist=False,
        foreign_keys="RelayMetrics.work_order_id"
    )
    
    def __repr__(self):
        return f"<WorkOrder(id={self.work_order_id}, status={self.status})>"


class WorkOrderTag(Base):
    """Tags for work order protocol and routing."""
    
    __tablename__ = "work_order_tag_model"
    
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    tag_text = Column(String, unique=True, nullable=False, index=True)  # e.g., "#1_analysis_required"
    weight = Column(Integer, nullable=False)  # 1 (highest) to 5 (lowest)
    category = Column(String, nullable=False)  # functional, behavioral, process, context
    description = Column(String, nullable=True)
    
    # Related work orders
    work_orders = relationship(
        "WorkOrder",
        secondary=work_order_tag_association,
        back_populates="tags"
    )
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Tag({self.tag_text})>"
