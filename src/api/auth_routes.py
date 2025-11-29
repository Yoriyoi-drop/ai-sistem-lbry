"""
Authentication API Routes with Rate Limiting
Based on B2B SaaS transformation strategy
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from src.database.session import get_db
from src.services.auth_service import AuthenticationService
from src.api.validation_models import AuthRequest
from src.middleware.multitenant import get_current_organization_id


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=dict)
async def login(
    auth_request: AuthRequest,
    db: Session = Depends(get_db)
):
    """
    User login endpoint
    """
    auth_service = AuthenticationService(db)
    
    result = auth_service.authenticate_user(
        auth_request.username, 
        auth_request.password
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user, organization = result
    token_data = auth_service.create_access_token(user, organization)
    
    # Get rate limit information
    rate_info = auth_service.get_rate_limit_info(user, organization)
    
    return {
        "access_token": token_data["access_token"],
        "token_type": token_data["token_type"],
        "expires_in": token_data["expires_in"],
        "user_info": token_data["user_info"],
        "rate_limits": rate_info
    }


@router.post("/api-key", response_model=dict)
async def create_api_key(
    request: Request,
    name: str,
    permissions: Optional[list] = None,
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Create an API key for the authenticated user
    """
    # Get the authenticated user (would typically be extracted from JWT in middleware)
    # For this example, we'll need to get user from organization context
    # In practice, this would be attached during auth middleware
    
    # First, get the user associated with this request
    # This requires that authentication middleware has already run and set user info
    if hasattr(request.state, 'user'):
        user = request.state.user
    else:
        # In a real implementation, we'd extract user from JWT token
        # For now, we'll find a user in the organization
        from src.database.models import User
        user = db.query(User).filter(
            User.organization_id == current_org_id
        ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in organization"
        )
    
    # Get the organization
    from src.database.models import Organization
    organization = db.query(Organization).filter(
        Organization.id == current_org_id
    ).first()
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    auth_service = AuthenticationService(db)
    
    # Check rate limits
    allowed, rate_info = auth_service.check_rate_limit(user, organization)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=rate_info["error"],
            headers={"Retry-After": str(rate_info["retry_after"])}
        )
    
    # Check if user has permission to create API keys (typically members and above)
    if user.role.value not in ["member", "admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to create API keys"
        )
    
    api_key_data = auth_service.create_api_key(user, organization, name, permissions)
    
    if not api_key_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create API key"
        )
    
    return api_key_data


@router.get("/me", response_model=dict)
async def get_current_user(
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get current user information
    """
    # In a real implementation, user info would be extracted from JWT token
    # For this example, we'll get the first user in the organization
    from src.database.models import User
    user = db.query(User).filter(
        User.organization_id == current_org_id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    from src.database.models import Organization
    organization = db.query(Organization).filter(
        Organization.id == current_org_id
    ).first()
    
    auth_service = AuthenticationService(db)
    
    # Check rate limits
    allowed, rate_info = auth_service.check_rate_limit(user, organization)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=rate_info["error"],
            headers={"Retry-After": str(rate_info["retry_after"])}
        )
    
    return {
        "user_id": str(user.id),
        "email": user.email,
        "username": user.username,
        "role": user.role.value,
        "organization_id": str(organization.id),
        "organization_name": organization.name,
        "organization_tier": organization.tier.value,
        "rate_limits": rate_info
    }


@router.get("/rate-limit", response_model=dict)
async def get_rate_limit_info(
    db: Session = Depends(get_db),
    current_org_id: uuid.UUID = Depends(get_current_organization_id)
):
    """
    Get current rate limit information for the user's organization
    """
    # Similar to above, get user from organization context
    from src.database.models import User
    user = db.query(User).filter(
        User.organization_id == current_org_id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    from src.database.models import Organization
    organization = db.query(Organization).filter(
        Organization.id == current_org_id
    ).first()
    
    auth_service = AuthenticationService(db)
    rate_info = auth_service.get_rate_limit_info(user, organization)
    
    return rate_info


# Rate limiting middleware function
def rate_limit_middleware():
    """
    This would be implemented as a middleware class in practice
    For the API routes, rate limiting is handled within the service
    """
    pass