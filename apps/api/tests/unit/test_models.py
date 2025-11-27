"""
Database model tests

Created: 2025-11-26
"""

import pytest
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from unittest.mock import Mock

from src.database.models import User, Role, Permission, Agent, SecurityScan, Threat, Vulnerability, Subscription, AuditLog, LabyrinthConfig
from src.database.models import RoleEnum, ThreatLevel, ScanStatus, AgentStatus


class TestUserModel:
    """Test suite for User model"""

    def test_user_creation(self):
        """Test creating a new user"""
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password"
        )

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed_password"
        assert user.is_active is True
        assert user.role == RoleEnum.USER
        assert user.is_superuser is False

    def test_user_repr(self):
        """Test user string representation"""
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password"
        )

        expected = "<User(username=testuser, email=test@example.com)>"
        assert repr(user) == expected

    def test_user_role_values(self):
        """Test user role enum values"""
        assert RoleEnum.ADMIN == "admin"
        assert RoleEnum.USER == "user"
        assert RoleEnum.ANALYST == "analyst"
        assert RoleEnum.VIEWER == "viewer"


class TestRoleModel:
    """Test suite for Role model"""

    def test_role_creation(self):
        """Test creating a new role"""
        role = Role(
            name="admin",
            description="Administrator role"
        )

        assert role.name == "admin"
        assert role.description == "Administrator role"

    def test_role_repr(self):
        """Test role string representation"""
        role = Role(name="admin")
        expected = "<Role(name=admin)>"
        assert repr(role) == expected


class TestPermissionModel:
    """Test suite for Permission model"""

    def test_permission_creation(self):
        """Test creating a new permission"""
        permission = Permission(
            name="read_users",
            resource="users",
            action="read",
            description="Can read user information"
        )

        assert permission.name == "read_users"
        assert permission.resource == "users"
        assert permission.action == "read"
        assert permission.description == "Can read user information"

    def test_permission_repr(self):
        """Test permission string representation"""
        permission = Permission(
            name="read_users",
            resource="users",
            action="read"
        )
        expected = "<Permission(name=read_users, resource=users, action=read)>"
        assert repr(permission) == expected


class TestAgentModel:
    """Test suite for Agent model"""

    def test_agent_creation(self):
        """Test creating a new agent"""
        agent = Agent(
            name="Test Agent",
            description="Test agent description",
            agent_type="security_scanner",
            status=AgentStatus.ACTIVE,
            configuration={"scan_depth": "full"},
            capabilities=["vulnerability_scanning", "reporting"],
            metrics={"success_rate": 0.95}
        )

        assert agent.name == "Test Agent"
        assert agent.description == "Test agent description"
        assert agent.agent_type == "security_scanner"
        assert agent.status == AgentStatus.ACTIVE
        assert agent.configuration == {"scan_depth": "full"}
        assert agent.capabilities == ["vulnerability_scanning", "reporting"]
        assert agent.metrics == {"success_rate": 0.95}

    def test_agent_repr(self):
        """Test agent string representation"""
        agent = Agent(
            name="Test Agent",
            agent_type="security_scanner",
            status=AgentStatus.ACTIVE
        )
        expected = "<Agent(name=Test Agent, type=security_scanner, status=active)>"
        assert repr(agent) == expected


class TestSecurityScanModel:
    """Test suite for SecurityScan model"""

    def test_security_scan_creation(self):
        """Test creating a new security scan"""
        scan = SecurityScan(
            scan_name="Vulnerability Scan",
            target="http://example.com",
            scan_type="vulnerability",
            status=ScanStatus.PENDING,
            progress=0,
            results={"vulnerabilities": 5},
            summary="Scan completed"
        )

        assert scan.scan_name == "Vulnerability Scan"
        assert scan.target == "http://example.com"
        assert scan.scan_type == "vulnerability"
        assert scan.status == ScanStatus.PENDING
        assert scan.progress == 0
        assert scan.results == {"vulnerabilities": 5}
        assert scan.summary == "Scan completed"

    def test_security_scan_repr(self):
        """Test security scan string representation"""
        scan = SecurityScan(
            scan_name="Vulnerability Scan",
            status=ScanStatus.PENDING,
            target="http://example.com"
        )
        expected = "<SecurityScan(name=Vulnerability Scan, status=pending, target=http://example.com)>"
        assert repr(scan) == expected


class TestThreatModel:
    """Test suite for Threat model"""

    def test_threat_creation(self):
        """Test creating a new threat"""
        threat = Threat(
            threat_type="SQL Injection",
            severity=ThreatLevel.CRITICAL,
            title="Potential SQL Injection",
            description="Detected potential SQL injection vulnerability",
            source="192.168.1.100",
            mitigated=False,
            mitigation_steps=["update input validation", "apply patch"],
            metadata={"severity_score": 9.8}
        )

        assert threat.threat_type == "SQL Injection"
        assert threat.severity == ThreatLevel.CRITICAL
        assert threat.title == "Potential SQL Injection"
        assert threat.description == "Detected potential SQL injection vulnerability"
        assert threat.source == "192.168.1.100"
        assert threat.mitigated is False
        assert threat.mitigation_steps == ["update input validation", "apply patch"]
        assert threat.metadata == {"severity_score": 9.8}

    def test_threat_repr(self):
        """Test threat string representation"""
        threat = Threat(
            threat_type="SQL Injection",
            severity=ThreatLevel.CRITICAL,
            title="Potential SQL Injection"
        )
        expected = "<Threat(type=SQL Injection, severity=critical, title=Potential SQL Injection)>"
        assert repr(threat) == expected


