"""
Database models for Infinite AI Security Platform
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Float, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from .base import Base


# Enumerations
class RoleEnum(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "admin"
    USER = "user"
    ANALYST = "analyst"
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


# Association table for many-to-many relationship between roles and permissions
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE')),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE'))
)


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)
    api_key = Column(String(255), unique=True, nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    agents = relationship("Agent", back_populates="owner", cascade="all, delete-orphan")
    scans = relationship("SecurityScan", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"


class Role(Base):
    """Role model for RBAC"""
    __tablename__ = "roles"
    
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    
    # Relationships
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

    def __repr__(self):
        return f"<Role(name={self.name})>"


class Permission(Base):
    """Permission model for RBAC"""
    __tablename__ = "permissions"
    
    name = Column(String(100), unique=True, nullable=False)
    resource = Column(String(100), nullable=False)  # e.g., "agents", "scans", "users"
    action = Column(String(50), nullable=False)  # e.g., "read", "write", "delete"
    description = Column(Text)
    
    # Relationships
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

    def __repr__(self):
        return f"<Permission(name={self.name}, resource={self.resource}, action={self.action})>"


class Agent(Base):
    """AI Agent model"""
    __tablename__ = "agents"
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    agent_type = Column(String(100))  # e.g., "security_scanner", "threat_detector", "labyrinth"
    status = Column(Enum(AgentStatus), default=AgentStatus.INACTIVE)
    configuration = Column(JSON)
    capabilities = Column(JSON)  # List of capabilities
    metrics = Column(JSON)  # Performance metrics
    last_active = Column(DateTime, nullable=True)
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    # Relationships
    owner = relationship("User", back_populates="agents")
    scans = relationship("SecurityScan", back_populates="agent")

    def __repr__(self):
        return f"<Agent(name={self.name}, type={self.agent_type}, status={self.status})>"


class SecurityScan(Base):
    """Security scan model"""
    __tablename__ = "security_scans"
    
    scan_name = Column(String(255), nullable=False)
    target = Column(String(500), nullable=False)  # URL, IP, or identifier
    scan_type = Column(String(100))  # e.g., "vulnerability", "malware", "network"
    status = Column(Enum(ScanStatus), default=ScanStatus.PENDING)
    progress = Column(Integer, default=0)  # 0-100
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    results = Column(JSON)
    summary = Column(Text)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    agent_id = Column(Integer, ForeignKey("agents.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="scans")
    agent = relationship("Agent", back_populates="scans")
    threats = relationship("Threat", back_populates="scan", cascade="all, delete-orphan")
    vulnerabilities = relationship("Vulnerability", back_populates="scan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SecurityScan(name={self.scan_name}, status={self.status}, target={self.target})>"


class Threat(Base):
    """Detected threat model"""
    __tablename__ = "threats"
    
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
    scan_id = Column(Integer, ForeignKey("security_scans.id", ondelete="CASCADE"))
    
    # Relationships
    scan = relationship("SecurityScan", back_populates="threats")

    def __repr__(self):
        return f"<Threat(type={self.threat_type}, severity={self.severity}, title={self.title})>"


class Vulnerability(Base):
    """Vulnerability model"""
    __tablename__ = "vulnerabilities"
    
    cve_id = Column(String(50), nullable=True, index=True)  # CVE identifier if applicable
    title = Column(String(255), nullable=False)
    description = Column(Text)
    severity = Column(Enum(ThreatLevel), nullable=False)
    cvss_score = Column(Float, nullable=True)
    affected_component = Column(String(255))
    remediation = Column(Text)
    references = Column(JSON)  # List of reference URLs
    status = Column(String(50), default="open")  # open, in_progress, resolved, false_positive
    
    # Foreign keys
    scan_id = Column(Integer, ForeignKey("security_scans.id", ondelete="CASCADE"))
    
    # Relationships
    scan = relationship("SecurityScan", back_populates="vulnerabilities")

    def __repr__(self):
        return f"<Vulnerability(cve={self.cve_id}, severity={self.severity}, title={self.title})>"


class Subscription(Base):
    """User subscription model"""
    __tablename__ = "subscriptions"
    
    plan_name = Column(String(100), nullable=False)  # free, basic, pro, enterprise
    status = Column(String(50), default="active")  # active, cancelled, expired
    started_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=True)
    features = Column(JSON)  # List of enabled features
    limits = Column(JSON)  # Usage limits
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    
    # Relationships
    user = relationship("User", back_populates="subscription")

    def __repr__(self):
        return f"<Subscription(plan={self.plan_name}, status={self.status})>"


class AuditLog(Base):
    """Audit log for tracking user actions"""
    __tablename__ = "audit_logs"
    
    action = Column(String(100), nullable=False)  # e.g., "login", "create_scan", "delete_agent"
    resource_type = Column(String(100))  # e.g., "user", "agent", "scan"
    resource_id = Column(Integer, nullable=True)
    details = Column(JSON)
    ip_address = Column(String(45))  # Support IPv6
    user_agent = Column(String(500))
    timestamp = Column(DateTime, default=func.now())
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(action={self.action}, resource={self.resource_type}, timestamp={self.timestamp})>"


class LabyrinthConfig(Base):
    """Labyrinth defense configuration"""
    __tablename__ = "labyrinth_configs"
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    complexity_level = Column(Integer, default=1)  # 1-10
    route_configs = Column(JSON)  # Labyrinth route configuration
    decoy_nodes = Column(JSON)  # Decoy node configuration
    detection_rules = Column(JSON)  # Detection rules
    is_active = Column(Boolean, default=False)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"<LabyrinthConfig(name={self.name}, complexity={self.complexity_level})>"