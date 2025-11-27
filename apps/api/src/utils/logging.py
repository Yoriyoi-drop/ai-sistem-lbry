import logging
import logging.config
import json
import os
from datetime import datetime
from typing import Dict, Any

# Configuration for structured logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s %(funcName)s:%(lineno)d: %(message)s"
        },
        "json": {
            "()": "src.utils.logging.JSONFormatter"
        }
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "formatter": "detailed",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
        "error_file": {
            "level": "ERROR",
            "formatter": "detailed",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/error.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        }
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False
        },
        "security": {
            "handlers": ["file", "error_file"],
            "level": "INFO",
            "propagate": False
        },
        "api": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}

class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging
    """
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_entry["user_id"] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry["request_id"] = record.request_id
        if hasattr(record, 'ip_address'):
            log_entry["ip_address"] = record.ip_address
        if hasattr(record, 'threat_type'):
            log_entry["threat_type"] = record.threat_type
            
        return json.dumps(log_entry)


class SecurityLogger:
    """
    Specialized logger for security events
    """
    def __init__(self, name: str = "security"):
        self.logger = logging.getLogger(name)
        
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
    def log_login(self, user_id: str, ip_address: str, success: bool, details: Dict[str, Any] = None):
        """Log a user login event"""
        self.logger.info(
            "User login event",
            extra={
                "user_id": user_id,
                "ip_address": ip_address,
                "success": success,
                "action": "login",
                "details": details or {}
            }
        )
    
    def log_logout(self, user_id: str, ip_address: str, details: Dict[str, Any] = None):
        """Log a user logout event"""
        self.logger.info(
            "User logout event",
            extra={
                "user_id": user_id,
                "ip_address": ip_address,
                "action": "logout",
                "details": details or {}
            }
        )
    
    def log_failed_login(self, username: str, ip_address: str, reason: str = "Invalid credentials"):
        """Log a failed login attempt"""
        self.logger.warning(
            "Failed login attempt",
            extra={
                "username": username,
                "ip_address": ip_address,
                "reason": reason,
                "action": "failed_login"
            }
        )
    
    def log_access(self, user_id: str, resource: str, action: str, ip_address: str, success: bool = True):
        """Log an access event"""
        self.logger.info(
            f"Access event: {user_id} {action} {resource}",
            extra={
                "user_id": user_id,
                "resource": resource,
                "action": action,
                "ip_address": ip_address,
                "success": success
            }
        )
    
    def log_security_scan(self, scan_id: str, scan_type: str, target: str, findings_count: int, ip_address: str):
        """Log a security scan event"""
        self.logger.info(
            f"Security scan completed: {scan_id}",
            extra={
                "scan_id": scan_id,
                "scan_type": scan_type,
                "target": target,
                "findings_count": findings_count,
                "ip_address": ip_address,
                "action": "security_scan"
            }
        )
    
    def log_threat_detected(self, threat_type: str, severity: str, source_ip: str, payload: str, confidence: float):
        """Log a threat detection event"""
        self.logger.warning(
            f"Threat detected: {threat_type}",
            extra={
                "threat_type": threat_type,
                "severity": severity,
                "source_ip": source_ip,
                "payload": payload[:100] if payload else "",  # Truncate long payloads
                "confidence": confidence,
                "action": "threat_detected"
            }
        )
    
    def log_config_change(self, user_id: str, config_name: str, old_value: str, new_value: str, ip_address: str):
        """Log a configuration change event"""
        self.logger.warning(
            f"Configuration change: {config_name}",
            extra={
                "user_id": user_id,
                "config_name": config_name,
                "old_value": old_value,
                "new_value": new_value,
                "ip_address": ip_address,
                "action": "config_change"
            }
        )


def setup_logging():
    """
    Setup logging configuration
    """
    os.makedirs("logs", exist_ok=True)
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Also setup root logger to use our JSON formatter for file logs
    root_logger = logging.getLogger()
    json_handler = logging.handlers.RotatingFileHandler(
        "logs/structured.log",
        maxBytes=10485760,  # 10MB
        backupCount=5,
    )
    json_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(json_handler)
    
    return root_logger


# Initialize logging
setup_logging()
security_logger = SecurityLogger()

# Convenience functions
def get_security_logger():
    return security_logger

def get_logger(name: str):
    return logging.getLogger(name)