class TestVulnerabilityModel:
    """Test suite for Vulnerability model"""

    def test_vulnerability_creation(self):
        """Test creating a new vulnerability"""
        vulnerability = Vulnerability(
            cve_id="CVE-2021-44228",
            title="Log4Shell",
            description="Remote code execution vulnerability in Log4j",
            severity=ThreatLevel.CRITICAL,
            cvss_score=9.8,
            affected_component="Log4j 2.x",
            remediation="Upgrade to version 2.15.0 or later",
            references=["https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44228"],
            status="open"
        )

        assert vulnerability.cve_id == "CVE-2021-44228"
        assert vulnerability.title == "Log4Shell"
        assert vulnerability.description == "Remote code execution vulnerability in Log4j"
        assert vulnerability.severity == ThreatLevel.CRITICAL
        assert vulnerability.cvss_score == 9.8
        assert vulnerability.affected_component == "Log4j 2.x"
        assert vulnerability.remediation == "Upgrade to version 2.15.0 or later"
        assert vulnerability.references == ["https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44228"]
        assert vulnerability.status == "open"

    def test_vulnerability_repr(self):
        """Test vulnerability string representation"""
        vulnerability = Vulnerability(
            cve_id="CVE-2021-44228",
            severity=ThreatLevel.CRITICAL,
            title="Log4Shell"
        )
        expected = "<Vulnerability(cve=CVE-2021-44228, severity=critical, title=Log4Shell)>"
        assert repr(vulnerability) == expected


class TestSubscriptionModel:
    """Test suite for Subscription model"""

    def test_subscription_creation(self):
        """Test creating a new subscription"""
        subscription = Subscription(
            plan_name="pro",
            status="active",
            features=["priority_support", "advanced_scans"],
            limits={"scans_per_month": 1000, "data_retention_days": 90}
        )

        assert subscription.plan_name == "pro"
        assert subscription.status == "active"
        assert subscription.features == ["priority_support", "advanced_scans"]
        assert subscription.limits == {"scans_per_month": 1000, "data_retention_days": 90}

    def test_subscription_repr(self):
        """Test subscription string representation"""
        subscription = Subscription(
            plan_name="pro",
            status="active"
        )
        expected = "<Subscription(plan=pro, status=active)>"
        assert repr(subscription) == expected


class TestAuditLogModel:
    """Test suite for AuditLog model"""

    def test_audit_log_creation(self):
        """Test creating a new audit log"""
        audit_log = AuditLog(
            action="user_login",
            resource_type="user",
            resource_id=1,
            details={"ip": "192.168.1.100", "success": True},
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0..."
        )

        assert audit_log.action == "user_login"
        assert audit_log.resource_type == "user"
        assert audit_log.resource_id == 1
        assert audit_log.details == {"ip": "192.168.1.100", "success": True}
        assert audit_log.ip_address == "192.168.1.100"
        assert audit_log.user_agent == "Mozilla/5.0..."

    def test_audit_log_repr(self):
        """Test audit log string representation"""
        audit_log = AuditLog(
            action="user_login",
            resource_type="user",
            timestamp=datetime(2024, 1, 1, 12, 0, 0)
        )
        expected = "<AuditLog(action=user_login, resource=user, timestamp=2024-01-01 12:00:00)>"
        assert repr(audit_log) == expected


class TestLabyrinthConfigModel:
    """Test suite for LabyrinthConfig model"""

    def test_labyrinth_config_creation(self):
        """Test creating a new labyrinth config"""
        config = LabyrinthConfig(
            name="Production Labyrinth",
            description="Main labyrinth configuration for production",
            complexity_level=7,
            route_configs={"primary_routes": ["route1", "route2"]},
            decoy_nodes={"node_type_a": 5, "node_type_b": 3},
            detection_rules={"rule1": "active", "rule2": "inactive"},
            is_active=True
        )

        assert config.name == "Production Labyrinth"
        assert config.description == "Main labyrinth configuration for production"
        assert config.complexity_level == 7
        assert config.route_configs == {"primary_routes": ["route1", "route2"]}
        assert config.decoy_nodes == {"node_type_a": 5, "node_type_b": 3}
        assert config.detection_rules == {"rule1": "active", "rule2": "inactive"}
        assert config.is_active is True

    def test_labyrinth_config_repr(self):
        """Test labyrinth config string representation"""
        config = LabyrinthConfig(
            name="Production Labyrinth",
            complexity=7
        )
        expected = "<LabyrinthConfig(name=Production Labyrinth, complexity=7)>"
        assert repr(config) == expected
