"""
Rate Limiting Middleware for API Endpoints
Based on B2B SaaS transformation strategy with tier-based limits
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
import time
from typing import Dict, Optional
import uuid

from src.database.session import get_db
from src.services.auth_service import rate_limiter
from src.database.models import Organization


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware to enforce rate limiting based on organization tier
    """
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for certain endpoints (like health checks, auth)
        if request.url.path.startswith('/health') or request.url.path.startswith('/auth/login'):
            response = await call_next(request)
            return response
        
        # Check if organization context is available
        org_id = getattr(request.state, 'organization_id', None)
        user_id = getattr(request.state, 'user_id', None)
        
        # Create a database session to get organization info
        db: Session = next(get_db())
        
        try:
            if org_id:
                # Get organization from database to check tier-based limits
                organization = db.query(Organization).filter(
                    Organization.id == uuid.UUID(str(org_id))
                ).first()
                
                if organization:
                    # Set rate limits based on organization tier
                    tier_limits = {
                        "starter": {"requests_per_minute": 100},
                        "professional": {"requests_per_minute": 1000},
                        "enterprise": {"requests_per_minute": 10000}
                    }
                    
                    limit_info = tier_limits.get(organization.tier.value, tier_limits["starter"])
                    org_limit = limit_info["requests_per_minute"]
                    user_limit = org_limit  # Same as org limit, but can be adjusted
                    
                    # Check organization-level rate limit
                    org_identifier = f"org_{org_id}"
                    if not rate_limiter.is_allowed(org_identifier, org_limit, 60):
                        raise HTTPException(
                            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                            detail="Organization rate limit exceeded",
                            headers={"Retry-After": "60"}
                        )
                    
                    # Check user-level rate limit if user_id is available
                    if user_id:
                        user_identifier = f"user_{user_id}"
                        if not rate_limiter.is_allowed(user_identifier, user_limit, 60):
                            raise HTTPException(
                                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                                detail="User rate limit exceeded",
                                headers={"Retry-After": "60"}
                            )
            
            # Process the request
            response = await call_next(request)
            
            # Add rate limit headers to response if organization context exists
            if org_id:
                organization = db.query(Organization).filter(
                    Organization.id == uuid.UUID(str(org_id))
                ).first()
                
                if organization:
                    tier_limits = {
                        "starter": {"requests_per_minute": 100},
                        "professional": {"requests_per_minute": 1000},
                        "enterprise": {"requests_per_minute": 10000}
                    }
                    
                    limit_info = tier_limits.get(organization.tier.value, tier_limits["starter"])
                    org_limit = limit_info["requests_per_minute"]
                    
                    # Set response headers for rate limiting info
                    remaining_org = rate_limiter.get_remaining_requests(
                        f"org_{org_id}", org_limit, 60
                    )
                    
                    user_remaining = remaining_org  # Simplified - in practice, track separately
                    if user_id:
                        user_remaining = rate_limiter.get_remaining_requests(
                            f"user_{user_id}", org_limit, 60
                        )
                    
                    response.headers["X-RateLimit-Limit"] = str(org_limit)
                    response.headers["X-RateLimit-Remaining-Org"] = str(remaining_org)
                    response.headers["X-RateLimit-Remaining-User"] = str(user_remaining)
                    response.headers["X-RateLimit-Reset"] = str(int(time.time()) + 60)
            
            return response
        finally:
            # Close the database session
            db.close()


# Function to get rate limit info for inclusion in responses
def get_rate_limit_headers(request: Request, db: Session) -> Dict[str, str]:
    """
    Get rate limit headers for response
    """
    org_id = getattr(request.state, 'organization_id', None)
    
    if not org_id:
        return {}
    
    organization = db.query(Organization).filter(
        Organization.id == uuid.UUID(str(org_id))
    ).first()
    
    if not organization:
        return {}
    
    # Rate limits based on tier
    tier_limits = {
        "starter": {"requests_per_minute": 100},
        "professional": {"requests_per_minute": 1000},
        "enterprise": {"requests_per_minute": 10000}
    }
    
    limit_info = tier_limits.get(organization.tier.value, tier_limits["starter"])
    org_limit = limit_info["requests_per_minute"]
    
    # Get remaining requests
    remaining_org = rate_limiter.get_remaining_requests(
        f"org_{org_id}", org_limit, 60
    )
    
    user_remaining = remaining_org
    user_id = getattr(request.state, 'user_id', None)
    if user_id:
        user_remaining = rate_limiter.get_remaining_requests(
            f"user_{user_id}", org_limit, 60
        )
    
    return {
        "X-RateLimit-Limit": str(org_limit),
        "X-RateLimit-Remaining-Org": str(remaining_org),
        "X-RateLimit-Remaining-User": str(user_remaining),
        "X-RateLimit-Reset": str(int(time.time()) + 60)
    }