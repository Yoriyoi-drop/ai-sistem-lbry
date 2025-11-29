"""
Database context management for multi-tenant operations
"""
from typing import Optional
from sqlalchemy.orm import Session
import uuid


def set_current_organization(db: Session, organization_id: Optional[uuid.UUID]):
    """
    Set the current organization context for Row Level Security (RLS)
    This function will be called for each request to ensure proper tenant isolation
    """
    if organization_id is None:
        # Clear the setting if no organization is provided
        db.execute("SELECT set_config('app.current_organization_id', NULL, false)")
    else:
        # Set the organization ID for RLS
        db.execute(
            "SELECT set_config('app.current_organization_id', :org_id, false)",
            {"org_id": str(organization_id)}
        )
    db.commit()


def get_current_organization(db: Session) -> Optional[uuid.UUID]:
    """
    Retrieve the current organization context
    """
    result = db.execute("SELECT current_setting('app.current_organization_id', true)")
    org_id_str = result.scalar()
    
    if org_id_str:
        try:
            return uuid.UUID(org_id_str)
        except ValueError:
            return None
    
    return None


def verify_organization_access(db: Session, requested_org_id: uuid.UUID, user_org_id: uuid.UUID) -> bool:
    """
    Verify that a user has access to a specific organization
    This is an additional security check beyond RLS
    """
    return requested_org_id == user_org_id