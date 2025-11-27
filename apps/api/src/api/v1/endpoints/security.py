from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.database.connection import get_db
from src.database.models import SecurityScan, Threat, Vulnerability, User
from src.schemas.scan import ScanCreate, ScanResponse
from src.utils.dependencies import get_current_active_user
from src.tasks.security_tasks import run_security_scan

router = APIRouter()

@router.get("/stats", response_model=Dict[str, Any])
def get_security_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get security dashboard statistics.
    """
    total_scans = db.query(SecurityScan).count()
    critical_threats = db.query(Threat).filter(Threat.severity == "critical").count()
    resolved_issues = db.query(Vulnerability).filter(Vulnerability.status == "resolved").count()
    active_agents = 5 # Placeholder until we query agents table
    
    return {
        "total_scans": total_scans,
        "critical_threats": critical_threats,
        "resolved_issues": resolved_issues,
        "active_agents": active_agents
    }

@router.post("/scans", response_model=ScanResponse)
def create_scan(
    *,
    db: Session = Depends(get_db),
    scan_in: ScanCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Initiate a new security scan.
    """
    scan = SecurityScan(
        scan_type=scan_in.scan_type,
        target=scan_in.target,
        status="pending",
        initiated_by_id=current_user.id
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    
    # Trigger Celery task
    run_security_scan.delay(scan.id)
    
    return scan

@router.get("/scans", response_model=List[ScanResponse])
def read_scans(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve security scans.
    """
    scans = db.query(SecurityScan).offset(skip).limit(limit).all()
    return scans
