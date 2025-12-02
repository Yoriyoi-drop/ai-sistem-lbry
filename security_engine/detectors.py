"""
Prompt Injection Detector Module
Detects attempts to manipulate AI behavior through prompt injection
"""
import re
from typing import Dict, List, Any
import asyncio


class PromptInjectionDetector:
    """
    Detects prompt injection attempts in user input
    """
    def __init__(self):
        # Common prompt injection patterns
        self.injection_patterns = [
            # Instructions to ignore previous instructions
            r"(?i)\bignore.*previous.*instructions?\b",
            r"(?i)\bforget.*previous.*instructions?\b",
            r"(?i)\bdisregard.*previous.*instructions?\b",
            r"(?i)\boverride.*instructions?\b",
            
            # Attempts to change role
            r"(?i)\bact.*as\b.*\b(evil|malicious|hacker|attacker)\b",
            r"(?i)\brole.*is\b.*\b(evil|malicious|hacker|attacker)\b",
            
            # System message manipulation
            r"(?i)\b[system|admin|root|user]::",
            r"(?i)\bsystem\b.*:",
            r"(?i)\buser\b.*:",
            
            # Separator injection
            r"(?i)\[sep\]|\[sep\+\]|\[sepl\]",
            r"---\s*system\s*---",
            r"###\s*system\s*###",
            
            # Common jailbreak phrases
            r"(?i)\bdo.*not.*follow.*previous.*instructions?\b",
            r"(?i)\bnow.*you.*are\b",
            r"(?i)\bfrom.*now.*on\b",
            r"(?i)\bignore.*all.*safety.*guidelines\b",
            r"(?i)\bignore.*safety.*rules\b",
        ]
        
        # Dangerous keywords
        self.dangerous_keywords = [
            "system", "admin", "root", "user", "role", "prompt", "instruction",
            "ignore", "forget", "disregard", "override", "bypass", "evade"
        ]

    async def detect(self, text: str) -> Dict[str, Any]:
        """
        Detect prompt injection attempts
        """
        findings = []
        severity = "safe"
        confidence = 0.0
        
        # Check for pattern matches
        for i, pattern in enumerate(self.injection_patterns):
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                findings.append({
                    "type": "prompt_injection",
                    "pattern_id": i,
                    "matched_text": matches,
                    "severity": "high" if i < 5 else "medium"  # First few patterns are more critical
                })
                
                # Update severity based on most critical finding
                pattern_severity = "high" if i < 5 else "medium"
                if pattern_severity == "high":
                    severity = "block"
                    confidence = 0.9
                elif severity != "block" and pattern_severity == "medium":
                    severity = "warning"
                    confidence = 0.7
        
        # Check for dangerous keywords frequency
        text_lower = text.lower()
        keyword_matches = []
        for keyword in self.dangerous_keywords:
            if keyword in text_lower:
                keyword_matches.append(keyword)
        
        if len(keyword_matches) > 3:  # If multiple dangerous keywords
            findings.append({
                "type": "potential_injection",
                "keywords": keyword_matches,
                "severity": "medium"
            })
            if severity == "safe":
                severity = "warning"
                confidence = 0.6
        
        # Calculate confidence based on number of findings
        if not findings:
            confidence = 0.1  # Low confidence in safety
        elif confidence == 0.0:
            confidence = min(0.5, len(findings) * 0.2)  # Medium confidence based on findings count
        
        return {
            "is_malicious": len(findings) > 0,
            "severity": severity,
            "confidence": confidence,
            "findings": findings,
            "matched_patterns": [f["matched_text"] for f in findings if "matched_text" in f]
        }


class JailbreakDetector:
    """
    Detects jailbreak attempts designed to bypass AI safety measures
    """
    def __init__(self):
        self.jailbreak_patterns = [
            # DAN (Do Anything Now) pattern
            r"(?i)\b(?:act|role|be|become)\b.*\bDAN\b",
            r"(?i)\bDAN\b.*\bcan.*do.*anything\b",
            
            # Repetition and character manipulation
            r"(?i)(?:[^\w\s]|\\s)*[a-z](?:[^\w\s]|\\s)*[a-z](?:[^\w\s]|\\s)*[a-z](?:[^\w\s]|\\s)*",
            
            # Common jailbreak phrases
            r"(?i)\b(developer|system|openai|creator)\b.*\bmode\b",
            r"(?i)\b(sandbox|testing|simulation)\b.*\bmode\b",
            r"(?i)\b[tq]:?[^.]*\b",
            
            # Reverse psychology
            r"(?i)\b(?:I.*shouldn't|you.*can't|it.*wouldn't)\b.*\b(?:but|however)\b.*\b(?:what.*if|suppose|imagine)\b",
        ]
        
        self.jailbreak_keywords = [
            "DAN", "jailbreak", "bypass", "system prompt", "ignore filters",
            "roleplay as", "act as", "developer mode", "debug mode"
        ]

    async def detect(self, text: str) -> Dict[str, Any]:
        """
        Detect jailbreak attempts
        """
        findings = []
        severity = "safe"
        confidence = 0.0
        
        # Check for pattern matches
        for i, pattern in enumerate(self.jailbreak_patterns):
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                findings.append({
                    "type": "jailbreak_attempt",
                    "pattern_id": i,
                    "matched_text": matches,
                    "severity": "high"
                })
                severity = "block"
                confidence = 0.9
        
        # Check for jailbreak keywords
        text_lower = text.lower()
        keyword_matches = []
        for keyword in self.jailbreak_keywords:
            if keyword.lower() in text_lower:
                keyword_matches.append(keyword)
        
        if keyword_matches:
            findings.append({
                "type": "jailbreak_keywords",
                "keywords": keyword_matches,
                "severity": "high" if len(keyword_matches) > 2 else "medium"
            })
            
            if len(keyword_matches) > 2:
                severity = "block"
                confidence = 0.85
            elif severity == "safe":
                severity = "warning"
                confidence = 0.65
        
        # Calculate confidence
        if not findings:
            confidence = 0.1
        elif confidence == 0.0:
            confidence = min(0.7, len(findings) * 0.3)
        
        return {
            "is_malicious": len(findings) > 0,
            "severity": severity,
            "confidence": confidence,
            "findings": findings,
            "matched_keywords": keyword_matches
        }


class MaliciousCodeDetector:
    """
    Detects potentially malicious code in text
    """
    def __init__(self):
        self.code_patterns = [
            # File system access
            r"(?i)\b(os|sys|subprocess|exec|eval|compile)\b.*\b(remove|unlink|open|rmdir|mkdir|chown|chmod)\b",
            r"(?i)\bimport.*\b(subprocess|os|sys|shutil|glob)\b",
            
            # Network access
            r"(?i)\bsocket\b|\b(requests|urllib|http|https)\b.*\b(get|post|put|delete)\b",
            
            # Command execution
            r"(?i)\bsubprocess\.(call|run|Popen|check_output)\b",
            r"(?i)\bos\.(system|popen|spawn|exec)\b",
            
            # Dangerous functions
            r"(?i)\b(eval|exec|compile|execfile|file_input|input_encoding)\b",
            r"(?i)\b__import__|getattr|setattr|delattr|hasattr\b",
            
            # Shell commands
            r"(?i)(?:sh|bash|cmd|powershell|shell)\s+",
            
            # Potential XSS
            r"(?i)<script.*?>|javascript:|vbscript:|on\w+\s*=",
            
            # SQL injection patterns
            r"(?i)(union\s+select|drop\s+\w+|exec\s*\(|';\s*--)",
        ]
        
        self.dangerous_keywords = [
            "rm -rf", "format", "delete", "shutdown", "reboot", "root", "admin",
            "__import__", "eval", "exec", "subprocess", "os.system"
        ]

    async def detect(self, text: str) -> Dict[str, Any]:
        """
        Detect malicious code patterns
        """
        findings = []
        severity = "safe"
        confidence = 0.0
        
        # Check for code patterns
        for i, pattern in enumerate(self.code_patterns):
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                findings.append({
                    "type": "malicious_code",
                    "pattern_id": i,
                    "matched_text": matches,
                    "severity": "high" if i < 4 else "medium"
                })
                
                if i < 4:  # Critical patterns
                    severity = "block"
                    confidence = 0.95
                elif severity != "block":
                    severity = "warning"
                    confidence = 0.75
        
        # Check for dangerous keywords
        text_lower = text.lower()
        keyword_matches = []
        for keyword in self.dangerous_keywords:
            if keyword in text_lower:
                keyword_matches.append(keyword)
        
        if keyword_matches:
            findings.append({
                "type": "dangerous_keywords",
                "keywords": keyword_matches,
                "severity": "high" if any(k in ["rm -rf", "format", "__import__", "eval", "exec"] for k in keyword_matches) else "medium"
            })
            
            if any(k in ["rm -rf", "format", "__import__", "eval", "exec"] for k in keyword_matches):
                severity = "block"
                confidence = 0.9
            elif severity == "safe":
                severity = "warning"
                confidence = 0.65
        
        # Calculate confidence
        if not findings:
            confidence = 0.1
        elif confidence == 0.0:
            confidence = min(0.8, len(findings) * 0.25)
        
        return {
            "is_malicious": len(findings) > 0,
            "severity": severity,
            "confidence": confidence,
            "findings": findings,
            "matched_patterns": [f["matched_text"] for f in findings if "matched_text" in f]
        }


