"""
API Schemas Module
Pydantic schemas for API requests and responses
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


# Enum definitions
class RoleEnum(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class SubscriptionTier(str, Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class ThreatLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ScanStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# Request Schemas
class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    role: Optional[RoleEnum] = RoleEnum.MEMBER
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    role: Optional[RoleEnum] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    is_active: Optional[bool] = None


class OrganizationCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    owner_email: EmailStr
    owner_password: str = Field(..., min_length=8)
    billing_email: Optional[EmailStr] = None
    tier: Optional[SubscriptionTier] = SubscriptionTier.STARTER


class OrganizationUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    billing_email: Optional[EmailStr] = None
    tier: Optional[SubscriptionTier] = None


class ScanCreateRequest(BaseModel):
    repository_url: str
    scan_type: str = "full"
    description: Optional[str] = None


class AgentTaskRequest(BaseModel):
    agent_type: str
    task_description: str
    parameters: Optional[Dict[str, Any]] = {}


class SecurityAnalysisRequest(BaseModel):
    content: str
    analysis_type: str = "comprehensive"  # comprehensive, prompt_injection, jailbreak, malicious_code, sensitive_data
    context: Optional[Dict[str, Any]] = {}


class APIKeyCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    permissions: Optional[List[str]] = ["read"]


# Response Schemas
class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: Optional[str]
    role: RoleEnum
    is_active: bool
    organization_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrganizationResponse(BaseModel):
    id: uuid.UUID
    name: str
    tier: SubscriptionTier
    status: str
    created_at: datetime
    max_users: int
    max_scans_per_month: int
    api_calls_remaining: int
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user_info: Dict[str, Any]
    rate_limits: Optional[Dict[str, Any]] = None


class ScanResponse(BaseModel):
    id: uuid.UUID
    organization_id: uuid.UUID
    repository_url: str
    status: ScanStatus
    scan_type: str
    findings: Dict[str, Any]
    severity_summary: Dict[str, Any]
    created_by: uuid.UUID
    created_at: datetime
    completed_at: Optional[datetime]
    scan_cost_credits: float
    
    class Config:
        from_attributes = True


class AgentResponse(BaseModel):
    success: bool
    result: Optional[Dict[str, Any]]
    error: Optional[str]
    processing_time: Optional[float]
    agent_type: str


class ThreatDetectionResponse(BaseModel):
    is_malicious: bool
    severity: str
    confidence: float
    findings: List[Dict[str, Any]]
    matched_patterns: List[str]
    analysis_time: datetime


class UsageMetricResponse(BaseModel):
    organization_id: uuid.UUID
    metric_type: str
    quantity: int
    period: str  # YYYY-MM
    created_at: datetime


class SubscriptionResponse(BaseModel):
    organization_id: uuid.UUID
    current_tier: SubscriptionTier
    status: str
    started_at: datetime
    ends_at: Optional[datetime]
    trial_ends_at: Optional[datetime]
    auto_renew: bool
    plan_details: Dict[str, Any]


class RateLimitResponse(BaseModel):
    tier: str
    user_rate_limit: int
    org_rate_limit: int
    user_requests_remaining: int
    org_requests_remaining: int
    reset_time: int


class APIKeyResponse(BaseModel):
    key_id: str
    name: str
    permissions: List[str]
    created_at: datetime
    last_used_at: Optional[datetime]
    is_active: bool


# Generic Response Schemas
class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    success: bool
    error: str
    detail: Optional[str] = None
    timestamp: datetime


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int


# AI Agent Specific Schemas
class AgentMessageRequest(BaseModel):
    to_agent: str
    intent: str
    payload: Dict[str, Any]
    priority: int = 1  # 1-5, with 5 being highest priority


class AgentMessageResponse(BaseModel):
    success: bool
    message_id: str
    result: Optional[Dict[str, Any]]
    error: Optional[str]
    status: str


class TaskExecutionRequest(BaseModel):
    task_definition: Dict[str, Any]
    timeout: int = 300  # 5 minutes default timeout
    priority: int = 1  # 1-5 priority


class TaskExecutionResponse(BaseModel):
    task_id: str
    success: bool
    results: List[Dict[str, Any]]
    status: str
    execution_time: Optional[float]


# Security Engine Specific Schemas
class SecurityEngineRequest(BaseModel):
    input_text: str
    analysis_types: List[str] = ["prompt_injection", "jailbreak", "malicious_code"]
    context: Optional[Dict[str, Any]] = {}


class SecurityEngineResponse(BaseModel):
    input_text_summary: str
    analysis_results: Dict[str, Any]
    overall_threat_level: str
    threat_score: float
    is_allowed: bool
    processed_output: Optional[str] = None
    timestamp: datetime