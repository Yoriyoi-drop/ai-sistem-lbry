"""
Database models for the Infinite AI Security platform
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class AgentTeam(str, enum.Enum):
    TEAM_A = "A"
    TEAM_B = "B"
    TEAM_C = "C"


class AgentStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default=UserRole.USER.value)  # user, admin, superadmin
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    sessions = relationship("Session", back_populates="user")
    api_keys = relationship("APIKey", back_populates="user")


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    status = Column(String, default=AgentStatus.ACTIVE.value)  # active, inactive, maintenance
    team = Column(String, default=AgentTeam.TEAM_A.value)  # A, B, C
    created_at = Column(DateTime, default=func.now())
    last_heartbeat = Column(DateTime, default=func.now())
    configuration = Column(JSON)  # Agent-specific configuration

    # Relationships
    workflows = relationship("Workflow", secondary="workflow_agents", back_populates="agents")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    last_accessed = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User", back_populates="sessions")


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="api_keys")


class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    definition = Column(JSON)  # Workflow definition as JSON
    status = Column(String, default="active")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))

    # Relationships
    agents = relationship("Agent", secondary="workflow_agents", back_populates="workflows")


class WorkflowAgent(Base):
    __tablename__ = "workflow_agents"

    workflow_id = Column(Integer, ForeignKey("workflows.id"), primary_key=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), primary_key=True)


class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="pending")  # pending, running, completed, failed
    scan_type = Column(String, default="security")  # security, vulnerability, compliance
    target = Column(String, nullable=False)  # file path, URL, or code snippet
    results = Column(JSON)  # Scan results as JSON
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))

    # Relationships
    user = relationship("User")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    severity = Column(String, default="medium")  # low, medium, high, critical
    status = Column(String, default="open")  # open, in_progress, resolved, closed
    created_at = Column(DateTime, default=func.now())
    resolved_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    assigned_to = Column(Integer, ForeignKey("users.id"))

    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    assignee = relationship("User", foreign_keys=[assigned_to])


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_name = Column(String, nullable=False)  # basic, pro, enterprise
    status = Column(String, default="active")  # active, inactive, cancelled, expired
    stripe_subscription_id = Column(String)  # Stripe subscription ID
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)  # login, logout, create, update, delete
    resource = Column(String, nullable=False)  # users, agents, workflows, etc.
    resource_id = Column(Integer, nullable=True)
    details = Column(JSON)  # Additional details as JSON
    ip_address = Column(String)
    user_agent = Column(String)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    user = relationship("User")


class AgentStatusLog(Base):
    __tablename__ = "agent_status_logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    status = Column(String, nullable=False)  # active, inactive, error
    message = Column(Text)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    agent = relationship("Agent")