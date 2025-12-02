"""
Services Module
Domain services following DDD pattern for business logic
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
import logging

from src.database.models import User, Organization
from app.context import app_context


class DomainService(ABC):
    """
    Abstract base class for domain services in DDD pattern
    """
    def __init__(self, db_session):
        self.db = db_session
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute the service operation
        """
        pass


class UserDomainService(DomainService):
    """
    Domain service for user-related business operations
    """
    def create_user(self, email: str, password: str, organization_id: uuid.UUID, 
                   role: str = "member", username: Optional[str] = None) -> User:
        """
        Create a new user with business rules validation
        """
        # Check if user already exists
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            raise ValueError(f"User with email {email} already exists")
        
        # Check organization user limit
        organization = self.db.query(Organization).filter(
            Organization.id == organization_id
        ).first()
        
        if organization:
            user_count = self.db.query(User).filter(
                User.organization_id == organization_id
            ).count()
            
            if user_count >= organization.max_users:
                raise ValueError(f"Organization has reached user limit of {organization.max_users}")
        
        # Business rule: password must meet complexity requirements
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        # In a real implementation, we would create the user here
        # For now, returning a placeholder
        from src.security import pwd_context
        from src.database.models import User, RoleEnum
        
        hashed_password = pwd_context.hash(password)
        
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            role=RoleEnum(role) if role in ["owner", "admin", "member", "viewer"] else RoleEnum.MEMBER,
            organization_id=organization_id,
            is_active=True
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def update_user_role(self, user_id: uuid.UUID, new_role: str, 
                        updater_id: uuid.UUID) -> bool:
        """
        Update user role with authorization checks
        """
        # Get the user to update
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Get the updater
        updater = self.db.query(User).filter(User.id == updater_id).first()
        if not updater:
            raise ValueError("Updater not found")
        
        # Business rule: only admins and owners can update roles
        if updater.role.value not in ["admin", "owner"]:
            raise PermissionError("Only admins and owners can update user roles")
        
        # Business rule: owner role can't be changed by admin (only other owner)
        if user.role.value == "owner" and updater.role.value == "admin":
            raise PermissionError("Admin cannot change owner role")
        
        # Update role
        from src.database.models import RoleEnum
        user.role = RoleEnum(new_role)
        self.db.commit()
        
        return True
    
    def soft_delete_user(self, user_id: uuid.UUID, deleter_id: uuid.UUID) -> bool:
        """
        Soft delete a user (set inactive)
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        deleter = self.db.query(User).filter(User.id == deleter_id).first()
        if not deleter:
            raise ValueError("Deleter not found")
        
        # Business rule: only admins and owners can delete users
        if deleter.role.value not in ["admin", "owner"]:
            raise PermissionError("Only admins and owners can delete users")
        
        # Business rule: owner cannot be deleted by admin
        if user.role.value == "owner" and deleter.role.value == "admin":
            raise PermissionError("Admin cannot delete owner")
        
        user.is_active = False
        self.db.commit()
        return True
    
    def execute(self, operation: str, *args, **kwargs):
        """
        Execute user domain operations
        """
        if operation == "create_user":
            return self.create_user(*args, **kwargs)
        elif operation == "update_role":
            return self.update_user_role(*args, **kwargs)
        elif operation == "soft_delete":
            return self.soft_delete_user(*args, **kwargs)
        else:
            raise ValueError(f"Unknown operation: {operation}")


class OrganizationDomainService(DomainService):
    """
    Domain service for organization-related business operations
    """
    def create_organization(self, name: str, owner_email: str, owner_password: str,
                           billing_email: Optional[str] = None) -> Organization:
        """
        Create a new organization with an owner user
        """
        # Business rule: organization name must be unique
        existing_org = self.db.query(Organization).filter(
            Organization.name == name
        ).first()
        if existing_org:
            raise ValueError(f"Organization with name {name} already exists")
        
        # Business rule: owner email must not exist in another organization
        existing_user = self.db.query(User).filter(User.email == owner_email).first()
        if existing_user:
            raise ValueError(f"User with email {owner_email} already exists")
        
        # Business rule: password complexity
        if len(owner_password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        # Create organization
        from src.database.models import Organization as OrgModel, SubscriptionTier
        
        organization = OrgModel(
            name=name,
            tier=SubscriptionTier.STARTER,
            billing_email=billing_email or owner_email,
            status="active"
        )
        self.db.add(organization)
        self.db.flush()  # Get the organization ID without committing
        
        # Create owner user
        from src.security import pwd_context
        from src.database.models import User, RoleEnum
        
        hashed_password = pwd_context.hash(owner_password)
        
        owner_user = User(
            email=owner_email,
            hashed_password=hashed_password,
            role=RoleEnum.OWNER,
            organization_id=organization.id,
            is_active=True
        )
        self.db.add(owner_user)
        
        # Create initial subscription
        from src.database.models import OrganizationSubscription, SubscriptionStatus
        
        # For now, we'll create a stub subscription
        # In real implementation, this would connect to the subscription service
        subscription = OrganizationSubscription(
            organization_id=organization.id,
            # We'd normally set plan_id here, but for demo purposes:
            # plan_id=plan.id,  # Would come from subscription service
            status=SubscriptionStatus.TRIAL,
            started_at=datetime.utcnow(),
            auto_renew=True
        )
        self.db.add(subscription)
        
        self.db.commit()
        self.db.refresh(organization)
        
        return organization
    
    def update_organization_tier(self, org_id: uuid.UUID, new_tier: str, 
                                requester_id: uuid.UUID) -> bool:
        """
        Update organization tier with authorization and validation
        """
        from src.database.models import Organization as OrgModel, SubscriptionTier
        
        organization = self.db.query(OrgModel).filter(OrgModel.id == org_id).first()
        if not organization:
            raise ValueError("Organization not found")
        
        requester = self.db.query(User).filter(User.id == requester_id).first()
        if not requester:
            raise ValueError("Requester not found")
        
        # Business rule: only owner can update tier
        if requester.role.value != "owner":
            raise PermissionError("Only organization owner can update tier")
        
        # Business rule: validate tier
        if new_tier not in ["starter", "professional", "enterprise"]:
            raise ValueError("Invalid tier provided")
        
        # Update tier
        organization.tier = SubscriptionTier(new_tier)
        self.db.commit()
        
        return True
    
    def execute(self, operation: str, *args, **kwargs):
        """
        Execute organization domain operations
        """
        if operation == "create_org":
            return self.create_organization(*args, **kwargs)
        elif operation == "update_tier":
            return self.update_organization_tier(*args, **kwargs)
        else:
            raise ValueError(f"Unknown operation: {operation}")


class SecurityDomainService(DomainService):
    """
    Domain service for security-related business operations
    """
    def __init__(self, db_session):
        super().__init__(db_session)
        
        # Initialize security engine
        from security_engine.engine import SecurityEngine
        self.security_engine = SecurityEngine()
    
    def validate_user_content(self, content: str, user_id: uuid.UUID) -> Dict[str, Any]:
        """
        Validate user content against security policies
        """
        # Get user to check their permissions and context
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Perform security analysis
        analysis_result = self.security_engine.analyze_request(content, {
            "user_id": str(user_id),
            "role": user.role.value,
            "organization_id": str(user.organization_id)
        })
        
        return {
            "content_review": analysis_result,
            "is_allowed": analysis_result["threat_level"] in ["safe", "info"],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def filter_response_content(self, response: str, original_request: str, 
                               user_id: uuid.UUID) -> Dict[str, Any]:
        """
        Filter AI response content for security
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Perform response filtering
        filter_result = self.security_engine.filter_response(
            response, 
            original_request, 
            {
                "user_id": str(user_id),
                "role": user.role.value,
                "organization_id": str(user.organization_id)
            }
        )
        
        return {
            "original_response": response,
            "filtered_response": filter_result["processed_response"],
            "analysis": filter_result["analysis"],
            "is_allowed": filter_result["is_allowed"],
            "timestamp": filter_result["timestamp"]
        }
    
    def execute(self, operation: str, *args, **kwargs):
        """
        Execute security domain operations
        """
        if operation == "validate_content":
            return self.validate_user_content(*args, **kwargs)
        elif operation == "filter_response":
            return self.filter_response_content(*args, **kwargs)
        else:
            raise ValueError(f"Unknown operation: {operation}")


class SubscriptionDomainService(DomainService):
    """
    Domain service for subscription and billing business operations
    """
    def __init__(self, db_session):
        super().__init__(db_session)
    
    def calculate_usage_cost(self, organization_id: uuid.UUID, 
                           usage_type: str, quantity: int) -> float:
        """
        Calculate cost based on usage for billing
        """
        # Get organization to determine tier
        from src.database.models import Organization as OrgModel, SubscriptionTier
        
        organization = self.db.query(OrgModel).filter(
            OrgModel.id == organization_id
        ).first()
        
        if not organization:
            raise ValueError("Organization not found")
        
        # Define pricing based on tier
        pricing = {
            SubscriptionTier.STARTER: {
                "scans": {"rate": 0.10, "included": 1000},
                "api_calls": {"rate": 0.001, "included": 10000},
                "agent_hours": {"rate": 4.00, "included": 0}
            },
            SubscriptionTier.PROFESSIONAL: {
                "scans": {"rate": 0.10, "included": 10000},
                "api_calls": {"rate": 0.001, "included": 100000},
                "agent_hours": {"rate": 4.00, "included": 0}
            },
            SubscriptionTier.ENTERPRISE: {
                "scans": {"rate": 0.05, "included": 1000000},  # Unlimited effectively
                "api_calls": {"rate": 0.0005, "included": 10000000},
                "agent_hours": {"rate": 3.00, "included": 0}
            }
        }
        
        # Get pricing for organization tier
        tier_pricing = pricing.get(organization.tier, pricing[SubscriptionTier.STARTER])
        
        if usage_type not in tier_pricing:
            raise ValueError(f"Unknown usage type: {usage_type}")
        
        pricing_info = tier_pricing[usage_type]
        
        # Calculate overage
        overage = max(0, quantity - pricing_info["included"])
        cost = overage * pricing_info["rate"]
        
        return cost
    
    def execute(self, operation: str, *args, **kwargs):
        """
        Execute subscription domain operations
        """
        if operation == "calculate_cost":
            return self.calculate_usage_cost(*args, **kwargs)
        else:
            raise ValueError(f"Unknown operation: {operation}")