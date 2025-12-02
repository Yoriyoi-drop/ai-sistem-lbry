"""
Monitoring API Router
API endpoints for monitoring, health checks, and metrics
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import asyncio
import time

from src.monitoring import (
    event_logger, metrics_collector, health_checker, 
    agent_monitor, threat_monitor
)
from api.dependencies.security import get_current_user, require_role
from fastapi import Depends


router = APIRouter(prefix="/monitoring", tags=["Monitoring & Health"])


@router.get("/health")
async def health_check():
    """
    Health check endpoint - returns system health status
    """
    # Register some basic health checks if not already registered
    if not health_checker.checks:
        # System health check
        def system_health():
            return {
                "status": "healthy",
                "component": "system",
                "timestamp": asyncio.get_event_loop().time()
            }
        
        # Database health check (placeholder)
        def db_health():
            return {
                "status": "healthy", 
                "component": "database",
                "timestamp": asyncio.get_event_loop().time()
            }
        
        # Security engine health check (placeholder)
        def security_health():
            return {
                "status": "healthy",
                "component": "security_engine", 
                "timestamp": asyncio.get_event_loop().time()
            }
        
        health_checker.register_check("system", system_health)
        health_checker.register_check("database", db_health)
        health_checker.register_check("security_engine", security_health)
    
    # Run all health checks
    results = await health_checker.run_all_checks()
    
    # Update system metrics
    try:
        metrics_collector.update_system_metrics()
    except:
        # If system metrics fail, continue anyway
        pass
    
    return {
        "status": results["overall_status"],
        "checks": results["checks"],
        "timestamp": results["timestamp"],
        "uptime": metrics_collector.get_uptime()
    }


@router.get("/metrics")
async def get_metrics():
    """
    Get system metrics
    """
    # Update system metrics
    try:
        metrics_collector.update_system_metrics()
    except:
        pass
    
    return metrics_collector.get_metrics_summary()


@router.get("/metrics/prometheus")
async def get_prometheus_metrics():
    """
    Get metrics in Prometheus format (if available)
    """
    try:
        from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
        PROMETHEUS_AVAILABLE = True
    except ImportError:
        PROMETHEUS_AVAILABLE = False

    if not PROMETHEUS_AVAILABLE:
        return {"error": "Prometheus not available", "metrics": metrics_collector.get_metrics_summary()}

    return {
        "metrics": generate_latest().decode("utf-8"),
        "content_type": CONTENT_TYPE_LATEST
    }


@router.get("/agents")
async def get_agent_health():
    """
    Get AI agent health and performance metrics
    """
    return agent_monitor.get_all_agent_health()


@router.get("/agents/{agent_id}")
async def get_specific_agent_health(agent_id: str):
    """
    Get health for a specific agent
    """
    health = agent_monitor.get_agent_health(agent_id)
    if not health or health["status"] == "unknown":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found"
        )
    return health


@router.get("/threats")
async def get_threats():
    """
    Get threat monitoring data
    """
    return threat_monitor.get_threat_summary()


@router.get("/threats/high")
async def get_high_severity_threats():
    """
    Get high severity threats
    """
    return threat_monitor.get_high_severity_threats()


@router.post("/log-event")
async def log_event(
    event_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """
    Log a custom event (requires member or higher)
    """
    event_type = event_data.get("type", "custom")
    details = event_data.get("details", {})
    
    event_logger.log_event(
        event_type,
        {
            "user_id": current_user.get("user_id"),
            "organization_id": current_user.get("organization_id"),
            "details": details
        }
    )
    
    return {"status": "logged", "event_type": event_type}


@router.get("/events")
async def get_events(
    current_user: dict = Depends(require_role("admin"))
):
    """
    Get event logs (admin only)
    """
    # This would require more sophisticated log handling in production
    return {
        "message": "Event log access endpoint",
        "available_logs": ["security", "access", "system"],
        "note": "Full event log implementation would require log aggregation system"
    }


@router.get("/status")
async def get_system_status():
    """
    Get comprehensive system status
    """
    # Collect all status information
    health_status = await health_checker.run_all_checks()
    
    # System metrics
    system_metrics = metrics_collector.get_metrics_summary()
    
    # Agent status
    agent_status = agent_monitor.get_all_agent_health()
    
    # Threat status
    threat_status = threat_monitor.get_threat_summary()
    
    return {
        "system_health": health_status,
        "system_metrics": system_metrics,
        "agent_status": agent_status,
        "threat_status": threat_status,
        "timestamp": asyncio.get_event_loop().time()
    }


@router.get("/heartbeat")
async def heartbeat():
    """
    Simple heartbeat endpoint to check service responsiveness
    """
    start_time = time.time()
    
    # Update system metrics
    try:
        metrics_collector.update_system_metrics()
    except:
        pass
    
    response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Record the heartbeat in metrics
    metrics_collector.record_api_request(
        method="GET",
        endpoint="/monitoring/heartbeat", 
        status_code=200,
        duration=response_time / 1000  # Convert back to seconds
    )
    
    return {
        "status": "alive",
        "response_time_ms": round(response_time, 2),
        "timestamp": asyncio.get_event_loop().time()
    }