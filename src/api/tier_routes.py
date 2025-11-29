"""
Subscription Tier Management API Routes
Based on B2B SaaS transformation strategy (Starter/Professional/Enterprise)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from src.database.session import get_db
from src.services.tier_service import TierService
from src.middleware.multitenant import get_current_organization_id


router = APIRouter(prefix="/tiers", tags=["Subscription Tiers"])


@router.get("/", response_model=List[dict])
async def get_all_tiers(
    db: Session = Depends(get_db)
):
    """
    Get all available subscription tiers
    """
    tier_service = TierService(db)
    tiers = tier_service.get_all_tiers()
    return tiers


@router.get("/{tier_name}", response_model=dict)
async def get_tier_by_name(
    tier_name: str,
    db: Session = Depends(get_db)
):
    """
    Get details for a specific subscription tier
    """
    tier_service = TierService(db)
    
    # Validate tier name
    valid_tiers = ["starter", "professional", "enterprise"]
    if tier_name.lower() not in valid_tiers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid tier name. Valid options are: {valid_tiers}"
        )
    
    tier = tier_service.get_tier_by_name(tier_name)
    if not tier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tier '{tier_name}' not found"
        )
    
    return tier


@router.get("/organization/{org_id}/subscription", response_model=dict)
async def get_organization_subscription(
    org_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get subscription information for an organization
    """
    # Verify the user has access to this organization
    if org_id != current_org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this organization"
        )
    
    tier_service = TierService(db)
    subscription_info = tier_service.get_organization_subscription_info(org_id)
    
    return subscription_info


@router.post("/organization/{org_id}/upgrade/{new_tier}", response_model=dict)
async def upgrade_organization_tier(
    org_id: uuid.UUID,
    new_tier: str,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Upgrade an organization to a new subscription tier
    """
    # Verify the user has access to this organization
    if org_id != current_org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this organization"
        )
    
    # Validate tier name
    valid_tiers = ["starter", "professional", "enterprise"]
    if new_tier.lower() not in valid_tiers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid tier name. Valid options are: {valid_tiers}"
        )
    
    # Convert string to enum
    from src.database.models import SubscriptionTier
    tier_enum = SubscriptionTier(new_tier.lower())
    
    tier_service = TierService(db)
    
    try:
        updated_subscription = tier_service.update_organization_subscription(
            org_id, tier_enum
        )
        return updated_subscription
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/organization/{org_id}/feature/{feature_name}", response_model=dict)
async def check_feature_availability(
    org_id: uuid.UUID,
    feature_name: str,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Check if a specific feature is available for an organization's tier
    """
    # Verify the user has access to this organization
    if org_id != current_org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this organization"
        )
    
    tier_service = TierService(db)
    is_available = tier_service.get_feature_availability(org_id, feature_name)
    
    return {
        "feature_name": feature_name,
        "is_available": is_available,
        "organization_id": str(org_id)
    }


@router.get("/calculate-cost", response_model=dict)
async def calculate_subscription_cost(
    tier: str,
    additional_scans: int = 0,
    additional_api_calls: int = 0,
    additional_agent_hours: int = 0,
    db: Session = Depends(get_db)
):
    """
    Calculate the total cost for a tier including usage-based components
    """
    # Validate tier name
    valid_tiers = ["starter", "professional", "enterprise"]
    if tier.lower() not in valid_tiers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid tier name. Valid options are: {valid_tiers}"
        )
    
    # Convert string to enum
    from src.database.models import SubscriptionTier
    tier_enum = SubscriptionTier(tier.lower())
    
    tier_service = TierService(db)
    cost_breakdown = tier_service.calculate_tier_cost(
        tier_enum, additional_scans, additional_api_calls, additional_agent_hours
    )
    
    return {
        "tier": tier,
        "cost_breakdown": cost_breakdown
    }


@router.get("/starter", response_model=dict)
async def get_starter_tier(
    db: Session = Depends(get_db)
):
    """
    Get details for the Starter subscription tier
    """
    tier_service = TierService(db)
    tier = tier_service.get_starter_tier()
    
    if not tier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Starter tier not found"
        )
    
    return tier


@router.get("/professional", response_model=dict)
async def get_professional_tier(
    db: Session = Depends(get_db)
):
    """
    Get details for the Professional subscription tier
    """
    tier_service = TierService(db)
    tier = tier_service.get_professional_tier()
    
    if not tier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professional tier not found"
        )
    
    return tier


@router.get("/enterprise", response_model=dict)
async def get_enterprise_tier(
    db: Session = Depends(get_db)
):
    """
    Get details for the Enterprise subscription tier
    """
    tier_service = TierService(db)
    tier = tier_service.get_enterprise_tier()
    
    if not tier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enterprise tier not found"
        )
    
    return tier