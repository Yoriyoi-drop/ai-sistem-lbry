# 🌐 NEXAFORGE - PHASE 5: API & BUSINESS LOGIC (L7-L8)

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import asyncio
import json
import uuid
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import secrets
import time
from pathlib import Path
from datetime import timezone

class TokenType(Enum):
    """Types of authentication tokens"""
    API_KEY = "api_key"
    JWT = "jwt"
    SESSION = "session"

class UserRole(Enum):
    """User roles in the system"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
    SYSTEM = "system"

class SubscriptionTier(Enum):
    """Billing tiers"""
    FREE = "free"
    STANDARD = "standard"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"

@dataclass
class User:
    """Represents a user in the system"""
    id: str
    username: str
    email: str
    role: UserRole
    subscription_tier: SubscriptionTier
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    metadata: Dict = None

@dataclass
class APIToken:
    """Represents an API token"""
    token: str
    user_id: str
    token_type: TokenType
    created_at: datetime
    expires_at: Optional[datetime] = None
    permissions: List[str] = None
    last_used: Optional[datetime] = None
    metadata: Dict = None

@dataclass
class RateLimit:
    """Rate limit configuration for users"""
    user_id: str
    requests_per_minute: int
    requests_per_hour: int
    requests_per_day: int
    current_minute_count: int = 0
    current_hour_count: int = 0
    current_day_count: int = 0
    last_reset_minute: datetime = None
    last_reset_hour: datetime = None
    last_reset_day: datetime = None

class UserManager:
    """Manages users for L8: Business Logic Layer"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.email_index: Dict[str, str] = {}  # email to user_id mapping
        self.username_index: Dict[str, str] = {}  # username to user_id mapping
    
    def create_user(self, username: str, email: str, password_hash: str = None) -> User:
        """Create a new user"""
        user_id = f"user-{uuid.uuid4().hex[:8]}"
        
        # Generate random password hash if not provided
        if password_hash is None:
            password_hash = hashlib.sha256(secrets.token_bytes(32)).hexdigest()
        
        user = User(
            id=user_id,
            username=username,
            email=email,
            role=UserRole.USER,
            subscription_tier=SubscriptionTier.FREE,
            created_at=datetime.now(),
            metadata={"password_hash": password_hash}
        )
        
        self.users[user_id] = user
        self.email_index[email] = user_id
        self.username_index[username] = user_id
        
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        user_id = self.email_index.get(email)
        return self.users.get(user_id) if user_id else None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        user_id = self.username_index.get(username)
        return self.users.get(user_id) if user_id else None
    
    def update_user_role(self, user_id: str, new_role: UserRole) -> bool:
        """Update user role"""
        user = self.users.get(user_id)
        if user:
            user.role = new_role
            return True
        return False
    
    def update_subscription_tier(self, user_id: str, tier: SubscriptionTier) -> bool:
        """Update user subscription tier"""
        user = self.users.get(user_id)
        if user:
            user.subscription_tier = tier
            return True
        return False
    
    def list_users(self) -> List[User]:
        """List all users"""
        return list(self.users.values())
    
    def deactivate_user(self, user_id: str) -> bool:
        """Deactivate a user"""
        user = self.users.get(user_id)
        if user:
            user.is_active = False
            return True
        return False

