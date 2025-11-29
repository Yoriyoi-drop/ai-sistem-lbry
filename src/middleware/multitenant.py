"""
Multi-tenant middleware for Infinite AI Security Platform API
Handles organization context switching for each request
"""
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from typing import Optional
import uuid

from src.database.context import set_current_organization
from src.database.session import get_db
from src.services.organization_service import OrganizationService


class MultiTenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware to set the current organization context for each request
    This ensures Row Level Security (RLS) works properly
    """
    async def dispatch(self, request: Request, call_next):
        # Get the organization ID from headers, JWT token, or session
        org_id = self.get_organization_id(request)
        
        # Create a database session
        db: Session = next(get_db())
        
        try:
            # Set the current organization in the database session
            set_current_organization(db, org_id)
            
            # Add the organization ID to the request state for use by endpoints
            request.state.organization_id = org_id
            
            # Process the request
            response = await call_next(request)
            
            return response
        finally:
            # Close the database session
            db.close()

    def get_organization_id(self, request: Request) -> Optional[uuid.UUID]:
        """
        Extract organization ID from the request
        This could come from JWT token, headers, or other authentication mechanism
        """
        # First, try to get from JWT token (assuming organization_id is in the token)
        if hasattr(request.state, 'user') and hasattr(request.state.user, 'organization_id'):
            return request.state.user.organization_id
        
        # Try to get from custom header
        org_header = request.headers.get('x-organization-id')
        if org_header:
            try:
                return uuid.UUID(org_header)
            except ValueError:
                # Invalid UUID in header
                pass
        
        # Try to get from cookies
        org_cookie = request.cookies.get('organization_id')
        if org_cookie:
            try:
                return uuid.UUID(org_cookie)
            except ValueError:
                # Invalid UUID in cookie
                pass
        
        # If no organization ID found, return None
        # This will result in RLS not filtering, which could be a security risk
        # In production, you might want to require an organization ID
        return None


# Example dependency for endpoints that require multi-tenant context
def get_current_organization_id(request: Request) -> uuid.UUID:
    """
    Dependency to retrieve the current organization ID from the request state
    """
    org_id = getattr(request.state, 'organization_id', None)
    if org_id is None:
        raise HTTPException(status_code=400, detail="Organization ID not found in request context")
    
    return uuid.UUID(str(org_id))


# Example usage in a dependency that requires organization service
def get_organization_service(request: Request) -> OrganizationService:
    """
    Get an organization service instance with the current organization context
    """
    db: Session = next(get_db())
    
    # Set the current organization context
    org_id = get_current_organization_id(request)
    set_current_organization(db, org_id)
    
    return OrganizationService(db)