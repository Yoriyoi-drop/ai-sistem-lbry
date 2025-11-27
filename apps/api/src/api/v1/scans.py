"""
Scan management endpoints for Infinite AI Security Platform
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.connection import get_db
from ..schemas.scan import ScanResponse, ScanCreate, ScanUpdate
from ..services.scan_service import ScanService
from ..services.agent_service import AgentService
from ..services.auth_service import get_current_active_user


router = APIRouter(prefix="/scans", tags=["Security Scans"])


@router.get("/", response_model=List[ScanResponse])
def read_scans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all scans with pagination"""
    scan_service = ScanService(db)
    scans = scan_service.get_scans(skip=skip, limit=limit)
    return scans


@router.get("/my", response_model=List[ScanResponse])
def read_my_scans(current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get scans owned by the current user"""
    scan_service = ScanService(db)
    scans = scan_service.get_scans_by_owner(current_user.id, skip=0, limit=100)
    return scans


@router.get("/{scan_id}", response_model=ScanResponse)
def read_scan(scan_id: int, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get a specific scan by ID"""
    scan_service = ScanService(db)
    scan = scan_service.get_scan_by_id(scan_id)
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    
    # Check if user owns this scan or is admin
    if scan.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this scan"
        )
    
    return scan


@router.post("/", response_model=ScanResponse)
def create_scan(scan_create: ScanCreate, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Create a new security scan"""
    scan_service = ScanService(db)
    
    # Validate that the agent belongs to the user or the user is admin
    agent_service = AgentService(db)
    agent = agent_service.get_agent_by_id(scan_create.agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    if agent.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to use this agent"
        )
    
    scan = scan_service.create_scan(scan_create, current_user.id, scan_create.agent_id)
    return scan


@router.put("/{scan_id}", response_model=ScanResponse)
def update_scan(scan_id: int, scan_update: ScanUpdate, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Update a specific scan"""
    scan_service = ScanService(db)
    scan = scan_service.get_scan_by_id(scan_id)
    
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    
    # Check if user owns this scan or is admin
    if scan.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this scan"
        )
    
    updated_scan = scan_service.update_scan(scan_id, scan_update)
    if not updated_scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    return updated_scan


@router.delete("/{scan_id}")
def delete_scan(scan_id: int, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Delete a specific scan"""
    scan_service = ScanService(db)
    scan = scan_service.get_scan_by_id(scan_id)
    
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    
    # Check if user owns this scan or is admin
    if scan.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this scan"
        )
    
    success = scan_service.delete_scan(scan_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    return {"message": "Scan deleted successfully"}


@router.post("/{scan_id}/start")
def start_scan(scan_id: int, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Start a specific scan"""
    scan_service = ScanService(db)
    scan = scan_service.get_scan_by_id(scan_id)
    
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    
    # Check if user owns this scan or is admin
    if scan.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to start this scan"
        )
    
    # Ensure agent is active
    agent_service = AgentService(db)
    agent = agent_service.get_agent_by_id(scan.agent_id)
    if not agent or agent.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agent is not active"
        )
    
    started_scan = scan_service.start_scan(scan_id)
    if not started_scan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not start scan"
        )
    return {"message": "Scan started successfully", "scan": started_scan}


@router.post("/{scan_id}/complete")
def complete_scan(scan_id: int, results: dict = None, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Manually complete a scan (for testing purposes)"""
    scan_service = ScanService(db)
    scan = scan_service.get_scan_by_id(scan_id)
    
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    
    # Check if user owns this scan or is admin
    if scan.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to complete this scan"
        )
    
    completed_scan = scan_service.complete_scan(scan_id, results)
    if not completed_scan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not complete scan"
        )
    return {"message": "Scan completed successfully", "scan": completed_scan}