class SensitiveDataDetector:
    """
    Detects sensitive data like passwords, tokens, etc.
    """
    def __init__(self):
        self.sensitive_patterns = [
            # API keys
            r"(?i)(?:^|[^0-9])(ak|sk|api|token|key)[_-]?(?:[a-z0-9]{10,})\b",
            r"(?i)(?:api|auth|bearer|token|key|secret|password)\s*[:=]\s*[a-z0-9_\-]{10,}",
            
            # Credit cards (simplified)
            r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
            
            # Emails
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            
            # Phone numbers
            r"\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b",
            
            # IP addresses
            r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
            
            # Potential SSN
            r"\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b",
            
            # Password patterns
            r"(?i)password\s*[:=]\s*\w+",
            r"(?i)pwd\s*[:=]\s*\w+",
        ]
        
        self.sensitive_keywords = [
            "password", "passwd", "pwd", "secret", "token", "api_key", 
            "private_key", "ssh_key", "access_key", "auth", "credential"
        ]

    async def detect(self, text: str) -> Dict[str, Any]:
        """
        Detect sensitive data patterns
        """
        findings = []
        severity = "safe"
        confidence = 0.0
        
        # Check for sensitive patterns
        for i, pattern in enumerate(self.sensitive_patterns):
            matches = re.findall(pattern, text)
            if matches:
                findings.append({
                    "type": "sensitive_data",
                    "pattern_id": i,
                    "matched_text": matches[:3],  # Limit to first 3 matches
                    "severity": "high" if i < 3 else "medium"
                })
                
                if i < 2:  # API keys and credit cards are high priority
                    if severity != "block":
                        severity = "warning"
                        confidence = 0.7
                elif severity == "safe":
                    severity = "info"
                    confidence = 0.5
        
        # Check for sensitive keywords
        text_lower = text.lower()
        keyword_matches = []
        for keyword in self.sensitive_keywords:
            if keyword in text_lower:
                keyword_matches.append(keyword)
        
        if keyword_matches:
            findings.append({
                "type": "sensitive_keywords",
                "keywords": keyword_matches,
                "severity": "medium" if len(keyword_matches) > 1 else "info"
            })
            
            if len(keyword_matches) > 1 and severity != "block":
                severity = "warning"
                confidence = max(confidence, 0.6)
            elif severity == "safe":
                severity = "info"
                confidence = max(confidence, 0.4)
        
        # Calculate confidence
        if not findings:
            confidence = 0.1
        elif confidence == 0.0:
            confidence = min(0.7, len(findings) * 0.2)
        
        return {
            "is_sensitive": len(findings) > 0,
            "severity": severity,
            "confidence": confidence,
            "findings": findings,
            "matched_patterns": [f["matched_text"] for f in findings if "matched_text" in f]
        }