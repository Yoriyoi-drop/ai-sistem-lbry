from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
from typing import Optional, List
import uuid
from ..models.subscription import User, SubscriptionPlan, Subscription, Payment, UsageRecord
from ..schemas.subscription import (
    UserCreate, UserUpdate, SubscriptionPlanCreate, SubscriptionPlanUpdate,
    SubscriptionCreate, SubscriptionUpdate, SubscriptionChangeRequest,
    PaymentCreate, UsageRecordCreate, SubscriptionAnalytics, SubscriptionStatus
)
from ..utils.security import get_password_hash
from decimal import Decimal


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_create: UserCreate, password: str = None) -> User:
        """Create a new user"""
        # Create hashed password if provided
        hashed_password = get_password_hash(password) if password else None
        
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update a user"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None

        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        return True


class SubscriptionPlanService:
    def __init__(self, db: Session):
        self.db = db

    def create_plan(self, plan_create: SubscriptionPlanCreate) -> SubscriptionPlan:
        """Create a new subscription plan"""
        db_plan = SubscriptionPlan(
            name=plan_create.name,
            tier=plan_create.tier,
            description=plan_create.description,
            price=plan_create.price,
            billing_cycle=plan_create.billing_cycle,
            features=plan_create.features,
            max_agents=plan_create.max_agents,
            scan_limit=plan_create.scan_limit,
            api_rate_limit=plan_create.api_rate_limit,
            support_level=plan_create.support_level
        )
        self.db.add(db_plan)
        self.db.commit()
        self.db.refresh(db_plan)
        return db_plan

    def get_plan_by_id(self, plan_id: int) -> Optional[SubscriptionPlan]:
        """Get a subscription plan by ID"""
        return self.db.query(SubscriptionPlan).filter(SubscriptionPlan.id == plan_id).first()

    def get_active_plans(self) -> List[SubscriptionPlan]:
        """Get all active subscription plans"""
        return self.db.query(SubscriptionPlan).filter(SubscriptionPlan.is_active == True).all()

    def get_plan_by_tier(self, tier: str) -> Optional[SubscriptionPlan]:
        """Get a subscription plan by tier"""
        return self.db.query(SubscriptionPlan).filter(SubscriptionPlan.tier == tier).first()

    def update_plan(self, plan_id: int, plan_update: SubscriptionPlanUpdate) -> Optional[SubscriptionPlan]:
        """Update a subscription plan"""
        db_plan = self.get_plan_by_id(plan_id)
        if not db_plan:
            return None

        update_data = plan_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_plan, field, value)

        self.db.commit()
        self.db.refresh(db_plan)
        return db_plan

    def delete_plan(self, plan_id: int) -> bool:
        """Delete a subscription plan (set as inactive)"""
        db_plan = self.get_plan_by_id(plan_id)
        if not db_plan:
            return False

        db_plan.is_active = False
        self.db.commit()
        return True


