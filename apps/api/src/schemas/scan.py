from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ScanBase(BaseModel):
    name: str
    description: Optional[str] = None
    scan_type: str  # vulnerability, compliance, penetration, etc.
    target: str  # target URL, IP, file, etc.
    parameters: Optional[Dict[str, Any]] = None
    is_active: bool = True


class ScanCreate(ScanBase):
    name: str
    scan_type: str
    target: str
    parameters: Optional[Dict[str, Any]] = None


class ScanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    scan_type: Optional[str] = None
    target: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None


class Scan(ScanBase):
    id: int
    status: str = "pending"  # pending, running, completed, failed, cancelled
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    results: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    owner_id: int
    agent_id: Optional[int] = None

    class Config:
        from_attributes = True


class ScanExecutionRequest(BaseModel):
    target: str
    scan_type: str
    parameters: Optional[Dict[str, Any]] = None


class ScanExecutionResponse(BaseModel):
    scan_id: int
    message: str
    status: str
    started_at: datetime