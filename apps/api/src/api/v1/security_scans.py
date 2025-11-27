"""
Security scanning endpoints for Infinite AI Security Platform
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel
import asyncio

from ..database.connection import get_db
from ..services.labyrinth_client import labyrinth_client
from ..services.auth_service import get_current_active_user


router = APIRouter(prefix="/security", tags=["Security Scans"])


class ThreatAnalysisRequest(BaseModel):
    """Request model for threat analysis"""
    payload: str
    source_ip: str = "127.0.0.1"


class SQLInjectionDetectionRequest(BaseModel):
    """Request model for SQL injection detection"""
    query: str


@router.post("/analyze-threat")
async def analyze_threat(request: ThreatAnalysisRequest):
    """
    Analyze a potential threat using the Rust Labyrinth engine
    """
    try:
        # Use the labyrinth client to analyze the threat
        async with labyrinth_client:
            result = await labyrinth_client.analyze_threat(
                payload=request.payload,
                source_ip=request.source_ip
            )
            return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing threat: {str(e)}"
        )


@router.post("/sql-injection/detect")
async def detect_sql_injection(request: SQLInjectionDetectionRequest):
    """
    Detect SQL injection attempts using the Rust Labyrinth engine
    """
    try:
        # Use the labyrinth client to analyze the SQL query
        async with labyrinth_client:
            result = await labyrinth_client.analyze_threat(
                payload=request.query,
                source_ip="127.0.0.1"  # Default source for API calls
            )
            
            # Format the result to match what the frontend expects
            formatted_result = {
                "is_malicious": result.get("confidence", 0) > 0.5,
                "threat_level": str(result.get("severity", "Low")),
                "confidence": result.get("confidence", 0),
                "detected_patterns": result.get("payload", "").split()[:5],  # Simplified
                "explanation": f"Threat detected with confidence {result.get('confidence', 0):.2f}",
                "query_sample": request.query
            }
            
            return formatted_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error detecting SQL injection: {str(e)}"
        )


@router.get("/labyrinth/stats")
async def get_labyrinth_stats():
    """
    Get statistics from the Rust Labyrinth engine
    """
    try:
        async with labyrinth_client:
            stats = await labyrinth_client.get_threat_statistics()
            return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting labyrinth stats: {str(e)}"
        )


@router.get("/labyrinth/health")
async def labyrinth_health():
    """
    Health check for the Rust Labyrinth engine
    """
    try:
        async with labyrinth_client:
            is_healthy = await labyrinth_client.health_check()
            return {"status": "healthy" if is_healthy else "unhealthy", "service": "labyrinth-rust-engine"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking labyrinth health: {str(e)}"
        )