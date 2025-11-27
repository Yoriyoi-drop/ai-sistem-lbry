from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging


class BaseAgent(ABC):
    """Abstract base class for all agents in the workflow system"""
    
    def __init__(self, name: str, agent_id: Optional[str] = None):
        self.name = name
        self.agent_id = agent_id or f"{name}_{id(self)}"
        self.logger = logging.getLogger(self.__class__.__name__)
        self.initialized = False
    
    @abstractmethod
    async def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process the given context and return results
        
        Args:
            context: Input context containing data for processing
            
        Returns:
            Dictionary containing results of processing
        """
        pass
    
    async def initialize(self) -> None:
        """Initialize the agent before first use"""
        self.initialized = True
        self.logger.info(f"Agent {self.name} initialized")
    
    async def cleanup(self) -> None:
        """Clean up resources when agent is no longer needed"""
        self.logger.info(f"Agent {self.name} cleaned up")
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent"""
        return {
            "name": self.name,
            "id": self.agent_id,
            "initialized": self.initialized,
            "type": self.__class__.__name__
        }