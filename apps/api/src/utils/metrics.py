from prometheus_client import Counter, Histogram, Summary, Gauge, generate_latest, CONTENT_TYPE_LATEST
from functools import wraps
import time
import logging
from typing import Callable, Any

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP requests', 
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 
    'HTTP request latency',
    ['method', 'endpoint']
)

REQUEST_SIZE = Summary(
    'http_request_size_bytes', 
    'HTTP request size',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections', 
    'Number of active connections'
)

# Security-specific metrics
SECURITY_SCANS = Counter(
    'security_scans_total',
    'Total security scans performed',
    ['scan_type', 'status']
)

THREAT_DETECTION = Counter(
    'threats_detected_total',
    'Total threats detected',
    ['threat_type', 'severity']
)

API_ERRORS = Counter(
    'api_errors_total',
    'Total API errors',
    ['error_type', 'endpoint']
)

def track_request_metrics(func: Callable) -> Callable:
    """
    Decorator to track request metrics
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            # Get method and endpoint information (this would be adapted to your framework)
            result = func(*args, **kwargs)
            
            # Record metrics
            REQUEST_COUNT.labels(
                method=getattr(func, '__name__', 'unknown'),
                endpoint=getattr(func, '__name__', 'unknown'),
                status='200'  # This would be dynamic based on response
            ).inc()
            
            REQUEST_LATENCY.labels(
                method=getattr(func, '__name__', 'unknown'),
                endpoint=getattr(func, '__name__', 'unknown')
            ).observe(time.time() - start_time)
            
            return result
        except Exception as e:
            API_ERRORS.labels(
                error_type=type(e).__name__,
                endpoint=getattr(func, '__name__', 'unknown')
            ).inc()
            raise
    return wrapper

def record_security_scan(scan_type: str, status: str):
    """
    Record a security scan in metrics
    """
    SECURITY_SCANS.labels(scan_type=scan_type, status=status).inc()

def record_threat_detection(threat_type: str, severity: str):
    """
    Record a threat detection in metrics
    """
    THREAT_DETECTION.labels(threat_type=threat_type, severity=severity).inc()

def get_metrics():
    """
    Get all metrics in Prometheus format
    """
    return generate_latest()

def metrics_endpoint():
    """
    FastAPI compatible metrics endpoint
    """
    from fastapi.responses import Response
    return Response(content=get_metrics(), media_type=CONTENT_TYPE_LATEST)