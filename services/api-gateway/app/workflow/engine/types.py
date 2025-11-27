from enum import Enum
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import uuid
from ..agents.base_agent import BaseAgent


class NodeType(Enum):
    """Types of nodes in the workflow"""
    START = "start"
    END = "end"
    AGENT = "agent"
    CONDITIONAL = "conditional"
    INPUT_VALIDATION = "input_validation"
    ANALYSIS = "analysis"
    EXECUTION = "execution"
    VERIFICATION = "verification"
    RECOVERY = "recovery"
    LOGGING = "logging"
    NOTIFICATION = "notification"
    DATA_TRANSFORM = "data_transform"
    SECURITY_CHECK = "security_check"


class NodeStatus(Enum):
    """Status of workflow nodes"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class WorkflowNode:
    """Represents a single node in the workflow"""
    id: str
    name: str
    node_type: NodeType
    status: NodeStatus = NodeStatus.PENDING
    agent_ref: Optional[BaseAgent] = None
    params: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    result: Any = None
    
    def execute(self, context: Dict[str, Any]) -> Any:
        """Execute the node with given context"""
        self.started_at = datetime.utcnow()
        self.status = NodeStatus.RUNNING
        
        try:
            if self.node_type == NodeType.AGENT and self.agent_ref:
                self.result = self.agent_ref.process(context)
            elif self.node_type in [NodeType.START, NodeType.END]:
                self.result = {"status": "ok"}
            else:
                # Default execution logic for other node types
                self.result = self._execute_default(context)
            
            self.status = NodeStatus.COMPLETED
            self.completed_at = datetime.utcnow()
            return self.result
        except Exception as e:
            self.status = NodeStatus.FAILED
            self.error_message = str(e)
            self.completed_at = datetime.utcnow()
            raise
    
    def _execute_default(self, context: Dict[str, Any]) -> Any:
        """Default execution logic for non-agent nodes"""
        return context


@dataclass
class WorkflowEdge:
    """Represents a directed edge between two nodes"""
    source_node_id: str
    target_node_id: str
    condition: Optional[Callable[[Dict[str, Any]], bool]] = None
    weight: float = 1.0
    label: Optional[str] = None


@dataclass
class WorkflowLevel:
    """Represents a level in the hierarchical workflow"""
    id: str
    name: str
    description: str
    nodes: List[str]  # List of node IDs in this level
    depends_on: List[str]  # List of level IDs this level depends on
    status: NodeStatus = NodeStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    async def execute(self, context: Dict[str, Any], workflow_engine) -> Dict[str, Any]:
        """Execute all nodes in this level"""
        self.status = NodeStatus.RUNNING
        
        # Execute all nodes in this level concurrently
        tasks = []
        for node_id in self.nodes:
            node = workflow_engine.get_node(node_id)
            if node:
                task = asyncio.create_task(node.execute(context))
                tasks.append(task)
        
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            self.status = NodeStatus.COMPLETED
            return {node_id: result for node_id, result in zip(self.nodes, results)}
        except Exception as e:
            self.status = NodeStatus.FAILED
            raise


@dataclass
class WorkflowState:
    """Represents the state of a running workflow"""
    workflow_id: str
    current_level: int
    current_node: str
    status: NodeStatus
    context: Dict[str, Any]
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    execution_path: List[str] = field(default_factory=list)