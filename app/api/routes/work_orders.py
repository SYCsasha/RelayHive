"""Work Order management endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.work_order import (
    WorkOrderCreate,
    WorkOrderUpdate,
    WorkOrderResponse,
    WorkOrderListResponse,
    WorkOrderClaimRequest,
    WorkOrderRejectRequest,
    WorkOrderDetailResponse
)
from app.schemas.result_package import ResultPackagePublishRequest
from app.services.work_order_service import WorkOrderService
from app.services.result_package_service import ResultPackageService

router = APIRouter(prefix="/workorders")


@router.post("", response_model=WorkOrderResponse, status_code=status.HTTP_201_CREATED)
def create_work_order(
    work_order_create: WorkOrderCreate,
    db: Session = Depends(get_db)
):
    """Create a new work order (for Main AI)."""
    try:
        work_order = WorkOrderService.create_work_order(work_order_create, db)
        return work_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/available", response_model=WorkOrderListResponse)
def get_available_work_orders(
    agent_id: str = Query(..., description="AI agent ID"),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get available work orders for an AI agent."""
    try:
        work_orders = WorkOrderService.query_available_work_orders(
            agent_id,
            limit,
            db
        )
        return {"total": len(work_orders), "work_orders": work_orders}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=WorkOrderListResponse)
def list_work_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status_filter: str = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """List work orders (for human observation)."""
    from app.models.work_order import WorkOrder
    query = db.query(WorkOrder)
    
    if status_filter:
        query = query.filter(WorkOrder.status == status_filter)
    
    total = query.count()
    work_orders = query.offset(skip).limit(limit).all()
    
    return {"total": total, "work_orders": work_orders}


@router.get("/{work_order_id}", response_model=WorkOrderDetailResponse)
def get_work_order(
    work_order_id: str,
    db: Session = Depends(get_db)
):
    """Get work order details with relay history."""
    try:
        work_order_data = WorkOrderService.get_work_order_with_history(
            work_order_id,
            db
        )
        work_order = work_order_data["work_order"]
        work_order.relay_history = work_order_data["relay_history"]
        work_order.result_packages = work_order_data["result_packages"]
        return work_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{work_order_id}/claim", response_model=WorkOrderResponse)
def claim_work_order(
    work_order_id: str,
    claim_request: WorkOrderClaimRequest,
    db: Session = Depends(get_db)
):
    """Claim a work order."""
    try:
        work_order = WorkOrderService.claim_work_order(
            work_order_id,
            claim_request.agent_id,
            db
        )
        return work_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{work_order_id}/start", response_model=WorkOrderResponse)
def start_execution(
    work_order_id: str,
    db: Session = Depends(get_db)
):
    """Mark work order as in progress."""
    try:
        work_order = WorkOrderService.start_work_order_execution(
            work_order_id,
            db
        )
        return work_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{work_order_id}/reject", response_model=WorkOrderResponse)
def reject_work_order(
    work_order_id: str,
    reject_request: WorkOrderRejectRequest,
    db: Session = Depends(get_db)
):
    """Reject a claimed work order."""
    try:
        work_order = WorkOrderService.reject_work_order(
            work_order_id,
            reject_request.agent_id,
            reject_request.reason,
            db
        )
        return work_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{work_order_id}/publish-result")
def publish_result_package(
    work_order_id: str,
    publish_request: ResultPackagePublishRequest,
    db: Session = Depends(get_db)
):
    """Publish a result package from an AI agent."""
    try:
        result_package = ResultPackageService.publish_result_package(
            work_order_id,
            publish_request,
            db
        )
        return {
            "package_id": result_package.package_id,
            "version": result_package.version,
            "checksum": result_package.checksum,
            "message": "Result package published successfully"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{work_order_id}/relay-chain")
def get_relay_chain(
    work_order_id: str,
    db: Session = Depends(get_db)
):
    """Get complete relay chain for a work order."""
    try:
        work_order_data = WorkOrderService.get_work_order_with_history(
            work_order_id,
            db
        )
        return {
            "work_order_id": work_order_id,
            "relay_steps": work_order_data["relay_history"],
            "result_packages": work_order_data["result_packages"]
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
