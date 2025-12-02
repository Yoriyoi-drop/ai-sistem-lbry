"""
Grader Module for Security Engine
Evaluates and grades security threats
"""
from typing import Dict, Any, List, Union


class ThreatGrader:
    """
    Grades threats based on severity and confidence
    """
    def __init__(self):
        # Define severity weights
        self.severity_weights = {
            "info": 0.1,
            "low": 0.3,
            "medium": 0.6,
            "high": 0.8,
            "block": 1.0
        }
        
        # Define threat multipliers
        self.threat_multipliers = {
            "prompt_injection": 1.5,
            "jailbreak_attempt": 2.0,
            "malicious_code": 2.0,
            "sensitive_data": 1.2,
            "context_leakage": 1.3,
        }

    def grade_threat(self, analysis_results: Dict[str, Any]) -> str:
        """
        Grade overall threat level based on analysis results
        """
        total_score = 0.0
        threat_count = 0
        
        # Calculate score based on each component
        for key, value in analysis_results.items():
            if isinstance(value, dict) and "severity" in value:
                # Handle nested analysis results
                severity = value.get("severity", "safe")
                confidence = value.get("confidence", 0.5)  # Default confidence 0.5
                
                if severity != "safe":
                    weight = self.severity_weights.get(severity, 0.0)
                    multiplier = self.threat_multipliers.get(key.replace("_analysis", ""), 1.0)
                    
                    # Calculate weighted score
                    score = weight * confidence * multiplier
                    total_score += score
                    threat_count += 1
            elif isinstance(value, list):
                # Handle finding lists
                for item in value:
                    if isinstance(item, dict) and "severity" in item:
                        severity = item["severity"]
                        weight = self.severity_weights.get(severity, 0.0)
                        # Assume default confidence for list items
                        score = weight * 0.7  # Default confidence for findings
                        total_score += score
                        threat_count += 1
            elif isinstance(value, str) and key in self.severity_weights:
                # Direct severity value
                severity = value
                weight = self.severity_weights.get(severity, 0.0)
                total_score += weight
                threat_count += 1
        
        # Calculate average threat level
        if threat_count > 0:
            avg_score = total_score / threat_count
        else:
            return "safe"
        
        # Determine overall threat level
        if avg_score >= 0.8:
            return "block"
        elif avg_score >= 0.6:
            return "warning"
        elif avg_score > 0.1:
            return "info"
        else:
            return "safe"

    def get_threat_assessment(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get detailed threat assessment
        """
        overall_grade = self.grade_threat(analysis_results)
        
        # Extract specific threat types and their severities
        threat_breakdown = {}
        for key, value in analysis_results.items():
            if isinstance(value, dict) and "severity" in value:
                threat_breakdown[key] = {
                    "severity": value.get("severity", "safe"),
                    "confidence": value.get("confidence", 0.0),
                    "details": value
                }
        
        return {
            "overall_threat_level": overall_grade,
            "threat_score": self._calculate_threat_score(analysis_results),
            "threat_breakdown": threat_breakdown,
            "recommendation": self._get_recommendation(overall_grade),
            "requires_human_review": overall_grade in ["warning", "block"]
        }

    def _calculate_threat_score(self, analysis_results: Dict[str, Any]) -> float:
        """
        Calculate numerical threat score between 0 and 1
        """
        score = 0.0
        max_possible_score = 0.0
        
        for key, value in analysis_results.items():
            if isinstance(value, dict) and "severity" in value:
                severity = value.get("severity", "safe")
                confidence = value.get("confidence", 0.5)
                
                weight = self.severity_weights.get(severity, 0.0)
                multiplier = self.threat_multipliers.get(key.replace("_analysis", ""), 1.0)
                
                score += weight * confidence * multiplier
                max_possible_score += 1.0 * 1.0 * multiplier  # Max possible for this component
        
        return min(1.0, score / max_possible_score if max_possible_score > 0 else 0.0)

    def _get_recommendation(self, threat_level: str) -> str:
        """
        Get action recommendation based on threat level
        """
        recommendations = {
            "safe": "Allow request/response to proceed",
            "info": "Log request/response for monitoring",
            "warning": "Flag for review, allow with monitoring",
            "block": "Block request/response, trigger alert"
        }
        
        return recommendations.get(threat_level, "Unknown")