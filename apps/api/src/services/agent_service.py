from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.agent import Agent as AgentModel
from ..schemas.agent import AgentCreate, AgentUpdate, Agent
from ..models.user import User as UserModel


class AgentService:
    def __init__(self, db: Session):
        self.db = db

    def get_agent_by_id(self, agent_id: int) -> Optional[Agent]:
        """
        Get an agent by ID
        """
        db_agent = self.db.query(AgentModel).filter(AgentModel.id == agent_id).first()
        if not db_agent:
            return None
        return Agent.from_orm(db_agent)

    def get_agents(self, skip: int = 0, limit: int = 100) -> List[Agent]:
        """
        Get a list of agents with pagination
        """
        db_agents = self.db.query(AgentModel).offset(skip).limit(limit).all()
        return [Agent.from_orm(agent) for agent in db_agents]

    def get_agents_by_owner(self, owner_id: int) -> List[Agent]:
        """
        Get agents owned by a specific user
        """
        db_agents = self.db.query(AgentModel).filter(AgentModel.owner_id == owner_id).all()
        return [Agent.from_orm(agent) for agent in db_agents]

    def create_agent(self, agent_create: AgentCreate, owner_id: int) -> Agent:
        """
        Create a new agent
        """
        now = datetime.utcnow()
        db_agent = AgentModel(
            name=agent_create.name,
            description=agent_create.description,
            agent_type=agent_create.type,
            configuration=agent_create.configuration,
            is_active=agent_create.is_active,
            owner_id=owner_id,
            created_at=now,
            updated_at=now
        )
        
        self.db.add(db_agent)
        self.db.commit()
        self.db.refresh(db_agent)
        
        return Agent.from_orm(db_agent)

    def update_agent(self, agent_id: int, agent_update: AgentUpdate) -> Optional[Agent]:
        """
        Update a specific agent
        """
        db_agent = self.get_agent_by_id(agent_id)
        if not db_agent:
            return None

        update_data = agent_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_agent, field, value)
        
        db_agent.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_agent)
        
        return Agent.from_orm(db_agent)

    def delete_agent(self, agent_id: int) -> bool:
        """
        Delete an agent by ID
        """
        db_agent = self.get_agent_by_id(agent_id)
        if not db_agent:
            return False
        
        self.db.delete(db_agent)
        self.db.commit()
        return True

    def activate_agent(self, agent_id: int) -> Optional[Agent]:
        """
        Activate an agent
        """
        db_agent = self.get_agent_by_id(agent_id)
        if not db_agent:
            return None
        
        db_agent.is_active = True
        db_agent.status = "active"
        db_agent.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_agent)
        
        return Agent.from_orm(db_agent)

    def deactivate_agent(self, agent_id: int) -> Optional[Agent]:
        """
        Deactivate an agent
        """
        db_agent = self.get_agent_by_id(agent_id)
        if not db_agent:
            return None
        
        db_agent.is_active = False
        db_agent.status = "inactive"
        db_agent.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_agent)
        
        return Agent.from_orm(db_agent)

    def execute_agent(self, agent_id: int) -> dict:
        """
        Execute an agent (simulate execution)
        """
        db_agent = self.get_agent_by_id(agent_id)
        if not db_agent or not db_agent.is_active:
            return {"error": "Agent not found or not active"}
        
        # Update last execution time
        db_agent.last_execution = datetime.utcnow()
        db_agent.tasks_completed += 1
        db_agent.updated_at = datetime.utcnow()
        
        self.db.commit()
        
        return {
            "message": f"Agent {db_agent.name} executed successfully",
            "agent_id": db_agent.id,
            "execution_time": datetime.utcnow().isoformat()
        }

    def update_agent_heartbeat(self, agent_id: int) -> Optional[Agent]:
        """
        Update agent heartbeat (for monitoring)
        """
        db_agent = self.get_agent_by_id(agent_id)
        if not db_agent:
            return None
        
        db_agent.last_heartbeat = datetime.utcnow()
        db_agent.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_agent)
        
        return Agent.from_orm(db_agent)