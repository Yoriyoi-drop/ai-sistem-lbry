"""
Advanced Security Detection API Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
from asm.advanced_security_detector import advanced_detector, ThreatType, DetectionResult
from apps.api.src.utils.dependencies import get_current_active_user, get_current_active_superuser
from apps.api.src.database.models import User

router = APIRouter(prefix="/advanced-security", tags=["Advanced Security Detection"])
logger = logging.getLogger(__name__)


class XSSDetectionRequest(BaseModel):
    content: str


class CommandInjectionRequest(BaseModel):
    command: str


class PathTraversalRequest(BaseModel):
    path: str


class AuthBruteforceRequest(BaseModel):
    username: str
    password: str


class SecurityDetectionResponse(BaseModel):
    threat_type: str
    severity: str
    confidence: float
    detected_patterns: List[str]
    explanation: str
    timestamp: str
    detection_id: Optional[int] = None


class AuthBruteforceDetectionRequest(BaseModel):
    username: str
    password: str


@router.post("/detect-xss", response_model=SecurityDetectionResponse)
async def detect_xss(
    request: XSSDetectionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Detect potential XSS in content
    """
    try:
        logger.info(f"Analyzing content for XSS: {request.content[:50]}...")

        result = advanced_detector.detect_xss(request.content)

        # Store the detection in database
        detection_id = advanced_detector.store_detection(result)

        logger.info(f"XSS detection result - Severity: {result.severity}, "
                   f"Confidence: {result.confidence}")

        return SecurityDetectionResponse(
            threat_type=result.threat_type.value,
            severity=result.severity,
            confidence=result.confidence,
            detected_patterns=result.detected_patterns,
            explanation=result.explanation,
            timestamp=result.timestamp.isoformat(),
            detection_id=detection_id
        )

    except Exception as e:
        logger.error(f"Error in XSS detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/detect-command-injection", response_model=SecurityDetectionResponse)
async def detect_command_injection(
    request: CommandInjectionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Detect potential command injection in commands
    """
    try:
        logger.info(f"Analyzing command for injection: {request.command[:50]}...")

        result = advanced_detector.detect_command_injection(request.command)

        # Store the detection in database
        detection_id = advanced_detector.store_detection(result)

        logger.info(f"Command injection detection result - Severity: {result.severity}, "
                   f"Confidence: {result.confidence}")

        return SecurityDetectionResponse(
            threat_type=result.threat_type.value,
            severity=result.severity,
            confidence=result.confidence,
            detected_patterns=result.detected_patterns,
            explanation=result.explanation,
            timestamp=result.timestamp.isoformat(),
            detection_id=detection_id
        )

    except Exception as e:
        logger.error(f"Error in command injection detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/detect-path-traversal", response_model=SecurityDetectionResponse)
async def detect_path_traversal(
    request: PathTraversalRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Detect potential path traversal attacks
    """
    try:
        logger.info(f"Analyzing path for traversal: {request.path[:50]}...")

        result = advanced_detector.detect_path_traversal(request.path)

        # Store the detection in database
        detection_id = advanced_detector.store_detection(result)

        logger.info(f"Path traversal detection result - Severity: {result.severity}, "
                   f"Confidence: {result.confidence}")

        return SecurityDetectionResponse(
            threat_type=result.threat_type.value,
            severity=result.severity,
            confidence=result.confidence,
            detected_patterns=result.detected_patterns,
            explanation=result.explanation,
            timestamp=result.timestamp.isoformat(),
            detection_id=detection_id
        )

    except Exception as e:
        logger.error(f"Error in path traversal detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/detect-auth-bruteforce", response_model=SecurityDetectionResponse)
async def detect_auth_bruteforce(
    request: AuthBruteforceDetectionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Detect potential authentication brute force attempts
    """
    try:
        logger.info(f"Analyzing login attempt: {request.username}")

        login_request = {
            "username": request.username,
            "password": request.password
        }

        result = advanced_detector.detect_auth_bruteforce(login_request)

        # Store the detection in database
        detection_id = advanced_detector.store_detection(result)

        logger.info(f"Auth brute force detection result - Severity: {result.severity}, "
                   f"Confidence: {result.confidence}")

        return SecurityDetectionResponse(
            threat_type=result.threat_type.value,
            severity=result.severity,
            confidence=result.confidence,
            detected_patterns=result.detected_patterns,
            explanation=result.explanation,
            timestamp=result.timestamp.isoformat(),
            detection_id=detection_id
        )

    except Exception as e:
        logger.error(f"Error in auth brute force detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/recent-detections")
async def get_recent_detections(
    limit: int = 10,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get recent security detections from database
    """
    try:
        detections = advanced_detector.get_recent_detections(limit)
        return {"detections": detections, "total": len(detections)}
    except Exception as e:
        logger.error(f"Error retrieving recent detections: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/test")
async def test_advanced_detector(
    current_user: User = Depends(get_current_active_user)
):
    """
    Test endpoint to verify advanced security detector is working
    """
    test_content = "<script>alert('XSS')</script>"
    xss_result = advanced_detector.detect_xss(test_content)

    test_command = "ls | cat /etc/passwd"
    cmd_result = advanced_detector.detect_command_injection(test_command)

    return {
        "xss_test": {
            "input": test_content,
            "result": {
                "threat_type": xss_result.threat_type.value,
                "severity": xss_result.severity,
                "confidence": xss_result.confidence
            }
        },
        "command_test": {
            "input": test_command,
            "result": {
                "threat_type": cmd_result.threat_type.value,
                "severity": cmd_result.severity,
                "confidence": cmd_result.confidence
            }
        },
        "status": "Advanced Security Detector is working correctly"
    }


if __name__ == "__main__":
    import asyncio
    
    async def test_api():
        # Test the API functionality
        test_content = "<script>alert('XSS')</script>"
        result = advanced_detector.detect_xss(test_content)
        print(f"XSS Test result: {result}")
    
    asyncio.run(test_api())