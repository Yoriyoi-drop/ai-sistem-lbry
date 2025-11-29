"""
Updated Database models for Infinite AI Security Platform with Multi-Tenant Support
Based on B2B SaaS transformation strategy
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Float, Enum, Table, Date, DECIMAL, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from .base import Base


# Enumerations
class RoleEnum(str, enum.Enum):
    """User role enumeration"""
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class ThreatLevel(str, enum.Enum):
    """Threat level enumeration"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ScanStatus(str, enum.Enum):
    """Scan status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentStatus(str, enum.Enum):
    """Agent status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class SubscriptionTier(str, enum.Enum):
    """Subscription tier enumeration"""
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, enum.Enum):
    """Subscription status enumeration"""
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PAST_DUE = "past_due"
    TRIAL = "trial"


class Organization(Base):
    """Organization model for multi-tenant architecture"""
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.STARTER)
    status = Column(String(50), default="trial")  # trial/active/suspended
    created_at = Column(DateTime, default=func.now())
    settings = Column(JSON, default=lambda: {})
    billing_email = Column(String(255))
    stripe_customer_id = Column(String(255))
    max_users = Column(Integer, default=5)  # tier-based limits
    max_scans_per_month = Column(Integer, default=1000)  # tier-based limits
    api_calls_remaining = Column(Integer, default=10000)  # tier-based limits
    api_calls_reset_date = Column(Date, default=lambda: func.current_date() + func.interval('1 month'))

    # Relationships
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    scans = relationship("SecurityScan", back_populates="organization", cascade="all, delete-orphan")
    usage_metrics = relationship("UsageMetric", back_populates="organization", cascade="all, delete-orphan")
    agent_sessions = relationship("AgentSession", back_populates="organization", cascade="all, delete-orphan")
    subscriptions = relationship("OrganizationSubscription", back_populates="organization", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Organization(name={self.name}, tier={self.tier}, status={self.status})>"


class User(Base):
    """User model with multi-tenant support"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True)
    hashed_password = Column(String(255))
    role = Column(Enum(RoleEnum), default=RoleEnum.MEMBER)
    is_active = Column(Boolean, default=True)
    auth_provider = Column(String(50), default='local')  # local/google/github/saml
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="users")
    scans = relationship("SecurityScan", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    agent_sessions = relationship("AgentSession", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email}, organization_id={self.organization_id})>"


class SecurityScan(Base):
    """Security scan model with multi-tenant support"""
    __tablename__ = "scans"  # Changed to "scans" to match the SQL schema

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    repository_url = Column(String(500))
    status = Column(Enum(ScanStatus), default=ScanStatus.PENDING)
    scan_type = Column(String(50), default='full')  # full/incremental/custom
    findings = Column(JSON, default=lambda: {})
    severity_summary = Column(JSON, default=lambda: {})
    scan_cost_credits = Column(DECIMAL(10, 4), default=0.0000)

    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="scans")
    user = relationship("User", back_populates="scans")
    threats = relationship("Threat", back_populates="scan", cascade="all, delete-orphan")
    vulnerabilities = relationship("Vulnerability", back_populates="scan", cascade="all, delete-orphan")

    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)

    def __repr__(self):
        return f"<SecurityScan(id={self.id}, organization_id={self.organization_id}, status={self.status}, target={self.repository_url})>"


class Threat(Base):
    """Detected threat model"""
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    threat_type = Column(String(100), nullable=False)
    severity = Column(Enum(ThreatLevel), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    source = Column(String(500))
    detected_at = Column(DateTime, default=func.now())
    mitigated = Column(Boolean, default=False)
    mitigation_steps = Column(JSON)
    metadata = Column(JSON)

    # Foreign keys
    scan_id = Column(UUID(as_uuid=True), ForeignKey("scans.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    scan = relationship("SecurityScan", back_populates="threats")

    def __repr__(self):
        return f"<Threat(type={self.threat_type}, severity={self.severity}, title={self.title})>"


class Vulnerability(Base):
    """Vulnerability model"""
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cve_id = Column(String(50), index=True)  # CVE identifier if applicable
    title = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(Enum(ThreatLevel), nullable=False)
    cvss_score = Column(Float)
    affected_component = Column(String(255))
    remediation = Column(Text)
    references = Column(JSON)  # List of reference URLs
    status = Column(String(50), default="open")  # open, in_progress, resolved, false_positive

    # Foreign keys
    scan_id = Column(UUID(as_uuid=True), ForeignKey("scans.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    scan = relationship("SecurityScan", back_populates="vulnerabilities")

    def __repr__(self):
        return f"<Vulnerability(cve={self.cve_id}, severity={self.severity}, title={self.title})>"


class UsageMetric(Base):
    """Usage tracking for consumption-based pricing"""
    __tablename__ = "usage_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    metric_type = Column(String(100), nullable=False)  # scans/api_calls/agent_hours
    quantity = Column(Integer, default=0)
    period = Column(Date, nullable=False)  # for monthly billing
    created_at = Column(DateTime, default=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="usage_metrics")

    def __repr__(self):
        return f"<UsageMetric(organization_id={self.organization_id}, metric_type={self.metric_type}, quantity={self.quantity}, period={self.period})>"


class AgentSession(Base):
    """AI Agent session model with multi-tenant support"""
    __tablename__ = "agent_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    agent_type = Column(String(100))
    task_description = Column(Text)
    duration_seconds = Column(Integer, default=0)
    status = Column(String(50), default="running")  # running/completed/failed
    results = Column(JSON, default=lambda: {})
    cost_credits = Column(DECIMAL(10, 4), default=0.0000)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="agent_sessions")
    user = relationship("User", back_populates="agent_sessions")

    def __repr__(self):
        return f"<AgentSession(organization_id={self.organization_id}, agent_type={self.agent_type}, status={self.status})>"


class SubscriptionPlan(Base):
    """Subscription plan model"""
    __tablename__ = "subscription_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    tier = Column(Enum(SubscriptionTier), nullable=False)
    price_monthly = Column(DECIMAL(10, 2), nullable=False)
    features = Column(JSON, default=lambda: [])
    limits = Column(JSON, default=lambda: {})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<SubscriptionPlan(name={self.name}, tier={self.tier}, price={self.price_monthly})>"


class OrganizationSubscription(Base):
    """Organization subscription model"""
    __tablename__ = "organization_subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("subscription_plans.id"), nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    started_at = Column(DateTime, default=func.now())
    ends_at = Column(DateTime)
    trial_ends_at = Column(DateTime)
    auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan")

    def __repr__(self):
        return f"<OrganizationSubscription(organization_id={self.organization_id}, status={self.status})>"


class AuditLog(Base):
    """Audit log for tracking user actions"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String(100), nullable=False)  # e.g., "login", "create_scan", "delete_agent"
    resource_type = Column(String(100))  # e.g., "user", "agent", "scan"
    resource_id = Column(Integer)
    details = Column(JSON)
    ip_address = Column(String(45))  # Support IPv6
    user_agent = Column(String(500))
    timestamp = Column(DateTime, default=func.now())

    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(action={self.action}, resource={self.resource_type}, timestamp={self.timestamp})>"


class LabyrinthConfig(Base):
    """Labyrinth defense configuration"""
    __tablename__ = "labyrinth_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    complexity_level = Column(Integer, default=1)  # 1-10
    route_configs = Column(JSON)  # Labyrinth route configuration
    decoy_nodes = Column(JSON)  # Decoy node configuration
    detection_rules = Column(JSON)  # Detection rules
    is_active = Column(Boolean, default=False)

    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"<LabyrinthConfig(name={self.name}, complexity={self.complexity_level})>"


class APIKey(Base):
    """API Key model with multi-tenant support"""
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    key_hash = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    permissions = Column(JSON, default=lambda: ["read", "write"])
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    last_used_at = Column(DateTime)

    # Relationships
    organization = relationship("Organization")
    user = relationship("User")

    def __repr__(self):
        return f"<APIKey(name={self.name}, organization_id={self.organization_id})>"