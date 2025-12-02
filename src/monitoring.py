"""
Monitoring and Observability Module
Comprehensive monitoring, logging, and health check system
"""
import asyncio
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import psutil
import os

# Try to import optional monitoring libraries
try:
    from prometheus_client import Counter, Histogram, Gauge, Summary, start_http_server
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    Counter = None
    Histogram = None
    Gauge = None
    Summary = None
    start_http_server = None


class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class Metric:
    """
    Data class for metrics
    """
    name: str
    value: float
    labels: Dict[str, str]
    timestamp: datetime


class EventLogger:
    """
    Event logging system for audit trails and monitoring
    """
    def __init__(self, log_file: str = "events.log"):
        self.logger = logging.getLogger("event_logger")
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_event(self, event_type: str, details: Dict[str, Any], 
                  level: LogLevel = LogLevel.INFO):
        """
        Log an event with details
        """
        message = f"{event_type}: {details}"
        if level == LogLevel.DEBUG:
            self.logger.debug(message)
        elif level == LogLevel.INFO:
            self.logger.info(message)
        elif level == LogLevel.WARNING:
            self.logger.warning(message)
        elif level == LogLevel.ERROR:
            self.logger.error(message)
        elif level == LogLevel.CRITICAL:
            self.logger.critical(message)
    
    def log_security_event(self, event_type: str, user_id: str, 
                          organization_id: str, details: Dict[str, Any]):
        """
        Log a security-related event
        """
        event_details = {
            "event_type": event_type,
            "user_id": user_id,
            "organization_id": organization_id,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details
        }
        
        self.log_event("SECURITY", event_details, LogLevel.INFO)


