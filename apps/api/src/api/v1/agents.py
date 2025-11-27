"""
Agent management endpoints for Infinite AI Security Platform
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.connection import get_db
from ..schemas.agent import AgentResponse, AgentCreate, AgentUpdate
from ..services.agent_service import AgentService
from ..services.auth_service import get_current_active_user


router = APIRouter(prefix="/agents", tags=["Security Agents"])


@router.get("/", response_model=List[AgentResponse])
def read_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all agents with pagination"""
    agent_service = AgentService(db)
    agents = agent_service.get_agents(skip=skip, limit=limit)
    return agents


@router.get("/my", response_model=List[AgentResponse])
def read_my_agents(current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get agents owned by the current user"""
    agent_service = AgentService(db)
    agents = agent_service.get_agents_by_owner(current_user.id, skip=0, limit=100)
    return agents


@router.get("/{agent_id}", response_model=AgentResponse)
def read_agent(agent_id: int, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get a specific agent by ID"""
    agent_service = AgentService(db)
    agent = agent_service.get_agent_by_id(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Check if user owns this agent or is admin
    if agent.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this agent"
        )
    
    return agent


@router.post("/", response_model=AgentResponse)
def create_agent(agent_create: AgentCreate, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Create a new security agent"""
    agent_service = AgentService(db)
    agent = agent_service.create_agent(agent_create, current_user.id)
    return agent


@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent(agent_id: int, agent_update: AgentUpdate, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Update a specific agent"""
    agent_service = AgentService(db)
    agent = agent_service.get_agent_by_id(agent_id)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Check if user owns this agent or is admin
    if agent.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this agent"
        )
    
    updated_agent = agent_service.update_agent(agent_id, agent_update)
    if not updated_agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return updated_agent


@router.delete("/{agent_id}")
def delete_agent(agent_id: int, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Delete a specific agent"""
    agent_service = AgentService(db)
    agent = agent_service.get_agent_by_id(agent_id)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Check if user owns this agent or is admin
    if agent.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this agent"
        )
    
    success = agent_service.delete_agent(agent_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return {"message": "Agent deleted successfully"}


@router.post("/{agent_id}/activate")
def activate_agent(agent_id: int, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Activate a specific agent"""
    agent_service = AgentService(db)
    agent = agent_service.get_agent_by_id(agent_id)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Check if user owns this agent or is admin
    if agent.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to activate this agent"
        )
    
    activated_agent = agent_service.activate_agent(agent_id)
    if not activated_agent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not activate agent"
        )
    return {"message": "Agent activated successfully", "agent": activated_agent}


@router.post("/{agent_id}/deactivate")
def deactivate_agent(agent_id: int, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Deactivate a specific agent"""
    agent_service = AgentService(db)
    agent = agent_service.get_agent_by_id(agent_id)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Check if user owns this agent or is admin
    if agent.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to deactivate this agent"
        )
    
    deactivated_agent = agent_service.deactivate_agent(agent_id)
    if not deactivated_agent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not deactivate agent"
        )
    return {"message": "Agent deactivated successfully", "agent": deactivated_agent}