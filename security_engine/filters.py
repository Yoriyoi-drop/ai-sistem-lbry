"""
Filters Module for Security Engine
Contains sanitization and content filtering functionality
"""
import re
from typing import Dict, Any, Optional


class OutputSanitizer:
    """
    Sanitizes AI output to remove potentially harmful content
    """
    def __init__(self):
        # Patterns to redact or remove
        self.redaction_patterns = [
            # Potential API keys or tokens
            (r"(?i)(api|auth|bearer|token|key|secret|password)\s*[:=]\s*([a-z0-9_\-]{10,})", 
             r'\1: [REDACTED_TOKEN]'),
            
            # Credit cards (simplified)
            (r"\b(\d{4}[-\s]?){3}(\d{4})\b", r"****-****-****-\4"),
            
            # Passwords
            (r"(?i)password\s*[:=]\s*(\w+)", r"password: [REDACTED]"),
            (r"(?i)pwd\s*[:=]\s*(\w+)", r"pwd: [REDACTED]"),
        ]
        
        self.removal_patterns = [
            # Script tags
            r"(?i)<script[^>]*>.*?</script>",
            r"(?i)<iframe[^>]*>.*?</iframe>",
            
            # JavaScript events
            r"(?i)on\w+\s*=\s*['\"][^'\"]*['\"]",
        ]

    def needs_sanitization(self, text: str) -> bool:
        """
        Check if text needs sanitization
        """
        for pattern, _ in self.redaction_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        for pattern in self.removal_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False

    def sanitize(self, text: str) -> str:
        """
        Sanitize the text by redacting or removing harmful content
        """
        result = text
        
        # Apply redaction patterns
        for pattern, replacement in self.redaction_patterns:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        # Apply removal patterns
        for pattern in self.removal_patterns:
            result = re.sub(pattern, "", result, flags=re.IGNORECASE)
        
        return result


class ContextGuard:
    """
    Guards against context leakage and ensures proper context handling
    """
    def __init__(self):
        self.context_keywords = [
            "previous", "prior", "earlier", "first", "initial", 
            "original", "above", "below", "before", "after"
        ]

    def check_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check context for potential security issues
        """
        issues = []
        
        # Check for sensitive keys in context
        sensitive_keys = [
            "password", "token", "secret", "api_key", "auth", "credential",
            "pwd", "passwd", "key"
        ]
        
        for key in sensitive_keys:
            if key in context:
                issues.append({
                    "type": "sensitive_context_data",
                    "key": key,
                    "severity": "high"
                })
        
        # Check for large context size
        context_size = len(str(context))
        if context_size > 100000:  # 100KB threshold
            issues.append({
                "type": "large_context",
                "size": context_size,
                "severity": "medium"
            })
        
        return {
            "is_safe": len(issues) == 0,
            "issues": issues,
            "risk_level": self._calculate_risk_level(issues)
        }

    def check_leakage(self, output: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if the output contains sensitive information from context
        """
        leakage_issues = []
        
        # Check for sensitive values from context appearing in output
        for key, value in context.items():
            if isinstance(value, str):
                if len(value) > 10 and value.lower() in output.lower():  # Potential leakage
                    # Don't flag short values that might be common
                    if len(value) > 20 or any(char.isdigit() for char in value):
                        leakage_issues.append({
                            "type": "context_leakage",
                            "key": key,
                            "value_length": len(str(value)),
                            "severity": "high"
                        })
        
        return {
            "has_leakage": len(leakage_issues) > 0,
            "leakage_issues": leakage_issues,
            "risk_level": self._calculate_risk_level(leakage_issues)
        }

    def _calculate_risk_level(self, issues: list) -> str:
        """
        Calculate risk level based on issues
        """
        if not issues:
            return "safe"
        
        high_risk = any(issue.get("severity") == "high" for issue in issues)
        medium_risk = any(issue.get("severity") == "medium" for issue in issues)
        
        if high_risk:
            return "high"
        elif medium_risk:
            return "medium"
        else:
            return "low"


class ProfanityFilter:
    """
    Filters profanity and inappropriate content
    """
    def __init__(self):
        # In practice, you'd want a more comprehensive list
        # This is just a basic example
        self.profanity_patterns = [
            r"(?i)\bfuck\b",
            r"(?i)\bshit\b",
            r"(?i)\bdamn\b",
            r"(?i)\bhell\b",
            r"(?i)\bbitch\b",
            r"(?i)\bast\b",
            r"(?i)\basshole\b",
            r"(?i)\bstupid\b",
            r"(?i)\bidiot\b",
            r"(?i)\bdumb\b",
        ]
        
        # Contextual profanity that might be more subtle
        self.contextual_patterns = [
            r"(?i)\byou suck\b",
            r"(?i)\bgo to hell\b",
            r"(?i)\bi hate you\b",
        ]

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for profanity
        """
        matches = []
        score = 0.0
        
        # Check for direct profanity
        for i, pattern in enumerate(self.profanity_patterns):
            found_matches = re.findall(pattern, text)
            if found_matches:
                matches.extend(found_matches)
                # Direct profanity gets higher weight
                score += 0.2 * len(found_matches)
        
        # Check for contextual profanity
        for pattern in self.contextual_patterns:
            found_matches = re.findall(pattern, text)
            if found_matches:
                matches.extend(found_matches)
                score += 0.1 * len(found_matches)
        
        # Cap the score at 1.0
        score = min(1.0, score)
        
        severity = "safe"
        if score >= 0.5:
            severity = "block"
        elif score >= 0.2:
            severity = "warning"
        elif score > 0:
            severity = "info"
        
        return {
            "profanity_count": len(matches),
            "matched_words": matches,
            "score": score,
            "severity": severity,
            "needs_review": score > 0.1
        }

    def filter_text(self, text: str) -> str:
        """
        Filter profanity from text (optional method)
        """
        # For now, just return original text
        # In production, you might replace with ***
        return text