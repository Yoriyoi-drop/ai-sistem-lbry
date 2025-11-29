"""
Tier Management Service for Subscription Tiers
Based on B2B SaaS transformation strategy (Starter/Professional/Enterprise)
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid

from src.database.models import (
    SubscriptionPlan, OrganizationSubscription, 
    SubscriptionTier, SubscriptionStatus
)


class TierService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_tiers(self) -> List[Dict[str, Any]]:
        """Get all available subscription tiers with their features and limits"""
        plans = self.db.query(SubscriptionPlan).filter(
            SubscriptionPlan.is_active == True
        ).all()
        
        return [
            {
                "id": str(plan.id),
                "name": plan.name,
                "tier": plan.tier.value,
                "price_monthly": float(plan.price_monthly),
                "features": plan.features,
                "limits": plan.limits,
                "is_active": plan.is_active
            }
            for plan in plans
        ]

    def get_tier_by_name(self, tier_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific tier by name"""
        plan = self.db.query(SubscriptionPlan).filter(
            SubscriptionPlan.tier == tier_name,
            SubscriptionPlan.is_active == True
        ).first()
        
        if plan:
            return {
                "id": str(plan.id),
                "name": plan.name,
                "tier": plan.tier.value,
                "price_monthly": float(plan.price_monthly),
                "features": plan.features,
                "limits": plan.limits,
                "is_active": plan.is_active
            }
        
        return None

    def get_tier_by_id(self, plan_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """Get a specific tier by ID"""
        plan = self.db.query(SubscriptionPlan).filter(
            SubscriptionPlan.id == plan_id
        ).first()
        
        if plan:
            return {
                "id": str(plan.id),
                "name": plan.name,
                "tier": plan.tier.value,
                "price_monthly": float(plan.price_monthly),
                "features": plan.features,
                "limits": plan.limits,
                "is_active": plan.is_active
            }
        
        return None

    def create_tier(self, name: str, tier: SubscriptionTier, price_monthly: float, 
                    features: List[str], limits: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new subscription tier"""
        plan = SubscriptionPlan(
            name=name,
            tier=tier,
            price_monthly=price_monthly,
            features=features,
            limits=limits,
            is_active=True
        )
        
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        
        return {
            "id": str(plan.id),
            "name": plan.name,
            "tier": plan.tier.value,
            "price_monthly": float(plan.price_monthly),
            "features": plan.features,
            "limits": plan.limits,
            "is_active": plan.is_active
        }

    def update_tier(self, plan_id: uuid.UUID, **kwargs) -> Optional[Dict[str, Any]]:
        """Update an existing subscription tier"""
        plan = self.db.query(SubscriptionPlan).filter(
            SubscriptionPlan.id == plan_id
        ).first()
        
        if not plan:
            return None
        
        # Update fields that were provided
        for field, value in kwargs.items():
            if hasattr(plan, field):
                setattr(plan, field, value)
        
        self.db.commit()
        self.db.refresh(plan)
        
        return {
            "id": str(plan.id),
            "name": plan.name,
            "tier": plan.tier.value,
            "price_monthly": float(plan.price_monthly),
            "features": plan.features,
            "limits": plan.limits,
            "is_active": plan.is_active
        }

    def get_starter_tier(self) -> Optional[Dict[str, Any]]:
        """Get the Starter tier details"""
        return self.get_tier_by_name(SubscriptionTier.STARTER.value)

    def get_professional_tier(self) -> Optional[Dict[str, Any]]:
        """Get the Professional tier details"""
        return self.get_tier_by_name(SubscriptionTier.PROFESSIONAL.value)

    def get_enterprise_tier(self) -> Optional[Dict[str, Any]]:
        """Get the Enterprise tier details"""
        return self.get_tier_by_name(SubscriptionTier.ENTERPRISE.value)

    def get_tier_limits(self, tier: SubscriptionTier) -> Dict[str, Any]:
        """Get the limits for a specific tier"""
        tier_info = self.get_tier_by_name(tier.value)
        return tier_info.get("limits", {}) if tier_info else {}

    def get_tier_features(self, tier: SubscriptionTier) -> List[str]:
        """Get the features for a specific tier"""
        tier_info = self.get_tier_by_name(tier.value)
        return tier_info.get("features", []) if tier_info else []

    def get_tier_price(self, tier: SubscriptionTier) -> float:
        """Get the monthly price for a specific tier"""
        tier_info = self.get_tier_by_name(tier.value)
        return float(tier_info.get("price_monthly", 0)) if tier_info else 0.0

    def get_organization_subscription_info(self, org_id: uuid.UUID) -> Dict[str, Any]:
        """Get the subscription information for an organization"""
        subscription = self.db.query(OrganizationSubscription).filter(
            OrganizationSubscription.organization_id == org_id
        ).first()
        
        if not subscription:
            # Return default info for free tier or no subscription
            return {
                "organization_id": str(org_id),
                "current_tier": SubscriptionTier.STARTER.value,
                "status": "trial",
                "started_at": datetime.utcnow().isoformat(),
                "ends_at": None,
                "trial_ends_at": (datetime.utcnow() + timedelta(days=14)).isoformat(),  # 14-day trial
                "auto_renew": True,
                "plan_details": self.get_tier_by_name(SubscriptionTier.STARTER.value)
            }
        
        plan_info = self.get_tier_by_id(subscription.plan_id)
        
        return {
            "organization_id": str(org_id),
            "current_tier": subscription.plan.tier.value,
            "status": subscription.status,
            "started_at": subscription.started_at.isoformat() if subscription.started_at else None,
            "ends_at": subscription.ends_at.isoformat() if subscription.ends_at else None,
            "trial_ends_at": subscription.trial_ends_at.isoformat() if subscription.trial_ends_at else None,
            "auto_renew": subscription.auto_renew,
            "plan_details": plan_info
        }

    def update_organization_subscription(self, org_id: uuid.UUID, 
                                       new_tier: SubscriptionTier) -> Dict[str, Any]:
        """Update organization subscription to a new tier"""
        # Get the plan for the new tier
        new_plan = self.db.query(SubscriptionPlan).filter(
            SubscriptionPlan.tier == new_tier,
            SubscriptionPlan.is_active == True
        ).first()
        
        if not new_plan:
            raise ValueError(f"Plan for tier {new_tier.value} not found or not active")
        
        # Check if organization already has a subscription
        existing_subscription = self.db.query(OrganizationSubscription).filter(
            OrganizationSubscription.organization_id == org_id
        ).first()
        
        if existing_subscription:
            # Update existing subscription
            existing_subscription.plan_id = new_plan.id
            existing_subscription.status = SubscriptionStatus.ACTIVE
            existing_subscription.updated_at = datetime.utcnow()
            
            # Update end date if it was a trial
            if existing_subscription.status == "trial":
                # Set to end in 30 days for paid plans
                if new_tier != SubscriptionTier.STARTER:
                    existing_subscription.ends_at = datetime.utcnow() + timedelta(days=30)
        else:
            # Create new subscription
            subscription = OrganizationSubscription(
                organization_id=org_id,
                plan_id=new_plan.id,
                status=SubscriptionStatus.ACTIVE,
                started_at=datetime.utcnow(),
                auto_renew=True
            )
            
            # Set end date for paid plans
            if new_tier != SubscriptionTier.STARTER:
                subscription.ends_at = datetime.utcnow() + timedelta(days=30)
            
            self.db.add(subscription)
        
        self.db.commit()
        
        return self.get_organization_subscription_info(org_id)

    def calculate_tier_cost(self, tier: SubscriptionTier, 
                           additional_scans: int = 0,
                           additional_api_calls: int = 0,
                           additional_agent_hours: int = 0) -> Dict[str, float]:
        """
        Calculate the total cost for a tier including usage-based components
        """
        base_price = self.get_tier_price(tier)
        
        # Define usage costs (these would typically come from config)
        scan_cost = 0.10  # $0.10 per additional scan beyond quota
        api_call_cost = 0.001  # $0.001 per additional API call beyond quota
        agent_hour_cost = 4.00  # $4.00 per agent hour
        
        additional_cost = 0.0
        
        # Calculate additional costs
        if additional_scans > 0:
            additional_cost += additional_scans * scan_cost
        if additional_api_calls > 0:
            additional_cost += additional_api_calls * api_call_cost
        if additional_agent_hours > 0:
            additional_cost += additional_agent_hours * agent_hour_cost
        
        total_cost = base_price + additional_cost
        
        return {
            "base_price": base_price,
            "additional_cost": additional_cost,
            "total_cost": total_cost,
            "scan_cost": additional_scans * scan_cost if additional_scans > 0 else 0,
            "api_call_cost": additional_api_calls * api_call_cost if additional_api_calls > 0 else 0,
            "agent_hour_cost": additional_agent_hours * agent_hour_cost if additional_agent_hours > 0 else 0
        }

    def get_feature_availability(self, org_id: uuid.UUID, feature_name: str) -> bool:
        """
        Check if a specific feature is available for an organization's tier
        """
        subscription_info = self.get_organization_subscription_info(org_id)
        plan_details = subscription_info.get("plan_details", {})
        features = plan_details.get("features", [])
        
        # Check if feature is in the plan's features
        for feature in features:
            if feature_name.lower() in feature.lower():
                return True
        
        return False