from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.connection import Base


class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    scan_type = Column(String, nullable=False)  # vulnerability, compliance, penetration, etc.
    target = Column(String, nullable=False)  # target URL, IP, file, etc.
    parameters = Column(JSON, nullable=True)  # scan parameters as JSON
    status = Column(String, default="pending")  # pending, running, completed, failed, cancelled
    results = Column(JSON, nullable=True)  # scan results as JSON
    is_active = Column(Boolean, default=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="scans")
    agent_id = Column(Integer, ForeignKey("agents.id"))
    agent = relationship("Agent", back_populates="scans")
    vulnerabilities = relationship("Vulnerability", back_populates="scan")


# Vulnerability model to store scan findings
class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String, unique=True, nullable=True)  # CVE identifier if available
    name = Column(String, nullable=False)  # vulnerability name
    description = Column(Text, nullable=True)  # vulnerability description
    severity = Column(String, default="medium")  # low, medium, high, critical
    cvss_score = Column(String, nullable=True)  # CVSS score if available
    cwe_id = Column(String, nullable=True)  # CWE identifier
    status = Column(String, default="new")  # new, confirmed, mitigated, false_positive
    remediation = Column(Text, nullable=True)  # suggested remediation steps
    references = Column(JSON, nullable=True)  # additional references as JSON
    is_active = Column(Boolean, default=True)
    discovered_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    scan_id = Column(Integer, ForeignKey("scans.id"))
    scan = relationship("Scan", back_populates="vulnerabilities")


# Add relationships to other models
User.scans = relationship("Scan", back_populates="owner")
Agent.scans = relationship("Scan", back_populates="agent")
Scan.vulnerabilities = relationship("Vulnerability", back_populates="scan")