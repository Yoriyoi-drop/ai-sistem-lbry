from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum


class SubscriptionTier(str, Enum):
    FREE = "free"
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class BillingCycle(str, Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class SupportLevel(str, Enum):
    COMMUNITY = "community"
    EMAIL = "email"
    PHONE = "phone"


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    subscription: Optional['SubscriptionRead'] = None

    class Config:
        from_attributes = True


# Subscription plan schemas
class SubscriptionPlanBase(BaseModel):
    name: str
    tier: SubscriptionTier
    description: Optional[str] = None
    price: float
    billing_cycle: BillingCycle
    features: Optional[str] = None  # JSON string of features
    max_agents: int
    scan_limit: int
    api_rate_limit: int
    support_level: SupportLevel


class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass


class SubscriptionPlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    features: Optional[str] = None
    max_agents: Optional[int] = None
    scan_limit: Optional[int] = None
    api_rate_limit: Optional[int] = None
    support_level: Optional[SupportLevel] = None
    is_active: Optional[bool] = None


class SubscriptionPlan(SubscriptionPlanBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Subscription schemas
class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PAST_DUE = "past_due"


class SubscriptionCreate(BaseModel):
    plan_id: int
    trial_days: Optional[int] = 0


class SubscriptionUpdate(BaseModel):
    plan_id: Optional[int] = None
    cancel_at_period_end: Optional[bool] = None


class SubscriptionRead(BaseModel):
    id: int
    plan_id: int
    status: SubscriptionStatus
    current_period_start: datetime
    current_period_end: datetime
    trial_start: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    cancel_at_period_end: bool
    cancelled_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    plan: SubscriptionPlan

    class Config:
        from_attributes = True


# Payment schemas
class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentCreate(BaseModel):
    user_id: int
    subscription_id: int
    amount: float
    currency: str = "USD"
    payment_method: Optional[str] = None


class PaymentRead(BaseModel):
    id: int
    user_id: int
    subscription_id: int
    amount: float
    currency: str
    status: PaymentStatus
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    receipt_url: Optional[str] = None
    processed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Subscription management schemas
class SubscriptionChangeRequest(BaseModel):
    new_plan_id: int
    prorate: bool = True  # Whether to prorate the change


class SubscriptionCancellationRequest(BaseModel):
    reason: Optional[str] = None


class BillingInfo(BaseModel):
    current_period_start: datetime
    current_period_end: datetime
    next_billing_date: datetime
    amount_due: float
    currency: str = "USD"


# Usage tracking schemas
class UsageRecordCreate(BaseModel):
    resource_type: str
    resource_id: Optional[str] = None
    quantity: int = 1


class UsageRecord(BaseModel):
    id: int
    user_id: int
    resource_type: str
    resource_id: Optional[str] = None
    quantity: int
    recorded_at: datetime

    class Config:
        from_attributes = True


# Response schemas
class SubscriptionResponse(BaseModel):
    user: User
    subscription: SubscriptionRead
    billing_info: Optional[BillingInfo] = None


class PaymentIntentResponse(BaseModel):
    client_secret: str
    payment_method_types: List[str] = ["card"]
    amount: float
    currency: str


# Admin schemas
class SubscriptionAnalytics(BaseModel):
    total_subscribers: int
    active_subscribers: int
    churn_rate: float
    mrr: float  # Monthly Recurring Revenue
    arr: float  # Annual Recurring Revenue
    subscription_tiers: dict


# Stripe integration schemas
class StripeWebhookPayload(BaseModel):
    type: str
    data: dict
    id: str
    created: int
    livemode: bool
    pending_webhooks: int