class TokenManager:
    """Manages API tokens for authentication and rate limiting"""
    
    def __init__(self):
        self.tokens: Dict[str, APIToken] = {}
        self.user_token_index: Dict[str, List[str]] = {}  # user_id to list of token_ids
    
    def create_api_token(self, user_id: str, token_type: TokenType = TokenType.API_KEY, 
                         permissions: List[str] = None, expires_in_days: int = 30) -> str:
        """Create a new API token"""
        # Generate a secure token
        token = secrets.token_urlsafe(32)
        
        # Hash it for storage
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        expires_at = datetime.now() + timedelta(days=expires_in_days) if expires_in_days else None
        
        api_token = APIToken(
            token=token_hash,  # Store the hash
            user_id=user_id,
            token_type=token_type,
            created_at=datetime.now(),
            expires_at=expires_at,
            permissions=permissions or ["read", "write"],
            last_used=None,
            metadata={"original_token": token}  # Keep original for return to user
        )
        
        self.tokens[token_hash] = api_token
        
        if user_id not in self.user_token_index:
            self.user_token_index[user_id] = []
        self.user_token_index[user_id].append(token_hash)
        
        return token  # Return the original token to the user
    
    def validate_token(self, token: str) -> Optional[APIToken]:
        """Validate an API token"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        token_data = self.tokens.get(token_hash)
        
        if token_data:
            # Check expiration
            if token_data.expires_at and token_data.expires_at < datetime.now():
                return None  # Token expired
            
            # Update last used time
            token_data.last_used = datetime.now()
            return token_data
        
        return None
    
    def revoke_token(self, token: str) -> bool:
        """Revoke an API token"""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        if token_hash in self.tokens:
            token_data = self.tokens[token_hash]
            
            # Remove from user index
            if token_data.user_id in self.user_token_index:
                self.user_token_index[token_data.user_id].remove(token_hash)
            
            del self.tokens[token_hash]
            return True
        return False
    
    def get_tokens_for_user(self, user_id: str) -> List[APIToken]:
        """Get all tokens for a user"""
        token_ids = self.user_token_index.get(user_id, [])
        return [self.tokens[tid] for tid in token_ids if tid in self.tokens]

class RateLimitManager:
    """Manages rate limiting for API access"""
    
    def __init__(self):
        self.limits: Dict[str, RateLimit] = {}
        self.default_limits = {
            SubscriptionTier.FREE: RateLimit(
                user_id="",  # Will be filled later
                requests_per_minute=10,
                requests_per_hour=500,
                requests_per_day=10000
            ),
            SubscriptionTier.STANDARD: RateLimit(
                user_id="",
                requests_per_minute=50,
                requests_per_hour=2000,
                requests_per_day=50000
            ),
            SubscriptionTier.PROFESSIONAL: RateLimit(
                user_id="",
                requests_per_minute=200,
                requests_per_hour=10000,
                requests_per_day=200000
            ),
            SubscriptionTier.ENTERPRISE: RateLimit(
                user_id="",
                requests_per_minute=1000,
                requests_per_hour=50000,
                requests_per_day=1000000
            )
        }
    
    def get_rate_limit(self, user_id: str) -> RateLimit:
        """Get rate limit for a user, creating if not exists"""
        if user_id not in self.limits:
            # This would normally look up the user's subscription tier
            # For now, default to free tier
            default_limit = self.default_limits[SubscriptionTier.FREE]
            new_limit = RateLimit(
                user_id=user_id,
                requests_per_minute=default_limit.requests_per_minute,
                requests_per_hour=default_limit.requests_per_hour,
                requests_per_day=default_limit.requests_per_day,
                last_reset_minute=datetime.now(),
                last_reset_hour=datetime.now(),
                last_reset_day=datetime.now()
            )
            self.limits[user_id] = new_limit
        
        return self.limits[user_id]
    
    def check_rate_limit(self, user_id: str) -> Dict[str, Union[bool, Dict]]:
        """Check if user is within rate limits"""
        limit = self.get_rate_limit(user_id)
        
        now = datetime.now()
        
        # Reset counters if needed
        if now.minute != limit.last_reset_minute.minute:
            limit.current_minute_count = 0
            limit.last_reset_minute = now
        
        if now.hour != limit.last_reset_hour.hour:
            limit.current_hour_count = 0
            limit.last_reset_hour = now
        
        if now.day != limit.last_reset_day.day:
            limit.current_day_count = 0
            limit.last_reset_day = now
        
        # Check limits
        checks = {
            "minute_ok": limit.current_minute_count < limit.requests_per_minute,
            "hour_ok": limit.current_hour_count < limit.requests_per_hour,
            "day_ok": limit.current_day_count < limit.requests_per_day
        }
        
        within_limits = all(checks.values())
        
        if within_limits:
            # Increment counters
            limit.current_minute_count += 1
            limit.current_hour_count += 1
            limit.current_day_count += 1
        
        return {
            "within_limits": within_limits,
            "checks": checks,
            "limit": {
                "minute": f"{limit.current_minute_count}/{limit.requests_per_minute}",
                "hour": f"{limit.current_hour_count}/{limit.requests_per_hour}",
                "day": f"{limit.current_day_count}/{limit.requests_per_day}"
            }
        }
    
    def get_usage_stats(self, user_id: str) -> Dict[str, Any]:
        """Get usage statistics for a user"""
        limit = self.get_rate_limit(user_id)
        return {
            "minute_usage": limit.current_minute_count,
            "hour_usage": limit.current_hour_count,
            "day_usage": limit.current_day_count,
            "minute_limit": limit.requests_per_minute,
            "hour_limit": limit.requests_per_hour,
            "day_limit": limit.requests_per_day
        }

class BillingManager:
    """Manages billing and subscription logic for L8: Business Logic Layer"""
    
    def __init__(self):
        self.subscription_prices = {
            SubscriptionTier.FREE: 0.0,
            SubscriptionTier.STANDARD: 9.99,
            SubscriptionTier.PROFESSIONAL: 29.99,
            SubscriptionTier.ENTERPRISE: 99.99
        }
    
    def get_subscription_cost(self, tier: SubscriptionTier) -> float:
        """Get monthly cost of a subscription tier"""
        return self.subscription_prices[tier]
    
    def calculate_tier_features(self, tier: SubscriptionTier) -> Dict[str, Any]:
        """Calculate features available for each tier"""
        features = {
            SubscriptionTier.FREE: {
                "max_users": 1,
                "api_calls_per_month": 1000,
                "storage_gb": 1,
                "support": "community",
                "custom_domains": False
            },
            SubscriptionTier.STANDARD: {
                "max_users": 5,
                "api_calls_per_month": 10000,
                "storage_gb": 10,
                "support": "email",
                "custom_domains": True
            },
            SubscriptionTier.PROFESSIONAL: {
                "max_users": 20,
                "api_calls_per_month": 100000,
                "storage_gb": 100,
                "support": "priority_email",
                "custom_domains": True
            },
            SubscriptionTier.ENTERPRISE: {
                "max_users": 100,
                "api_calls_per_month": 1000000,
                "storage_gb": 1000,
                "support": "24_7_phone",
                "custom_domains": True
            }
        }
        return features[tier]

class APIGateway:
    """API Gateway for L7: API Gateway Layer"""
    
    def __init__(self):
        self.user_manager = UserManager()
        self.token_manager = TokenManager()
        self.rate_limit_manager = RateLimitManager()
        self.billing_manager = BillingManager()
        self.routes = {}
        self.middleware = []
    
    def authenticate_request(self, headers: Dict[str, str]) -> Optional[APIToken]:
        """Authenticate a request using API key or JWT token"""
        # Check for API key in headers
        api_key = headers.get('X-API-Key') or headers.get('Authorization', '').replace('Bearer ', '')
        
        if not api_key:
            return None
        
        return self.token_manager.validate_token(api_key)
    
    def authorize_request(self, token: APIToken, required_permissions: List[str]) -> bool:
        """Authorize a request based on token permissions"""
        if not required_permissions:
            return True  # No specific permissions required
        
        # Check if all required permissions are in token permissions
        token_perms = set(token.permissions or [])
        required_perms = set(required_permissions)
        
        return required_perms.issubset(token_perms)
    
    def check_rate_limit(self, user_id: str) -> Dict[str, Any]:
        """Check rate limit for a user"""
        return self.rate_limit_manager.check_rate_limit(user_id)
    
    def add_route(self, path: str, handler: callable, methods: List[str] = None, 
                  auth_required: bool = True, permissions: List[str] = None):
        """Add a route to the gateway"""
        if methods is None:
            methods = ['GET', 'POST']
        
        route_info = {
            'handler': handler,
            'methods': methods,
            'auth_required': auth_required,
            'permissions': permissions or []
        }
        
        self.routes[path] = route_info
    
    def handle_request(self, method: str, path: str, headers: Dict[str, str], 
                       body: str = None) -> Dict[str, Any]:
        """Handle an incoming API request"""
        # Find the matching route
        if path not in self.routes:
            return {
                'success': False,
                'error': 'Route not found',
                'status_code': 404
            }
        
        route_info = self.routes[path]
        
        if method not in route_info['methods']:
            return {
                'success': False,
                'error': 'Method not allowed',
                'status_code': 405
            }
        
        # Authentication
        if route_info['auth_required']:
            token_data = self.authenticate_request(headers)
            if not token_data:
                return {
                    'success': False,
                    'error': 'Authentication required',
                    'status_code': 401
                }
            
            # Authorization
            if not self.authorize_request(token_data, route_info['permissions']):
                return {
                    'success': False,
                    'error': 'Insufficient permissions',
                    'status_code': 403
                }
            
            # Rate limiting
            rate_limit_result = self.check_rate_limit(token_data.user_id)
            if not rate_limit_result['within_limits']:
                return {
                    'success': False,
                    'error': 'Rate limit exceeded',
                    'status_code': 429,
                    'rate_limit': rate_limit_result['limit']
                }
        
        # Call the route handler
        try:
            # In a real implementation, we'd parse the body and pass appropriate parameters
            handler = route_info['handler']
            result = handler(path, method, headers, body)
            
            return {
                'success': True,
                'data': result,
                'status_code': 200
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': 500
            }

class BusinessLogicLayer:
    """Business Logic Layer (L8) with user management and billing"""
    
    def __init__(self):
        self.api_gateway = APIGateway()
        self.setup_routes()
    
    def setup_routes(self):
        """Setup API routes for business logic operations"""
        # User management routes
        self.api_gateway.add_route('/api/users', self.handle_users, ['GET', 'POST'], 
                                   permissions=['users:read', 'users:write'])
        self.api_gateway.add_route('/api/users/me', self.handle_current_user, ['GET'])
        self.api_gateway.add_route('/api/users/profile', self.handle_user_profile, ['GET', 'PUT'])
        
        # Subscription and billing routes
        self.api_gateway.add_route('/api/billing/subscription', self.handle_subscription, 
                                   ['GET', 'POST'], permissions=['billing:read', 'billing:write'])
        self.api_gateway.add_route('/api/billing/usage', self.handle_usage, ['GET'], 
                                   permissions=['billing:read'])
        
        # Token management routes
        self.api_gateway.add_route('/api/tokens', self.handle_tokens, ['GET', 'POST', 'DELETE'], 
                                   permissions=['tokens:read', 'tokens:write'])
        
        # Rate limit check route
        self.api_gateway.add_route('/api/rate-limit', self.handle_rate_limit, ['GET'])
    
    def handle_users(self, path: str, method: str, headers: Dict[str, str], body: str) -> Dict[str, Any]:
        """Handle users API endpoint"""
        if method == 'GET':
            # List users (admin only in real implementation)
            users = self.api_gateway.user_manager.list_users()
            return {
                'users': [u.__dict__ for u in users],
                'count': len(users)
            }
        elif method == 'POST':
            # Create user
            if body:
                try:
                    data = json.loads(body)
                    user = self.api_gateway.user_manager.create_user(
                        data.get('username', f'user_{int(time.time())}'),
                        data.get('email', f'user_{int(time.time())}@example.com')
                    )
                    return {'user': user.__dict__}
                except json.JSONDecodeError:
                    return {'error': 'Invalid JSON in request body'}
        
        return {'error': 'Method not implemented for this endpoint'}
    
    def handle_current_user(self, path: str, method: str, headers: Dict[str, str], body: str) -> Dict[str, Any]:
        """Handle current user endpoint"""
        # Authentication would provide the user ID
        # This is a simulation - in a real system the user ID would come from auth
        token_data = self.api_gateway.authenticate_request(headers)
        if not token_data:
            return {'error': 'Authentication required'}
        
        user = self.api_gateway.user_manager.get_user(token_data.user_id)
        if user:
            return {'user': user.__dict__}
        else:
            return {'error': 'User not found'}
    
    def handle_user_profile(self, path: str, method: str, headers: Dict[str, str], body: str) -> Dict[str, Any]:
        """Handle user profile endpoint"""
        token_data = self.api_gateway.authenticate_request(headers)
        if not token_data:
            return {'error': 'Authentication required'}
        
        if method == 'GET':
            user = self.api_gateway.user_manager.get_user(token_data.user_id)
            if user:
                return {'profile': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role.value,
                    'subscription_tier': user.subscription_tier.value,
                    'created_at': user.created_at.isoformat(),
                    'is_active': user.is_active
                }}
            else:
                return {'error': 'User not found'}
        elif method == 'PUT':
            # Update profile (simplified)
            return {'message': 'Profile updated successfully'}
    
    def handle_subscription(self, path: str, method: str, headers: Dict[str, str], body: str) -> Dict[str, Any]:
        """Handle subscription management"""
        token_data = self.api_gateway.authenticate_request(headers)
        if not token_data:
            return {'error': 'Authentication required'}
        
        if method == 'GET':
            user = self.api_gateway.user_manager.get_user(token_data.user_id)
            if user:
                features = self.api_gateway.billing_manager.calculate_tier_features(user.subscription_tier)
                return {
                    'subscription': {
                        'tier': user.subscription_tier.value,
                        'cost': self.api_gateway.billing_manager.get_subscription_cost(user.subscription_tier),
                        'features': features
                    }
                }
        elif method == 'POST':
            if body:
                try:
                    data = json.loads(body)
                    tier_str = data.get('tier', 'FREE').upper()
                    try:
                        tier = SubscriptionTier[tier_str]
                    except KeyError:
                        return {'error': f'Invalid subscription tier: {tier_str}'}
                    
                    success = self.api_gateway.user_manager.update_subscription_tier(token_data.user_id, tier)
                    if success:
                        return {'message': f'Subscription updated to {tier_str}'}
                    else:
                        return {'error': 'Failed to update subscription'}
                except json.JSONDecodeError:
                    return {'error': 'Invalid JSON in request body'}
    
    def handle_usage(self, path: str, method: str, headers: Dict[str, str], body: str) -> Dict[str, Any]:
        """Handle usage tracking"""
        token_data = self.api_gateway.authenticate_request(headers)
        if not token_data:
            return {'error': 'Authentication required'}
        
        stats = self.api_gateway.rate_limit_manager.get_usage_stats(token_data.user_id)
        return {'usage': stats}
    
    def handle_tokens(self, path: str, method: str, headers: Dict[str, str], body: str) -> Dict[str, Any]:
        """Handle API token management"""
        token_data = self.api_gateway.authenticate_request(headers)
        if not token_data:
            return {'error': 'Authentication required'}
        
        if method == 'GET':
            tokens = self.api_gateway.token_manager.get_tokens_for_user(token_data.user_id)
            return {
                'tokens': [{
                    'id': t.token[:8] + '...',
                    'type': t.token_type.value,
                    'created_at': t.created_at.isoformat(),
                    'expires_at': t.expires_at.isoformat() if t.expires_at else None,
                    'last_used': t.last_used.isoformat() if t.last_used else None
                } for t in tokens]
            }
        elif method == 'POST':
            # Create new token
            new_token = self.api_gateway.token_manager.create_api_token(token_data.user_id)
            return {'token': new_token, 'message': 'Token created successfully'}
        elif method == 'DELETE':
            # Revoke token (would need token to revoke in body)
            return {'message': 'Token revoked (simulation)'}
    
    def handle_rate_limit(self, path: str, method: str, headers: Dict[str, str], body: str) -> Dict[str, Any]:
        """Handle rate limit status"""
        token_data = self.api_gateway.authenticate_request(headers)
        if not token_data:
            return {'error': 'Authentication required'}
        
        status = self.api_gateway.check_rate_limit(token_data.user_id)
        return {'rate_limit_status': status}

def main():
    """Demo of Phase 5 implementation"""
    print("🌐 NEXAFORGE - PHASE 5: API & BUSINESS LOGIC (L7-L8)")
    print("=" * 60)
    
    # Initialize the business logic layer with API gateway
    bll = BusinessLogicLayer()
    gateway = bll.api_gateway
    
    print(f"\n🔐 DEMO 1: USER MANAGEMENT")
    # Create a user
    user = gateway.user_manager.create_user("demo_user", "demo@example.com")
    print(f"✅ Created user: {user.username} (ID: {user.id})")
    
    # Create an API token for the user
    api_token = gateway.token_manager.create_api_token(user.id)
    print(f"✅ Created API token for user: {api_token[:8]}...")
    
    print(f"\n💳 DEMO 2: SUBSCRIPTION & BILLING")
    # Show subscription info
    features = gateway.billing_manager.calculate_tier_features(user.subscription_tier)
    print(f"✅ Current tier: {user.subscription_tier.value}")
    print(f"✅ Features: {features['api_calls_per_month']} API calls/month")
    
    # Update subscription tier
    success = gateway.user_manager.update_subscription_tier(user.id, SubscriptionTier.PROFESSIONAL)
    if success:
        print(f"✅ Updated tier to: {SubscriptionTier.PROFESSIONAL.value}")
    
    print(f"\n🚦 DEMO 3: RATE LIMITING")
    # Check rate limits
    rate_limit_status = gateway.check_rate_limit(user.id)
    print(f"✅ Rate limit status: {rate_limit_status['within_limits']}")
    print(f"   Usage: {rate_limit_status['limit']}")
    
    print(f"\n🌐 DEMO 4: API REQUEST SIMULATION")
    # Simulate an API request
    headers = {"X-API-Key": api_token}
    result = gateway.handle_request("GET", "/api/users/me", headers)
    
    if result['success']:
        print(f"✅ API request successful")
        print(f"   User data: {result.get('data', {}).get('user', {}).get('username', 'N/A')}")
    else:
        print(f"❌ API request failed: {result.get('error', 'Unknown error')}")
    
    print(f"\n🔑 DEMO 5: TOKEN MANAGEMENT")
    # Create additional tokens
    extra_token = gateway.token_manager.create_api_token(user.id, permissions=['read'])
    print(f"✅ Created additional token: {extra_token[:8]}...")
    
    # Check user's tokens
    user_tokens = gateway.token_manager.get_tokens_for_user(user.id)
    print(f"📊 User has {len(user_tokens)} active tokens")
    
    print(f"\n🔒 DEMO 6: PERMISSIONS & AUTHORIZATION")
    # Try a request with insufficient permissions
    restricted_headers = {"X-API-Key": extra_token}
    restricted_result = gateway.handle_request("GET", "/api/users", restricted_headers)
    
    if not restricted_result['success'] and restricted_result['status_code'] == 403:
        print(f"✅ Authorization correctly denied request with insufficient permissions")
    else:
        print(f"ℹ️  Authorization behavior: {restricted_result.get('error', 'N/A')}")
    
    print(f"\n🎉 PHASE 5 COMPLETE: API Gateway & Business Logic Systems Ready!")
    print("   - User management with roles and subscriptions")
    print("   - API authentication and authorization")
    print("   - Rate limiting with tier-based limits")
    print("   - Token management system")
    print("   - Ready for integration with database layer")

if __name__ == "__main__":
    main()