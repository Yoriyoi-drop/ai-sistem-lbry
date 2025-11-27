from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.scan import Scan as ScanModel
from ..schemas.scan import ScanCreate, ScanUpdate, Scan
from ..models.user import User as UserModel
from ..models.agent import Agent as AgentModel
from .labyrinth_client import labyrinth_client
import asyncio


class ScanService:
    def __init__(self, db: Session):
        self.db = db

    def get_scan_by_id(self, scan_id: int) -> Optional[Scan]:
        """
        Get a scan by ID
        """
        db_scan = self.db.query(ScanModel).filter(ScanModel.id == scan_id).first()
        if not db_scan:
            return None
        return Scan.from_orm(db_scan)

    def get_scans(self, skip: int = 0, limit: int = 100) -> List[Scan]:
        """
        Get a list of scans with pagination
        """
        db_scans = self.db.query(ScanModel).offset(skip).limit(limit).all()
        return [Scan.from_orm(scan) for scan in db_scans]

    def get_scans_by_owner(self, owner_id: int) -> List[Scan]:
        """
        Get scans owned by a specific user
        """
        db_scans = self.db.query(ScanModel).filter(ScanModel.owner_id == owner_id).all()
        return [Scan.from_orm(scan) for scan in db_scans]

    def get_scans_by_agent(self, agent_id: int) -> List[Scan]:
        """
        Get scans assigned to a specific agent
        """
        db_scans = self.db.query(ScanModel).filter(ScanModel.agent_id == agent_id).all()
        return [Scan.from_orm(scan) for scan in db_scans]

    def create_scan(self, scan_create: ScanCreate, owner_id: int, agent_id: Optional[int] = None) -> Scan:
        """
        Create a new scan
        """
        now = datetime.utcnow()
        db_scan = ScanModel(
            name=scan_create.name,
            description=scan_create.description,
            scan_type=scan_create.scan_type,
            target=scan_create.target,
            parameters=scan_create.parameters,
            is_active=scan_create.is_active,
            owner_id=owner_id,
            agent_id=agent_id,
            created_at=now,
            updated_at=now
        )
        
        self.db.add(db_scan)
        self.db.commit()
        self.db.refresh(db_scan)
        
        return Scan.from_orm(db_scan)

    def update_scan(self, scan_id: int, scan_update: ScanUpdate) -> Optional[Scan]:
        """
        Update a specific scan
        """
        db_scan = self.get_scan_by_id(scan_id)
        if not db_scan:
            return None

        update_data = scan_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_scan, field, value)
        
        db_scan.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_scan)
        
        return Scan.from_orm(db_scan)

    def delete_scan(self, scan_id: int) -> bool:
        """
        Delete a scan by ID
        """
        db_scan = self.get_scan_by_id(scan_id)
        if not db_scan:
            return False
        
        self.db.delete(db_scan)
        self.db.commit()
        return True

    def start_scan(self, scan_id: int) -> Optional[Scan]:
        """
        Start a scan
        """
        db_scan = self.get_scan_by_id(scan_id)
        if not db_scan or db_scan.status not in ["pending", "cancelled", "failed"]:
            return None
        
        db_scan.status = "running"
        db_scan.started_at = datetime.utcnow()
        db_scan.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_scan)
        
        return Scan.from_orm(db_scan)

    def complete_scan(self, scan_id: int, results: Optional[dict] = None) -> Optional[Scan]:
        """
        Complete a scan
        """
        db_scan = self.get_scan_by_id(scan_id)
        if not db_scan or db_scan.status != "running":
            return None
        
        db_scan.status = "completed"
        db_scan.completed_at = datetime.utcnow()
        if results:
            db_scan.results = results
        db_scan.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_scan)
        
        return Scan.from_orm(db_scan)

    def fail_scan(self, scan_id: int, error_message: Optional[str] = None) -> Optional[Scan]:
        """
        Mark a scan as failed
        """
        db_scan = self.get_scan_by_id(scan_id)
        if not db_scan or db_scan.status != "running":
            return None
        
        db_scan.status = "failed"
        db_scan.completed_at = datetime.utcnow()
        if error_message:
            if not db_scan.results:
                db_scan.results = {}
            db_scan.results["error"] = error_message
        db_scan.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_scan)
        
        return Scan.from_orm(db_scan)

    def cancel_scan(self, scan_id: int) -> Optional[Scan]:
        """
        Cancel a scan
        """
        db_scan = self.get_scan_by_id(scan_id)
        if not db_scan or db_scan.status not in ["pending", "running"]:
            return None
        
        db_scan.status = "cancelled"
        db_scan.completed_at = datetime.utcnow()
        db_scan.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_scan)
        
        return Scan.from_orm(db_scan)

    def get_scan_results(self, scan_id: int) -> Optional[dict]:
        """
        Get results for a specific scan
        """
        db_scan = self.get_scan_by_id(scan_id)
        if not db_scan:
            return None
        return db_scan.results