"""Result Package model for versioned outputs."""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from app.db.base import Base


class ResultPackage(Base):
    """Versioned result package from work order execution."""
    
    __tablename__ = "result_package"
    
    package_id = Column(String, primary_key=True, index=True)  # pkg_task_20260522_0001_v2
    work_order_id = Column(String, ForeignKey('work_order.work_order_id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Versioning
    version = Column(Integer, nullable=False)
    producer_agent_id = Column(String, ForeignKey('ai_agent.agent_id'), nullable=False)
    
    # Dependency tracking
    input_refs = Column(JSON, nullable=True, default=[])  # Previous package IDs
    
    # Quality metrics
    qa_summary = Column(JSON, nullable=True, default={})  # {passed: true, notes: "..."}
    confidence_score = Column(Float, nullable=True)  # 0-1.0
    
    # Next step recommendations
    next_tags = Column(JSON, nullable=True, default=[])
    next_agent_recommendation = Column(String, nullable=True)
    
    # Output metadata
    output_manifest = Column(JSON, nullable=True, default=[])  # List of output files with paths and hashes
    checksum = Column(String, nullable=True)  # sha256 of entire package
    
    # Audit trail
    execution_log = Column(Text, nullable=True)
    api_calls_made = Column(JSON, nullable=True, default=[])
    
    # Lifecycle
    is_final = Column(Boolean, default=False)
    retention_until = Column(DateTime, nullable=True)  # Auto-cleanup date
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    work_order = relationship("WorkOrder", back_populates="result_packages", foreign_keys=[work_order_id])
    producer_agent = relationship(
        "AIAgent",
        foreign_keys=[producer_agent_id],
        backref="produced_result_packages"
    )
    
    outputs = relationship(
        "ResultPackageOutput",
        back_populates="package",
        cascade="all, delete-orphan",
        foreign_keys="ResultPackageOutput.package_id"
    )
    
    def __repr__(self):
        return f"<ResultPackage(id={self.package_id}, version={self.version})>"


class ResultPackageOutput(Base):
    """Individual output artifacts from result package."""
    
    __tablename__ = "result_package_output"
    
    output_id = Column(String, primary_key=True, index=True)
    package_id = Column(String, ForeignKey('result_package.package_id', ondelete='CASCADE'), nullable=False, index=True)
    
    # File information
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=True)  # mime type
    file_size = Column(Integer, nullable=True)
    
    # Checksum and integrity
    sha256_hash = Column(String, nullable=True)
    
    # Storage location
    storage_location = Column(String, nullable=True)  # local, github, s3, etc.
    storage_path = Column(String, nullable=True)
    
    # Metadata
    description = Column(String, nullable=True)
    is_artifact = Column(Boolean, default=False)  # True for intermediate, False for final output
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    package = relationship("ResultPackage", back_populates="outputs", foreign_keys=[package_id])
    
    def __repr__(self):
        return f"<Output(path={self.file_path})>"
