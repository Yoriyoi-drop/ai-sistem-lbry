"""
Security Analysis Router
API endpoints for security analysis and threat detection
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import asyncio

from api.dependencies.security import (
    get_current_user, 
    check_feature_access, 
    rate_limit_dependency
)
from api.schemas.models import (
    SecurityAnalysisRequest, 
    ThreatDetectionResponse, 
    SecurityEngineRequest,
    SecurityEngineResponse
)
from src.database.session import get_db
from security_engine.engine import SecurityEngine


router = APIRouter(prefix="/security", tags=["Security Analysis"])


@router.post("/analyze", response_model=SecurityEngineResponse)
async def analyze_content(
    request: SecurityAnalysisRequest,
    current_user: dict = Depends(get_current_user),
    check_access: dict = Depends(check_feature_access("basic_security_scanning")),
    rate_limit: dict = Depends(rate_limit_dependency(100, 60)),
    db: Session = Depends(get_db)
):
    """
    Analyze content for security threats
    """
    try:
        security_engine = SecurityEngine()
        
        # Perform comprehensive analysis based on requested analysis type
        if request.analysis_type == "comprehensive":
            # Run all security checks
            request.analysis_type = ["prompt_injection", "jailbreak", "malicious_code", "sensitive_data"]
        else:
            request.analysis_type = [request.analysis_type]
        
        # Perform analysis
        if "prompt_injection" in request.analysis_type:
            injection_result = await security_engine.prompt_injection_detector.detect(request.content)
        else:
            injection_result = {"is_malicious": False, "severity": "safe", "confidence": 0.1}
        
        if "jailbreak" in request.analysis_type:
            jailbreak_result = await security_engine.jailbreak_detector.detect(request.content)
        else:
            jailbreak_result = {"is_malicious": False, "severity": "safe", "confidence": 0.1}
        
        if "malicious_code" in request.analysis_type:
            code_result = await security_engine.malicious_code_detector.detect(request.content)
        else:
            code_result = {"is_malicious": False, "severity": "safe", "confidence": 0.1}
        
        if "sensitive_data" in request.analysis_type:
            data_result = await security_engine.sensitive_data_detector.detect(request.content)
        else:
            data_result = {"is_sensitive": False, "severity": "safe", "confidence": 0.1}
        
        # Combine results
        analysis_results = {
            "prompt_injection": injection_result,
            "jailbreak_attempt": jailbreak_result,
            "malicious_code": code_result,
            "sensitive_data": data_result
        }
        
        # Determine overall threat level
        threat_level = security_engine.threat_grader.grade_threat(analysis_results)
        
        # Determine if content is allowed
        is_allowed = threat_level in ["safe", "info"]
        
        return SecurityEngineResponse(
            input_text_summary=request.content[:100] + "..." if len(request.content) > 100 else request.content,
            analysis_results=analysis_results,
            overall_threat_level=threat_level,
            threat_score=security_engine.threat_grader._calculate_threat_score(analysis_results),
            is_allowed=is_allowed,
            processed_output=None,
            timestamp=security_engine.threat_grader.__class__.__name__  # Placeholder for actual timestamp
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing content: {str(e)}"
        )


@router.post("/analyze-advanced", response_model=SecurityEngineResponse)
async def analyze_content_advanced(
    request: SecurityEngineRequest,
    current_user: dict = Depends(get_current_user),
    check_access: dict = Depends(check_feature_access("multi_agent_ai")),
    rate_limit: dict = Depends(rate_limit_dependency(50, 60)),
    db: Session = Depends(get_db)
):
    """
    Advanced security analysis with full security engine capabilities
    """
    try:
        security_engine = SecurityEngine()
        
        # Perform request analysis
        request_analysis = await security_engine.analyze_request(
            request.input_text, 
            request.context
        )
        
        # Determine if request is allowed
        filter_result = await security_engine.filter_request(
            request.input_text,
            request.context
        )
        
        # Calculate threat score
        threat_score = security_engine.threat_grader._calculate_threat_score(request_analysis)
        
        return SecurityEngineResponse(
            input_text_summary=(
                request.input_text[:100] + "..." if len(request.input_text) > 100 
                else request.input_text
            ),
            analysis_results=request_analysis,
            overall_threat_level=filter_result["analysis"]["threat_level"],
            threat_score=threat_score,
            is_allowed=filter_result["is_allowed"],
            processed_output=filter_result["analysis"].get("sanitized_request"),
            timestamp=filter_result["timestamp"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in advanced security analysis: {str(e)}"
        )


@router.post("/execute-safe", response_model=Dict[str, Any])
async def execute_code_safely(
    execute_request: Dict[str, Any],
    current_user: dict = Depends(get_current_user),
    check_access: dict = Depends(check_feature_access("multi_agent_ai")),
    rate_limit: dict = Depends(rate_limit_dependency(20, 60)),
    db: Session = Depends(get_db)
):
    """
    Execute code in a secure sandbox environment
    """
    try:
        security_engine = SecurityEngine()
        code = execute_request.get("code", "")
        language = execute_request.get("language", "python")
        timeout = execute_request.get("timeout", 5)
        
        # Check if code is safe to execute
        safety_check = security_engine.sandbox.check_safety(code, language)
        
        if safety_check["risk_level"] == "high":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Code deemed too risky to execute: {safety_check['issues']}"
            )
        
        # Execute in sandbox
        result = security_engine.sandbox.execute(code, language, timeout)
        
        return {
            "execution_result": result,
            "safety_check": safety_check,
            "timestamp": security_engine.__class__.__name__  # Placeholder
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing code safely: {str(e)}"
        )


@router.post("/detect-threats", response_model=List[ThreatDetectionResponse])
async def detect_multiple_threats(
    content_list: Dict[str, list],
    current_user: dict = Depends(get_current_user),
    check_access: dict = Depends(check_feature_access("basic_security_scanning")),
    rate_limit: dict = Depends(rate_limit_dependency(200, 60)),
    db: Session = Depends(get_db)
):
    """
    Detect threats in multiple pieces of content
    """
    try:
        security_engine = SecurityEngine()
        results = []
        
        for i, content in enumerate(content_list.get("content", [])):
            # Perform all detections
            injection_result = await security_engine.prompt_injection_detector.detect(content)
            jailbreak_result = await security_engine.jailbreak_detector.detect(content)
            code_result = await security_engine.malicious_code_detector.detect(content)
            data_result = await security_engine.sensitive_data_detector.detect(content)
            
            # Combine findings
            all_findings = []
            all_findings.extend(injection_result.get("findings", []))
            all_findings.extend(jailbreak_result.get("findings", []))
            all_findings.extend(code_result.get("findings", []))
            all_findings.extend(data_result.get("findings", []))
            all_findings.extend([item for f in data_result.get("findings", [])
                                for item in f.get("matched_text", []) if isinstance(f.get("matched_text"), list)])

            # Determine overall result
            result = ThreatDetectionResponse(
                is_malicious=(
                    injection_result.get("is_malicious", False) or 
                    jailbreak_result.get("is_malicious", False) or 
                    code_result.get("is_malicious", False) or 
                    data_result.get("is_sensitive", False)
                ),
                severity=max([
                    injection_result.get("severity", "safe"),
                    jailbreak_result.get("severity", "safe"),
                    code_result.get("severity", "safe"),
                    data_result.get("severity", "safe")
                ], key=lambda x: ["safe", "info", "low", "medium", "high", "block"].index(x) if x in ["safe", "info", "low", "medium", "high", "block"] else 0),
                confidence=max([
                    injection_result.get("confidence", 0.0),
                    jailbreak_result.get("confidence", 0.0),
                    code_result.get("confidence", 0.0),
                    data_result.get("confidence", 0.0)
                ]),
                findings=all_findings,
                matched_patterns=(
                    injection_result.get("matched_patterns", []) +
                    jailbreak_result.get("matched_patterns", []) +
                    code_result.get("matched_patterns", []) +
                    [item for f in data_result.get("findings", []) 
                     for item in f.get("matched_text", []) if isinstance(f.get("matched_text"), list)]
                ),
                analysis_time=security_engine.__class__.__name__  # Placeholder
            )
            results.append(result)
        
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error detecting threats: {str(e)}"
        )