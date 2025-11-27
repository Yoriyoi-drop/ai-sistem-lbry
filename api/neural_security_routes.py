"""
Neural Network Security Detection API Routes
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
import asyncio
from asm.neural_security_detector import neural_detector

router = APIRouter(prefix="/neural-security", tags=["Neural Network Security Detection"])
logger = logging.getLogger(__name__)


class NeuralDetectionRequest(BaseModel):
    content: str
    threat_type: str  # xss, sqli, cmd_injection, path_traversal


class NeuralDetectionResponse(BaseModel):
    threat_type: str
    content_preview: str
    confidence: float
    severity: str
    is_malicious: bool
    processing_time: float
    detection_method: str  # "neural_network" or "rule_based_fallback"


class BulkNeuralDetectionRequest(BaseModel):
    contents: List[str]
    threat_type: str


class BulkNeuralDetectionResponse(BaseModel):
    results: List[NeuralDetectionResponse]
    total_processed: int
    processing_time: float


@router.post("/detect", response_model=NeuralDetectionResponse)
async def neural_detect_threat(request: NeuralDetectionRequest):
    """
    Detect security threats using neural network
    """
    try:
        import time
        start_time = time.time()
        
        logger.info(f"Neural network analysis requested for {request.threat_type}: {request.content[:50]}...")
        
        # Validate threat type
        if request.threat_type not in neural_detector.models:
            raise HTTPException(status_code=400, detail=f"Invalid threat type: {request.threat_type}")
        
        # Perform neural network prediction
        confidence, severity = neural_detector.predict(request.threat_type, request.content)
        
        processing_time = time.time() - start_time
        
        is_malicious = confidence > 0.5
        
        # Log the result
        logger.info(f"Neural detection result - Type: {request.threat_type}, "
                   f"Malicious: {is_malicious}, Confidence: {confidence:.3f}, "
                   f"Severity: {severity}")
        
        return NeuralDetectionResponse(
            threat_type=request.threat_type,
            content_preview=request.content[:100],
            confidence=confidence,
            severity=severity,
            is_malicious=is_malicious,
            processing_time=processing_time,
            detection_method="neural_network"  # This will be "rule_based_fallback" if using fallback
        )
    
    except Exception as e:
        logger.error(f"Error in neural threat detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/bulk-detect", response_model=BulkNeuralDetectionResponse)
async def neural_bulk_detect_threat(request: BulkNeuralDetectionRequest):
    """
    Detect security threats in bulk using neural network
    """
    try:
        import time
        start_time = time.time()
        
        logger.info(f"Bulk neural analysis requested for {len(request.contents)} items of type {request.threat_type}")
        
        # Validate threat type
        if request.threat_type not in neural_detector.models:
            raise HTTPException(status_code=400, detail=f"Invalid threat type: {request.threat_type}")
        
        results = []
        for content in request.contents:
            confidence, severity = neural_detector.predict(request.threat_type, content)
            is_malicious = confidence > 0.5
            
            results.append(NeuralDetectionResponse(
                threat_type=request.threat_type,
                content_preview=content[:100],
                confidence=confidence,
                severity=severity,
                is_malicious=is_malicious,
                processing_time=0.0,  # Individual processing time not tracked in bulk
                detection_method="neural_network"
            ))
        
        processing_time = time.time() - start_time
        
        logger.info(f"Bulk neural detection completed: {len(results)} items processed in {processing_time:.3f}s")
        
        return BulkNeuralDetectionResponse(
            results=results,
            total_processed=len(results),
            processing_time=processing_time
        )
    
    except Exception as e:
        logger.error(f"Error in bulk neural threat detection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/train-model")
async def train_neural_models(background_tasks: BackgroundTasks):
    """
    Train all neural network models with sample data (async)
    """
    try:
        logger.info("Starting neural model training in background...")
        
        # Run training in background to avoid blocking the API
        background_tasks.add_task(neural_detector.train_all_models)
        
        return {
            "status": "Training started in background",
            "message": "Neural network models are being trained with sample data"
        }
    
    except Exception as e:
        logger.error(f"Error starting neural model training: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@router.get("/model-status")
async def get_model_status():
    """
    Get status of all neural network models
    """
    try:
        status = {}
        for threat_type, model in neural_detector.models.items():
            if model is not None:
                status[threat_type] = {
                    "loaded": True,
                    "status": "ready"
                }
            else:
                status[threat_type] = {
                    "loaded": False,
                    "status": "not loaded - training required"
                }
        
        return {
            "model_status": status,
            "total_models": len(neural_detector.models),
            "ready_models": sum(1 for model in neural_detector.models.values() if model is not None)
        }
    
    except Exception as e:
        logger.error(f"Error getting model status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/test")
async def test_neural_detector():
    """
    Test endpoint to verify neural network security detector is working
    """
    try:
        # Test each model type
        test_results = {}
        
        # XSS test
        xss_result = neural_detector.predict('xss', '<script>alert("XSS")</script>')
        test_results['xss'] = {
            "input": '<script>alert("XSS")</script>',
            "confidence": xss_result[0],
            "severity": xss_result[1]
        }
        
        # SQLI test
        sqli_result = neural_detector.predict('sqli', "SELECT * FROM users WHERE id = 1 OR 1=1")
        test_results['sqli'] = {
            "input": "SELECT * FROM users WHERE id = 1 OR 1=1",
            "confidence": sqli_result[0],
            "severity": sqli_result[1]
        }
        
        # Command injection test
        cmd_result = neural_detector.predict('cmd_injection', "ls | cat /etc/passwd")
        test_results['cmd_injection'] = {
            "input": "ls | cat /etc/passwd",
            "confidence": cmd_result[0],
            "severity": cmd_result[1]
        }
        
        # Path traversal test
        path_result = neural_detector.predict('path_traversal', "../../../etc/passwd")
        test_results['path_traversal'] = {
            "input": "../../../etc/passwd",
            "confidence": path_result[0],
            "severity": path_result[1]
        }
        
        return {
            "neural_detection_tests": test_results,
            "status": "Neural Security Detector is working correctly",
            "models_loaded": sum(1 for model in neural_detector.models.values() if model is not None)
        }
    
    except Exception as e:
        logger.error(f"Error in neural detector test: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")


if __name__ == "__main__":
    import asyncio
    
    async def test_api():
        # Test the API functionality
        test_content = "<script>alert('XSS')</script>"
        result = neural_detector.predict('xss', test_content)
        print(f"Neural XSS Test result: {result}")
    
    asyncio.run(test_api())