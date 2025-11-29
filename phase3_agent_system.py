# 🤖 NEXAFORGE - PHASE 3: AGENT SYSTEM (L4)

import json
import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import threading
from pathlib import Path

class AgentType(Enum):
    """Type of agent"""
    PLANNER = "planner"
    WORKER = "worker"
    COORDINATOR = "coordinator"

class TaskStatus(Enum):
    """Status of a task"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    """Represents a task in the agent system"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    agent_type: AgentType = AgentType.WORKER
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 0  # Higher number = higher priority
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    assigned_agent: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    result: Optional[Dict] = None
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)

@dataclass
class MemoryChunk:
    """Represents a memory chunk in the agent's memory system"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    importance: float = 0.5  # 0.0 to 1.0
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    short_term: bool = True  # True for short-term, False for long-term

class ShortTermMemory:
    """Short-term memory for agents"""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.memory: List[MemoryChunk] = []
        self.lock = threading.Lock()
    
    def add(self, content: str, tags: List[str] = None, importance: float = 0.5, metadata: Dict = None) -> str:
        """Add a memory chunk to short-term memory"""
        with self.lock:
            chunk = MemoryChunk(
                content=content,
                tags=tags or [],
                importance=importance,
                metadata=metadata or {},
                short_term=True
            )
            self.memory.append(chunk)
            
            # Keep only the most important memories within max_size
            if len(self.memory) > self.max_size:
                self.memory.sort(key=lambda x: x.importance, reverse=True)
                self.memory = self.memory[:self.max_size]
            
            return chunk.id
    
    def search(self, query: str, limit: int = 10) -> List[MemoryChunk]:
        """Search for memory chunks containing the query"""
        with self.lock:
            results = []
            query_lower = query.lower()
            
            for chunk in self.memory:
                if query_lower in chunk.content.lower():
                    results.append(chunk)
                    
            # Sort by importance
            results.sort(key=lambda x: x.importance, reverse=True)
            return results[:limit]
    
    def get_all(self) -> List[MemoryChunk]:
        """Get all memory chunks"""
        with self.lock:
            return self.memory.copy()

class LongTermMemory:
    """Long-term memory for agents"""
    
    def __init__(self, storage_path: str = "~/nexaforge/memory"):
        self.storage_path = Path(storage_path).expanduser()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.storage_path / "long_term_memory.json"
        self.memory: List[MemoryChunk] = self._load_memory()
        self.lock = threading.Lock()
    
    def _load_memory(self) -> List[MemoryChunk]:
        """Load memory from file"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    return [MemoryChunk(**item) for item in data]
            return []
        except Exception:
            return []
    
    def _save_memory(self):
        """Save memory to file"""
        with self.lock:
            data = []
            for chunk in self.memory:
                # Convert datetime objects to ISO format for JSON serialization
                chunk_dict = {
                    "id": chunk.id,
                    "content": chunk.content,
                    "timestamp": chunk.timestamp.isoformat(),
                    "importance": chunk.importance,
                    "tags": chunk.tags,
                    "metadata": chunk.metadata,
                    "short_term": chunk.short_term
                }
                data.append(chunk_dict)
            
            with open(self.memory_file, 'w') as f:
                json.dump(data, f, indent=2)
    
    def add(self, content: str, tags: List[str] = None, importance: float = 0.5, metadata: Dict = None) -> str:
        """Add a memory chunk to long-term memory"""
        with self.lock:
            chunk = MemoryChunk(
                content=content,
                tags=tags or [],
                importance=importance,
                metadata=metadata or {},
                short_term=False
            )
            self.memory.append(chunk)
            
            # Periodically save to file
            if len(self.memory) % 10 == 0:  # Save every 10 additions
                self._save_memory()
            
            return chunk.id
    
    def search(self, query: str, limit: int = 10) -> List[MemoryChunk]:
        """Search for memory chunks containing the query"""
        with self.lock:
            results = []
            query_lower = query.lower()
            
            for chunk in self.memory:
                if query_lower in chunk.content.lower() or \
                   any(query_lower in tag.lower() for tag in chunk.tags):
                    results.append(chunk)
            
            # Sort by importance and recency
            results.sort(key=lambda x: (x.importance, x.timestamp), reverse=True)
            return results[:limit]
    
    def get_all(self) -> List[MemoryChunk]:
        """Get all memory chunks"""
        with self.lock:
            return self.memory.copy()

