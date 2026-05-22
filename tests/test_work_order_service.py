"""Tests for work order service."""

import pytest
from app.services.work_order_service import WorkOrderService
from app.schemas.work_order import WorkOrderCreate
from app.models.ai_agent import AIAgent
from app.models.work_order import WorkOrder


def test_create_work_order(db_session):
    """Test creating a work order."""
    # Create issuer agent first
    agent = AIAgent(
        agent_id="main_ai",
        agent_name="Main AI Translator",
        description="Main AI that issues work orders",
        is_active=True
    )
    db_session.add(agent)
    db_session.commit()
    
    # Create work order
    work_order_create = WorkOrderCreate(
        title="Test Work Order",
        description="This is a test work order",
        issuer_agent_id="main_ai",
        tags=["#1_analysis_required"],
        priority_level=2
    )
    
    work_order = WorkOrderService.create_work_order(work_order_create, db_session)
    
    assert work_order is not None
    assert work_order.work_order_id.startswith("wo_")
    assert work_order.title == "Test Work Order"
    assert work_order.issuer_agent_id == "main_ai"
    assert len(work_order.tags) > 0


def test_claim_work_order(db_session):
    """Test claiming a work order."""
    # Create agents
    issuer = AIAgent(
        agent_id="main_ai",
        agent_name="Main AI",
        is_active=True
    )
    worker = AIAgent(
        agent_id="worker_ai",
        agent_name="Worker AI",
        is_active=True
    )
    db_session.add(issuer)
    db_session.add(worker)
    db_session.commit()
    
    # Create work order
    work_order_create = WorkOrderCreate(
        title="Test",
        description="Test",
        issuer_agent_id="main_ai",
        tags=[]
    )
    work_order = WorkOrderService.create_work_order(work_order_create, db_session)
    
    # Claim it
    claimed = WorkOrderService.claim_work_order(
        work_order.work_order_id,
        "worker_ai",
        db_session
    )
    
    assert claimed.claiming_agent_id == "worker_ai"
    assert claimed.status == "claimed"
    assert len(claimed.relay_history) == 1


def test_query_available_work_orders(db_session):
    """Test querying available work orders for an agent."""
    # Create agents
    main_ai = AIAgent(
        agent_id="main_ai",
        agent_name="Main AI",
        is_active=True
    )
    from app.models.ai_agent import AIAgentCapabilityAssociation
    analysis_agent = AIAgent(
        agent_id="analysis_ai",
        agent_name="Analysis AI",
        is_active=True
    )
    analysis_agent.capabilities.append(
        AIAgentCapabilityAssociation(capability="analysis", proficiency_level=4)
    )
    
    db_session.add(main_ai)
    db_session.add(analysis_agent)
    db_session.commit()
    
    # Create work orders with different tags
    wo1 = WorkOrderCreate(
        title="Analysis Task",
        description="Needs analysis",
        issuer_agent_id="main_ai",
        tags=["#1_analysis_required"]
    )
    WorkOrderService.create_work_order(wo1, db_session)
    
    wo2 = WorkOrderCreate(
        title="Design Task",
        description="Needs design",
        issuer_agent_id="main_ai",
        tags=["#1_design_needed"]
    )
    WorkOrderService.create_work_order(wo2, db_session)
    
    # Query available for analysis agent
    available = WorkOrderService.query_available_work_orders(
        "analysis_ai",
        limit=10,
        db=db_session
    )
    
    # Should match analysis task only
    assert len(available) >= 1
    titles = [wo.title for wo in available]
    assert "Analysis Task" in titles


def test_reject_work_order(db_session):
    """Test rejecting a claimed work order."""
    # Setup
    agent1 = AIAgent(agent_id="agent1", agent_name="Agent 1", is_active=True)
    agent2 = AIAgent(agent_id="agent2", agent_name="Agent 2", is_active=True)
    db_session.add(agent1)
    db_session.add(agent2)
    db_session.commit()
    
    # Create and claim
    wo_create = WorkOrderCreate(
        title="Test",
        description="Test",
        issuer_agent_id="agent1",
        tags=[]
    )
    wo = WorkOrderService.create_work_order(wo_create, db_session)
    WorkOrderService.claim_work_order(wo.work_order_id, "agent2", db_session)
    
    # Reject
    rejected = WorkOrderService.reject_work_order(
        wo.work_order_id,
        "agent2",
        "Cannot handle this task",
        db_session
    )
    
    assert rejected.claiming_agent_id is None
    assert rejected.status == "created"
    assert len(rejected.relay_history) == 1
