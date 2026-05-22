"""AI Agent management endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.ai_agent import AIAgent, AIAgentCapabilityAssociation
from app.schemas.ai_agent import (
    AIAgentCreate,
    AIAgentUpdate,
    AIAgentResponse,
    AIAgentListResponse,
    AIAgentCapabilityCreate
)

router = APIRouter(prefix="/ai-agents")


@router.post("", response_model=AIAgentResponse, status_code=status.HTTP_201_CREATED)
def create_ai_agent(
    agent_create: AIAgentCreate,
    db: Session = Depends(get_db)
):
    """Create a new AI agent."""
    # Check if agent already exists
    existing = db.query(AIAgent).filter(
        AIAgent.agent_id == agent_create.agent_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Agent {agent_create.agent_id} already exists"
        )
    
    agent = AIAgent(
        agent_id=agent_create.agent_id,
        agent_name=agent_create.agent_name,
        description=agent_create.description,
        api_endpoint=agent_create.api_endpoint,
        max_concurrent_tasks=agent_create.max_concurrent_tasks,
        supports_relay_handoff=agent_create.supports_relay_handoff,
        requires_context_history=agent_create.requires_context_history,
        config=agent_create.config or {}
    )
    
    # Add capabilities
    for cap_create in agent_create.capabilities:
        capability = AIAgentCapabilityAssociation(
            capability=cap_create.capability,
            proficiency_level=cap_create.proficiency_level,
            notes=cap_create.notes
        )
        agent.capabilities.append(capability)
    
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return agent


@router.get("/{agent_id}", response_model=AIAgentResponse)
def get_ai_agent(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Get AI agent by ID."""
    agent = db.query(AIAgent).filter(
        AIAgent.agent_id == agent_id
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )
    
    return agent


@router.get("", response_model=AIAgentListResponse)
def list_ai_agents(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all AI agents."""
    total = db.query(AIAgent).count()
    agents = db.query(AIAgent).offset(skip).limit(limit).all()
    
    return {"total": total, "agents": agents}


@router.put("/{agent_id}", response_model=AIAgentResponse)
def update_ai_agent(
    agent_id: str,
    agent_update: AIAgentUpdate,
    db: Session = Depends(get_db)
):
    """Update an AI agent."""
    agent = db.query(AIAgent).filter(
        AIAgent.agent_id == agent_id
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )
    
    # Update fields
    update_data = agent_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
    
    db.commit()
    db.refresh(agent)
    
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ai_agent(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Delete an AI agent."""
    agent = db.query(AIAgent).filter(
        AIAgent.agent_id == agent_id
    ).first()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )
    
    db.delete(agent)
    db.commit()
