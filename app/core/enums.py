"""Enumeration types for Work Order System."""

from enum import Enum


class WorkOrderStatus(str, Enum):
    """Work Order lifecycle states."""
    CREATED = "created"  # AI-issued but not claimed
    CLAIMED = "claimed"  # AI has accepted
    IN_PROGRESS = "in_progress"  # AI actively processing
    HANDOVER_PENDING = "handover_pending"  # Waiting for next AI to claim
    RELAY_REQUIRED = "relay_required"  # Multiple AIs to process in sequence
    COMPLETED = "completed"  # Final delivery ready
    BLOCKED = "blocked"  # Cannot proceed, escalation needed
    FAILED = "failed"  # Execution failed


class AIAgentCapability(str, Enum):
    """AI agent capability types."""
    ANALYSIS = "analysis"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    REVIEW = "review"
    TRANSLATION = "translation"
    RESEARCH = "research"
    COORDINATION = "coordination"


class TagCategory(str, Enum):
    """Tag categories for protocol classification."""
    FUNCTIONAL = "functional"  # Task ability requirements
    BEHAVIORAL = "behavioral"  # Execution constraints
    PROCESS = "process"  # Stage/workflow tags
    CONTEXT = "context"  # Input scope requirements


class RelayStepStatus(str, Enum):
    """Status of individual relay steps."""
    PENDING = "pending"
    CLAIMED = "claimed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    REJECTED = "rejected"
    ESCALATED = "escalated"
