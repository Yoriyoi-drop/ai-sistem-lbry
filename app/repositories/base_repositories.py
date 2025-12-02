"""
Repositories Module
Data access repositories following DDD pattern
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from src.database.models import User, Organization, SecurityScan, UsageMetric


class BaseRepository(ABC):
    """
    Abstract base repository for DDD pattern
    """
    def __init__(self, db_session: Session):
        self.db = db_session
    
    @abstractmethod
    def get_by_id(self, id: uuid.UUID):
        """
        Get entity by ID
        """
        pass
    
    @abstractmethod
    def create(self, entity_data: Dict[str, Any]):
        """
        Create a new entity
        """
        pass
    
    @abstractmethod
    def update(self, id: uuid.UUID, entity_data: Dict[str, Any]):
        """
        Update an entity
        """
        pass
    
    @abstractmethod
    def delete(self, id: uuid.UUID) -> bool:
        """
        Delete an entity
        """
        pass


class UserRepository(BaseRepository):
    """
    Repository for User entity
    """
    def get_by_id(self, id: uuid.UUID) -> Optional[User]:
        return self.db.query(User).filter(User.id == id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_organization(self, organization_id: uuid.UUID) -> List[User]:
        return self.db.query(User).filter(User.organization_id == organization_id).all()
    
    def create(self, entity_data: Dict[str, Any]) -> User:
        user = User(**entity_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, id: uuid.UUID, entity_data: Dict[str, Any]) -> Optional[User]:
        user = self.get_by_id(id)
        if user:
            for key, value in entity_data.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def delete(self, id: uuid.UUID) -> bool:
        user = self.get_by_id(id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
    
    def get_by_role(self, organization_id: uuid.UUID, role: str) -> List[User]:
        """
        Get users by role within an organization
        """
        from src.database.models import RoleEnum
        return self.db.query(User).filter(
            and_(
                User.organization_id == organization_id,
                User.role == RoleEnum(role)
            )
        ).all()
    
    def get_active_users_count(self, organization_id: uuid.UUID) -> int:
        """
        Get count of active users in an organization
        """
        return self.db.query(User).filter(
            and_(
                User.organization_id == organization_id,
                User.is_active == True
            )
        ).count()


class OrganizationRepository(BaseRepository):
    """
    Repository for Organization entity
    """
    def get_by_id(self, id: uuid.UUID) -> Optional[Organization]:
        return self.db.query(Organization).filter(Organization.id == id).first()
    
    def get_by_name(self, name: str) -> Optional[Organization]:
        return self.db.query(Organization).filter(Organization.name == name).first()
    
    def create(self, entity_data: Dict[str, Any]) -> Organization:
        org = Organization(**entity_data)
        self.db.add(org)
        self.db.commit()
        self.db.refresh(org)
        return org
    
    def update(self, id: uuid.UUID, entity_data: Dict[str, Any]) -> Optional[Organization]:
        org = self.get_by_id(id)
        if org:
            for key, value in entity_data.items():
                setattr(org, key, value)
            self.db.commit()
            self.db.refresh(org)
        return org
    
    def delete(self, id: uuid.UUID) -> bool:
        org = self.get_by_id(id)
        if org:
            self.db.delete(org)
            self.db.commit()
            return True
        return False
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Organization]:
        return self.db.query(Organization).offset(skip).limit(limit).all()
    
    def get_by_tier(self, tier: str) -> List[Organization]:
        """
        Get organizations by subscription tier
        """
        from src.database.models import SubscriptionTier
        return self.db.query(Organization).filter(
            Organization.tier == SubscriptionTier(tier)
        ).all()
    
    def get_active_count(self) -> int:
        """
        Get count of active organizations
        """
        return self.db.query(Organization).filter(
            Organization.status == "active"
        ).count()


class SecurityScanRepository(BaseRepository):
    """
    Repository for SecurityScan entity
    """
    def get_by_id(self, id: uuid.UUID) -> Optional[SecurityScan]:
        return self.db.query(SecurityScan).filter(SecurityScan.id == id).first()
    
    def create(self, entity_data: Dict[str, Any]) -> SecurityScan:
        scan = SecurityScan(**entity_data)
        self.db.add(scan)
        self.db.commit()
        self.db.refresh(scan)
        return scan
    
    def update(self, id: uuid.UUID, entity_data: Dict[str, Any]) -> Optional[SecurityScan]:
        scan = self.get_by_id(id)
        if scan:
            for key, value in entity_data.items():
                setattr(scan, key, value)
            self.db.commit()
            self.db.refresh(scan)
        return scan
    
    def delete(self, id: uuid.UUID) -> bool:
        scan = self.get_by_id(id)
        if scan:
            self.db.delete(scan)
            self.db.commit()
            return True
        return False
    
    def get_by_organization(self, organization_id: uuid.UUID, 
                          skip: int = 0, limit: int = 100) -> List[SecurityScan]:
        """
        Get scans by organization
        """
        return self.db.query(SecurityScan).filter(
            SecurityScan.organization_id == organization_id
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, organization_id: uuid.UUID, status: str) -> List[SecurityScan]:
        """
        Get scans by status within an organization
        """
        from src.database.models import ScanStatus
        return self.db.query(SecurityScan).filter(
            and_(
                SecurityScan.organization_id == organization_id,
                SecurityScan.status == ScanStatus(status)
            )
        ).all()
    
    def get_recent(self, organization_id: uuid.UUID, hours: int = 24) -> List[SecurityScan]:
        """
        Get scans from recent hours
        """
        from datetime import timedelta
        since = datetime.utcnow() - timedelta(hours=hours)
        
        return self.db.query(SecurityScan).filter(
            and_(
                SecurityScan.organization_id == organization_id,
                SecurityScan.created_at >= since
            )
        ).all()
    
    def get_stats(self, organization_id: uuid.UUID) -> Dict[str, Any]:
        """
        Get scan statistics for an organization
        """
        from src.database.models import ScanStatus
        
        total_scans = self.db.query(SecurityScan).filter(
            SecurityScan.organization_id == organization_id
        ).count()
        
        status_counts = self.db.query(
            SecurityScan.status, 
            func.count(SecurityScan.id)
        ).filter(
            SecurityScan.organization_id == organization_id
        ).group_by(SecurityScan.status).all()
        
        status_dict = {status: count for status, count in status_counts}
        
        return {
            "total_scans": total_scans,
            "completed_scans": status_dict.get(ScanStatus.COMPLETED, 0),
            "failed_scans": status_dict.get(ScanStatus.FAILED, 0),
            "running_scans": status_dict.get(ScanStatus.RUNNING, 0),
            "pending_scans": status_dict.get(ScanStatus.PENDING, 0)
        }


class UsageMetricRepository(BaseRepository):
    """
    Repository for UsageMetric entity
    """
    def get_by_id(self, id: uuid.UUID) -> Optional[UsageMetric]:
        return self.db.query(UsageMetric).filter(UsageMetric.id == id).first()
    
    def create(self, entity_data: Dict[str, Any]) -> UsageMetric:
        metric = UsageMetric(**entity_data)
        self.db.add(metric)
        self.db.commit()
        self.db.refresh(metric)
        return metric
    
    def update(self, id: uuid.UUID, entity_data: Dict[str, Any]) -> Optional[UsageMetric]:
        metric = self.get_by_id(id)
        if metric:
            for key, value in entity_data.items():
                setattr(metric, key, value)
            self.db.commit()
            self.db.refresh(metric)
        return metric
    
    def delete(self, id: uuid.UUID) -> bool:
        metric = self.get_by_id(id)
        if metric:
            self.db.delete(metric)
            self.db.commit()
            return True
        return False
    
    def get_by_organization_and_type(self, organization_id: uuid.UUID, 
                                   metric_type: str, period) -> Optional[UsageMetric]:
        """
        Get usage metric by organization, type, and period
        """
        return self.db.query(UsageMetric).filter(
            and_(
                UsageMetric.organization_id == organization_id,
                UsageMetric.metric_type == metric_type,
                UsageMetric.period == period
            )
        ).first()
    
    def get_organization_usage(self, organization_id: uuid.UUID, 
                             period_start, period_end) -> List[UsageMetric]:
        """
        Get all usage metrics for an organization in a period
        """
        return self.db.query(UsageMetric).filter(
            and_(
                UsageMetric.organization_id == organization_id,
                UsageMetric.period >= period_start,
                UsageMetric.period <= period_end
            )
        ).all()
    
    def get_metric_totals(self, organization_id: uuid.UUID, 
                         metric_type: str, period_start, period_end) -> int:
        """
        Get total usage for a specific metric type in a period
        """
        result = self.db.query(func.sum(UsageMetric.quantity)).filter(
            and_(
                UsageMetric.organization_id == organization_id,
                UsageMetric.metric_type == metric_type,
                UsageMetric.period >= period_start,
                UsageMetric.period <= period_end
            )
        ).scalar()
        
        return result or 0
    
    def create_or_update(self, organization_id: uuid.UUID, metric_type: str, 
                        quantity: int, period) -> UsageMetric:
        """
        Create new usage metric or update existing one for the period
        """
        existing = self.get_by_organization_and_type(organization_id, metric_type, period)
        
        if existing:
            existing.quantity += quantity
            self.db.commit()
            self.db.refresh(existing)
            return existing
        else:
            return self.create({
                "organization_id": organization_id,
                "metric_type": metric_type,
                "quantity": quantity,
                "period": period
            })