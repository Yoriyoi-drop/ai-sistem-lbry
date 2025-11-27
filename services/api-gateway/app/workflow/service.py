from typing import Dict, Any, Optional, List
from fastapi import HTTPException, status
from .engine.types import WorkflowState
from .orchestrator.orchestrator import global_orchestrator, initialize_workflows
import asyncio
import uuid


class WorkflowService:
    """Service layer for workflow management"""
    
    def __init__(self):
        self.initialized = False
    
    async def initialize(self):
        """Initialize the workflow service and all workflows"""
        if not self.initialized:
            await initialize_workflows()
            self.initialized = True
    
    async def create_workflow_execution(self, workflow_type: str, 
                                      context: Dict[str, Any]) -> Dict[str, Any]:
        """Create and start a new workflow execution"""
        if not self.initialized:
            await self.initialize()
        
        # Generate unique workflow ID
        workflow_id = f"wf_{uuid.uuid4().hex[:8]}"
        
        # Choose appropriate engine based on workflow type
        if workflow_type == "basic":
            engine_id = "basic_security_engine"
        elif workflow_type == "advanced":
            engine_id = "complex_workflow_engine"
        else:
            engine_id = "basic_security_engine"  # default
        
        try:
            # Start the workflow execution
            result = await global_orchestrator.execute_workflow(engine_id, workflow_id, context)
            
            return {
                "workflow_id": workflow_id,
                "status": result.status.value,
                "started_at": result.started_at.isoformat() if result.started_at else None,
                "completed_at": result.completed_at.isoformat() if result.completed_at else None,
                "result": result.context,
                "execution_path": result.execution_path
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to execute workflow: {str(e)}"
            )
    
    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get the status of a running workflow"""
        # Note: In a real implementation, this would check the active states
        # For now, this is a placeholder
        return {
            "workflow_id": workflow_id,
            "status": "completed",  # placeholder
            "progress": 100,  # placeholder
            "execution_path": [],  # placeholder
            "last_updated": "2025-11-27T06:00:00Z"  # placeholder
        }
    
    async def get_all_workflows(self) -> Dict[str, Any]:
        """Get information about all available workflows"""
        validation_results = global_orchestrator.validate_all_workflows()
        
        return {
            "workflow_engines": list(validation_results.keys()),
            "validation_results": validation_results,
            "status": "active" if self.initialized else "not_initialized",
            "available_types": ["basic", "advanced", "complex"]
        }
    
    async def get_workflow_statistics(self) -> Dict[str, Any]:
        """Get statistics about workflow executions"""
        validation_results = global_orchestrator.validate_all_workflows()
        
        total_nodes = sum(result["node_count"] for result in validation_results.values())
        total_levels = sum(result["level_count"] for result in validation_results.values())
        
        return {
            "total_workflows": len(validation_results),
            "total_nodes": total_nodes,
            "total_levels": total_levels,
            "engines": len(validation_results),
            "average_nodes_per_engine": total_nodes / len(validation_results) if validation_results else 0,
            "average_levels_per_engine": total_levels / len(validation_results) if validation_results else 0
        }


# Global workflow service instance
workflow_service = WorkflowService()


async def get_workflow_service():
    """Dependency to get the workflow service"""
    if not workflow_service.initialized:
        await workflow_service.initialize()
    return workflow_service