"""
Notification background tasks

Created: 2025-11-26
"""

import logging
from typing import Dict, Any, List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from .celery_app import celery_app
from src.database.session import get_db_session
from src.database.models import User, SecurityScan, Threat

logger = logging.getLogger(__name__)

# Email configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@infiniteai.security")


@celery_app.task(bind=True, max_retries=3)
def send_email_notification(self, to_email: str, subject: str, body: str, html: bool = False):
    """
    Send email notification
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body content
        html: Whether body is HTML
    """
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        
        if html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            if SMTP_USER and SMTP_PASSWORD:
                server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent to {to_email}: {subject}")
        return {"status": "sent", "to": to_email}
    
    except Exception as e:
        logger.error(f"Error sending email to {to_email}: {e}")
        raise self.retry(exc=e, countdown=60)


@celery_app.task
def notify_scan_completed(scan_id: int):
    """
    Notify user when security scan is completed
    """
    try:
        with get_db_session() as db:
            scan = db.query(SecurityScan).filter(SecurityScan.id == scan_id).first()
            if not scan:
                logger.error(f"Scan {scan_id} not found")
                return
            
            user = db.query(User).filter(User.id == scan.user_id).first()
            if not user:
                logger.error(f"User {scan.user_id} not found")
                return
            
            # Prepare email
            subject = f"Security Scan Completed: {scan.scan_name}"
            body = f"""
            Hello {user.full_name or user.username},
            
            Your security scan "{scan.scan_name}" has completed.
            
            Target: {scan.target}
            Status: {scan.status.value}
            Summary: {scan.summary}
            
            Visit the dashboard to view detailed results.
            
            Best regards,
            Infinite AI Security Team
            """
            
            send_email_notification.delay(user.email, subject, body)
            
            logger.info(f"Sent scan completion notification for scan {scan_id}")
    
    except Exception as e:
        logger.error(f"Error sending scan notification: {e}")


@celery_app.task
def notify_critical_threat(threat_id: int):
    """
    Notify user immediately about critical threats
    """
    try:
        with get_db_session() as db:
            threat = db.query(Threat).filter(Threat.id == threat_id).first()
            if not threat:
                return
            
            scan = db.query(SecurityScan).filter(SecurityScan.id == threat.scan_id).first()
            if not scan:
                return
            
            user = db.query(User).filter(User.id == scan.user_id).first()
            if not user:
                return
            
            subject = f"🚨 CRITICAL THREAT DETECTED: {threat.title}"
            body = f"""
            CRITICAL SECURITY ALERT
            
            A critical threat has been detected:
            
            Threat Type: {threat.threat_type}
            Severity: {threat.severity.value}
            Title: {threat.title}
            Description: {threat.description}
            Source: {threat.source}
            
            IMMEDIATE ACTION REQUIRED
            
            Please review and mitigate this threat immediately.
            
            Infinite AI Security System
            """
            
            send_email_notification.delay(user.email, subject, body)
            
            # TODO: Also send SMS, Slack, or other urgent notifications
            
            logger.info(f"Sent critical threat notification for threat {threat_id}")
    
    except Exception as e:
        logger.error(f"Error sending threat notification: {e}")


@celery_app.task
def send_daily_digest(user_id: int):
    """
    Send daily security digest to user
    """
    try:
        with get_db_session() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return
            
            # TODO: Gather daily statistics
            # - Scans completed
            # - New threats found
            # - Security score changes
            # - Recommendations
            
            subject = "Daily Security Digest"
            body = f"""
            Hello {user.full_name or user.username},
            
            Here's your daily security digest:
            
            [Statistics will be included here]
            
            Stay secure,
            Infinite AI Security Team
            """
            
            send_email_notification.delay(user.email, subject, body)
    
    except Exception as e:
        logger.error(f"Error sending daily digest: {e}")


@celery_app.task
def send_webhook_notification(webhook_url: str, data: Dict[str, Any]):
    """
    Send webhook notification to external service
    """
    try:
        import requests
        
        response = requests.post(webhook_url, json=data, timeout=10)
        response.raise_for_status()
        
        logger.info(f"Webhook sent to {webhook_url}")
        return {"status": "sent", "url": webhook_url}
    
    except Exception as e:
        logger.error(f"Error sending webhook: {e}")
        raise
