from fastapi import APIRouter, HTTPException, status
from typing import Dict
from datetime import datetime

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=Dict[str, str])
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "API Gateway"
    }


@router.get("/ready", response_model=Dict[str, str])
def readiness_check():
    """
    Readiness check endpoint
    """
    # Here you would check if all required services are available
    # For now, just return healthy
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/live", response_model=Dict[str, str])
def liveness_check():
    """
    Liveness check endpoint
    """
    # Here you would check if the service is alive and functioning
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }