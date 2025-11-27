from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...database.connection import get_db
from ...schemas.scan import Scan, ScanCreate, ScanUpdate
from ...services.scan_service import ScanService
from ...utils.dependencies import get_current_user, get_current_superuser
from ...models.scan import Scan as ScanModel

router = APIRouter(prefix="/scans", tags=["scans"])


@router.get("/", response_model=List[Scan])
def read_scans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
               current_user: dict = Depends(get_current_user)):
    """
    Retrieve scans with pagination
    """
    scan_service = ScanService(db)
    scans = scan_service.get_scans(skip=skip, limit=limit)
    return scans


@router.get("/{scan_id}", response_model=Scan)
def read_scan(scan_id: int, db: Session = Depends(get_db),
              current_user: dict = Depends(get_current_user)):
    """
    Retrieve a specific scan by ID
    """
    scan_service = ScanService(db)
    scan = scan_service.get_scan_by_id(scan_id)
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    return scan


@router.post("/", response_model=Scan)
def create_scan(scan_create: ScanCreate, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    """
    Create a new scan
    """
    scan_service = ScanService(db)
    scan = scan_service.create_scan(scan_create, current_user.id)
    return scan


@router.put("/{scan_id}", response_model=Scan)
def update_scan(scan_id: int, scan_update: ScanUpdate, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    """
    Update a specific scan by ID
    """
    scan_service = ScanService(db)
    scan = scan_service.update_scan(scan_id, scan_update)
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    return scan


@router.delete("/{scan_id}")
def delete_scan(scan_id: int, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_superuser)):
    """
    Delete a specific scan by ID
    """
    scan_service = ScanService(db)
    success = scan_service.delete_scan(scan_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    return {"message": "Scan deleted successfully"}


@router.post("/{scan_id}/start")
def start_scan(scan_id: int, db: Session = Depends(get_db),
               current_user: dict = Depends(get_current_user)):
    """
    Start a specific scan by ID
    """
    scan_service = ScanService(db)
    scan = scan_service.get_scan_by_id(scan_id)
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    
    if scan.status not in ["pending", "completed", "failed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scan is already running or paused"
        )
    
    # Update the scan status to running
    scan.started_at = datetime.utcnow()
    scan.status = "running"
    
    db.commit()
    db.refresh(scan)
    
    return {"message": f"Scan {scan.name} started successfully", "scan_id": scan.id}


@router.post("/{scan_id}/stop")
def stop_scan(scan_id: int, db: Session = Depends(get_db),
              current_user: dict = Depends(get_current_user)):
    """
    Stop a specific scan by ID
    """
    scan_service = ScanService(db)
    scan = scan_service.get_scan_by_id(scan_id)
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scan not found"
        )
    
    if scan.status != "running":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scan is not currently running"
        )
    
    # Update the scan status to stopped
    scan.completed_at = datetime.utcnow()
    scan.status = "stopped"
    
    db.commit()
    db.refresh(scan)
    
    return {"message": f"Scan {scan.name} stopped successfully", "scan_id": scan.id}