class MetricsCollector:
    """
    Metrics collection system
    """
    def __init__(self):
        self.metrics: List[Metric] = []
        self.start_time = time.time()
        
        # Initialize Prometheus metrics if available
        if PROMETHEUS_AVAILABLE and Counter is not None:
            # API request metrics
            self.api_requests_total = Counter(
                'api_requests_total',
                'Total API requests',
                ['method', 'endpoint', 'status']
            )

            self.api_request_duration = Histogram(
                'api_request_duration_seconds',
                'API request duration',
                ['method', 'endpoint']
            )

            # System metrics
            self.cpu_usage = Gauge('system_cpu_percent', 'CPU usage percentage')
            self.memory_usage = Gauge('system_memory_percent', 'Memory usage percentage')
            self.disk_usage = Gauge('system_disk_percent', 'Disk usage percentage')

            # Custom business metrics
            self.active_users = Gauge('active_users', 'Number of active users')
            self.active_organizations = Gauge('active_organizations', 'Number of active organizations')
            self.scans_per_minute = Counter('scans_per_minute', 'Scans processed per minute')
            self.security_events_total = Counter('security_events_total', 'Total security events')
        else:
            # Set to None when Prometheus is not available
            self.api_requests_total = None
            self.api_request_duration = None
            self.cpu_usage = None
            self.memory_usage = None
            self.disk_usage = None
            self.active_users = None
            self.active_organizations = None
            self.scans_per_minute = None
            self.security_events_total = None
    
    def record_api_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """
        Record an API request metric
        """
        if PROMETHEUS_AVAILABLE and self.api_requests_total is not None:
            self.api_requests_total.labels(
                method=method,
                endpoint=endpoint,
                status=str(status_code)
            ).inc()

            self.api_request_duration.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)

        # Store locally too
        metric = Metric(
            name="api_request",
            value=duration,
            labels={
                "method": method,
                "endpoint": endpoint,
                "status_code": str(status_code)
            },
            timestamp=datetime.utcnow()
        )
        self.metrics.append(metric)
    
    def record_scan_completion(self):
        """
        Record a completed scan
        """
        if PROMETHEUS_AVAILABLE and self.scans_per_minute is not None:
            self.scans_per_minute.inc()

        metric = Metric(
            name="scan_completed",
            value=1.0,
            labels={},
            timestamp=datetime.utcnow()
        )
        self.metrics.append(metric)

    def record_security_event(self, event_type: str):
        """
        Record a security event
        """
        if PROMETHEUS_AVAILABLE and self.security_events_total is not None:
            self.security_events_total.inc()

        metric = Metric(
            name="security_event",
            value=1.0,
            labels={"type": event_type},
            timestamp=datetime.utcnow()
        )
        self.metrics.append(metric)

    def update_system_metrics(self):
        """
        Update system-level metrics (CPU, memory, disk)
        """
        if PROMETHEUS_AVAILABLE and self.cpu_usage is not None:
            self.cpu_usage.set(psutil.cpu_percent())
            self.memory_usage.set(psutil.virtual_memory().percent)
            self.disk_usage.set(psutil.disk_usage('/').percent)

    def update_business_metrics(self, active_users: int, active_orgs: int):
        """
        Update business-level metrics
        """
        if PROMETHEUS_AVAILABLE and self.active_users is not None:
            self.active_users.set(active_users)
            self.active_organizations.set(active_orgs)
    
    def get_uptime(self) -> float:
        """
        Get system uptime in seconds
        """
        return time.time() - self.start_time
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Get a summary of collected metrics
        """
        # Count recent metrics (last 5 minutes)
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
        recent_metrics = [m for m in self.metrics if m.timestamp > five_minutes_ago]
        
        summary = {
            "total_metrics": len(self.metrics),
            "recent_metrics": len(recent_metrics),
            "uptime_seconds": self.get_uptime(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Count by name
        name_counts = {}
        for metric in recent_metrics:
            name = metric.name
            name_counts[name] = name_counts.get(name, 0) + 1
        
        summary["recent_by_name"] = name_counts
        return summary


class HealthChecker:
    """
    Health check system for monitoring service availability
    """
    def __init__(self):
        self.checks: Dict[str, Callable[[], Dict[str, Any]]] = {}
        self.last_check_results: Dict[str, Dict[str, Any]] = {}
    
    def register_check(self, name: str, check_func: Callable[[], Dict[str, Any]]):
        """
        Register a health check function
        """
        self.checks[name] = check_func
    
    async def run_check(self, name: str) -> Dict[str, Any]:
        """
        Run a specific health check
        """
        if name not in self.checks:
            return {
                "status": "unknown",
                "error": f"Check '{name}' not registered",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        try:
            result = self.checks[name]()
            self.last_check_results[name] = result
            return result
        except Exception as e:
            error_result = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            self.last_check_results[name] = error_result
            return error_result
    
    async def run_all_checks(self) -> Dict[str, Any]:
        """
        Run all registered health checks
        """
        results = {}
        overall_status = "healthy"
        
        for name in self.checks:
            results[name] = await self.run_check(name)
            if results[name]["status"] == "error":
                overall_status = "unhealthy"
        
        return {
            "overall_status": overall_status,
            "checks": results,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_status(self) -> str:
        """
        Get overall health status
        """
        if not self.last_check_results:
            return "unknown"
        
        statuses = [result["status"] for result in self.last_check_results.values()]
        if "error" in statuses:
            return "unhealthy"
        return "healthy"


class AgentMonitor:
    """
    Monitor AI agents and their activities
    """
    def __init__(self):
        self.agent_stats: Dict[str, Dict[str, Any]] = {}
        self.agent_performance: Dict[str, List[Dict[str, Any]]] = {}
        self.heartbeat_times: Dict[str, datetime] = {}
    
    def record_agent_activity(self, agent_id: str, task_type: str, 
                            duration: float, success: bool = True):
        """
        Record an agent's activity
        """
        if agent_id not in self.agent_stats:
            self.agent_stats[agent_id] = {
                "total_tasks": 0,
                "successful_tasks": 0,
                "failed_tasks": 0,
                "total_duration": 0.0,
                "avg_duration": 0.0
            }
        
        stats = self.agent_stats[agent_id]
        stats["total_tasks"] += 1
        
        if success:
            stats["successful_tasks"] += 1
        else:
            stats["failed_tasks"] += 1
        
        stats["total_duration"] += duration
        stats["avg_duration"] = stats["total_duration"] / stats["total_tasks"]
        
        # Store performance record
        if agent_id not in self.agent_performance:
            self.agent_performance[agent_id] = []
        
        self.agent_performance[agent_id].append({
            "task_type": task_type,
            "duration": duration,
            "success": success,
            "timestamp": datetime.utcnow()
        })
        
        # Keep only last 100 records per agent
        if len(self.agent_performance[agent_id]) > 100:
            self.agent_performance[agent_id] = self.agent_performance[agent_id][-100:]
    
    def record_heartbeat(self, agent_id: str):
        """
        Record agent heartbeat
        """
        self.heartbeat_times[agent_id] = datetime.utcnow()
    
    def get_agent_health(self, agent_id: str) -> Dict[str, Any]:
        """
        Get health status for a specific agent
        """
        if agent_id not in self.agent_stats:
            return {
                "agent_id": agent_id,
                "status": "unknown",
                "last_heartbeat": None,
                "stats": None
            }
        
        # Check if agent is alive (heartbeat in last 5 minutes)
        last_heartbeat = self.heartbeat_times.get(agent_id)
        is_alive = (datetime.utcnow() - last_heartbeat) < timedelta(minutes=5) if last_heartbeat else False
        
        return {
            "agent_id": agent_id,
            "status": "alive" if is_alive else "dead",
            "last_heartbeat": last_heartbeat.isoformat() if last_heartbeat else None,
            "stats": self.agent_stats[agent_id]
        }
    
    def get_all_agent_health(self) -> Dict[str, Any]:
        """
        Get health status for all agents
        """
        health_status = {}
        
        for agent_id in self.agent_stats:
            health_status[agent_id] = self.get_agent_health(agent_id)
        
        return {
            "agents": health_status,
            "total_agents": len(health_status),
            "alive_agents": sum(1 for agent in health_status.values() if agent["status"] == "alive"),
            "timestamp": datetime.utcnow().isoformat()
        }


class ThreatMonitor:
    """
    Monitor security threats and events
    """
    def __init__(self):
        self.threat_events: List[Dict[str, Any]] = []
        self.threat_counts: Dict[str, int] = {}
        self.severity_counts: Dict[str, int] = {}
    
    def record_threat(self, threat_type: str, severity: str, 
                     details: Dict[str, Any], organization_id: str = None):
        """
        Record a security threat
        """
        threat_event = {
            "type": threat_type,
            "severity": severity,
            "details": details,
            "organization_id": organization_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.threat_events.append(threat_event)
        
        # Update counts
        self.threat_counts[threat_type] = self.threat_counts.get(threat_type, 0) + 1
        self.severity_counts[severity] = self.severity_counts.get(severity, 0) + 1
        
        # Keep only last 1000 events
        if len(self.threat_events) > 1000:
            self.threat_events = self.threat_events[-1000:]
    
    def get_threat_summary(self) -> Dict[str, Any]:
        """
        Get a summary of threats
        """
        # Count threats in last hour
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_threats = [
            t for t in self.threat_events
            if datetime.fromisoformat(t["timestamp"]) > one_hour_ago
        ]
        
        return {
            "total_threats": len(self.threat_events),
            "recent_threats": len(recent_threats),
            "threat_counts": self.threat_counts,
            "severity_counts": self.severity_counts,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_high_severity_threats(self) -> List[Dict[str, Any]]:
        """
        Get all high or critical severity threats
        """
        high_severity = ["high", "critical"]
        return [
            t for t in self.threat_events
            if t["severity"] in high_severity
        ]


# Global monitoring instances
event_logger = EventLogger()
metrics_collector = MetricsCollector()
health_checker = HealthChecker()
agent_monitor = AgentMonitor()
threat_monitor = ThreatMonitor()