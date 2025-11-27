from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.connection import get_db
from ..schemas.subscription import (
    User, UserCreate, UserUpdate, SubscriptionPlan, SubscriptionPlanCreate,
    SubscriptionPlanUpdate, SubscriptionRead, SubscriptionCreate, SubscriptionUpdate,
    SubscriptionChangeRequest, SubscriptionCancellationRequest, PaymentRead, PaymentCreate,
    UsageRecord, UsageRecordCreate, SubscriptionResponse, SubscriptionAnalytics,
    PaymentIntentResponse
)
from ..services.subscription import (
    UserService, SubscriptionPlanService, SubscriptionService,
    PaymentService, UsageTrackingService, SubscriptionAnalyticsService
)
from ..utils.dependencies import get_current_user
from datetime import datetime


router = APIRouter(prefix="/subscription", tags=["subscription"])


# User management endpoints
@router.post("/users/", response_model=User)
def create_user(
    user_create: UserCreate,
    password: str,
    db: Session = Depends(get_db)
):
    """Create a new user"""
    user_service = UserService(db)
    
    # Check if user already exists
    if user_service.get_user_by_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    if user_service.get_user_by_username(user_create.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )
    
    user = user_service.create_user(user_create, password)
    return user


@router.get("/users/{user_id}", response_model=User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a user by ID"""
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Only allow users to access their own information or admins
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user"
        )
    
    return user


@router.put("/users/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a user"""
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Only allow users to update their own information or admins
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    updated_user = user_service.update_user(user_id, user_update)
    return updated_user


# Subscription plan endpoints
@router.get("/plans/", response_model=List[SubscriptionPlan])
def get_active_plans(
    db: Session = Depends(get_db)
):
    """Get all active subscription plans"""
    plan_service = SubscriptionPlanService(db)
    plans = plan_service.get_active_plans()
    return plans


@router.get("/plans/{plan_id}", response_model=SubscriptionPlan)
def get_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):
    """Get a subscription plan by ID"""
    plan_service = SubscriptionPlanService(db)
    plan = plan_service.get_plan_by_id(plan_id)
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription plan not found"
        )
    
    return plan


