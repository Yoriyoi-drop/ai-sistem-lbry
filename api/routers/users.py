"""
User Management Router
API endpoints for user management operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from api.dependencies.security import get_current_user, require_role, rate_limit_dependency
from api.schemas.models import (
    UserCreateRequest, UserResponse, UserUpdateRequest, 
    SuccessResponse, ErrorResponse
)
from src.database.session import get_db
from src.services.organization_service import OrganizationService


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
async def get_users(
    current_user: dict = Depends(get_current_user),
    require_admin: dict = Depends(require_role("admin")),
    rate_limit: dict = Depends(rate_limit_dependency(50, 60)),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all users in the current organization
    Requires admin role or higher
    """
    org_service = OrganizationService(db)
    users = org_service.get_organization_users(uuid.UUID(current_user["organization_id"]))
    
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a user by ID
    Users can view their own information, admins can view any user
    """
    # In a real implementation, we would fetch from database
    # For now, raising not implemented
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User retrieval not implemented in this example"
    )


@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreateRequest,
    current_user: dict = Depends(get_current_user),
    require_admin: dict = Depends(require_role("admin")),
    rate_limit: dict = Depends(rate_limit_dependency(10, 60)),
    db: Session = Depends(get_db)
):
    """
    Create a new user in the organization
    Requires admin role or higher
    """
    org_service = OrganizationService(db)
    
    try:
        user = org_service.create_user_in_organization(
            org_id=uuid.UUID(current_user["organization_id"]),
            email=user_data.email,
            password=user_data.password,
            role=user_data.role,
            username=user_data.username
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create user: {str(e)}"
        )


@router.patch("/{user_id}", response_model=SuccessResponse)
async def update_user(
    user_id: uuid.UUID,
    user_update: UserUpdateRequest,
    current_user: dict = Depends(get_current_user),
    require_admin: dict = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Update a user's information
    Requires admin role or higher
    """
    # In a real implementation, we would update the user
    # For now, raising not implemented
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User update not implemented in this example"
    )


@router.delete("/{user_id}", response_model=SuccessResponse)
async def delete_user(
    user_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    require_owner: dict = Depends(require_role("owner")),
    db: Session = Depends(get_db)
):
    """
    Delete a user
    Requires owner role
    """
    # In a real implementation, we would delete the user
    # For now, raising not implemented
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User deletion not implemented in this example"
    )