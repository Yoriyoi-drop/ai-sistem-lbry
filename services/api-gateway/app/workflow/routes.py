from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from .service import get_workflow_service, WorkflowService
from pydantic import BaseModel


class WorkflowRequest(BaseModel):
    """Request model for workflow execution"""
    workflow_type: str
    context: Dict[str, Any]


class WorkflowResponse(BaseModel):
    """Response model for workflow execution"""
    workflow_id: str
    status: str
    started_at: str
    completed_at: str
    result: Dict[str, Any]
    execution_path: list


class WorkflowStatusResponse(BaseModel):
    """Response model for workflow status"""
    workflow_id: str
    status: str
    progress: int
    execution_path: list
    last_updated: str


router = APIRouter(prefix="/workflow", tags=["workflow"])


@router.post("/execute", response_model=WorkflowResponse)
async def execute_workflow(
    request: WorkflowRequest,
    service: WorkflowService = Depends(get_workflow_service)
) -> Dict[str, Any]:
    """Execute a new workflow"""
    return await service.create_workflow_execution(request.workflow_type, request.context)


@router.get("/{workflow_id}/status", response_model=WorkflowStatusResponse)
async def get_workflow_status(
    workflow_id: str,
    service: WorkflowService = Depends(get_workflow_service)
) -> Dict[str, Any]:
    """Get the status of a running workflow"""
    return await service.get_workflow_status(workflow_id)


@router.get("/engines", response_model=Dict[str, Any])
async def get_all_workflows(
    service: WorkflowService = Depends(get_workflow_service)
) -> Dict[str, Any]:
    """Get information about all available workflows"""
    return await service.get_all_workflows()


@router.get("/stats", response_model=Dict[str, Any])
async def get_workflow_stats(
    service: WorkflowService = Depends(get_workflow_service)
) -> Dict[str, Any]:
    """Get statistics about workflow engines"""
    return await service.get_workflow_statistics()


@router.post("/validate")
async def validate_workflows(
    service: WorkflowService = Depends(get_workflow_service)
) -> Dict[str, Any]:
    """Validate all workflow configurations"""
    results = service.global_orchestrator.validate_all_workflows()
    return results