class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db
        self.plan_service = SubscriptionPlanService(db)

    def create_subscription(self, user_id: int, subscription_create: SubscriptionCreate) -> Subscription:
        """Create a new subscription for a user"""
        # Get the plan
        plan = self.plan_service.get_plan_by_id(subscription_create.plan_id)
        if not plan:
            raise ValueError("Plan not found")
        
        # Calculate period dates
        now = datetime.utcnow()
        if plan.billing_cycle == "monthly":
            period_end = now + timedelta(days=30)
        else:  # yearly
            period_end = now + timedelta(days=365)
        
        # Handle trial
        trial_start = None
        trial_end = None
        if subscription_create.trial_days and subscription_create.trial_days > 0:
            trial_start = now
            trial_end = now + timedelta(days=subscription_create.trial_days)
            # Extend period end to account for trial
            if plan.billing_cycle == "monthly":
                period_end = trial_end + timedelta(days=30)
            else:
                period_end = trial_end + timedelta(days=365)

        db_subscription = Subscription(
            user_id=user_id,
            plan_id=subscription_create.plan_id,
            status="active" if not trial_end else "trialing",  # Set as trialing if trial exists
            current_period_start=trial_end or now if trial_end else now,
            current_period_end=period_end,
            trial_start=trial_start,
            trial_end=trial_end
        )
        
        self.db.add(db_subscription)
        self.db.commit()
        self.db.refresh(db_subscription)
        return db_subscription

    def get_user_subscription(self, user_id: int) -> Optional[Subscription]:
        """Get the current subscription for a user"""
        return self.db.query(Subscription).filter(Subscription.user_id == user_id).first()

    def get_subscription_by_id(self, subscription_id: int) -> Optional[Subscription]:
        """Get a subscription by ID"""
        return self.db.query(Subscription).filter(Subscription.id == subscription_id).first()

    def update_subscription(self, subscription_id: int, subscription_update: SubscriptionUpdate) -> Optional[Subscription]:
        """Update a subscription"""
        db_subscription = self.get_subscription_by_id(subscription_id)
        if not db_subscription:
            return None

        update_data = subscription_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_subscription, field, value)

        self.db.commit()
        self.db.refresh(db_subscription)
        return db_subscription

    def cancel_subscription(self, subscription_id: int, immediate: bool = False) -> Optional[Subscription]:
        """Cancel a subscription"""
        db_subscription = self.get_subscription_by_id(subscription_id)
        if not db_subscription:
            return None

        if immediate:
            # Cancel immediately
            db_subscription.status = "cancelled"
            db_subscription.cancelled_at = datetime.utcnow()
        else:
            # Cancel at period end
            db_subscription.cancel_at_period_end = True

        self.db.commit()
        self.db.refresh(db_subscription)
        return db_subscription

    def change_subscription_plan(self, subscription_id: int, change_request: SubscriptionChangeRequest) -> Optional[Subscription]:
        """Change a subscription to a different plan"""
        db_subscription = self.get_subscription_by_id(subscription_id)
        if not db_subscription:
            return None

        old_plan = self.plan_service.get_plan_by_id(db_subscription.plan_id)
        new_plan = self.plan_service.get_plan_by_id(change_request.new_plan_id)
        if not new_plan:
            raise ValueError("New plan not found")

        # Update the plan
        db_subscription.plan_id = change_request.new_plan_id

        # If prorating, calculate new period end based on usage
        if change_request.prorate:
            # For now, just extend to the next billing cycle based on new plan
            now = datetime.utcnow()
            if new_plan.billing_cycle == "monthly":
                new_period_end = now + timedelta(days=30)
            else:
                new_period_end = now + timedelta(days=365)
            
            db_subscription.current_period_start = now
            db_subscription.current_period_end = new_period_end
        else:
            # Keep the same period end to align with original billing cycle
            pass

        self.db.commit()
        self.db.refresh(db_subscription)
        return db_subscription

    def check_user_entitlements(self, user_id: int) -> dict:
        """Check what a user is entitled to based on their subscription"""
        subscription = self.get_user_subscription(user_id)
        if not subscription or subscription.status not in ["active", "trialing"]:
            # Return free tier entitlements
            free_plan = self.plan_service.get_plan_by_tier("free")
            if not free_plan:
                # Default free tier if not found
                return {
                    "max_agents": 1,
                    "scan_limit": 10,
                    "api_rate_limit": 1000,
                    "support_level": "community",
                    "features": []
                }
            return {
                "max_agents": free_plan.max_agents,
                "scan_limit": free_plan.scan_limit,
                "api_rate_limit": free_plan.api_rate_limit,
                "support_level": free_plan.support_level,
                "features": free_plan.features
            }

        plan = subscription.plan
        return {
            "max_agents": plan.max_agents,
            "scan_limit": plan.scan_limit,
            "api_rate_limit": plan.api_rate_limit,
            "support_level": plan.support_level,
            "features": plan.features
        }

    def is_subscription_active(self, user_id: int) -> bool:
        """Check if a user's subscription is active"""
        subscription = self.get_user_subscription(user_id)
        if not subscription:
            return False

        # Check if the subscription is active and not expired
        now = datetime.utcnow()
        is_active_status = subscription.status in ["active", "trialing"]
        is_not_expired = subscription.current_period_end > now
        is_not_cancelled = not (subscription.cancel_at_period_end and subscription.current_period_end <= now)

        return is_active_status and is_not_expired and is_not_cancelled


