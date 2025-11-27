"""
Report generation background tasks

Created: 2025-11-26
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any
import json

from .celery_app import celery_app
from src.database.session import get_db_session
from src.database.models import User, SecurityScan, Threat, Vulnerability, ThreatLevel

logger = logging.getLogger(__name__)


@celery_app.task
def generate_scan_report(scan_id: int) -> Dict[str, Any]:
    """
    Generate comprehensive report for a security scan
    
    Args:
        scan_id: Security scan ID
        
    Returns:
        Report data dictionary
    """
    try:
        with get_db_session() as db:
            scan = db.query(SecurityScan).filter(SecurityScan.id == scan_id).first()
            if not scan:
                return {"error": "Scan not found"}
            
            # Count threats by severity
            threats = db.query(Threat).filter(Threat.scan_id == scan_id).all()
            threat_summary = {
                "critical": sum(1 for t in threats if t.severity == ThreatLevel.CRITICAL),
                "high": sum(1 for t in threats if t.severity == ThreatLevel.HIGH),
                "medium": sum(1 for t in threats if t.severity == ThreatLevel.MEDIUM),
                "low": sum(1 for t in threats if t.severity == ThreatLevel.LOW),
                "info": sum(1 for t in threats if t.severity == ThreatLevel.INFO),
            }
            
            # Count vulnerabilities
            vulns = db.query(Vulnerability).filter(Vulnerability.scan_id == scan_id).all()
            vuln_summary = {
                "critical": sum(1 for v in vulns if v.severity == ThreatLevel.CRITICAL),
                "high": sum(1 for v in vulns if v.severity == ThreatLevel.HIGH),
                "medium": sum(1 for v in vulns if v.severity == ThreatLevel.MEDIUM),
                "low": sum(1 for v in vulns if v.severity == ThreatLevel.LOW),
            }
            
            report = {
                "scan_id": scan_id,
                "scan_name": scan.scan_name,
                "target": scan.target,
                "scan_type": scan.scan_type,
                "started_at": scan.started_at.isoformat() if scan.started_at else None,
                "completed_at": scan.completed_at.isoformat() if scan.completed_at else None,
                "status": scan.status.value,
                "summary": {
                    "total_threats": len(threats),
                    "total_vulnerabilities": len(vulns),
                    "threat_breakdown": threat_summary,
                    "vulnerability_breakdown": vuln_summary,
                },
                "threats": [
                    {
                        "type": t.threat_type,
                        "severity": t.severity.value,
                        "title": t.title,
                        "description": t.description,
                    }
                    for t in threats[:10]  # Top 10 threats
                ],
                "vulnerabilities": [
                    {
                        "cve_id": v.cve_id,
                        "title": v.title,
                        "severity": v.severity.value,
                        "cvss_score": v.cvss_score,
                    }
                    for v in vulns[:10]  # Top 10 vulnerabilities
                ],
                "generated_at": datetime.utcnow().isoformat(),
            }
            
            logger.info(f"Generated report for scan {scan_id}")
            return report
    
    except Exception as e:
        logger.error(f"Error generating scan report: {e}")
        raise


@celery_app.task
def generate_daily_security_report(user_id: int = None):
    """
    Generate daily security report for user or all users
    """
    try:
        with get_db_session() as db:
            if user_id:
                users = [db.query(User).filter(User.id == user_id).first()]
            else:
                users = db.query(User).filter(User.is_active == True).all()
            
            reports = []
            
            for user in users:
                if not user:
                    continue
                
                # Get scans from last 24 hours
                yesterday = datetime.utcnow() - timedelta(days=1)
                recent_scans = db.query(SecurityScan).filter(
                    SecurityScan.user_id == user.id,
                    SecurityScan.created_at >= yesterday
                ).all()
                
                # Aggregate statistics
                total_threats = 0
                total_vulns = 0
                
                for scan in recent_scans:
                    threats = db.query(Threat).filter(Threat.scan_id == scan.id).count()
                    vulns = db.query(Vulnerability).filter(Vulnerability.scan_id == scan.id).count()
                    total_threats += threats
                    total_vulns += vulns
                
                report = {
                    "user_id": user.id,
                    "username": user.username,
                    "period": "24_hours",
                    "scans_completed": len(recent_scans),
                    "total_threats": total_threats,
                    "total_vulnerabilities": total_vulns,
                    "generated_at": datetime.utcnow().isoformat(),
                }
                
                reports.append(report)
                
                # TODO: Send report via email
                logger.info(f"Generated daily report for user {user.id}")
            
            return {"reports_generated": len(reports)}
    
    except Exception as e:
        logger.error(f"Error generating daily reports: {e}")
        raise


@celery_app.task
def generate_weekly_summary(user_id: int):
    """Generate weekly security summary for user"""
    try:
        with get_db_session() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"error": "User not found"}
            
            # Get scans from last 7 days
            week_ago = datetime.utcnow() - timedelta(days=7)
            weekly_scans = db.query(SecurityScan).filter(
                SecurityScan.user_id == user.id,
                SecurityScan.created_at >= week_ago
            ).all()
            
            summary = {
                "user_id": user.id,
                "period": "7_days",
                "total_scans": len(weekly_scans),
                "scans_by_type": {},
                "security_score": 85,  # TODO: Calculate actual security score
                "trends": {
                    "improving": True,
                    "areas_of_concern": [],
                },
                "generated_at": datetime.utcnow().isoformat(),
            }
            
            logger.info(f"Generated weekly summary for user {user_id}")
            return summary
    
    except Exception as e:
        logger.error(f"Error generating weekly summary: {e}")
        raise


@celery_app.task
def export_report_pdf(report_data: Dict[str, Any]) -> str:
    """
    Export report to PDF format
    
    Returns:
        Path to generated PDF file
    """
    try:
        # TODO: Implement PDF generation using reportlab or similar
        logger.info("PDF export requested")
        
        pdf_path = f"/tmp/report_{report_data.get('scan_id', 'unknown')}.pdf"
        
        # Placeholder: Save JSON for now
        with open(pdf_path.replace('.pdf', '.json'), 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return pdf_path
    
    except Exception as e:
        logger.error(f"Error exporting PDF: {e}")
        raise
