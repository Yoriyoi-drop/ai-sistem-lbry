from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: str  # scanner, analyzer, defender, etc.
    configuration: Optional[Dict[str, Any]] = None
    is_active: bool = True


class AgentCreate(AgentBase):
    name: str
    type: str
    description: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class Agent(AgentBase):
    id: int
    status: str = "inactive"
    last_heartbeat: Optional[datetime] = None
    last_execution: Optional[datetime] = None
    tasks_completed: int = 0
    efficiency: int = 0
    created_at: datetime
    updated_at: datetime
    owner_id: Optional[int] = None

    class Config:
        from_attributes = True


class AgentExecutionRequest(BaseModel):
    target: str
    parameters: Optional[Dict[str, Any]] = None


class AgentExecutionResponse(BaseModel):
    success: bool
    message: str
    results: Optional[Dict[str, Any]] = None
    execution_id: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None