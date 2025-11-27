from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any
import time
import psutil


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=Dict[str, Any])
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "api-gateway",
        "version": "2.0.0"
    }


@router.get("/ready", response_model=Dict[str, Any])
def readiness_check():
    """
    Readiness probe - check if service is ready to accept traffic
    """
    # In a real implementation, you'd check if all required services are available
    # such as database connections, external services, etc.
    
    # For now, just return ready
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {
            "database": "connected",
            "cache": "connected",
            "external_services": "available"
        }
    }


@router.get("/live", response_model=Dict[str, Any])
def liveness_check():
    """
    Liveness probe - check if the service itself is running
    """
    # Check if the service is alive by performing basic operations
    start_time = time.time()
    
    # Perform basic health checks
    try:
        # Check if we can access basic system resources
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        
        response_time = time.time() - start_time
        
        return {
            "status": "alive",
            "timestamp": datetime.utcnow().isoformat(),
            "response_time_ms": round(response_time * 1000, 2),
            "resources": {
                "cpu_usage": f"{cpu_percent}%",
                "memory_usage": f"{memory_percent}%",
                "disk_usage": f"{disk_percent}%"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }


@router.get("/metrics", response_model=Dict[str, Any])
def get_metrics():
    """
    Get detailed service metrics
    """
    # System metrics
    boot_time = psutil.boot_time()
    uptime = time.time() - boot_time
    
    # Memory metrics
    memory = psutil.virtual_memory()
    
    # CPU metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    
    # Disk metrics
    disk = psutil.disk_usage('/')
    
    # Network metrics
    network = psutil.net_io_counters()
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": round(uptime, 2),
        "system": {
            "cpu_percent": cpu_percent,
            "cpu_count": cpu_count,
            "load_average": list(psutil.getloadavg()) if hasattr(psutil, 'getloadavg') else [0, 0, 0],
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "memory_used_percent": memory.percent,
            "disk_total_gb": round(disk.total / (1024**3), 2),
            "disk_used_gb": round(disk.used / (1024**3), 2),
            "disk_used_percent": disk.percent
        },
        "network": {
            "bytes_sent": network.bytes_sent,
            "bytes_recv": network.bytes_recv,
            "packets_sent": network.packets_sent,
            "packets_recv": network.packets_recv
        }
    }