"""
Security Engine Core Module
Enterprise-level security detection and protection system
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from .detectors import (
    PromptInjectionDetector, 
    JailbreakDetector, 
    MaliciousCodeDetector, 
    SensitiveDataDetector
)
from .filters import OutputSanitizer, ContextGuard, ProfanityFilter
from .grader import ThreatGrader
from .sandbox import ExecutionSandbox


class SecurityEngine:
    """
    Main security engine that orchestrates all security modules
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize detectors
        self.prompt_injection_detector = PromptInjectionDetector()
        self.jailbreak_detector = JailbreakDetector()
        self.malicious_code_detector = MaliciousCodeDetector()
        self.sensitive_data_detector = SensitiveDataDetector()
        
        # Initialize filters
        self.output_sanitizer = OutputSanitizer()
        self.context_guard = ContextGuard()
        self.profanity_filter = ProfanityFilter()
        
        # Initialize grader
        self.threat_grader = ThreatGrader()
        
        # Initialize sandbox
        self.sandbox = ExecutionSandbox()
        
        self.logger.info("Security Engine initialized")

    async def analyze_request(self, prompt: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze incoming prompt/request for security threats
        """
        results = {
            "prompt_injection": await self.prompt_injection_detector.detect(prompt),
            "jailbreak_attempt": await self.jailbreak_detector.detect(prompt),
            "malicious_code": await self.malicious_code_detector.detect(prompt),
            "sensitive_data": await self.sensitive_data_detector.detect(prompt),
            "context_risk": self.context_guard.check_context(context or {}),
            "profanity_score": self.profanity_filter.analyze(prompt)
        }
        
        # Grade the overall threat level
        threat_level = self.threat_grader.grade_threat(results)
        results["threat_level"] = threat_level
        
        return results

    async def analyze_response(self, response: str, original_prompt: str, 
                             context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze AI response for security threats
        """
        results = {
            "output_sanitization_needed": self.output_sanitizer.needs_sanitization(response),
            "context_leakage": self.context_guard.check_leakage(response, context or {}),
            "malicious_content": await self.malicious_code_detector.detect(response),
            "sensitive_data_exposure": await self.sensitive_data_detector.detect(response),
            "profanity_score": self.profanity_filter.analyze(response)
        }
        
        # Grade the overall threat level
        threat_level = self.threat_grader.grade_threat({**results, "original_prompt": original_prompt})
        results["threat_level"] = threat_level
        
        # Sanitize if needed
        if results["output_sanitization_needed"]:
            results["sanitized_response"] = self.output_sanitizer.sanitize(response)
        
        return results

    async def filter_request(self, prompt: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Filter incoming request and return allowed status
        """
        analysis = await self.analyze_request(prompt, context)
        
        # Block if threat level is high
        is_allowed = analysis["threat_level"] in ["safe", "warning"]
        
        return {
            "is_allowed": is_allowed,
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def filter_response(self, response: str, original_prompt: str, 
                            context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Filter AI response and return processed result
        """
        analysis = await self.analyze_response(response, original_prompt, context)
        
        result = {
            "original_response": response,
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # If high threat, block completely
        if analysis["threat_level"] == "block":
            result["is_allowed"] = False
            result["processed_response"] = "[BLOCKED: Security threat detected]"
        else:
            result["is_allowed"] = True
            # Use sanitized version if available
            result["processed_response"] = analysis.get("sanitized_response", response)
        
        return result

    def execute_safely(self, code: str, timeout: int = 5) -> Dict[str, Any]:
        """
        Execute code in a secure sandbox
        """
        return self.sandbox.execute(code, timeout)