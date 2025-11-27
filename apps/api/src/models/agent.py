from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.connection import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    agent_type = Column(String, nullable=False)  # scanner, analyzer, defender, etc.
    configuration = Column(Text, nullable=True)  # JSON configuration as string
    status = Column(String, default="inactive")  # inactive, active, paused, error
    is_active = Column(Boolean, default=True)
    last_heartbeat = Column(DateTime, nullable=True)
    last_execution = Column(DateTime, nullable=True)
    tasks_completed = Column(Integer, default=0)
    efficiency = Column(Integer, default=0)  # percentage
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="agents")
    scans = relationship("Scan", back_populates="agent")


# Agent log table for tracking agent activities
class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    level = Column(String, default="INFO")  # INFO, WARNING, ERROR, DEBUG
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    agent = relationship("Agent", back_populates="logs")


# Add relationship to Agent model
Agent.logs = relationship("AgentLog", back_populates="agent")