class AgentMemory:
    """Combined memory system for agents"""
    
    def __init__(self, max_short_term: int = 100, long_term_path: str = "~/nexaforge/memory"):
        self.short_term = ShortTermMemory(max_short_term)
        self.long_term = LongTermMemory(long_term_path)
    
    def add_memory(self, content: str, tags: List[str] = None, importance: float = 0.5, short_term: bool = True) -> str:
        """Add memory to appropriate memory system"""
        if short_term:
            return self.short_term.add(content, tags, importance)
        else:
            return self.long_term.add(content, tags, importance)
    
    def search_memories(self, query: str, short_term_only: bool = False, long_term_only: bool = False, limit: int = 10) -> List[MemoryChunk]:
        """Search memories in both systems"""
        results = []
        
        if not long_term_only:
            results.extend(self.short_term.search(query, limit))
        
        if not short_term_only:
            results.extend(self.long_term.search(query, limit))
        
        # Sort by importance while preserving order within each memory type
        results.sort(key=lambda x: x.importance, reverse=True)
        return results[:limit]
    
    def get_all_memories(self) -> Dict[str, List[MemoryChunk]]:
        """Get all memories from both systems"""
        return {
            "short_term": self.short_term.get_all(),
            "long_term": self.long_term.get_all()
        }

