# 📊 NEXAFORGE - PHASE 7: MONITORING & OBSERVABILITY (L10)

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
import time
import uuid
import threading
import asyncio
from enum import Enum
import psutil
import GPUtil
from pathlib import Path

class AlertSeverity(Enum):
    """Severity levels for alerts"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class MetricType(Enum):
    """Types of metrics collected"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

@dataclass
class SystemMetrics:
    """Represents system metrics"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, float]
    gpu_usage: Optional[Dict[str, float]] = None

@dataclass
class ServiceMetrics:
    """Represents service metrics"""
    service_name: str
    timestamp: datetime
    requests_per_second: float
    error_rate: float
    latency_ms: float
    active_connections: int
    queue_size: int

@dataclass
class AgentMetrics:
    """Represents agent-specific metrics"""
    agent_id: str
    timestamp: datetime
    tasks_completed: int
    tasks_failed: int
    average_task_time: float
    memory_usage_mb: float

class Alert:
    """Represents an alert in the system"""
    def __init__(self, name: str, severity: AlertSeverity, message: str, 
                 service: str = "system", metadata: Dict[str, Any] = None):
        self.id = f"alert-{uuid.uuid4().hex[:8]}"
        self.name = name
        self.severity = severity
        self.message = message
        self.service = service
        self.timestamp = datetime.now()
        self.resolved = False
        self.metadata = metadata or {}
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "severity": self.severity.value,
            "message": self.message,
            "service": self.service,
            "timestamp": self.timestamp.isoformat(),
            "resolved": self.resolved,
            "metadata": self.metadata
        }

class MetricsCollector:
    """Collects various system and service metrics"""
    
    def __init__(self):
        self.system_metrics_history = []
        self.service_metrics_history = []
        self.agent_metrics_history = []
        self.max_history = 1000  # Keep last 1000 metrics
        self.collection_interval = 5  # seconds
        self.is_collecting = False
        self.collection_thread = None
    
    def start_collection(self):
        """Start metrics collection in a background thread"""
        if self.is_collecting:
            return
        
        self.is_collecting = True
        self.collection_thread = threading.Thread(target=self._collection_loop)
        self.collection_thread.daemon = True
        self.collection_thread.start()
        print("📊 Metrics collection started")
    
    def stop_collection(self):
        """Stop metrics collection"""
        self.is_collecting = False
        if self.collection_thread:
            self.collection_thread.join()
        print("📊 Metrics collection stopped")
    
    def _collection_loop(self):
        """Main collection loop running in background thread"""
        while self.is_collecting:
            try:
                # Collect system metrics
                system_metrics = self._collect_system_metrics()
                self.system_metrics_history.append(system_metrics)
                
                # Collect service metrics (simulated)
                service_metrics = self._collect_service_metrics()
                self.service_metrics_history.append(service_metrics)
                
                # Collect agent metrics (simulated)
                agent_metrics = self._collect_agent_metrics()
                self.agent_metrics_history.append(agent_metrics)
                
                # Maintain history size
                self._trim_history()
                
            except Exception as e:
                print(f"⚠️ Error in metrics collection: {e}")
            
            time.sleep(self.collection_interval)
    
    def _collect_system_metrics(self) -> SystemMetrics:
        """Collect system-level metrics"""
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Disk usage
        disk_usage = psutil.disk_usage('/').percent
        
        # Network I/O
        net_io = psutil.net_io_counters()
        network_io = {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }
        
        # GPU usage if available
        gpu_info = None
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]  # Use first GPU
            gpu_info = {
                "id": gpu.id,
                "name": gpu.name,
                "load": gpu.load * 100,
                "memory_util": gpu.memoryUtil * 100,
                "temperature": gpu.temperature
            }
        
        return SystemMetrics(
            timestamp=datetime.now(),
            cpu_usage=cpu_percent,
            memory_usage=memory_percent,
            disk_usage=disk_usage,
            network_io=network_io,
            gpu_usage=gpu_info
        )
    
    def _collect_service_metrics(self) -> ServiceMetrics:
        """Collect service-level metrics (simulated)"""
        import random
        
        return ServiceMetrics(
            service_name="nexaforge-api",
            timestamp=datetime.now(),
            requests_per_second=random.uniform(10, 100),
            error_rate=random.uniform(0, 5) / 100,  # 0-5% error rate
            latency_ms=random.uniform(50, 500),
            active_connections=random.randint(1, 50),
            queue_size=random.randint(0, 20)
        )
    
    def _collect_agent_metrics(self) -> AgentMetrics:
        """Collect agent-specific metrics (simulated)"""
        import random
        
        return AgentMetrics(
            agent_id=f"agent-{random.randint(1000, 9999)}",
            timestamp=datetime.now(),
            tasks_completed=random.randint(0, 100),
            tasks_failed=random.randint(0, 10),
            average_task_time=random.uniform(0.1, 5.0),
            memory_usage_mb=random.uniform(100, 1000)
        )
    
    def _trim_history(self):
        """Trim history to maintain max size"""
        if len(self.system_metrics_history) > self.max_history:
            self.system_metrics_history = self.system_metrics_history[-self.max_history:]
        if len(self.service_metrics_history) > self.max_history:
            self.service_metrics_history = self.service_metrics_history[-self.max_history:]
        if len(self.agent_metrics_history) > self.max_history:
            self.agent_metrics_history = self.agent_metrics_history[-self.max_history:]
    
    def get_recent_system_metrics(self, limit: int = 10) -> List[SystemMetrics]:
        """Get recent system metrics"""
        return self.system_metrics_history[-limit:]
    
    def get_recent_service_metrics(self, limit: int = 10) -> List[ServiceMetrics]:
        """Get recent service metrics"""
        return self.service_metrics_history[-limit:]
    
    def get_recent_agent_metrics(self, limit: int = 10) -> List[AgentMetrics]:
        """Get recent agent metrics"""
        return self.agent_metrics_history[-limit:]

class AlertManager:
    """Manages alerts and alerting rules"""
    
    def __init__(self):
        self.active_alerts = []
        self.resolved_alerts = []
        self.rules = []
        self.is_monitoring = False
        self.monitoring_thread = None
        self.metrics_collector = MetricsCollector()
        
        # Add default alerting rules
        self._add_default_rules()
    
    def _add_default_rules(self):
        """Add default alerting rules"""
        # High CPU usage alert
        self.add_rule(
            name="high_cpu_usage",
            condition=lambda metrics: metrics.cpu_usage > 80,
            severity=AlertSeverity.HIGH,
            message="CPU usage is above 80%",
            service="system"
        )
        
        # High memory usage alert
        self.add_rule(
            name="high_memory_usage",
            condition=lambda metrics: metrics.memory_usage > 85,
            severity=AlertSeverity.HIGH,
            message="Memory usage is above 85%",
            service="system"
        )
        
        # High error rate alert
        self.add_rule(
            name="high_error_rate",
            condition=lambda metrics: metrics.error_rate > 0.05,  # > 5%
            severity=AlertSeverity.CRITICAL,
            message="Service error rate is above 5%",
            service="api"
        )
        
        # High latency alert
        self.add_rule(
            name="high_latency",
            condition=lambda metrics: metrics.latency_ms > 1000,  # > 1 second
            severity=AlertSeverity.MEDIUM,
            message="Service latency is above 1000ms",
            service="api"
        )
    
    def add_rule(self, name: str, condition, severity: AlertSeverity, 
                 message: str, service: str):
        """Add an alerting rule"""
        rule = {
            "name": name,
            "condition": condition,
            "severity": severity,
            "message": message,
            "service": service
        }
        self.rules.append(rule)
    
    def start_monitoring(self):
        """Start monitoring and alerting in background"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        
        # Start metrics collection
        self.metrics_collector.start_collection()
        
        print("🚨 Alert monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring and alerting"""
        self.is_monitoring = False
        self.metrics_collector.stop_collection()
        if self.monitoring_thread:
            self.monitoring_thread.join()
        print("🚨 Alert monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop running in background"""
        while self.is_monitoring:
            try:
                # Check system metrics against rules
                recent_system_metrics = self.metrics_collector.get_recent_system_metrics(1)
                if recent_system_metrics:
                    for rule in self.rules:
                        if rule["service"] == "system":
                            if rule["condition"](recent_system_metrics[0]):
                                self._create_alert(
                                    rule["name"], 
                                    rule["severity"], 
                                    rule["message"],
                                    rule["service"]
                                )
                
                # Check service metrics against rules
                recent_service_metrics = self.metrics_collector.get_recent_service_metrics(1)
                if recent_service_metrics:
                    for rule in self.rules:
                        if rule["service"] == "api":
                            if rule["condition"](recent_service_metrics[0]):
                                self._create_alert(
                                    rule["name"], 
                                    rule["severity"], 
                                    rule["message"],
                                    rule["service"]
                                )
                
            except Exception as e:
                print(f"⚠️ Error in alert monitoring: {e}")
            
            time.sleep(10)  # Check every 10 seconds
    
    def _create_alert(self, name: str, severity: AlertSeverity, message: str, service: str):
        """Create a new alert"""
        alert = Alert(name, severity, message, service)
        
        # Check if alert with same name is already active
        for existing in self.active_alerts:
            if existing.name == name and not existing.resolved:
                return  # Don't create duplicate active alerts
        
        self.active_alerts.append(alert)
        print(f"🚨 ALERT: {alert.severity.value.upper()} - {alert.message}")
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get all active alerts"""
        return [alert.to_dict() for alert in self.active_alerts if not alert.resolved]
    
    def get_resolved_alerts(self) -> List[Dict[str, Any]]:
        """Get all resolved alerts"""
        return [alert.to_dict() for alert in self.resolved_alerts]
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an active alert"""
        for i, alert in enumerate(self.active_alerts):
            if alert.id == alert_id and not alert.resolved:
                alert.resolved = True
                resolved_alert = self.active_alerts.pop(i)
                self.resolved_alerts.append(resolved_alert)
                return True
        return False
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary of alerts by severity"""
        summary = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "total_active": 0
        }
        
        for alert in self.active_alerts:
            if not alert.resolved:
                summary[alert.severity.value] += 1
                summary["total_active"] += 1
        
        return summary

class LogCollector:
    """Collects and stores logs for observability"""
    
    def __init__(self, storage_path: str = "./logs"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.log_file = self.storage_path / "system.log"
        
    def write_log(self, level: str, service: str, message: str, 
                  metadata: Dict[str, Any] = None):
        """Write a log entry"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level.upper(),
            "service": service,
            "message": message,
            "metadata": metadata or {}
        }
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def get_recent_logs(self, count: int = 50) -> List[Dict[str, Any]]:
        """Get recent log entries"""
        if not self.log_file.exists():
            return []
        
        with open(self.log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        logs = []
        for line in lines[-count:]:
            try:
                log = json.loads(line.strip())
                logs.append(log)
            except json.JSONDecodeError:
                continue
        
        return logs[::-1]  # Return in reverse chronological order
    
    def search_logs(self, query: str = "", level: str = "", service: str = "") -> List[Dict[str, Any]]:
        """Search logs with filters"""
        if not self.log_file.exists():
            return []
        
        with open(self.log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        logs = []
        for line in lines:
            try:
                log = json.loads(line.strip())
                
                # Apply filters
                if query and query.lower() not in log["message"].lower():
                    continue
                if level and log["level"].lower() != level.lower():
                    continue
                if service and log["service"].lower() != service.lower():
                    continue
                
                logs.append(log)
            except json.JSONDecodeError:
                continue
        
        # Return most recent first
        return logs[::-1]

class MonitoringDashboard:
    """Provides dashboard data for monitoring systems"""
    
    def __init__(self):
        self.alert_manager = AlertManager()
        self.log_collector = LogCollector()
        self.metrics_collector = MetricsCollector()
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Get system overview metrics"""
        recent_system_metrics = self.metrics_collector.get_recent_system_metrics(1)
        recent_service_metrics = self.metrics_collector.get_recent_service_metrics(1)
        
        system_data = recent_system_metrics[0] if recent_system_metrics else None
        service_data = recent_service_metrics[0] if recent_service_metrics else None
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_usage": system_data.cpu_usage if system_data else 0,
                "memory_usage": system_data.memory_usage if system_data else 0,
                "disk_usage": system_data.disk_usage if system_data else 0,
                "gpu_usage": system_data.gpu_usage if system_data and system_data.gpu_usage else None
            } if system_data else {},
            "service": {
                "requests_per_second": service_data.requests_per_second if service_data else 0,
                "error_rate": service_data.error_rate if service_data else 0,
                "latency_ms": service_data.latency_ms if service_data else 0,
                "active_connections": service_data.active_connections if service_data else 0
            } if service_data else {},
            "alerts": self.alert_manager.get_alert_summary(),
            "log_count": len(self.log_collector.get_recent_logs(100))
        }
    
    def get_service_health(self, service_name: str) -> Dict[str, Any]:
        """Get health metrics for a specific service"""
        recent_metrics = self.metrics_collector.get_recent_service_metrics(10)
        
        # Filter metrics for specific service
        service_metrics = [m for m in recent_metrics if m.service_name == service_name]
        
        if not service_metrics:
            return {
                "service": service_name,
                "status": "unknown",
                "metrics": {}
            }
        
        # Calculate averages
        avg_rps = sum(m.requests_per_second for m in service_metrics) / len(service_metrics)
        avg_error_rate = sum(m.error_rate for m in service_metrics) / len(service_metrics)
        avg_latency = sum(m.latency_ms for m in service_metrics) / len(service_metrics)
        
        # Determine status based on metrics
        status = "healthy"
        if avg_error_rate > 0.05 or avg_latency > 2000:  # >5% error rate or >2s latency
            status = "critical"
        elif avg_error_rate > 0.02 or avg_latency > 1000:  # >2% error rate or >1s latency
            status = "warning"
        
        return {
            "service": service_name,
            "status": status,
            "metrics": {
                "average_requests_per_second": avg_rps,
                "average_error_rate": avg_error_rate,
                "average_latency_ms": avg_latency,
                "sample_size": len(service_metrics)
            }
        }

def main():
    """Demo of Phase 7 implementation"""
    print("📊 NEXAFORGE - PHASE 7: MONITORING & OBSERVABILITY (L10)")
    print("=" * 60)
    
    # Initialize monitoring system
    dashboard = MonitoringDashboard()
    alert_manager = dashboard.alert_manager
    
    print(f"\n🔍 DEMO 1: INITIALIZING MONITORING SYSTEM")
    print(f"   Metrics collection: Ready")
    print(f"   Alert management: Ready")
    print(f"   Log collection: Ready")
    
    # Start monitoring in background
    alert_manager.start_monitoring()
    
    print(f"\n📈 DEMO 2: SYSTEM METRICS COLLECTION")
    metrics_collector = alert_manager.metrics_collector
    
    # Get some metrics
    system_metrics = metrics_collector.get_recent_system_metrics(1)
    service_metrics = metrics_collector.get_recent_service_metrics(1)
    
    if system_metrics:
        latest_system = system_metrics[0]
        print(f"   CPU Usage: {latest_system.cpu_usage}%")
        print(f"   Memory Usage: {latest_system.memory_usage}%")
        print(f"   Disk Usage: {latest_system.disk_usage}%")
        if latest_system.gpu_usage:
            print(f"   GPU Load: {latest_system.gpu_usage['load']:.1f}%")
    
    if service_metrics:
        latest_service = service_metrics[0]
        print(f"   Requests/Sec: {latest_service.requests_per_second:.2f}")
        print(f"   Error Rate: {latest_service.error_rate*100:.2f}%")
        print(f"   Latency: {latest_service.latency_ms:.2f}ms")
    
    print(f"\n🚨 DEMO 3: ALERT MANAGEMENT")
    print(f"   Default alert rules configured:")
    for i, rule in enumerate(alert_manager.rules, 1):
        print(f"   {i}. {rule['name']} - {rule['severity'].value} severity")
    
    # Show current alerts
    active_alerts = alert_manager.get_active_alerts()
    print(f"   Active alerts: {len(active_alerts)}")
    
    # Show alert summary
    alert_summary = alert_manager.get_alert_summary()
    print(f"   Alert summary: {alert_summary}")
    
    print(f"\n📝 DEMO 4: LOG COLLECTION")
    log_collector = dashboard.log_collector
    
    # Write some sample logs
    log_collector.write_log("INFO", "api", "Service started successfully")
    log_collector.write_log("WARNING", "database", "Connection pool reaching limits", 
                           {"connections": 45, "threshold": 50})
    log_collector.write_log("ERROR", "workflow", "Task execution failed", 
                           {"task_id": "task-123", "error": "timeout"})
    
    recent_logs = log_collector.get_recent_logs(5)
    print(f"   Recent logs: {len(recent_logs)} entries")
    
    # Show last log
    if recent_logs:
        last_log = recent_logs[0]
        print(f"   Latest: [{last_log['level']}] {last_log['service']} - {last_log['message']}")
    
    print(f"\n📊 DEMO 5: DASHBOARD OVERVIEW")
    overview = dashboard.get_system_overview()
    print(f"   System Overview:")
    print(f"   - CPU: {overview['system'].get('cpu_usage', 0)}%")
    print(f"   - Memory: {overview['system'].get('memory_usage', 0)}%")
    print(f"   - Active Alerts: {overview['alerts']['total_active']}")
    print(f"   - Recent Logs: {overview['log_count']}")
    
    print(f"\n🏥 DEMO 6: SERVICE HEALTH CHECK")
    service_health = dashboard.get_service_health("nexaforge-api")
    print(f"   Service: {service_health['service']}")
    print(f"   Status: {service_health['status']}")
    if service_health['metrics']:
        metrics = service_health['metrics']
        print(f"   - Avg RPS: {metrics['average_requests_per_second']:.2f}")
        print(f"   - Error Rate: {metrics['average_error_rate']*100:.2f}%")
        print(f"   - Avg Latency: {metrics['average_latency_ms']:.2f}ms")
    
    print(f"\n🔄 DEMO 7: SIMULATING SYSTEM EVENTS")
    # Simulate writing more logs to see the system in action
    for i in range(3):
        log_collector.write_log("INFO", "monitoring", f"Metric collection cycle {i+1}")
    
    print(f"   Additional logs written to system")
    
    print(f"\n🎯 PHASE 7 COMPLETE: Monitoring & Observability Systems Ready!")
    print("   - System metrics collection")
    print("   - Alert management with custom rules")
    print("   - Log collection and search capabilities")
    print("   - Dashboard overview with service health")
    print("   - Ready for integration with monitoring tools (Prometheus, Grafana)")

if __name__ == "__main__":
    main()