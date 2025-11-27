from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
import asyncio
import json
from .engine.types import WorkflowState, NodeStatus


class WorkflowStateStorage:
    """In-memory storage for workflow states"""
    
    def __init__(self):
        self.states: Dict[str, WorkflowState] = {}
        self.history: List[WorkflowState] = []
        self.lock = asyncio.Lock()
    
    async def save_state(self, state: WorkflowState) -> None:
        """Save workflow state"""
        async with self.lock:
            self.states[state.workflow_id] = state
            if state.status in [NodeStatus.COMPLETED, NodeStatus.FAILED]:
                self.history.append(state)
    
    async def get_state(self, workflow_id: str) -> Optional[WorkflowState]:
        """Get workflow state by ID"""
        async with self.lock:
            return self.states.get(workflow_id)
    
    async def update_state(self, workflow_id: str, updates: Dict[str, Any]) -> Optional[WorkflowState]:
        """Update workflow state"""
        async with self.lock:
            if workflow_id not in self.states:
                return None
            
            state = self.states[workflow_id]
            
            for key, value in updates.items():
                if hasattr(state, key):
                    setattr(state, key, value)
            
            return state
    
    async def get_history(self, limit: int = 100) -> List[WorkflowState]:
        """Get workflow execution history"""
        async with self.lock:
            return self.history[-limit:]
    
    async def cleanup_completed(self) -> int:
        """Clean up completed workflows from memory"""
        async with self.lock:
            completed_ids = [
                wf_id for wf_id, state in self.states.items() 
                if state.status in [NodeStatus.COMPLETED, NodeStatus.FAILED]
            ]
            
            for wf_id in completed_ids:
                del self.states[wf_id]
            
            return len(completed_ids)


class PersistentWorkflowStateStorage(WorkflowStateStorage):
    """Persistent storage for workflow states (extends in-memory with file persistence)"""
    
    def __init__(self, storage_file: str = "workflow_states.json"):
        super().__init__()
        self.storage_file = storage_file
        self.load_from_file()
    
    def load_from_file(self):
        """Load workflow states from file"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                # Convert back to objects
                for state_data in data.get('states', []):
                    # Convert datetime strings back to datetime objects
                    started_at = datetime.fromisoformat(state_data['started_at']) if state_data.get('started_at') else None
                    completed_at = datetime.fromisoformat(state_data['completed_at']) if state_data.get('completed_at') else None
                    
                    state = WorkflowState(
                        workflow_id=state_data['workflow_id'],
                        current_level=state_data['current_level'],
                        current_node=state_data['current_node'],
                        status=NodeStatus(state_data['status']),
                        context=state_data['context'],
                        started_at=started_at,
                        completed_at=completed_at,
                        error_message=state_data.get('error_message'),
                        execution_path=state_data.get('execution_path', [])
                    )
                    self.states[state.workflow_id] = state
        
        except FileNotFoundError:
            # File doesn't exist yet, that's OK
            pass
        except Exception as e:
            print(f"Error loading workflow states from file: {e}")
    
    async def save_state(self, state: WorkflowState) -> None:
        """Save workflow state to memory and persist to file"""
        await super().save_state(state)
        self.save_to_file()
    
    def save_to_file(self):
        """Save workflow states to file"""
        try:
            # Convert states to serializable format
            states_data = []
            for state in self.states.values():
                state_dict = {
                    'workflow_id': state.workflow_id,
                    'current_level': state.current_level,
                    'current_node': state.current_node,
                    'status': state.status.value,
                    'context': state.context,
                    'started_at': state.started_at.isoformat() if state.started_at else None,
                    'completed_at': state.completed_at.isoformat() if state.completed_at else None,
                    'error_message': state.error_message,
                    'execution_path': state.execution_path
                }
                states_data.append(state_dict)
            
            with open(self.storage_file, 'w') as f:
                json.dump({'states': states_data}, f, indent=2)
        
        except Exception as e:
            print(f"Error saving workflow states to file: {e}")


# Global instance
state_storage = PersistentWorkflowStateStorage()