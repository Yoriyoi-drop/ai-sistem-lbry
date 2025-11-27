"""
Advanced Security Detection Engine
Implements multiple detection mechanisms with AI/ML capabilities
"""
import re
import hashlib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import sqlite3
import json
from enum import Enum


class ThreatType(Enum):
    SQL_INJECTION = "SQL_INJECTION"
    XSS = "XSS"
    COMMAND_INJECTION = "COMMAND_INJECTION"
    AUTH_BRUTEFORCE = "AUTH_BRUTEFORCE"
    PATH_TRAVERSAL = "PATH_TRAVERSAL"


@dataclass
class DetectionResult:
    threat_type: ThreatType
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    confidence: float
    detected_patterns: List[str]
    explanation: str
    timestamp: datetime
    request_details: Optional[Dict] = None


class AdvancedSecurityDetector:
    """
    Advanced Security Detection Engine with multiple detection modes
    """
    
    def __init__(self):
        # XSS patterns
        self.xss_patterns = [
            r'(?i)(<script[^>]*>.*?</script>)',
            r'(?i)(javascript\s*:)',
            r'(?i)(on\w+\s*=)',
            r'(?i)(<iframe[^>]*>)',
            r'(?i)(<object[^>]*>)',
            r'(?i)(<embed[^>]*>)',
            r'(?i)(<svg[^>]*>)',
            r'(?i)(onerror\s*=)',
        ]
        
        # Command injection patterns
        self.command_patterns = [
            r'(?i)(\|\s*cat\s+)',
            r'(?i)(\|\s*ls\s+)',
            r'(?i)(\|\s*rm\s+)',
            r'(?i)(\|\s*chmod\s+)',
            r'(?i)(\|\s*chown\s+)',
            r'(?i)(`.*?`)',
            r'(?i)(\$\([^)]*\))',
            r'(?i)(\|\s*nc\s+)',
            r'(?i)(\|\s*netcat\s+)',
            r'(?i)(\|\s*wget\s+)',
            r'(?i)(\|\s*curl\s+)',
            r'(?i)(\|\s*python\s+)',
            r'(?i)(\|\s*perl\s+)',
            r'(?i)(\|\s*php\s+)',
        ]
        
        # Path traversal patterns
        self.path_traversal_patterns = [
            r'(\.\./)',
            r'(\.\.\\)',
            r'(%2e%2e%2f)',
            r'(%2e%2e%5c)',
            r'(\.\.\%2f)',
            r'(\.\.\%5c)',
            r'(%2e%2e%2f)',
        ]
        
        # Authentication brute force detection
        self.auth_patterns = [
            r'(?i)(password\s*[\'"][^\'"]{0,4}[\'"])',  # Short passwords
            r'(?i)(admin["\']?\s*[\'"]?(or|and))',      # Admin login attempts
            r'(?i)(root["\']?\s*[\'"]?(or|and))',       # Root login attempts
        ]
        
        # Initialize database connection
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for storing detection results"""
        self.conn = sqlite3.connect('security_detections.db', check_same_thread=False)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                threat_type TEXT,
                severity TEXT,
                confidence REAL,
                detected_patterns TEXT,
                explanation TEXT,
                timestamp TEXT,
                request_details TEXT,
                hash TEXT UNIQUE
            )
        ''')
        self.conn.commit()
    
    def detect_xss(self, content: str) -> DetectionResult:
        """Detect potential XSS in content"""
        detected_patterns = []
        confidence = 0.0
        
        for pattern in self.xss_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            if matches:
                detected_patterns.extend(matches)
                confidence += len(matches) * 0.15
        
        confidence = min(1.0, confidence + (len(detected_patterns) * 0.1))
        
        if confidence >= 0.8:
            severity = "CRITICAL"
        elif confidence >= 0.5:
            severity = "HIGH"
        elif confidence >= 0.2:
            severity = "MEDIUM"
        else:
            severity = "LOW"
        
        explanation = f"Detected {len(detected_patterns)} potential XSS pattern(s)" if detected_patterns else "No XSS patterns detected"
        
        return DetectionResult(
            threat_type=ThreatType.XSS,
            severity=severity,
            confidence=confidence,
            detected_patterns=list(set(detected_patterns)),
            explanation=explanation,
            timestamp=datetime.now()
        )
    
    def detect_command_injection(self, command: str) -> DetectionResult:
        """Detect potential command injection"""
        detected_patterns = []
        confidence = 0.0
        
        for pattern in self.command_patterns:
            matches = re.findall(pattern, command, re.IGNORECASE)
            if matches:
                detected_patterns.extend(matches)
                confidence += len(matches) * 0.2
        
        # Check for command execution symbols
        if '|' in command or '`' in command or '$(' in command:
            confidence += 0.3
        
        confidence = min(1.0, confidence)
        
        if confidence >= 0.8:
            severity = "CRITICAL"
        elif confidence >= 0.5:
            severity = "HIGH"
        elif confidence >= 0.2:
            severity = "MEDIUM"
        else:
            severity = "LOW"
        
        explanation = f"Detected {len(detected_patterns)} potential command injection pattern(s)" if detected_patterns else "No command injection patterns detected"
        
        return DetectionResult(
            threat_type=ThreatType.COMMAND_INJECTION,
            severity=severity,
            confidence=confidence,
            detected_patterns=list(set(detected_patterns)),
            explanation=explanation,
            timestamp=datetime.now()
        )
    
    def detect_path_traversal(self, path: str) -> DetectionResult:
        """Detect potential path traversal attacks"""
        detected_patterns = []
        confidence = 0.0
        
        for pattern in self.path_traversal_patterns:
            matches = re.findall(pattern, path, re.IGNORECASE)
            if matches:
                detected_patterns.extend(matches)
                confidence += len(matches) * 0.3
        
        confidence = min(1.0, confidence)
        
        if confidence >= 0.8:
            severity = "CRITICAL"
        elif confidence >= 0.5:
            severity = "HIGH"
        elif confidence >= 0.2:
            severity = "MEDIUM"
        else:
            severity = "LOW"
        
        explanation = f"Detected {len(detected_patterns)} potential path traversal pattern(s)" if detected_patterns else "No path traversal patterns detected"
        
        return DetectionResult(
            threat_type=ThreatType.PATH_TRAVERSAL,
            severity=severity,
            confidence=confidence,
            detected_patterns=list(set(detected_patterns)),
            explanation=explanation,
            timestamp=datetime.now()
        )
    
    def detect_auth_bruteforce(self, login_request: Dict) -> DetectionResult:
        """Detect potential authentication brute force attempts"""
        detected_patterns = []
        confidence = 0.0
        
        username = login_request.get('username', '')
        password = login_request.get('password', '')
        
        # Check for suspicious patterns
        for pattern in self.auth_patterns:
            if re.search(pattern, f"{username} {password}", re.IGNORECASE):
                detected_patterns.append(pattern)
                confidence += 0.25
        
        # Check for common attack usernames/passwords
        common_attacks = ['admin', 'root', 'password', '123456', 'test']
        if username.lower() in common_attacks or password in common_attacks:
            confidence += 0.2
            detected_patterns.append(f"Suspicious credentials: {username}/{password}")
        
        # Short passwords are often suspicious
        if len(password) < 4:
            confidence += 0.15
            detected_patterns.append(f"Short password: {password}")
        
        confidence = min(1.0, confidence)
        
        if confidence >= 0.8:
            severity = "CRITICAL"
        elif confidence >= 0.5:
            severity = "HIGH"
        elif confidence >= 0.2:
            severity = "MEDIUM"
        else:
            severity = "LOW"
        
        explanation = f"Detected {len(detected_patterns)} potential brute force pattern(s)" if detected_patterns else "No brute force patterns detected"
        
        return DetectionResult(
            threat_type=ThreatType.AUTH_BRUTEFORCE,
            severity=severity,
            confidence=confidence,
            detected_patterns=detected_patterns,
            explanation=explanation,
            timestamp=datetime.now(),
            request_details=login_request
        )
    
    def store_detection(self, result: DetectionResult) -> int:
        """Store detection result in database"""
        try:
            # Create a hash of the detection to prevent duplicates
            hash_content = f"{result.threat_type.value}{result.confidence}{result.timestamp.isoformat()}"
            detection_hash = hashlib.sha256(hash_content.encode()).hexdigest()
            
            # Convert patterns to JSON string
            patterns_json = json.dumps(result.detected_patterns)
            details_json = json.dumps(result.request_details) if result.request_details else "null"
            
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO detections 
                (threat_type, severity, confidence, detected_patterns, explanation, 
                 timestamp, request_details, hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result.threat_type.value,
                result.severity,
                result.confidence,
                patterns_json,
                result.explanation,
                result.timestamp.isoformat(),
                details_json,
                detection_hash
            ))
            
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error storing detection: {e}")
            return None
    
    def get_recent_detections(self, limit: int = 10) -> List[Dict]:
        """Get recent security detections"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM detections 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            
            results = []
            for row in rows:
                detection = dict(zip(columns, row))
                detection['detected_patterns'] = json.loads(detection['detected_patterns'])
                if detection['request_details'] != 'null':
                    detection['request_details'] = json.loads(detection['request_details'])
                results.append(detection)
            
            return results
        except Exception as e:
            print(f"Error retrieving detections: {e}")
            return []


# Global instance
advanced_detector = AdvancedSecurityDetector()