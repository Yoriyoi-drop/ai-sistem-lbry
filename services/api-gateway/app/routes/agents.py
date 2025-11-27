"""
Agents routes – expose example AI agents.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_agents():
    """Return a list of available agents (stub)."""
    return {
        "agents": [
            {"id": "example", "name": "Example Agent", "status": "active"},
            {"id": "scanner", "name": "Scanner Agent", "status": "active"},
            {"id": "analyzer", "name": "Analyzer Agent", "status": "active"}
        ]
    }

@router.post("/process")
async def process_agent(payload: dict):
    """Process a payload through an agent (stub)."""
    return {
        "status": "success",
        "agent": "example",
        "input": payload,
        "output": {"message": "Processed successfully", "data": payload}
    }
