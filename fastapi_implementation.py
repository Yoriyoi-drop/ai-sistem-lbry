# 🌐 NEXAFORGE - FASTAPI IMPLEMENTATION (L7 Component)

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime, timedelta
import hashlib
import secrets

# Import from our business logic layer
from phase5_api_business import UserManager, TokenManager, RateLimitManager, BillingManager
from phase5_api_business import User, APIToken, TokenType, UserRole, SubscriptionTier

# Initialize the business logic components
user_manager = UserManager()
token_manager = TokenManager()
rate_limit_manager = RateLimitManager()
billing_manager = BillingManager()

# Security scheme
security = HTTPBearer()

# Create FastAPI app
app = FastAPI(
    title="NexaForge API Gateway",
    description="API Gateway for the NexaForge platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response bodies
class UserCreateRequest(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str
    subscription_tier: str
    created_at: str
    is_active: bool

class TokenCreateRequest(BaseModel):
    permissions: Optional[List[str]] = None
    expires_in_days: Optional[int] = 30

class TokenResponse(BaseModel):
    token: str
    message: str

class SubscriptionUpdateRequest(BaseModel):
    tier: str

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get the current user based on the API token"""
    token_data = token_manager.validate_token(credentials.credentials)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = user_manager.get_user(token_data.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

# Rate limiting dependency
async def check_rate_limit(request: Request, user: User = Depends(get_current_user)):
    """Check rate limits for the current user"""
    result = rate_limit_manager.check_rate_limit(user.id)
    
    if not result["within_limits"]:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={
                "X-RateLimit-Remaining-Minute": str(result["limit"]["minute"]),
                "X-RateLimit-Remaining-Hour": str(result["limit"]["hour"]),
                "X-RateLimit-Remaining-Day": str(result["limit"]["day"])
            }
        )

# API Routes
@app.post("/api/users", response_model=UserResponse)
async def create_user(user_data: UserCreateRequest):
    """Create a new user"""
    user = user_manager.create_user(
        user_data.username,
        user_data.email
    )
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role.value,
        subscription_tier=user.subscription_tier.value,
        created_at=user.created_at.isoformat(),
        is_active=user.is_active
    )

@app.get("/api/users/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role.value,
        subscription_tier=current_user.subscription_tier.value,
        created_at=current_user.created_at.isoformat(),
        is_active=current_user.is_active
    )

@app.get("/api/users", response_model=List[UserResponse])
async def list_users(current_user: User = Depends(get_current_user)):
    """List all users (admin only in real implementation)"""
    # In a real implementation, check if user has admin rights
    users = user_manager.list_users()
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role.value,
            subscription_tier=user.subscription_tier.value,
            created_at=user.created_at.isoformat(),
            is_active=user.is_active
        )
        for user in users
    ]

@app.post("/api/tokens", response_model=TokenResponse)
async def create_token(
    token_data: TokenCreateRequest,
    current_user: User = Depends(get_current_user)
):
    """Create a new API token for the current user"""
    try:
        tier = SubscriptionTier[current_user.subscription_tier.value]
        permissions = token_data.permissions or ["read", "write"]
        
        token = token_manager.create_api_token(
            current_user.id,
            token_type=TokenType.API_KEY,
            permissions=permissions,
            expires_in_days=token_data.expires_in_days
        )
        
        return TokenResponse(
            token=token,
            message="Token created successfully"
        )
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid subscription tier")

@app.get("/api/subscription")
async def get_subscription(current_user: User = Depends(get_current_user)):
    """Get current user's subscription details"""
    features = billing_manager.calculate_tier_features(current_user.subscription_tier)
    return {
        "subscription": {
            "tier": current_user.subscription_tier.value,
            "cost": billing_manager.get_subscription_cost(current_user.subscription_tier),
            "features": features
        }
    }

@app.post("/api/subscription")
async def update_subscription(
    subscription_data: SubscriptionUpdateRequest,
    current_user: User = Depends(get_current_user)
):
    """Update user's subscription tier"""
    try:
        new_tier = SubscriptionTier[subscription_data.tier.upper()]
        success = user_manager.update_subscription_tier(current_user.id, new_tier)
        
        if success:
            return {"message": f"Subscription updated to {new_tier.value}"}
        else:
            raise HTTPException(status_code=400, detail="Failed to update subscription")
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid subscription tier: {subscription_data.tier}")

@app.get("/api/usage")
async def get_usage(current_user: User = Depends(get_current_user)):
    """Get current user's API usage statistics"""
    stats = rate_limit_manager.get_usage_stats(current_user.id)
    return {"usage": stats}

@app.get("/api/status")
async def api_status():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "NexaForge API Gateway"
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return {"error": "Endpoint not found", "status_code": 404}

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    return {"error": "Internal server error", "status_code": 500}

def main():
    """Demo of FastAPI implementation"""
    print("🌐 NEXAFORGE - FASTAPI IMPLEMENTATION (L7 Component)")
    print("=" * 50)
    print("\nThis FastAPI app provides:")
    print("  • User management endpoints")
    print("  • API token creation and management")
    print("  • Subscription and billing endpoints")
    print("  • Rate limiting with tier-based limits")
    print("  • Authentication and authorization")
    print("  • Health check and status endpoints")
    print("\nTo run this API server:")
    print("  uvicorn fastapi_implementation:app --reload")
    print("\nThe API includes proper CORS, security, and dependency injection.")

if __name__ == "__main__":
    main()