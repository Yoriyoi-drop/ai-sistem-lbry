"""
Organization Management API Routes
Based on B2B SaaS transformation strategy
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from src.database.session import get_db
from src.database.models import User, Organization, RoleEnum, SubscriptionTier
from src.services.organization_service import OrganizationService
from src.middleware.multitenant import get_current_organization_id
from src.api.validation_models import (
    OrganizationCreateRequest, 
    OrganizationUpdateRequest, 
    UserCreateRequest,
    UserUpdateRequest
)

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/", response_model=dict)
async def create_organization(
    org_data: OrganizationCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new organization with an owner user
    """
    try:
        org_service = OrganizationService(db)
        
        organization = org_service.create_organization(
            name=org_data.name,
            owner_email=org_data.owner_email,
            owner_password=org_data.owner_password,
            billing_email=org_data.billing_email,
            tier=org_data.tier or SubscriptionTier.STARTER
        )
        
        return {
            "id": str(organization.id),
            "name": organization.name,
            "tier": organization.tier.value,
            "status": organization.status,
            "created_at": organization.created_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create organization: {str(e)}"
        )


@router.get("/{org_id}", response_model=dict)
async def get_organization(
    org_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get organization details by ID
    """
    # Verify the user has access to this organization
    if org_id != current_org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this organization"
        )
    
    org_service = OrganizationService(db)
    organization = org_service.get_organization_by_id(org_id)
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    return {
        "id": str(organization.id),
        "name": organization.name,
        "tier": organization.tier.value,
        "status": organization.status,
        "created_at": organization.created_at.isoformat(),
        "max_users": organization.max_users,
        "max_scans_per_month": organization.max_scans_per_month,
        "api_calls_remaining": organization.api_calls_remaining
    }


@router.patch("/{org_id}", response_model=dict)
async def update_organization(
    org_id: uuid.UUID,
    org_update: OrganizationUpdateRequest,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Update organization details
    """
    # Only organization owners should be able to update organization details
    if org_id != current_org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this organization"
        )
    
    # Verify user is owner
    current_user: User = db.query(User).filter(
        and_(User.organization_id == org_id, User.role == RoleEnum.OWNER)
    ).first()
    
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organization owners can update organization details"
        )
    
    org_service = OrganizationService(db)
    
    if org_update.tier:
        success = org_service.update_organization_tier(org_id, org_update.tier)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
    
    # Update other fields if provided
    organization = org_service.get_organization_by_id(org_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    if org_update.name:
        organization.name = org_update.name
    if org_update.billing_email:
        organization.billing_email = org_update.billing_email
    
    db.commit()
    db.refresh(organization)
    
    return {
        "id": str(organization.id),
        "name": organization.name,
        "tier": organization.tier.value,
        "status": organization.status,
        "billing_email": organization.billing_email
    }


@router.get("/{org_id}/users", response_model=List[dict])
async def get_organization_users(
    org_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get all users in the organization
    """
    if org_id != current_org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this organization"
        )
    
    org_service = OrganizationService(db)
    users = org_service.get_organization_users(org_id)
    
    return [
        {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "role": user.role.value,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat()
        }
        for user in users
    ]


@router.post("/{org_id}/users", response_model=dict)
async def create_user_in_organization(
    org_id: uuid.UUID,
    user_data: UserCreateRequest,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Create a new user within the organization
    """
    if org_id != current_org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this organization"
        )
    
    # Only admins and owners can create users
    current_user: User = db.query(User).filter(
        and_(
            User.organization_id == org_id,
            User.id == current_org_id,
            User.role.in_([RoleEnum.OWNER, RoleEnum.ADMIN])
        )
    ).first()
    
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organization owners and admins can create users"
        )
    
    org_service = OrganizationService(db)
    
    try:
        user = org_service.create_user_in_organization(
            org_id=org_id,
            email=user_data.email,
            password=user_data.password,
            role=user_data.role or RoleEnum.MEMBER,
            username=user_data.username
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        
        return {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "role": user.role.value,
            "created_at": user.created_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create user: {str(e)}"
        )


@router.get("/{org_id}/subscription", response_model=dict)
async def get_organization_subscription(
    org_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get organization subscription details
    """
    if org_id != current_org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this organization"
        )
    
    org_service = OrganizationService(db)
    limits = org_service.get_subscription_limits(org_id)
    
    organization = org_service.get_organization_by_id(org_id)
    
    return {
        "organization_id": str(org_id),
        "tier": organization.tier.value,
        "limits": limits,
        "usage": {
            "current_scans": org_service.get_current_usage(org_id, "scans"),
            "current_api_calls": org_service.get_current_usage(org_id, "api_calls"),
            "current_agent_hours": org_service.get_current_usage(org_id, "agent_hours")
        }
    }