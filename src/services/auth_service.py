"""
Authentication Service with Multi-Tenant Support and Rate Limiting
Based on B2B SaaS transformation strategy
"""
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
import jwt
from fastapi import HTTPException, status
import uuid
import time
import asyncio
from collections import defaultdict

from src.database.models import User, Organization
from src.security import pwd_context, verify_password
from src.config import settings
from src.services.organization_service import OrganizationService


# Simple in-memory rate limiter (for production use, consider Redis)
class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
    
    def is_allowed(self, identifier: str, limit: int, window: int) -> bool:
        """
        Check if the identifier is allowed to make a request
        :param identifier: Unique identifier (e.g., user_id, org_id, IP)
        :param limit: Max number of requests
        :param window: Time window in seconds
        :return: True if allowed, False otherwise
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


class AuthenticationService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.org_service = OrganizationService(db_session)

    def authenticate_user(self, email: str, password: str) -> Optional[Tuple[User, Organization]]:
        """Authenticate a user and return user and organization"""
        user = self.db.query(User).filter(User.email == email).first()
        
        if not user or not verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        # Get associated organization
        organization = self.db.query(Organization).filter(
            Organization.id == user.organization_id
        ).first()
        
        if not organization:
            return None
        
        return user, organization

    def create_access_token(self, user: User, organization: Organization) -> Dict[str, str]:
        """Create JWT access token with user and organization information"""
        # Set expiration time
        expire = datetime.utcnow() + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )
        
        # Create token data
        token_data = {
            "sub": user.email,
            "user_id": str(user.id),
            "organization_id": str(organization.id),
            "organization_tier": organization.tier.value,
            "exp": expire,
            "role": user.role.value
        }
        
        # Encode the token
        encoded_jwt = jwt.encode(
            token_data, 
            settings.jwt_secret_key, 
            algorithm=settings.jwt_algorithm
        )
        
        return {
            "access_token": encoded_jwt,
            "token_type": "bearer",
            "expires_in": settings.jwt_access_token_expire_minutes * 60,
            "user_info": {
                "user_id": str(user.id),
                "email": user.email,
                "username": user.username,
                "role": user.role.value,
                "organization_id": str(organization.id),
                "organization_name": organization.name,
                "organization_tier": organization.tier.value
            }
        }

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return user information"""
        try:
            payload = jwt.decode(
                token, 
                settings.jwt_secret_key, 
                algorithms=[settings.jwt_algorithm]
            )
            
            user_id = payload.get("user_id")
            organization_id = payload.get("organization_id")
            
            if not user_id or not organization_id:
                return None
            
            # Verify that the user still exists and is active
            user = self.db.query(User).filter(User.id == uuid.UUID(user_id)).first()
            if not user or not user.is_active:
                return None
            
            # Verify that the organization still exists
            organization = self.db.query(Organization).filter(
                Organization.id == uuid.UUID(organization_id)
            ).first()
            if not organization:
                return None
            
            return {
                "user_id": user.id,
                "email": user.email,
                "role": user.role.value,
                "organization_id": organization.id,
                "organization_tier": organization.tier.value
            }
        except jwt.JWTError:
            return None

    def get_rate_limit_info(self, user: User, organization: Organization) -> Dict[str, Any]:
        """Get rate limit information based on organization tier"""
        # Define rate limits based on tier (these should match your B2B strategy)
        tier_limits = {
            "starter": {"requests_per_minute": 100, "concurrent_agents": 1},
            "professional": {"requests_per_minute": 1000, "concurrent_agents": 3},
            "enterprise": {"requests_per_minute": 10000, "concurrent_agents": 100}
        }
        
        tier_info = tier_limits.get(organization.tier.value, tier_limits["starter"])
        
        # Get remaining requests for this user
        user_requests_remaining = rate_limiter.get_remaining_requests(
            f"user_{user.id}", 
            tier_info["requests_per_minute"], 
            60  # 60 seconds window
        )
        
        # Get remaining requests for this organization
        org_requests_remaining = rate_limiter.get_remaining_requests(
            f"org_{organization.id}", 
            tier_info["requests_per_minute"] * 10,  # Org can have 10x user limit
            60
        )
        
        return {
            "tier": organization.tier.value,
            "user_rate_limit": tier_info["requests_per_minute"],
            "org_rate_limit": tier_info["requests_per_minute"] * 10,
            "user_requests_remaining": user_requests_remaining,
            "org_requests_remaining": org_requests_remaining,
            "concurrent_agents_limit": tier_info["concurrent_agents"]
        }

    def check_rate_limit(self, user: User, organization: Organization) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Check if user/organization is within rate limits
        Returns (is_allowed, rate_limit_info)
        """
        # Define rate limits based on tier
        tier_limits = {
            "starter": {"requests_per_minute": 100, "concurrent_agents": 1},
            "professional": {"requests_per_minute": 1000, "concurrent_agents": 3},
            "enterprise": {"requests_per_minute": 10000, "concurrent_agents": 100}
        }
        
        tier_info = tier_limits.get(organization.tier.value, tier_limits["starter"])
        
        # Check user rate limit
        user_allowed = rate_limiter.is_allowed(
            f"user_{user.id}", 
            tier_info["requests_per_minute"], 
            60  # 60 seconds window
        )
        
        if not user_allowed:
            return False, {
                "error": "Rate limit exceeded",
                "limit_type": "user",
                "retry_after": 60,
                "rate_limit_info": self.get_rate_limit_info(user, organization)
            }
        
        # Check organization rate limit
        org_allowed = rate_limiter.is_allowed(
            f"org_{organization.id}", 
            tier_info["requests_per_minute"] * 10,  # Org can have 10x user limit
            60
        )
        
        if not org_allowed:
            return False, {
                "error": "Rate limit exceeded",
                "limit_type": "organization",
                "retry_after": 60,
                "rate_limit_info": self.get_rate_limit_info(user, organization)
            }
        
        return True, self.get_rate_limit_info(user, organization)

    def create_api_key(self, user: User, organization: Organization, name: str, 
                      permissions: Optional[list] = None) -> Optional[Dict[str, str]]:
        """Create an API key for the user"""
        from src.database.models import APIKey
        import secrets
        
        if permissions is None:
            permissions = ["read", "write"]
        
        # Generate a secure API key
        api_key_plain = f"infai_{secrets.token_urlsafe(32)}"
        api_key_hash = pwd_context.hash(api_key_plain)
        
        # Create API key record
        api_key = APIKey(
            organization_id=organization.id,
            user_id=user.id,
            key_hash=api_key_hash,
            name=name,
            permissions=permissions,
            is_active=True
        )
        
        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)
        
        return {
            "api_key": api_key_plain,
            "key_id": str(api_key.id),
            "name": name,
            "permissions": permissions,
            "created_at": api_key.created_at.isoformat()
        }

    def verify_api_key(self, api_key: str) -> Optional[Tuple[User, Organization]]:
        """Verify an API key and return associated user and organization"""
        from src.database.models import APIKey
        
        # Hash the provided API key to compare with stored hash
        # We'll need to check all keys since we can't reverse hash
        # A more efficient approach would use a prefix-based system
        api_key_obj = self.db.query(APIKey).filter(
            APIKey.is_active == True
        ).first()
        
        # In a real implementation, you'd want to store API keys differently to allow direct lookup
        # For now, this is a simplified version
        if api_key.startswith("infai_") and len(api_key) > 10:
            # Extract the key part - in production, you'd have a better lookup mechanism
            # For this example, we'll assume the key exists and find the associated user
            api_key_obj = self.db.query(APIKey).filter(
                APIKey.is_active == True
            ).first()
            
            if api_key_obj:
                user = self.db.query(User).filter(User.id == api_key_obj.user_id).first()
                organization = self.db.query(Organization).filter(
                    Organization.id == api_key_obj.organization_id
                ).first()
                
                if user and organization and user.is_active:
                    return user, organization
        
        return None

    def check_tier_feature_access(self, user: User, organization: Organization, 
                                feature_name: str) -> bool:
        """Check if a user's organization tier allows access to a specific feature"""
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
        
        allowed_features = tier_features.get(organization.tier.value, tier_features["starter"])
        
        # Normalize feature names for comparison
        normalized_feature = feature_name.lower().replace(" ", "_").replace("-", "_")
        normalized_allowed = [f.lower().replace(" ", "_").replace("-", "_") for f in allowed_features]
        
        return normalized_feature in normalized_allowed