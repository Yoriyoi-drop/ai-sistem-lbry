"""
Orchestrator Agent Module
Main orchestrator for managing other agents
"""
import asyncio
import uuid
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import logging

from ..security_engine.engine import SecurityEngine


class AgentMessage:
    """
    Message structure for agent communication
    """
    def __init__(self, from_agent: str, to_agent: str, intent: str, 
                 payload: Dict[str, Any], trace_id: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.intent = intent
        self.payload = payload
        self.trace_id = trace_id or str(uuid.uuid4())
        self.timestamp = datetime.utcnow().isoformat()
        self.status = "pending"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "intent": self.intent,
            "payload": self.payload,
            "trace_id": self.trace_id,
            "timestamp": self.timestamp,
            "status": self.status
        }


class AgentOrchestrator:
    """
    Main orchestrator agent that manages other agents
    """
    def __init__(self):
        self.agent_registry = {}
        self.message_queue = []
        self.security_engine = SecurityEngine()
        self.logger = logging.getLogger(__name__)
        self.active_tasks = {}
        self.agent_configs = {}

    def register_agent(self, agent_name: str, agent_callable: Callable, config: Dict[str, Any] = None):
        """
        Register an agent with the orchestrator
        """
        self.agent_registry[agent_name] = agent_callable
        self.agent_configs[agent_name] = config or {}
        self.logger.info(f"Registered agent: {agent_name}")

    async def send_message(self, message: AgentMessage) -> Dict[str, Any]:
        """
        Send a message to another agent with security checks
        """
        # Security check on the message
        is_safe = await self.security_engine.filter_request(
            f"Message from {message.from_agent} to {message.to_agent}: {message.intent}",
            context={"payload_keys": list(message.payload.keys()) if isinstance(message.payload, dict) else []}
        )
        
        if not is_safe["is_allowed"]:
            self.logger.warning(f"Security blocked message from {message.from_agent} to {message.to_agent}")
            return {
                "success": False,
                "error": "Message blocked by security engine",
                "message_id": message.id
            }
        
        # Add to message queue
        self.message_queue.append(message)
        
        # Process message
        result = await self._route_message(message)
        
        return {
            "success": True,
            "result": result,
            "message_id": message.id
        }

    async def _route_message(self, message: AgentMessage) -> Dict[str, Any]:
        """
        Route message to the appropriate agent
        """
        if message.to_agent not in self.agent_registry:
            return {
                "error": f"Agent {message.to_agent} not found",
                "status": "error"
            }
        
        try:
            agent_func = self.agent_registry[message.to_agent]
            
            # Execute agent function with the message payload
            result = await agent_func(message.payload) if asyncio.iscoroutinefunction(agent_func) else agent_func(message.payload)
            
            return {
                "result": result,
                "status": "success",
                "processed_by": message.to_agent
            }
        except Exception as e:
            self.logger.error(f"Error in agent {message.to_agent}: {str(e)}")
            return {
                "error": str(e),
                "status": "error",
                "processed_by": message.to_agent
            }

    async def execute_task(self, task_definition: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a complex task using multiple agents
        """
        task_id = str(uuid.uuid4())
        self.logger.info(f"Starting task execution: {task_id}")
        
        try:
            # Parse task definition and create steps
            steps = task_definition.get("steps", [])
            results = []
            
            for step in steps:
                step_result = await self._execute_step(step, task_id)
                results.append(step_result)
                
                # Check if we need to stop due to error or condition
                if not step_result.get("success", True):
                    self.logger.warning(f"Task {task_id} stopped at step due to error")
                    break
            
            return {
                "task_id": task_id,
                "success": True,
                "results": results,
                "status": "completed"
            }
        except Exception as e:
            self.logger.error(f"Error in task execution {task_id}: {str(e)}")
            return {
                "task_id": task_id,
                "success": False,
                "error": str(e),
                "status": "error"
            }

    async def _execute_step(self, step: Dict[str, Any], task_id: str) -> Dict[str, Any]:
        """
        Execute a single step in a task
        """
        agent_name = step.get("agent")
        intent = step.get("intent", "process")
        payload = step.get("payload", {})
        
        if agent_name not in self.agent_registry:
            return {
                "success": False,
                "error": f"Agent {agent_name} not found",
                "step_status": "failed"
            }
        
        # Create message for this step
        message = AgentMessage(
            from_agent=f"orchestrator_{task_id}",
            to_agent=agent_name,
            intent=intent,
            payload=payload
        )
        
        # Route message and get result
        result = await self._route_message(message)
        
        return {
            "step": step,
            "result": result,
            "success": result.get("status") == "success",
            "step_status": result.get("status")
        }

    async def get_agent_status(self) -> Dict[str, Any]:
        """
        Get status of all registered agents
        """
        status = {}
        
        for agent_name in self.agent_registry:
            # In a real implementation, you'd check if agent is responsive
            status[agent_name] = {
                "registered": True,
                "status": "active",  # This would come from actual agent health check
                "config": self.agent_configs[agent_name]
            }
        
        return {
            "orchestrator_id": "main_orchestrator",
            "timestamp": datetime.utcnow().isoformat(),
            "agent_count": len(self.agent_registry),
            "agents": status,
            "queue_size": len(self.message_queue)
        }

    def create_resolution_tree(self, problem: str) -> Dict[str, Any]:
        """
        Create a resolution tree for a given problem
        """
        # This would use AI to break down the problem into subtasks
        # For now, using a simple template approach
        return {
            "problem": problem,
            "root_task": problem,
            "subtasks": [
                {"id": 1, "description": "Analyze the problem", "agent": "worker"},
                {"id": 2, "description": "Gather relevant information", "agent": "worker"},
                {"id": 3, "description": "Generate solution", "agent": "worker"},
                {"id": 4, "description": "Validate solution", "agent": "security_guard"},
                {"id": 5, "description": "Return result", "agent": "orchestrator"}
            ],
            "dependencies": {
                "2": [1],
                "3": [2],
                "4": [3],
                "5": [4]
            }
        }

    async def resolve_problem(self, problem: str) -> Dict[str, Any]:
        """
        Resolve a problem using the resolution tree and agents
        """
        resolution_tree = self.create_resolution_tree(problem)
        
        # Execute the resolution tree
        task_definition = {
            "steps": resolution_tree["subtasks"]
        }
        
        result = await self.execute_task(task_definition)
        
        return {
            "problem": problem,
            "resolution_tree": resolution_tree,
            "execution_result": result,
            "timestamp": datetime.utcnow().isoformat()
        }

    def detect_conflicts(self, task_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect potential conflicts between tasks
        """
        conflicts = []
        # Simple conflict detection based on resource names
        resources = {}
        
        for i, task in enumerate(task_list):
            resource = task.get("resource")
            if resource:
                if resource in resources:
                    conflicts.append({
                        "task1": resources[resource],
                        "task2": i,
                        "resource": resource,
                        "type": "resource_conflict"
                    })
                else:
                    resources[resource] = i
        
        return conflicts