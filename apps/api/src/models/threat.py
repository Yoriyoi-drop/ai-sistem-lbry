from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.connection import Base


class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String, unique=True, index=True, nullable=True)  # CVE identifier
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String, default="medium")  # low, medium, high, critical
    cvss_score = Column(String, nullable=True)  # CVSS score if available
    cvss_vector = Column(String, nullable=True)  # CVSS vector string
    cwe_id = Column(String, nullable=True)  # CWE identifier
    status = Column(String, default="new")  # new, confirmed, mitigated, false_positive
    remediation = Column(Text, nullable=True)  # How to fix the vulnerability
    references = Column(JSON, nullable=True)  # Additional references as JSON
    is_active = Column(Boolean, default=True)
    discovered_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    scan_id = Column(Integer, ForeignKey("scans.id"))
    
    # Relationships
    scan = relationship("Scan", back_populates="vulnerabilities")


class ThreatIntelligence(Base):
    __tablename__ = "threat_intelligence"

    id = Column(Integer, primary_key=True, index=True)
    indicator_type = Column(String, nullable=False)  # ip, domain, hash, url
    indicator_value = Column(String, nullable=False)  # The actual indicator
    threat_type = Column(String, nullable=False)  # malware, phishing, c2, etc.
    severity = Column(String, default="medium")  # low, medium, high, critical
    confidence = Column(Integer, default=50)  # Confidence level 0-100
    source = Column(String, nullable=True)  # Source of intelligence
    tags = Column(JSON, nullable=True)  # Tags as JSON array
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # Foreign key to users
    action = Column(String, nullable=False)  # login, logout, create, update, delete, etc.
    resource_type = Column(String, nullable=True)  # user, agent, scan, etc.
    resource_id = Column(Integer, nullable=True)  # ID of the resource
    details = Column(JSON, nullable=True)  # Additional details as JSON
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)