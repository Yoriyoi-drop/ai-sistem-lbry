"""
API Dependencies Module
Contains authentication, rate limiting, and other dependencies for API endpoints
"""
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Dict, Any, Optional
from datetime import datetime
import time
from collections import defaultdict
import logging

import sys
import os
# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config import settings
from src.database.session import get_db
from src.database.models import User, Organization
from src.services.auth_service import AuthenticationService


# Rate limiter implementation
class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.logger = logging.getLogger(__name__)
    
    def is_allowed(self, identifier: str, limit: int, window: int) -> bool:
        """
        Check if the identifier is allowed to make a request
        """
        now = time.time()
        # Remove old requests outside the window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier] 
            if now - req_time < window
        ]
        
        # Check if we're under the limit
        if len(self.requests[identifier]) < limit:
            # Add the current request
            self.requests[identifier].append(now)
            return True
        
        self.logger.warning(f"Rate limit exceeded for {identifier}: {len(self.requests[identifier])}/{limit}")
        return False

    def get_remaining_requests(self, identifier: str, limit: int, window: int) -> int:
        """Get remaining requests for the identifier"""
        now = time.time()
        # Remove old requests outside the window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier] 
            if now - req_time < window
        ]
        return limit - len(self.requests[identifier])

# Global rate limiter instance
rate_limiter = RateLimiter()

# Initialize security schemes
security_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
) -> Dict[str, Any]:
    """
    Dependency to get current authenticated user from JWT token
    """
    token = credentials.credentials
    
    auth_service = AuthenticationService(next(get_db()))
    user_info = auth_service.verify_token(token)
    
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_info


def get_current_active_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Dependency to get current active user
    """
    # Check if user is active (this would require an additional DB call in real implementation)
    return current_user


def get_current_organization_id(current_user: Dict[str, Any] = Depends(get_current_user)) -> str:
    """
    Dependency to extract organization ID from current user
    """
    return current_user.get("organization_id")


def require_role(required_role: str):
    """
    Dependency to check if user has required role
    """
    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)):
        user_role = current_user.get("role", "member")
        allowed_roles = ["owner", "admin", "member", "viewer"]
        
        # Define role hierarchy (owner > admin > member > viewer)
        role_hierarchy = {"owner": 4, "admin": 3, "member": 2, "viewer": 1}
        
        required_level = role_hierarchy.get(required_role, 1)
        user_level = role_hierarchy.get(user_role, 1)
        
        if user_level < required_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires {required_role} role or higher"
            )
        
        return current_user
    
    return role_checker


def rate_limit_dependency(limit: int = 100, window: int = 60):
    """
    Dependency to apply rate limiting based on user/organization
    """
    def rate_limiter_func(
        request: Request,
        current_user: Dict[str, Any] = Depends(get_current_user)
    ):
        user_id = current_user.get("user_id")
        org_id = current_user.get("organization_id")
        
        # Check user-specific rate limit
        user_key = f"user_{user_id}"
        if not rate_limiter.is_allowed(user_key, limit, window):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
                headers={"Retry-After": str(window)}
            )
        
        # Check organization-specific rate limit (more generous)
        org_key = f"org_{org_id}"
        org_limit = limit * 10  # Organization can have 10x user limit
        if not rate_limiter.is_allowed(org_key, org_limit, window):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Organization rate limit exceeded",
                headers={"Retry-After": str(window)}
            )
        
        return current_user
    
    return rate_limiter_func


def get_rate_limit_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get current rate limit information for the user
    """
    user_id = current_user.get("user_id")
    org_id = current_user.get("organization_id")
    
    # For starter tier: 100 requests per minute
    # For professional tier: 1000 requests per minute
    # For enterprise tier: 10000 requests per minute
    tier_limits = {
        "starter": {"requests_per_minute": 100},
        "professional": {"requests_per_minute": 1000},
        "enterprise": {"requests_per_minute": 10000}
    }
    
    user_tier = current_user.get("organization_tier", "starter")
    limit_info = tier_limits.get(user_tier, tier_limits["starter"])
    
    user_remaining = rate_limiter.get_remaining_requests(
        f"user_{user_id}", 
        limit_info["requests_per_minute"], 
        60
    )
    
    org_remaining = rate_limiter.get_remaining_requests(
        f"org_{org_id}", 
        limit_info["requests_per_minute"] * 10,  # Org can have 10x user limit
        60
    )
    
    return {
        "tier": user_tier,
        "user_rate_limit": limit_info["requests_per_minute"],
        "org_rate_limit": limit_info["requests_per_minute"] * 10,
        "user_requests_remaining": user_remaining,
        "org_requests_remaining": org_remaining,
        "reset_time": int(time.time()) + 60
    }


def check_feature_access(feature_name: str):
    """
    Dependency to check if user's tier allows access to a specific feature
    """
    def feature_checker(current_user: Dict[str, Any] = Depends(get_current_user)):
        # For now, we'll implement basic feature access based on tier
        # In a real implementation, this would connect to the tier service
        tier_features = {
            "starter": [
                "basic_security_scanning", 
                "email_support",
                "dashboard_access",
                "api_access"
            ],
            "professional": [
                "basic_security_scanning",
                "multi_agent_ai",
                "labyrinth_defense_basic",
                "compliance_reports",
                "priority_support",
                "custom_security_policies",
                "api_access",
                "team_collaboration"
            ],
            "enterprise": [
                "unlimited_scans",
                "unlimited_agents",
                "advanced_labyrinth",
                "dedicated_support",
                "on_premise_deployment",
                "sso_integration",
                "advanced_rbac",
                "custom_integrations",
                "white_label_option",
                "24_7_support",
                "advanced_compliance",
                "custom_ai_models",
                "api_access"
            ]
        }
        
        user_tier = current_user.get("organization_tier", "starter")
        allowed_features = tier_features.get(user_tier, tier_features["starter"])
        
        # Normalize feature names for comparison
        normalized_feature = feature_name.lower().replace(" ", "_").replace("-", "_")
        normalized_allowed = [f.lower().replace(" ", "_").replace("-", "_") for f in allowed_features]
        
        if normalized_feature not in normalized_allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Feature '{feature_name}' not available in {user_tier} tier"
            )
        
        return current_user
    
    return feature_checker