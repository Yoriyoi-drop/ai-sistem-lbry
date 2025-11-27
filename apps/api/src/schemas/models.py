"""
Pydantic schema definitions for Infinite AI Security Platform
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    SUPERUSER = "superuser"


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    is_superuser: bool = False


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AgentType(str, Enum):
    SCANNER = "scanner"
    ANALYZER = "analyzer"
    DEFENDER = "defender"
    DETECTOR = "detector"
    HONEYPOT = "honeypot"


class AgentStatus(str, Enum):
    INACTIVE = "inactive"
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"


class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    agent_type: AgentType
    configuration: Optional[Dict[str, Any]] = None
    is_active: bool = True
    heartbeat_interval: int = 30  # seconds


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    agent_type: Optional[AgentType] = None
    configuration: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    heartbeat_interval: Optional[int] = None


class AgentResponse(AgentBase):
    id: int
    status: AgentStatus = AgentStatus.INACTIVE
    last_heartbeat: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        from_attributes = True


class ScanType(str, Enum):
    VULNERABILITY = "vulnerability"
    COMPLIANCE = "compliance"
    PENETRATION = "penetration"
    NETWORK = "network"
    WEB_APPLICATION = "web_application"
    MOBILE = "mobile"
    SOURCE_CODE = "source_code"


class ScanStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ScanBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    scan_type: ScanType
    target: str = Field(..., min_length=1)  # URL, IP, file path, etc.
    parameters: Optional[Dict[str, Any]] = None
    is_active: bool = True


class ScanCreate(ScanBase):
    agent_id: int  # Agent to run this scan


class ScanUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    scan_type: Optional[ScanType] = None
    target: Optional[str] = Field(None, min_length=1)
    parameters: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    status: Optional[ScanStatus] = None


class ScanResponse(ScanBase):
    id: int
    status: ScanStatus = ScanStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    results: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    owner_id: int
    agent_id: int

    class Config:
        from_attributes = True


class VulnerabilitySeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    CATASTROPHIC = "catastrophic"


class VulnerabilityBase(BaseModel):
    name: str
    description: Optional[str] = None
    severity: VulnerabilitySeverity
    cve_id: Optional[str] = None
    cwe_id: Optional[str] = None
    cvss_score: Optional[float] = None
    remediation: Optional[str] = None
    is_confirmed: bool = False
    is_false_positive: bool = False


class VulnerabilityCreate(VulnerabilityBase):
    scan_id: int


class VulnerabilityUpdate(BaseModel):
    description: Optional[str] = None
    severity: Optional[VulnerabilitySeverity] = None
    cve_id: Optional[str] = None
    cwe_id: Optional[str] = None
    cvss_score: Optional[float] = None
    remediation: Optional[str] = None
    is_confirmed: Optional[bool] = None
    is_false_positive: Optional[bool] = None


class VulnerabilityResponse(VulnerabilityBase):
    id: int
    scan_id: int
    discovered_at: datetime
    confirmed_at: Optional[datetime] = None
    is_active: bool = True

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    user_id: int
    username: str
    role: UserRole