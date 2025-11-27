"""
Prometheus metrics exporter for the Infinite AI Security Platform
"""

from prometheus_client import make_wsgi_app, Counter, Histogram, Gauge
from wsgiref.simple_server import make_server
import threading
import logging
from datetime import datetime
import time


# Application metrics
REQUEST_COUNT = Counter(
    'infinite_ai_requests_total',
    'Total requests to the application',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'infinite_ai_request_duration_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)

ACTIVE_USERS = Gauge(
    'infinite_ai_active_users',
    'Number of active users'
)

ACTIVE_SCANS = Gauge(
    'infinite_ai_active_scans',
    'Number of active security scans'
)

THREAT_LEVEL = Gauge(
    'infinite_ai_threat_level',
    'Current threat level (0-100)',
    ['severity']
)

# Security metrics
SECURITY_FINDINGS = Counter(
    'infinite_ai_security_findings_total',
    'Total security findings',
    ['scan_type', 'severity']
)

FAILED_LOGINS = Counter(
    'infinite_ai_failed_logins_total',
    'Total failed login attempts'
)

BLOCKED_IPS = Gauge(
    'infinite_ai_blocked_ips',
    'Number of currently blocked IPs'
)


class MetricsCollector:
    """Collects and exposes metrics for Prometheus"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.start_time = time.time()
        self.request_count = 0
        
    def record_request(self, method: str, endpoint: str, status_code: int):
        """Record an HTTP request"""
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status_code=status_code
        ).inc()
        
        self.request_count += 1
    
    def record_request_latency(self, method: str, endpoint: str, latency: float):
        """Record request latency"""
        REQUEST_LATENCY.labels(
            method=method,
            endpoint=endpoint
        ).observe(latency)
    
    def set_active_users(self, count: int):
        """Set the number of active users"""
        ACTIVE_USERS.set(count)
    
    def set_active_scans(self, count: int):
        """Set the number of active scans"""
        ACTIVE_SCANS.set(count)
    
    def set_threat_level(self, severity: str, level: float):
        """Set the current threat level"""
        THREAT_LEVEL.labels(severity=severity).set(level)
    
    def record_security_finding(self, scan_type: str, severity: str):
        """Record a security finding"""
        SECURITY_FINDINGS.labels(
            scan_type=scan_type,
            severity=severity
        ).inc()
    
    def record_failed_login(self):
        """Record a failed login attempt"""
        FAILED_LOGINS.inc()
    
    def set_blocked_ips(self, count: int):
        """Set the number of blocked IPs"""
        BLOCKED_IPS.set(count)
    
    def get_uptime(self) -> float:
        """Get application uptime in seconds"""
        return time.time() - self.start_time


# Global metrics collector instance
metrics_collector = MetricsCollector()


def start_metrics_server(port: int = 9090):
    """Start the Prometheus metrics server"""
    app = make_wsgi_app()
    server = make_server('', port, app)
    
    def run_server():
        print(f"🚀 Prometheus metrics server starting on port {port}")
        server.serve_forever()
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    return server_thread


def metrics_middleware(app):
    """Middleware to record metrics for each request"""
    def middleware(environ, start_response):
        start_time = time.time()
        
        # Get method and path
        method = environ.get('REQUEST_METHOD', 'UNKNOWN')
        path = environ.get('PATH_INFO', 'UNKNOWN')
        
        # Call the original app
        response = app(environ, start_response)
        
        # Record metrics after response
        status_code = int(start_response.__self__.status.split()[0])
        latency = time.time() - start_time
        
        # Record metrics
        metrics_collector.record_request(method, path, status_code)
        metrics_collector.record_request_latency(method, path, latency)
        
        return response
    
    return middleware


if __name__ == "__main__":
    # Example of starting the metrics server
    server_thread = start_metrics_server()
    
    # Keep the server running
    try:
        server_thread.join()
    except KeyboardInterrupt:
        print("Shutting down metrics server...")