from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.database.models import Agent, User
from src.schemas.agent import AgentCreate, AgentUpdate, AgentResponse
from src.utils.dependencies import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[AgentResponse])
def read_agents(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve agents.
    """
    agents = db.query(Agent).offset(skip).limit(limit).all()
    return agents

@router.post("/", response_model=AgentResponse)
def create_agent(
    *,
    db: Session = Depends(get_db),
    agent_in: AgentCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new agent.
    """
    agent = Agent(
        name=agent_in.name,
        description=agent_in.description,
        agent_type=agent_in.agent_type,
        status="inactive",
        config=agent_in.config,
        created_by_id=current_user.id
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent(
    *,
    db: Session = Depends(get_db),
    agent_id: int,
    agent_in: AgentUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update an agent.
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    for field, value in agent_in.dict(exclude_unset=True).items():
        setattr(agent, field, value)
        
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.post("/{agent_id}/start", response_model=AgentResponse)
def start_agent(
    *,
    db: Session = Depends(get_db),
    agent_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Start an agent.
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    agent.status = "active"
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.post("/{agent_id}/stop", response_model=AgentResponse)
def stop_agent(
    *,
    db: Session = Depends(get_db),
    agent_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Stop an agent.
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
        
    agent.status = "inactive"
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent