"""
Organization and User Management Service for Multi-Tenant Infinite AI Security Platform
Based on B2B SaaS transformation strategy
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
import uuid

from src.database.models import (
    Organization, User, RoleEnum, SubscriptionTier, OrganizationSubscription,
    SubscriptionPlan, UsageMetric
)
from src.security import pwd_context


class OrganizationService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_organization(
        self, 
        name: str, 
        owner_email: str, 
        owner_password: str, 
        billing_email: Optional[str] = None,
        tier: SubscriptionTier = SubscriptionTier.STARTER
    ) -> Organization:
        """Create a new organization with an owner user"""
        # Create the organization
        organization = Organization(
            name=name,
            tier=tier,
            billing_email=billing_email or owner_email,
            status="active"
        )
        self.db.add(organization)
        self.db.flush()  # Get the organization ID without committing
        
        # Hash the owner's password
        hashed_password = pwd_context.hash(owner_password)
        
        # Create the owner user
        owner_user = User(
            email=owner_email,
            hashed_password=hashed_password,
            role=RoleEnum.OWNER,
            organization_id=organization.id,
            is_active=True
        )
        self.db.add(owner_user)
        
        # Create the initial subscription
        # Get the default subscription plan based on tier
        plan = self.db.query(SubscriptionPlan).filter(
            SubscriptionPlan.tier == tier
        ).first()
        
        if plan:
            subscription = OrganizationSubscription(
                organization_id=organization.id,
                plan_id=plan.id,
                status="active",
                started_at=datetime.utcnow(),
                auto_renew=True
            )
            self.db.add(subscription)
        
        self.db.commit()
        self.db.refresh(organization)
        
        return organization

    def get_organization_by_id(self, org_id: uuid.UUID) -> Optional[Organization]:
        """Get organization by ID"""
        return self.db.query(Organization).filter(Organization.id == org_id).first()

    def get_organization_by_name(self, name: str) -> Optional[Organization]:
        """Get organization by name"""
        return self.db.query(Organization).filter(Organization.name == name).first()

    def update_organization_tier(self, org_id: uuid.UUID, tier: SubscriptionTier) -> bool:
        """Update organization subscription tier"""
        organization = self.get_organization_by_id(org_id)
        if not organization:
            return False

        organization.tier = tier
        
        # Update the subscription plan
        plan = self.db.query(SubscriptionPlan).filter(
            SubscriptionPlan.tier == tier
        ).first()
        
        if plan:
            # Find existing subscription
            existing_subscription = self.db.query(OrganizationSubscription).filter(
                OrganizationSubscription.organization_id == org_id
            ).first()
            
            if existing_subscription:
                existing_subscription.plan_id = plan.id
                existing_subscription.updated_at = datetime.utcnow()
            else:
                # Create new subscription
                subscription = OrganizationSubscription(
                    organization_id=org_id,
                    plan_id=plan.id,
                    status="active",
                    started_at=datetime.utcnow(),
                    auto_renew=True
                )
                self.db.add(subscription)
        
        self.db.commit()
        return True

    def get_organization_users(self, org_id: uuid.UUID) -> List[User]:
        """Get all users in an organization"""
        return self.db.query(User).filter(User.organization_id == org_id).all()

    def create_user_in_organization(
        self, 
        org_id: uuid.UUID, 
        email: str, 
        password: str, 
        role: RoleEnum = RoleEnum.MEMBER,
        username: Optional[str] = None
    ) -> Optional[User]:
        """Create a new user within an organization"""
        organization = self.get_organization_by_id(org_id)
        if not organization:
            return None

        # Check if user already exists
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            return None

        # Check if organization has reached user limit
        user_count = self.db.query(User).filter(
            User.organization_id == org_id
        ).count()
        
        if user_count >= organization.max_users:
            raise Exception(f"Organization has reached user limit of {organization.max_users}")

        # Hash the password
        hashed_password = pwd_context.hash(password)

        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            role=role,
            organization_id=org_id,
            is_active=True
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user

    def get_subscription_limits(self, org_id: uuid.UUID) -> Dict[str, Any]:
        """Get current subscription limits for an organization"""
        organization = self.get_organization_by_id(org_id)
        if not organization:
            return {}

        # Get the subscription plan
        subscription = self.db.query(OrganizationSubscription).filter(
            OrganizationSubscription.organization_id == org_id
        ).first()

        if not subscription:
            return {}

        plan = self.db.query(SubscriptionPlan).filter(
            SubscriptionPlan.id == subscription.plan_id
        ).first()

        if not plan:
            return {}

        return plan.limits

    def track_usage(self, org_id: uuid.UUID, metric_type: str, quantity: int = 1) -> bool:
        """Track usage for consumption-based billing"""
        try:
            # Check if we already have a usage record for this period
            current_date = datetime.utcnow().date()
            current_period = current_date.replace(day=1)  # Start of current month

            usage_record = self.db.query(UsageMetric).filter(
                and_(
                    UsageMetric.organization_id == org_id,
                    UsageMetric.metric_type == metric_type,
                    UsageMetric.period == current_period
                )
            ).first()

            if usage_record:
                # Update existing record
                usage_record.quantity += quantity
                usage_record.created_at = datetime.utcnow()
            else:
                # Create new record
                usage_record = UsageMetric(
                    organization_id=org_id,
                    metric_type=metric_type,
                    quantity=quantity,
                    period=current_period
                )
                self.db.add(usage_record)

            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def get_usage_for_period(self, org_id: uuid.UUID, metric_type: str, period: datetime.date) -> int:
        """Get usage for a specific metric type and period"""
        usage_record = self.db.query(UsageMetric).filter(
            and_(
                UsageMetric.organization_id == org_id,
                UsageMetric.metric_type == metric_type,
                UsageMetric.period == period
            )
        ).first()

        return usage_record.quantity if usage_record else 0

    def get_current_usage(self, org_id: uuid.UUID, metric_type: str) -> int:
        """Get current month usage for a specific metric type"""
        current_date = datetime.utcnow().date()
        current_period = current_date.replace(day=1)  # Start of current month

        return self.get_usage_for_period(org_id, metric_type, current_period)

    def check_usage_limit(self, org_id: uuid.UUID, metric_type: str) -> tuple[bool, int, int]:
        """
        Check if organization has exceeded usage limit for a metric type
        Returns: (is_within_limit, current_usage, limit)
        """
        # Get subscription limits
        limits = self.get_subscription_limits(org_id)
        if not limits:
            return True, 0, 0  # If no limits, assume unlimited

        # Get the limit for this metric type
        limit_key = f"max_{metric_type.replace('-', '_')}_per_month" if 'per_month' not in metric_type else metric_type
        limit = limits.get(limit_key, 0)

        # Get current usage
        current_usage = self.get_current_usage(org_id, metric_type)

        is_within_limit = current_usage < limit if limit > 0 else True
        return is_within_limit, current_usage, limit