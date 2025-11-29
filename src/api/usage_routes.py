"""
Usage Tracking API Routes for Consumption-Based Billing
Based on B2B SaaS transformation strategy
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List
import uuid
from datetime import date, datetime

from src.database.session import get_db
from src.services.usage_tracking_service import UsageTrackingService
from src.middleware.multitenant import get_current_organization_id


router = APIRouter(prefix="/usage", tags=["Usage Tracking"])


@router.get("/", response_model=Dict)
async def get_usage_summary(
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get usage summary for the current month
    """
    usage_service = UsageTrackingService(db)
    
    try:
        summary = usage_service.get_usage_summary(current_org_id)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving usage summary: {str(e)}"
        )


@router.get("/breakdown", response_model=Dict)
async def get_usage_breakdown(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get detailed usage breakdown for a date range
    """
    usage_service = UsageTrackingService(db)
    
    try:
        breakdown = usage_service.get_usage_breakdown(
            current_org_id, start_date, end_date
        )
        return breakdown
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving usage breakdown: {str(e)}"
        )


@router.get("/limits", response_model=Dict)
async def check_usage_limits(
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Check current usage against limits for all metric types
    """
    usage_service = UsageTrackingService(db)
    
    try:
        limits_status = usage_service.check_usage_limits(current_org_id)
        return limits_status
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking usage limits: {str(e)}"
        )


@router.get("/projection", response_model=Dict)
async def get_billing_projection(
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get billing projection based on current usage patterns
    """
    usage_service = UsageTrackingService(db)
    
    try:
        projection = usage_service.get_billing_projection(current_org_id)
        return projection
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating billing projection: {str(e)}"
        )


@router.get("/metric/{metric_type}", response_model=Dict)
async def get_metric_usage(
    metric_type: str,
    period: date = None,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get usage for a specific metric type
    """
    if period is None:
        period = datetime.utcnow().date().replace(day=1)
    
    usage_service = UsageTrackingService(db)
    
    try:
        current_usage = usage_service.get_current_usage(current_org_id, metric_type)
        
        # Check if organization has allowance for this metric
        _, usage_info = usage_service.check_usage_allowance(current_org_id, metric_type, 0)
        
        return {
            "organization_id": str(current_org_id),
            "metric_type": metric_type,
            "current_usage": current_usage,
            "usage_info": usage_info,
            "period": period.isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving metric usage: {str(e)}"
        )


@router.post("/check-allowance/{metric_type}", response_model=Dict)
async def check_usage_allowance(
    metric_type: str,
    requested_amount: int = 1,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Check if an organization can perform an action based on usage limits
    """
    usage_service = UsageTrackingService(db)
    
    try:
        is_allowed, usage_info = usage_service.check_usage_allowance(
            current_org_id, metric_type, requested_amount
        )
        
        return {
            "is_allowed": is_allowed,
            "usage_info": usage_info,
            "organization_id": str(current_org_id),
            "metric_type": metric_type,
            "requested_amount": requested_amount
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking usage allowance: {str(e)}"
        )


@router.get("/available-metrics", response_model=List[str])
async def get_available_metrics(
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get list of available usage metrics for the organization
    """
    usage_service = UsageTrackingService(db)
    
    try:
        # Query the database to get all unique metric types for this organization
        from src.database.models import UsageMetric
        metric_types = db.query(UsageMetric.metric_type).filter(
            UsageMetric.organization_id == current_org_id
        ).distinct().all()
        
        return [metric[0] for metric in metric_types]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving available metrics: {str(e)}"
        )