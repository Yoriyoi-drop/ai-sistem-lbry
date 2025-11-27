"""
SQL Injection Detection API Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import logging

from asm.sql_injection_detector import detect_sql_injection, DetectionResult

router = APIRouter(prefix="/sql-injection", tags=["SQL Injection Detection"])
logger = logging.getLogger(__name__)


class SQLQueryRequest(BaseModel):
    query: str


class SQLDetectionResponse(BaseModel):
    is_malicious: bool
    confidence: float
    threat_level: str
    detected_patterns: List[str]
    explanation: str
    query_sample: str


@router.post("/detect", response_model=SQLDetectionResponse)
async def detect_sql_injection_endpoint(request: SQLQueryRequest):
    """
    Detect potential SQL injection in a given SQL query
    """
    try:
        logger.info(f"Analyzing SQL query for injection: {request.query[:50]}...")
        
        # Perform real SQL injection detection
        result = detect_sql_injection(request.query)
        
        # Log the detection result
        logger.info(f"SQL injection detection result - Malicious: {result['is_malicious']}, "
                   f"Confidence: {result['confidence']}, Threat: {result['threat_level']}")
        
        return SQLDetectionResponse(
            is_malicious=result["is_malicious"],
            confidence=result["confidence"],
            threat_level=result["threat_level"],
            detected_patterns=result["detected_patterns"],
            explanation=result["explanation"],
            query_sample=request.query[:100]  # Return query sample (truncated)
        )
    
    except Exception as e:
        logger.error(f"Error in SQL injection detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/batch-detect")
async def batch_detect_sql_injection(queries: List[str]):
    """
    Detect potential SQL injection in multiple queries
    """
    try:
        results = []
        for query in queries:
            result = detect_sql_injection(query)
            results.append({
                "query": query[:100],  # Truncated query
                "is_malicious": result["is_malicious"],
                "confidence": result["confidence"],
                "threat_level": result["threat_level"],
                "detected_patterns": result["detected_patterns"],
                "explanation": result["explanation"]
            })
        
        return {"results": results}
    
    except Exception as e:
        logger.error(f"Error in batch SQL injection detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/test")
async def test_sql_detector():
    """
    Test endpoint to verify SQL injection detector is working
    """
    test_query = "SELECT * FROM users WHERE id = 1 OR 1=1"
    result = detect_sql_injection(test_query)
    
    return {
        "test_query": test_query,
        "result": result,
        "status": "SQL Injection Detector is working correctly"
    }


if __name__ == "__main__":
    import asyncio
    
    async def test_api():
        # Test the API functionality
        test_query = "SELECT * FROM users WHERE id = 1 OR 1=1"
        result = detect_sql_injection(test_query)
        print(f"Test result: {result}")
    
    asyncio.run(test_api())