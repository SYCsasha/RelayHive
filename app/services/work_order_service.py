"""Work Order service for business logic."""

import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.work_order import WorkOrder, WorkOrderTag
from app.models.ai_agent import AIAgent
from app.models.relay_history import RelayStepHistory
from app.core.enums import WorkOrderStatus, RelayStepStatus
from app.services.tag_service import TagProtocolService
from app.schemas.work_order import WorkOrderCreate, WorkOrderUpdate


class WorkOrderService:
    """Service for work order operations."""
    
    @staticmethod
    def create_work_order(
        work_order_create: WorkOrderCreate,
        db: Session
    ) -> WorkOrder:
        """Create a new work order."""
        work_order_id = f"wo_{datetime.utcnow().strftime('%Y%m%d')}_{uuid.uuid4().hex[:8]}"
        
        # Get or create tags
        tags = []
        for tag_text in work_order_create.tags:
            tag = db.query(WorkOrderTag).filter(
                WorkOrderTag.tag_text == tag_text
            ).first()
            
            if not tag:
                # Parse tag to extract weight
                try:
                    parsed = TagProtocolService.parse_tag(tag_text)
                    tag = WorkOrderTag(
                        tag_text=tag_text,
                        weight=parsed["weight"],
                        category="functional"  # Default category
                    )
                    db.add(tag)
                    db.flush()
                except ValueError:
                    continue
            
            tags.append(tag)
        
        # Verify issuer agent exists
        issuer = db.query(AIAgent).filter(
            AIAgent.agent_id == work_order_create.issuer_agent_id
        ).first()
        
        if not issuer:
            raise ValueError(f"Issuer agent not found: {work_order_create.issuer_agent_id}")
        
        work_order = WorkOrder(
            work_order_id=work_order_id,
            title=work_order_create.title,
            description=work_order_create.description,
            issuer_agent_id=work_order_create.issuer_agent_id,
            priority_level=work_order_create.priority_level,
            estimated_complexity=work_order_create.estimated_complexity,
            max_relay_depth=work_order_create.max_relay_depth,
            acceptance_criteria=work_order_create.acceptance_criteria or [],
            ai_readable_requirements=work_order_create.ai_readable_requirements,
            context_data=work_order_create.context_data or {},
            dependency_ids=work_order_create.dependency_ids or [],
            tags=tags,
            status=WorkOrderStatus.CREATED.value
        )
        
        db.add(work_order)
        db.commit()
        db.refresh(work_order)
        
        return work_order
    
    @staticmethod
    def claim_work_order(
        work_order_id: str,
        agent_id: str,
        db: Session
    ) -> WorkOrder:
        """Claim a work order by an AI agent."""
        work_order = db.query(WorkOrder).filter(
            WorkOrder.work_order_id == work_order_id
        ).first()
        
        if not work_order:
            raise ValueError(f"Work order not found: {work_order_id}")
        
        if work_order.status != WorkOrderStatus.CREATED.value:
            raise ValueError(f"Work order already claimed or completed: {work_order.status}")
        
        # Verify agent exists
        agent = db.query(AIAgent).filter(AIAgent.agent_id == agent_id).first()
        if not agent:
            raise ValueError(f"Agent not found: {agent_id}")
        
        # Record relay step
        step_number = len(work_order.relay_history)
        step_id = f"step_{work_order_id}_{step_number}"
        
        relay_step = RelayStepHistory(
            step_id=step_id,
            work_order_id=work_order_id,
            agent_id=agent_id,
            step_number=step_number,
            status=RelayStepStatus.CLAIMED.value,
            claimed_at=datetime.utcnow()
        )
        
        work_order.claiming_agent_id = agent_id
        work_order.status = WorkOrderStatus.CLAIMED.value
        work_order.started_at = datetime.utcnow()
        
        db.add(relay_step)
        db.commit()
        db.refresh(work_order)
        
        return work_order
    
    @staticmethod
    def start_work_order_execution(
        work_order_id: str,
        db: Session
    ) -> WorkOrder:
        """Mark work order as in progress."""
        work_order = db.query(WorkOrder).filter(
            WorkOrder.work_order_id == work_order_id
        ).first()
        
        if not work_order:
            raise ValueError(f"Work order not found: {work_order_id}")
        
        if work_order.status != WorkOrderStatus.CLAIMED.value:
            raise ValueError(f"Work order not in claimed state: {work_order.status}")
        
        work_order.status = WorkOrderStatus.IN_PROGRESS.value
        db.commit()
        db.refresh(work_order)
        
        return work_order
    
    @staticmethod
    def reject_work_order(
        work_order_id: str,
        agent_id: str,
        reason: str,
        db: Session
    ) -> WorkOrder:
        """Reject a claimed work order."""
        work_order = db.query(WorkOrder).filter(
            WorkOrder.work_order_id == work_order_id
        ).first()
        
        if not work_order:
            raise ValueError(f"Work order not found: {work_order_id}")
        
        if work_order.claiming_agent_id != agent_id:
            raise ValueError("Only claiming agent can reject")
        
        work_order.claiming_agent_id = None
        work_order.status = WorkOrderStatus.CREATED.value
        work_order.started_at = None
        
        # Record rejection in relay step
        step = db.query(RelayStepHistory).filter(
            and_(
                RelayStepHistory.work_order_id == work_order_id,
                RelayStepHistory.agent_id == agent_id
            )
        ).order_by(RelayStepHistory.step_number.desc()).first()
        
        if step:
            step.status = RelayStepStatus.REJECTED.value
            step.error_message = reason
        
        db.commit()
        db.refresh(work_order)
        
        return work_order
    
    @staticmethod
    def query_available_work_orders(
        agent_id: str,
        limit: int = 10,
        db: Session = None
    ) -> List[WorkOrder]:
        """Query available work orders for an AI agent."""
        # Get agent and their capabilities
        agent = db.query(AIAgent).filter(AIAgent.agent_id == agent_id).first()
        if not agent:
            raise ValueError(f"Agent not found: {agent_id}")
        
        agent_capabilities = [cap.capability for cap in agent.capabilities]
        
        # Get unclaimed work orders
        available_orders = db.query(WorkOrder).filter(
            WorkOrder.status == WorkOrderStatus.CREATED.value
        ).limit(limit).all()
        
        # Filter by capability match
        matching_orders = []
        for order in available_orders:
            tag_texts = [tag.tag_text for tag in order.tags]
            match_result = TagProtocolService.match_tags_to_capabilities(
                tag_texts,
                agent_capabilities,
                db
            )
            
            if match_result["can_handle"]:
                matching_orders.append(order)
        
        return matching_orders
    
    @staticmethod
    def get_work_order_with_history(
        work_order_id: str,
        db: Session
    ) -> Dict[str, Any]:
        """Get work order with full relay history."""
        work_order = db.query(WorkOrder).filter(
            WorkOrder.work_order_id == work_order_id
        ).first()
        
        if not work_order:
            raise ValueError(f"Work order not found: {work_order_id}")
        
        relay_history = []
        for step in work_order.relay_history:
            relay_history.append({
                "step_id": step.step_id,
                "step_number": step.step_number,
                "agent_id": step.agent_id,
                "status": step.status,
                "claimed_at": step.claimed_at,
                "started_at": step.started_at,
                "completed_at": step.completed_at,
                "error_message": step.error_message
            })
        
        result_packages = []
        for pkg in work_order.result_packages:
            result_packages.append({
                "package_id": pkg.package_id,
                "version": pkg.version,
                "producer_agent_id": pkg.producer_agent_id,
                "confidence_score": pkg.confidence_score,
                "next_tags": pkg.next_tags,
                "created_at": pkg.created_at
            })
        
        return {
            "work_order": work_order,
            "relay_history": relay_history,
            "result_packages": result_packages
        }
