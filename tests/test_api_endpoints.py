"""Tests for API endpoints."""

import json
import pytest


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_ai_agent(client, db_session):
    """Test creating an AI agent via API."""
    from app.models.ai_agent import AIAgent
    
    payload = {
        "agent_id": "test_agent",
        "agent_name": "Test Agent",
        "description": "A test agent",
        "capabilities": [
            {
                "capability": "analysis",
                "proficiency_level": 4
            }
        ]
    }
    
    response = client.post("/v1/ai-agents", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["agent_id"] == "test_agent"
    assert data["agent_name"] == "Test Agent"
    assert len(data["capabilities"]) == 1


def test_create_work_order_via_api(client, db_session):
    """Test creating a work order via API."""
    from app.models.ai_agent import AIAgent
    
    # First create an issuer agent
    agent = AIAgent(
        agent_id="main_ai",
        agent_name="Main AI",
        is_active=True
    )
    db_session.add(agent)
    db_session.commit()
    
    # Then create work order
    payload = {
        "title": "Test Work Order",
        "description": "This is a test",
        "issuer_agent_id": "main_ai",
        "tags": ["#1_analysis_required"],
        "priority_level": 2
    }
    
    response = client.post("/v1/workorders", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Work Order"
    assert data["issuer_agent_id"] == "main_ai"


def test_list_work_orders(client, db_session):
    """Test listing work orders."""
    from app.models.ai_agent import AIAgent
    from app.models.work_order import WorkOrder
    
    # Create agent and work order
    agent = AIAgent(agent_id="main_ai", agent_name="Main AI", is_active=True)
    db_session.add(agent)
    db_session.commit()
    
    wo = WorkOrder(
        work_order_id="test_wo",
        title="Test",
        description="Test",
        issuer_agent_id="main_ai",
        status="created"
    )
    db_session.add(wo)
    db_session.commit()
    
    response = client.get("/v1/workorders")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1


def test_claim_work_order_via_api(client, db_session):
    """Test claiming a work order via API."""
    from app.models.ai_agent import AIAgent
    from app.models.work_order import WorkOrder
    
    # Create agents
    issuer = AIAgent(agent_id="main_ai", agent_name="Main AI", is_active=True)
    worker = AIAgent(agent_id="worker_ai", agent_name="Worker AI", is_active=True)
    db_session.add(issuer)
    db_session.add(worker)
    db_session.commit()
    
    # Create work order
    wo = WorkOrder(
        work_order_id="test_wo_claim",
        title="Test",
        description="Test",
        issuer_agent_id="main_ai",
        status="created"
    )
    db_session.add(wo)
    db_session.commit()
    
    # Claim it
    response = client.post(
        "/v1/workorders/test_wo_claim/claim",
        json={"agent_id": "worker_ai"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "claimed"
    assert data["claiming_agent_id"] == "worker_ai"
