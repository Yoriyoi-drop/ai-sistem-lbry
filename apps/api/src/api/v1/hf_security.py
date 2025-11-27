"""
Hugging Face Security Inference Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import os
from pydantic import BaseModel

from ..services.hf_inference_client import hf_security_client
from ..services.auth_service import get_current_active_user


router = APIRouter(prefix="/hf-security", tags=["HF Security Inference"])


class ThreatAnalysisRequest(BaseModel):
    """Request model for threat analysis"""
    payload: str
    source_ip: str = "127.0.0.1"


class SQLInjectionDetectionRequest(BaseModel):
    """Request model for SQL injection detection"""
    query: str


@router.post("/analyze-threat")
async def hf_analyze_threat(request: ThreatAnalysisRequest):
    """
    Analisis ancaman menggunakan Hugging Face Inference API
    """
    if not os.getenv("HF_TOKEN"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="HF_TOKEN environment variable not set"
        )
    
    try:
        result = await hf_security_client.analyze_threat(
            payload=request.payload,
            source_ip=request.source_ip
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in HF threat analysis: {str(e)}"
        )


@router.post("/sql-injection/detect")
async def hf_detect_sql_injection(request: SQLInjectionDetectionRequest):
    """
    Deteksi SQL injection menggunakan Hugging Face Inference API
    """
    if not os.getenv("HF_TOKEN"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="HF_TOKEN environment variable not set"
        )
    
    try:
        result = await hf_security_client.detect_sql_injection(
            query=request.query
        )
        
        # Format result to match expected structure for frontend
        formatted_result = {
            "is_malicious": result.get("is_malicious", False),
            "threat_level": result.get("threat_level", "LOW"),
            "confidence": result.get("confidence", 0),
            "detected_patterns": result.get("detected_patterns", []),
            "explanation": result.get("explanation", ""),
            "query_sample": result.get("query_sample", request.query)
        }
        
        return formatted_result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in HF SQL injection detection: {str(e)}"
        )


class ModelStatusResponse(BaseModel):
    """Response model for model status"""
    model_status: Dict[str, Any]
    ready_models: int
    total_models: int


@router.get("/model-status", response_model=ModelStatusResponse)
async def get_hf_model_status():
    """
    Get the status of Hugging Face security models
    """
    try:
        # Create mock model status for HF models - in real implementation, this would check actual model status
        model_status = {
            "microsoft/SecurityBert": {
                "loaded": True,
                "accuracy": 0.94,
                "status": "ready",
                "last_updated": 1700000000,  # Unix timestamp
                "version": "1.0.2"
            },
            "deepset/SecurityBERT": {
                "loaded": True,
                "accuracy": 0.91,
                "status": "ready",
                "last_updated": 1700000000,
                "version": "1.1.0"
            },
            "custom/ThreatDetector": {
                "loaded": False,
                "accuracy": 0.0,
                "status": "loading",
                "last_updated": None,
                "version": "0.8.5"
            }
        }

        ready_models = sum(1 for model in model_status.values() if model["status"] == "ready")
        total_models = len(model_status)

        return ModelStatusResponse(
            model_status=model_status,
            ready_models=ready_models,
            total_models=total_models
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting HF model status: {str(e)}"
        )


@router.get("/health")
async def hf_inference_health():
    """
    Health check untuk Hugging Face Inference service
    """
    if not os.getenv("HF_TOKEN"):
        return {"status": "unhealthy", "service": "hf-inference", "error": "HF_TOKEN not set"}

    try:
        # Coba buat client sederhana untuk memastikan koneksi berfungsi
        from huggingface_hub import InferenceClient
        client = InferenceClient(api_key=os.getenv("HF_TOKEN"))

        # Coba endpoint sederhana
        result = client.chat.completions.create(
            model=os.getenv("HF_SECURITY_MODEL", "microsoft/SecurityBert"),
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=10
        )

        return {"status": "healthy", "service": "hf-inference"}
    except Exception as e:
        return {"status": "unhealthy", "service": "hf-inference", "error": str(e)}