class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    def create_payment(self, payment_create: PaymentCreate) -> Payment:
        """Create a new payment record"""
        db_payment = Payment(
            user_id=payment_create.user_id,
            subscription_id=payment_create.subscription_id,
            amount=payment_create.amount,
            currency=payment_create.currency,
            payment_method=payment_create.payment_method
        )
        self.db.add(db_payment)
        self.db.commit()
        self.db.refresh(db_payment)
        return db_payment

    def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        """Get a payment by ID"""
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def get_payments_by_user(self, user_id: int) -> List[Payment]:
        """Get all payments for a user"""
        return self.db.query(Payment).filter(Payment.user_id == user_id).all()

    def get_payments_by_subscription(self, subscription_id: int) -> List[Payment]:
        """Get all payments for a subscription"""
        return self.db.query(Payment).filter(Payment.subscription_id == subscription_id).all()

    def update_payment_status(self, payment_id: int, status: str) -> Optional[Payment]:
        """Update payment status"""
        db_payment = self.get_payment_by_id(payment_id)
        if not db_payment:
            return None

        db_payment.status = status
        if status in ["completed", "failed", "refunded"]:
            db_payment.processed_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(db_payment)
        return db_payment


class UsageTrackingService:
    def __init__(self, db: Session):
        self.db = db

    def record_usage(self, user_id: int, usage_record: UsageRecordCreate) -> UsageRecord:
        """Record a usage event"""
        db_usage = UsageRecord(
            user_id=user_id,
            resource_type=usage_record.resource_type,
            resource_id=usage_record.resource_id,
            quantity=usage_record.quantity
        )
        self.db.add(db_usage)
        self.db.commit()
        self.db.refresh(db_usage)
        return db_usage

    def get_usage_for_user(self, user_id: int, start_date: datetime, end_date: datetime) -> List[UsageRecord]:
        """Get usage records for a user within a date range"""
        return self.db.query(UsageRecord).filter(
            UsageRecord.user_id == user_id,
            UsageRecord.recorded_at >= start_date,
            UsageRecord.recorded_at <= end_date
        ).all()

    def get_total_usage(self, user_id: int, resource_type: str, start_date: datetime, end_date: datetime) -> int:
        """Get total usage of a specific resource type for a user"""
        result = self.db.query(func.sum(UsageRecord.quantity)).filter(
            UsageRecord.user_id == user_id,
            UsageRecord.resource_type == resource_type,
            UsageRecord.recorded_at >= start_date,
            UsageRecord.recorded_at <= end_date
        ).scalar()
        return result or 0

    def get_current_period_usage(self, user_id: int, resource_type: str) -> int:
        """Get usage for the current period (last 30 days)"""
        now = datetime.utcnow()
        start_date = now - timedelta(days=30)
        return self.get_total_usage(user_id, resource_type, start_date, now)


class SubscriptionAnalyticsService:
    def __init__(self, db: Session):
        self.db = db
        self.subscription_service = SubscriptionService(db)

    def get_analytics(self) -> SubscriptionAnalytics:
        """Get comprehensive subscription analytics"""
        now = datetime.utcnow()
        
        # Total subscribers
        total_subscribers = self.db.query(Subscription).count()
        
        # Active subscribers
        active_subscribers = self.db.query(Subscription).filter(
            Subscription.status == "active",
            Subscription.current_period_end > now
        ).count()
        
        # Churn rate (simplified calculation)
        # This would be more complex in a real system
        churn_rate = 0.0  # Placeholder - would need historical data
        
        # MRR and ARR calculations
        active_subscriptions = self.db.query(Subscription).join(SubscriptionPlan).filter(
            Subscription.status == "active",
            Subscription.current_period_end > now
        ).all()
        
        mrr = 0
        for sub in active_subscriptions:
            if sub.plan.billing_cycle == "monthly":
                mrr += float(sub.plan.price)
            else:  # yearly
                mrr += float(sub.plan.price) / 12
        
        arr = mrr * 12
        
        # Subscription tier distribution
        tier_counts = {}
        for tier in ["free", "basic", "professional", "enterprise"]:
            count = self.db.query(Subscription).join(SubscriptionPlan).filter(
                SubscriptionPlan.tier == tier,
                Subscription.status == "active",
                Subscription.current_period_end > now
            ).count()
            tier_counts[tier] = count

        return SubscriptionAnalytics(
            total_subscribers=total_subscribers,
            active_subscribers=active_subscribers,
            churn_rate=churn_rate,
            mrr=round(mrr, 2),
            arr=round(arr, 2),
            subscription_tiers=tier_counts
        )