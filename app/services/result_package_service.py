"""Result Package service."""

import uuid
import hashlib
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.result_package import ResultPackage, ResultPackageOutput
from app.models.work_order import WorkOrder
from app.config import get_settings
from app.schemas.result_package import ResultPackagePublishRequest


class ResultPackageService:
    """Service for result package operations."""
    
    @staticmethod
    def publish_result_package(
        work_order_id: str,
        publish_request: ResultPackagePublishRequest,
        db: Session
    ) -> ResultPackage:
        """Publish a result package for a work order."""
        work_order = db.query(WorkOrder).filter(
            WorkOrder.work_order_id == work_order_id
        ).first()
        
        if not work_order:
            raise ValueError(f"Work order not found: {work_order_id}")
        
        # Get next version number
        latest_version = db.query(ResultPackage).filter(
            ResultPackage.work_order_id == work_order_id
        ).order_by(ResultPackage.version.desc()).first()
        
        next_version = (latest_version.version + 1) if latest_version else 1
        package_id = f"pkg_{work_order_id}_v{next_version}"
        
        # Calculate checksum
        package_data = {
            "work_order_id": work_order_id,
            "version": next_version,
            "producer_agent_id": publish_request.producer_agent_id,
            "execution_log": publish_request.execution_log,
            "qa_summary": publish_request.qa_summary
        }
        checksum = hashlib.sha256(
            json.dumps(package_data, sort_keys=True).encode()
        ).hexdigest()
        
        # Calculate retention date
        settings = get_settings()
        retention_until = datetime.utcnow() + timedelta(
            days=settings.WORK_ORDER_RETENTION_DAYS
        )
        
        result_package = ResultPackage(
            package_id=package_id,
            work_order_id=work_order_id,
            version=next_version,
            producer_agent_id=publish_request.producer_agent_id,
            input_refs=publish_request.input_refs or [],
            qa_summary=publish_request.qa_summary or {},
            confidence_score=publish_request.confidence_score,
            next_tags=publish_request.next_tags or [],
            next_agent_recommendation=publish_request.next_agent_recommendation,
            execution_log=publish_request.execution_log,
            api_calls_made=publish_request.api_calls_made or [],
            output_manifest=publish_request.outputs or [],
            checksum=checksum,
            is_final=publish_request.is_final,
            retention_until=retention_until
        )
        
        # Add outputs
        for output_create in publish_request.outputs or []:
            output_id = f"out_{uuid.uuid4().hex[:8]}"
            output = ResultPackageOutput(
                output_id=output_id,
                package_id=package_id,
                file_path=output_create.file_path,
                file_type=output_create.file_type,
                description=output_create.description,
                is_artifact=output_create.is_artifact
            )
            result_package.outputs.append(output)
        
        db.add(result_package)
        db.commit()
        db.refresh(result_package)
        
        return result_package
    
    @staticmethod
    def get_result_package(
        package_id: str,
        db: Session
    ) -> ResultPackage:
        """Get a result package by ID."""
        package = db.query(ResultPackage).filter(
            ResultPackage.package_id == package_id
        ).first()
        
        if not package:
            raise ValueError(f"Result package not found: {package_id}")
        
        return package
    
    @staticmethod
    def get_work_order_result_chain(
        work_order_id: str,
        db: Session
    ) -> List[ResultPackage]:
        """Get complete result package chain for a work order."""
        packages = db.query(ResultPackage).filter(
            ResultPackage.work_order_id == work_order_id
        ).order_by(ResultPackage.version.asc()).all()
        
        return packages
    
    @staticmethod
    def cleanup_expired_packages(db: Session) -> int:
        """Clean up expired result packages beyond retention period."""
        deleted_count = db.query(ResultPackage).filter(
            ResultPackage.retention_until < datetime.utcnow()
        ).delete()
        
        db.commit()
        return deleted_count