class ToolExecutor:
    """Executes tools for agents"""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools for agents"""
        self.register_tool("calculate", self._calculate)
        self.register_tool("search_web", self._search_web)
        self.register_tool("read_file", self._read_file)
        self.register_tool("write_file", self._write_file)
        self.register_tool("list_files", self._list_files)
    
    def register_tool(self, name: str, func: Callable):
        """Register a new tool"""
        self.tools[name] = func
    
    def execute(self, tool_name: str, **kwargs) -> Dict:
        """Execute a tool with given parameters"""
        if tool_name not in self.tools:
            return {
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(self.tools.keys())
            }
        
        try:
            result = self.tools[tool_name](**kwargs)
            return {
                "success": True,
                "result": result,
                "tool": tool_name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name
            }
    
    def _calculate(self, expression: str) -> Any:
        """Calculate a mathematical expression (safe evaluation)"""
        # For security, in a real implementation you'd want to use a safe evaluation method
        # This is simplified for demonstration
        try:
            # Just return the expression as is for now, in a real system you'd use a safe eval
            return f"Calculated: {expression}"
        except:
            raise ValueError(f"Invalid expression: {expression}")
    
    def _search_web(self, query: str) -> List[Dict]:
        """Search the web (simulated)"""
        # This is a simulation - in reality, you'd integrate with a search API
        return [
            {"title": f"Results for '{query}'", "url": "https://example.com", "snippet": "This is a simulated search result"}
        ]
    
    def _read_file(self, path: str) -> str:
        """Read a file"""
        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            raise e
    
    def _write_file(self, path: str, content: str) -> bool:
        """Write to a file"""
        try:
            with open(path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            raise e
    
    def _list_files(self, directory: str = ".") -> List[str]:
        """List files in a directory"""
        try:
            import os
            return os.listdir(directory)
        except Exception as e:
            raise e

class AgentBrain:
    """Core brain of an AI agent"""
    
    def __init__(self, agent_id: str, agent_type: AgentType, memory: AgentMemory = None):
        self.id = agent_id
        self.type = agent_type
        self.memory = memory or AgentMemory()
        self.tool_executor = ToolExecutor()
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
    
    def think(self, input_data: str) -> Dict:
        """Process input and form a response"""
        self.last_activity = datetime.now()
        
        # Add input to memory
        self.memory.add_memory(input_data, tags=["input"], importance=0.8)
        
        # Perform some basic reasoning based on agent type
        if self.type == AgentType.PLANNER:
            response = self._plan_task(input_data)
        elif self.type == AgentType.WORKER:
            response = self._execute_task(input_data)
        else:  # COORDINATOR
            response = self._coordinate_tasks(input_data)
        
        # Add response to memory
        self.memory.add_memory(response.get("response", ""), tags=["response"], importance=0.7)
        
        return response
    
    def _plan_task(self, input_data: str) -> Dict:
        """Plan a complex task"""
        # Search for relevant memories
        memories = self.memory.search_memories(input_data)
        
        # Create a plan based on input and memories
        plan = {
            "task": input_data,
            "subtasks": [],
            "estimated_time": "TBD",
            "required_tools": [],
            "dependencies": []
        }
        
        # Basic planning logic - in reality this would be more sophisticated
        if "code" in input_data.lower():
            plan["subtasks"] = ["analyze requirements", "design solution", "implement code", "test solution"]
            plan["required_tools"] = ["calculate", "write_file"]
        elif "research" in input_data.lower():
            plan["subtasks"] = ["identify sources", "gather information", "analyze data", "summarize findings"]
            plan["required_tools"] = ["search_web", "read_file"]
        
        return {
            "type": "plan",
            "response": f"Planned task: {input_data}",
            "plan": plan,
            "context": [mem.content[:100] + "..." for mem in memories[:3]]
        }
    
    def _execute_task(self, input_data: str) -> Dict:
        """Execute a task"""
        # Search for relevant memories
        memories = self.memory.search_memories(input_data)
        
        # Execute based on task content
        if "calculate" in input_data.lower() or any(op in input_data for op in ["+", "-", "*", "/", "="]):
            result = self.tool_executor.execute("calculate", expression=input_data)
            return {
                "type": "execution",
                "response": f"Calculation result: {result.get('result', 'Unknown')}",
                "tool_result": result
            }
        elif "file" in input_data.lower():
            # Determine if reading or writing based on input
            if "read" in input_data.lower():
                # Extract file path from input - simplified
                import re
                path_match = re.search(r'["\']([^"\']+\.[^"\']+)["\']', input_data)
                if path_match:
                    path = path_match.group(1)
                    result = self.tool_executor.execute("read_file", path=path)
                    return {
                        "type": "execution",
                        "response": f"File content: {result.get('result', 'Error reading file')}",
                        "tool_result": result
                    }
        
        return {
            "type": "execution",
            "response": f"Executed task: {input_data}",
            "context": [mem.content[:100] + "..." for mem in memories[:3]]
        }
    
    def _coordinate_tasks(self, input_data: str) -> Dict:
        """Coordinate multiple tasks"""
        # Search for relevant memories
        memories = self.memory.search_memories(input_data)
        
        response = {
            "type": "coordination",
            "response": f"Coordinated tasks for: {input_data}",
            "context": [mem.content[:100] + "..." for mem in memories[:3]]
        }
        
        # Add coordination logic here in a more complete implementation
        return response

class TaskDecompositionEngine:
    """Engine to decompose complex tasks into subtasks"""
    
    def __init__(self):
        self.decomposition_rules = {
            "coding": ["requirements_analysis", "design", "implementation", "testing", "documentation"],
            "research": ["topic_identification", "source_gathering", "data_analysis", "synthesis", "reporting"],
            "analysis": ["data_collection", "data_cleaning", "exploration", "modeling", "interpretation"],
            "creative": ["brainstorming", "concept_development", "drafting", "refinement", "finalization"]
        }
    
    def decompose_task(self, task_description: str) -> List[Task]:
        """Decompose a task into subtasks"""
        # Identify task type
        task_type = self._identify_task_type(task_description)
        
        # Get decomposition steps
        steps = self.decomposition_rules.get(task_type, ["analyze", "plan", "execute", "review"])
        
        subtasks = []
        for i, step in enumerate(steps):
            subtask = Task(
                title=f"{step.replace('_', ' ').title()}",
                description=f"Subtask {i+1}: {step} for '{task_description}'",
                agent_type=AgentType.WORKER if i < len(steps)-1 else AgentType.COORDINATOR,
                priority=len(steps)-i,  # Later steps have lower priority
                dependencies=[subtasks[-1].id] if subtasks else []  # Each depends on previous
            )
            subtasks.append(subtask)
        
        # Create a parent task that encompasses all subtasks
        parent_task = Task(
            title=f"Parent: {task_description}",
            description=f"Parent task that decomposes '{task_description}'",
            agent_type=AgentType.PLANNER,
            priority=5
        )
        
        # Add parent task as first in the list
        return [parent_task] + subtasks
    
    def _identify_task_type(self, task_description: str) -> str:
        """Identify the type of task based on keywords"""
        desc_lower = task_description.lower()
        
        if any(keyword in desc_lower for keyword in ["code", "program", "develop", "function", "algorithm"]):
            return "coding"
        elif any(keyword in desc_lower for keyword in ["research", "study", "investigate", "analyze", "examine"]):
            return "research"
        elif any(keyword in desc_lower for keyword in ["analyze", "analysis", "data", "pattern", "trend"]):
            return "analysis"
        elif any(keyword in desc_lower for keyword in ["write", "create", "design", "story", "poem", "article"]):
            return "creative"
        else:
            return "general"

class AgentSystem:
    """Main agent system controller"""
    
    def __init__(self):
        self.agents: Dict[str, AgentBrain] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_queue: List[Task] = []
        self.memory = AgentMemory()
        self.task_decomposer = TaskDecompositionEngine()
        self._create_default_agents()
    
    def _create_default_agents(self):
        """Create default planner and worker agents"""
        planner = AgentBrain("planner-001", AgentType.PLANNER, self.memory)
        worker = AgentBrain("worker-001", AgentType.WORKER, self.memory)
        coordinator = AgentBrain("coordinator-001", AgentType.COORDINATOR, self.memory)
        
        self.agents[planner.id] = planner
        self.agents[worker.id] = worker
        self.agents[coordinator.id] = coordinator
    
    def create_agent(self, agent_type: AgentType, custom_memory: AgentMemory = None) -> AgentBrain:
        """Create a new agent"""
        agent_id = f"{agent_type.value}-{uuid.uuid4().hex[:8]}"
        agent = AgentBrain(agent_id, agent_type, custom_memory or self.memory)
        self.agents[agent_id] = agent
        return agent
    
    def submit_task(self, description: str, agent_type: AgentType = AgentType.WORKER) -> str:
        """Submit a new task"""
        task = Task(
            title=description[:50] + ("..." if len(description) > 50 else ""),
            description=description,
            agent_type=agent_type,
            status=TaskStatus.PENDING
        )
        
        self.tasks[task.id] = task
        self.task_queue.append(task)
        
        # Sort queue by priority
        self.task_queue.sort(key=lambda x: x.priority, reverse=True)
        
        return task.id
    
    def decompose_task(self, task_description: str) -> List[str]:
        """Decompose a complex task into subtasks"""
        subtasks = self.task_decomposer.decompose_task(task_description)
        task_ids = []
        
        for subtask in subtasks:
            self.tasks[subtask.id] = subtask
            self.task_queue.append(subtask)
            task_ids.append(subtask.id)
        
        # Sort queue by priority
        self.task_queue.sort(key=lambda x: x.priority, reverse=True)
        
        return task_ids
    
    def get_task_status(self, task_id: str) -> Optional[Task]:
        """Get status of a specific task"""
        return self.tasks.get(task_id)
    
    def get_active_tasks(self) -> List[Task]:
        """Get all active tasks"""
        return [task for task in self.tasks.values() 
                if task.status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]]
    
    def process_next_task(self) -> Optional[Dict]:
        """Process the next task in the queue"""
        if not self.task_queue:
            return None
        
        # Get highest priority pending task
        pending_tasks = [t for t in self.task_queue if t.status == TaskStatus.PENDING]
        if not pending_tasks:
            return None
        
        task = max(pending_tasks, key=lambda x: x.priority)
        
        # Find appropriate agent
        suitable_agents = [a for a in self.agents.values() if a.type == task.agent_type]
        if not suitable_agents:
            suitable_agents = [a for a in self.agents.values()]  # Fallback to any agent
        
        if not suitable_agents:
            return {"error": "No agents available"}
        
        agent = suitable_agents[0]  # Select first available agent of correct type
        
        # Process the task
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()
        task.assigned_agent = agent.id
        
        result = agent.think(task.description)
        
        # Update task status
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        task.result = result
        
        # Remove from queue
        self.task_queue.remove(task)
        
        return {
            "task_id": task.id,
            "agent_id": agent.id,
            "result": result,
            "task": task
        }

def main():
    """Demo of Phase 3 implementation"""
    print("🚀 NEXAFORGE - PHASE 3: AGENT SYSTEM (L4)")
    print("=" * 50)
    
    # Initialize the agent system
    agent_system = AgentSystem()
    
    print(f"\n🤖 AGENTS CREATED:")
    for agent_id, agent in agent_system.agents.items():
        print(f"  • {agent_id} ({agent.type.value})")
    
    print(f"\n📋 AVAILABLE TASKS IN QUEUE: {len(agent_system.task_queue)}")
    
    # Demo task decomposition
    print(f"\n🔄 TASK DECOMPOSITION DEMO:")
    complex_task = "Write a Python program that analyzes sales data and generates a report"
    print(f"Original task: {complex_task}")
    
    subtask_ids = agent_system.decompose_task(complex_task)
    print(f"Created {len(subtask_ids)} subtasks:")
    
    for i, task_id in enumerate(subtask_ids[1:], 1):  # Skip parent task
        task = agent_system.get_task_status(task_id)
        print(f"  {i}. {task.title} (Priority: {task.priority})")
    
    # Submit some additional tasks
    print(f"\n📝 SUBMITTING ADDITIONAL TASKS:")
    task1_id = agent_system.submit_task("Calculate the sum of 15 and 27", AgentType.WORKER)
    print(f"  • Task submitted: {task1_id} - Calculate sum")
    
    task2_id = agent_system.submit_task("Research information about quantum computing", AgentType.WORKER)
    print(f"  • Task submitted: {task2_id} - Research quantum computing")
    
    print(f"\n📋 TOTAL TASKS IN SYSTEM: {len(agent_system.tasks)}")
    print(f"📋 TASKS IN QUEUE: {len(agent_system.task_queue)}")
    
    # Process some tasks
    print(f"\n⚙️  PROCESSING TASKS:")
    for i in range(2):  # Process 2 tasks
        result = agent_system.process_next_task()
        if result:
            print(f"  Processed task {result['task_id'][:8]}... with agent {result['agent_id']}")
            print(f"  Result type: {result['result'].get('type', 'unknown')}")
        else:
            print("  No tasks to process")
            break
    
    # Show active tasks
    active_tasks = agent_system.get_active_tasks()
    print(f"\n📊 ACTIVE TASKS: {len(active_tasks)}")
    for task in active_tasks:
        print(f"  • {task.title} - {task.status.value}")

if __name__ == "__main__":
    main()