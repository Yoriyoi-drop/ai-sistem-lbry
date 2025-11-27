"""
Additional security scanning endpoints for Infinite AI Security Platform
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, List, Any
from pydantic import BaseModel
import asyncio
import time

from fastapi import Depends
from sqlalchemy.orm import Session
from ..database.connection import get_db
from ..services.labyrinth_client import labyrinth_client
from ..services.auth_service import get_current_active_user


router = APIRouter(prefix="/advanced-security", tags=["Advanced Security Scans"])


class XssDetectionRequest(BaseModel):
    content: str


class CommandInjectionDetectionRequest(BaseModel):
    command: str


class PathTraversalDetectionRequest(BaseModel):
    path: str


class AuthBruteForceDetectionRequest(BaseModel):
    username: str
    password: str


class ThreatDetectionResponse(BaseModel):
    threat_type: str
    severity: str
    confidence: float
    detected_patterns: List[str]
    explanation: str
    timestamp: float


class RecentDetectionsResponse(BaseModel):
    detections: List[ThreatDetectionResponse]


@router.post("/detect-xss", response_model=ThreatDetectionResponse)
async def detect_xss(request: XssDetectionRequest):
    """
    Detect XSS threats using the Rust Labyrinth engine
    """
    try:
        async with labyrinth_client:
            result = await labyrinth_client.analyze_threat(
                payload=request.content,
                source_ip="127.0.0.1"
            )
            
            # Format the result to match expected structure
            formatted_result = ThreatDetectionResponse(
                threat_type="XSS",
                severity=result.get("severity", "Low"),
                confidence=result.get("confidence", 0),
                detected_patterns=[request.content[:50]] if "<script>" in request.content.lower() else [],
                explanation=f"XSS threat detected in content with confidence {result.get('confidence', 0):.2f}",
                timestamp=time.time()
            )
            
            return formatted_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error detecting XSS: {str(e)}"
        )


@router.post("/detect-command-injection", response_model=ThreatDetectionResponse)
async def detect_command_injection(request: CommandInjectionDetectionRequest):
    """
    Detect command injection threats using the Rust Labyrinth engine
    """
    try:
        async with labyrinth_client:
            result = await labyrinth_client.analyze_threat(
                payload=request.command,
                source_ip="127.0.0.1"
            )
            
            # Format the result to match expected structure
            formatted_result = ThreatDetectionResponse(
                threat_type="COMMAND_INJECTION",
                severity=result.get("severity", "Low"),
                confidence=result.get("confidence", 0),
                detected_patterns=[request.command[:50]] if "|" in request.command or "&" in request.command else [],
                explanation=f"Command injection threat detected in command with confidence {result.get('confidence', 0):.2f}",
                timestamp=time.time()
            )
            
            return formatted_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error detecting command injection: {str(e)}"
        )


@router.post("/detect-path-traversal", response_model=ThreatDetectionResponse)
async def detect_path_traversal(request: PathTraversalDetectionRequest):
    """
    Detect path traversal threats using the Rust Labyrinth engine
    """
    try:
        async with labyrinth_client:
            result = await labyrinth_client.analyze_threat(
                payload=request.path,
                source_ip="127.0.0.1"
            )
            
            # Format the result to match expected structure
            formatted_result = ThreatDetectionResponse(
                threat_type="PATH_TRAVERSAL",
                severity=result.get("severity", "Low"),
                confidence=result.get("confidence", 0),
                detected_patterns=[request.path[:50]] if "../" in request.path or "..\\" in request.path else [],
                explanation=f"Path traversal threat detected in path with confidence {result.get('confidence', 0):.2f}",
                timestamp=time.time()
            )
            
            return formatted_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error detecting path traversal: {str(e)}"
        )


@router.post("/detect-auth-bruteforce", response_model=ThreatDetectionResponse)
async def detect_auth_bruteforce(request: AuthBruteForceDetectionRequest):
    """
    Detect potential auth bruteforce attempts using the Rust Labyrinth engine
    """
    try:
        # Create a payload that represents a potential auth bruteforce attempt
        payload = f"username={request.username}&password={request.password}"
        
        async with labyrinth_client:
            result = await labyrinth_client.analyze_threat(
                payload=payload,
                source_ip="127.0.0.1"
            )
            
            # Format the result to match expected structure
            formatted_result = ThreatDetectionResponse(
                threat_type="AUTH_BRUTEFORCE",
                severity=result.get("severity", "Low"),
                confidence=result.get("confidence", 0),
                detected_patterns=[request.username[:30]],
                explanation=f"Potential auth bruteforce detected with confidence {result.get('confidence', 0):.2f}",
                timestamp=time.time()
            )
            
            return formatted_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error detecting auth bruteforce: {str(e)}"
        )


@router.get("/recent-detections", response_model=RecentDetectionsResponse)
async def get_recent_detections(limit: int = 10):
    """
    Get recent detections (mock implementation for now)
    """
    # This is a mock implementation - in a real system, this would fetch from a database
    import random
    from datetime import datetime, timedelta

    # Generate more realistic mock data
    threat_types = ["SQL_INJECTION", "XSS", "COMMAND_INJECTION", "PATH_TRAVERSAL", "AUTH_BRUTEFORCE"]
    severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

    mock_detections = []
    for i in range(min(limit, 15)):  # Generate up to 15, but respect limit
        threat_type = random.choice(threat_types)
        severity = random.choice(severities)

        detection = {
            "threat_type": threat_type,
            "severity": severity,
            "confidence": round(random.uniform(0.6, 0.99), 2),
            "detected_patterns": [f"pattern_{i}", f"signature_{i}"],
            "explanation": f"Detected potential {threat_type.lower()} threat with {severity.lower()} severity",
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 60))).timestamp()
        }
        mock_detections.append(detection)

    return RecentDetectionsResponse(detections=mock_detections)