@router.post("/plans/", response_model=SubscriptionPlan)
def create_plan(
    plan_create: SubscriptionPlanCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new subscription plan (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create subscription plans"
        )
    
    plan_service = SubscriptionPlanService(db)
    plan = plan_service.create_plan(plan_create)
    return plan


@router.put("/plans/{plan_id}", response_model=SubscriptionPlan)
def update_plan(
    plan_id: int,
    plan_update: SubscriptionPlanUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a subscription plan (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update subscription plans"
        )
    
    plan_service = SubscriptionPlanService(db)
    plan = plan_service.update_plan(plan_id, plan_update)
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription plan not found"
        )
    
    return plan


# Subscription endpoints
@router.get("/users/{user_id}/subscription", response_model=SubscriptionResponse)
def get_user_subscription(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get the subscription details for a user"""
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this subscription"
        )
    
    subscription_service = SubscriptionService(db)
    subscription = subscription_service.get_user_subscription(user_id)
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No subscription found for this user"
        )
    
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    
    # Calculate billing info
    billing_info = None
    if subscription.status in ["active", "trialing"]:
        from ..schemas.subscription import BillingInfo
        billing_info = BillingInfo(
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            next_billing_date=subscription.current_period_end,
            amount_due=float(subscription.plan.price),
            currency="USD"
        )
    
    return SubscriptionResponse(
        user=user,
        subscription=subscription,
        billing_info=billing_info
    )


@router.post("/users/{user_id}/subscription", response_model=SubscriptionRead)
def create_user_subscription(
    user_id: int,
    subscription_create: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a subscription for a user"""
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to manage this subscription"
        )
    
    # Check if user already has an active subscription
    subscription_service = SubscriptionService(db)
    existing_subscription = subscription_service.get_user_subscription(user_id)
    if existing_subscription and existing_subscription.status in ["active", "trialing"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an active subscription"
        )
    
    subscription = subscription_service.create_subscription(user_id, subscription_create)
    return subscription


@router.put("/subscriptions/{subscription_id}", response_model=SubscriptionRead)
def update_subscription(
    subscription_id: int,
    subscription_update: SubscriptionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update a subscription"""
    subscription_service = SubscriptionService(db)
    subscription = subscription_service.get_subscription_by_id(subscription_id)
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    # Check authorization: user can update their own subscription or admin
    if subscription.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this subscription"
        )
    
    updated_subscription = subscription_service.update_subscription(subscription_id, subscription_update)
    return updated_subscription


@router.post("/subscriptions/{subscription_id}/change-plan", response_model=SubscriptionRead)
def change_subscription_plan(
    subscription_id: int,
    change_request: SubscriptionChangeRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Change a subscription to a different plan"""
    subscription_service = SubscriptionService(db)
    subscription = subscription_service.get_subscription_by_id(subscription_id)
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    # Check authorization
    if subscription.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to manage this subscription"
        )
    
    updated_subscription = subscription_service.change_subscription_plan(subscription_id, change_request)
    return updated_subscription


@router.post("/subscriptions/{subscription_id}/cancel")
def cancel_subscription(
    subscription_id: int,
    cancellation_request: SubscriptionCancellationRequest = None,
    immediate: bool = False,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Cancel a subscription"""
    subscription_service = SubscriptionService(db)
    subscription = subscription_service.get_subscription_by_id(subscription_id)
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    # Check authorization
    if subscription.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this subscription"
        )
    
    subscription_service.cancel_subscription(subscription_id, immediate)
    
    return {"message": "Subscription cancelled successfully"}


# Payment endpoints
@router.get("/payments/{payment_id}", response_model=PaymentRead)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a payment by ID"""
    payment_service = PaymentService(db)
    payment = payment_service.get_payment_by_id(payment_id)
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    # Check authorization
    if payment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this payment"
        )
    
    return payment


@router.get("/users/{user_id}/payments", response_model=List[PaymentRead])
def get_user_payments(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all payments for a user"""
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these payments"
        )
    
    payment_service = PaymentService(db)
    payments = payment_service.get_payments_by_user(user_id)
    return payments


@router.post("/payments/intent", response_model=PaymentIntentResponse)
def create_payment_intent(
    amount: float,
    currency: str = "USD",
    payment_method_types: List[str] = ["card"],
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a payment intent for Stripe integration"""
    # Generate a mock client secret for demonstration
    # In a real implementation, this would call Stripe's API
    from uuid import uuid4
    client_secret = f"pi_{uuid4().hex}_secret_{uuid4().hex}"
    
    return PaymentIntentResponse(
        client_secret=client_secret,
        payment_method_types=payment_method_types,
        amount=amount,
        currency=currency
    )


# Usage tracking endpoints
@router.post("/users/{user_id}/usage", response_model=UsageRecord)
def record_usage(
    user_id: int,
    usage_record: UsageRecordCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Record usage for a user"""
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to record usage for this user"
        )
    
    usage_service = UsageTrackingService(db)
    recorded_usage = usage_service.record_usage(user_id, usage_record)
    return recorded_usage


@router.get("/users/{user_id}/usage", response_model=List[UsageRecord])
def get_user_usage(
    user_id: int,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get usage records for a user"""
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this usage data"
        )
    
    usage_service = UsageTrackingService(db)
    
    # Convert string dates to datetime if provided
    from datetime import datetime
    start_dt = datetime.fromisoformat(start_date) if start_date else datetime.min
    end_dt = datetime.fromisoformat(end_date) if end_date else datetime.utcnow()
    
    usage_records = usage_service.get_usage_for_user(user_id, start_dt, end_dt)
    return usage_records


# Analytics endpoints
@router.get("/analytics", response_model=SubscriptionAnalytics)
def get_subscription_analytics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get subscription analytics (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access analytics"
        )
    
    analytics_service = SubscriptionAnalyticsService(db)
    analytics = analytics_service.get_analytics()
    return analytics


# Entitlements endpoint
@router.get("/users/{user_id}/entitlements")
def get_user_entitlements(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get what a user is entitled to based on their subscription"""
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these entitlements"
        )
    
    subscription_service = SubscriptionService(db)
    entitlements = subscription_service.check_user_entitlements(user_id)
    return entitlements