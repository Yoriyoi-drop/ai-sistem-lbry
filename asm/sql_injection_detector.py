"""
Real SQL Injection Detection Engine
This module implements actual SQL injection detection logic based on 
common patterns and heuristics, not just simulation
"""
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class DetectionResult:
    is_malicious: bool
    confidence: float
    threat_level: str
    detected_patterns: List[str]
    explanation: str


class SQLInjectionDetector:
    """
    Advanced SQL Injection Detection Engine
    Uses multiple detection methods: signature matching, heuristic analysis, 
    and pattern recognition to detect SQL injection attempts
    """
    
    def __init__(self):
        # SQL injection patterns and keywords
        self.patterns = [
            # Union-based attacks
            r'(?i)(union\s+select|union\s+all\s+select)',
            # Boolean-based attacks (including 'OR 1=1', 'OR 1=2', etc.)
            r"(?i)(\s+or\s+['\"]?\d+['\"]?\s*[=<>]\s*['\"]?\d+['\"]?|\s+and\s+['\"]?\d+['\"]?\s*[=<>]\s*['\"]?\d+['\"]?)",
            # Time-based attacks
            r"(?i)(sleep\s*\(|benchmark\s*\(|waitfor\s+delay\s+|pg_sleep\s*\()",
            # Common SQL keywords in user input
            r"(?i)(drop\s+\w+|create\s+\w+|exec\s*\(|execute\s*\(|insert\s+into|delete\s+from|update\s+\w+\s+set)",
            # Comment bypass attempts
            r"(?i)(\s*\-\-|\s*#|\/\*|\*\/)",
            # SQL functions in user input
            r"(?i)(concat\s*\(|substring\s*\(|ascii\s*\(|char\s*\(|chr\s*\(|ord\s*\()",
            # Hex encoding
            r"(?i)(0x[0-9a-f]+|hex\s*\(|unhex\s*\()",
            # Alternative encodings
            r"(?i)(cast\s*\(|convert\s*\(|declare\s+|\@[\w]+)"
        ]
        
        # Context-aware patterns (sensitive to common SQL structures)
        self.context_patterns = [
            # Suspicious query structures
            r"(?i)(select.*from.*where.*=.*select)",
            r"(?i)(select.*case.*when.*then.*end)",
            r"(?i)(from.*information_schema|from.*pg_|from.*sysobjects)",
        ]
        
        # High-risk indicators
        self.high_risk_keywords = [
            'admin', 'password', 'user', 'login', 'auth',
            'master', 'root', 'sa', 'dbo', 'sysadmin'
        ]

    def analyze(self, query: str) -> DetectionResult:
        """
        Analyze a SQL query for injection patterns
        """
        if not query or not isinstance(query, str):
            return DetectionResult(
                is_malicious=False,
                confidence=0.0,
                threat_level="LOW",
                detected_patterns=[],
                explanation="Invalid input"
            )
        
        detected_patterns = []
        confidence_score = 0.0
        
        # Check against all patterns
        for i, pattern in enumerate(self.patterns):
            matches = re.findall(pattern, query)
            if matches:
                detected_patterns.extend(matches)
                # Increase confidence based on pattern severity
                confidence_score += (i + 1) * 0.15
        
        # Check context patterns (more severe)
        for i, pattern in enumerate(self.context_patterns):
            matches = re.findall(pattern, query, re.IGNORECASE)
            if matches:
                detected_patterns.extend(matches)
                confidence_score += (i + 1) * 0.25  # Higher weight for context patterns
        
        # Check for high-risk indicators
        query_lower = query.lower()
        for keyword in self.high_risk_keywords:
            if keyword in query_lower:
                confidence_score += 0.1
        
        # Consider length and complexity as heuristic
        if len(query) > 100:  # Suspiciously long queries
            confidence_score += 0.05
        if query.count("'") > 5:  # Multiple quotes suggest manipulation
            confidence_score += 0.1
        
        # Normalize confidence score
        confidence_score = min(1.0, confidence_score)
        
        # Determine threat level
        if confidence_score >= 0.8:
            threat_level = "CRITICAL"
            is_malicious = True
        elif confidence_score >= 0.5:
            threat_level = "HIGH" 
            is_malicious = True
        elif confidence_score >= 0.2:
            threat_level = "MEDIUM"
            is_malicious = True
        else:
            threat_level = "LOW"
            is_malicious = False
        
        # Create explanation
        explanation = self._generate_explanation(detected_patterns, confidence_score)
        
        return DetectionResult(
            is_malicious=is_malicious,
            confidence=confidence_score,
            threat_level=threat_level,
            detected_patterns=list(set(detected_patterns)),  # Remove duplicates
            explanation=explanation
        )
    
    def _generate_explanation(self, detected_patterns: List[str], confidence: float) -> str:
        """
        Generate human-readable explanation of the detection
        """
        if not detected_patterns:
            return "No SQL injection patterns detected in the query."
        
        explanation = f"Detected {len(detected_patterns)} potential SQL injection pattern(s): "
        explanation += ", ".join(detected_patterns[:3])  # Show first 3 patterns
        
        if len(detected_patterns) > 3:
            explanation += f" (and {len(detected_patterns) - 3} more patterns)"
        
        confidence_percent = int(confidence * 100)
        explanation += f". Confidence level: {confidence_percent}%"
        
        return explanation


# Global instance for easy access
detector = SQLInjectionDetector()


def detect_sql_injection(query: str) -> Dict:
    """
    Main function to detect SQL injection in a query
    """
    result = detector.analyze(query)
    
    return {
        "is_malicious": result.is_malicious,
        "confidence": result.confidence,
        "threat_level": result.threat_level,
        "detected_patterns": result.detected_patterns,
        "explanation": result.explanation
    }


if __name__ == "__main__":
    # Test the detector with real examples
    test_queries = [
        "SELECT * FROM users WHERE id = 1",
        "SELECT * FROM users WHERE id = 1 OR 1=1",
        "SELECT * FROM users WHERE name = 'admin' -- comment",
        "SELECT * FROM users WHERE name = 'admin' UNION SELECT password FROM admin_table",
        "SELECT * FROM users WHERE id = 1; DROP TABLE users; --",
        "SELECT * FROM users WHERE id = '1' OR '1'='1'",
    ]
    
    print("SQL Injection Detection Test Results:")
    print("=" * 50)
    
    for query in test_queries:
        result = detect_sql_injection(query)
        print(f"Query: {query}")
        print(f"  Malicious: {result['is_malicious']}")
        print(f"  Confidence: {result['confidence']:.2f}")
        print(f"  Threat Level: {result['threat_level']}")
        print(f"  Patterns: {result['detected_patterns']}")
        print("-" * 30)