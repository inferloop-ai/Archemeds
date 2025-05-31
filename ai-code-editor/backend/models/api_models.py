"""
API-specific models for request/response handling.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from .agent_models import AgentType, TaskStatus


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str = "0.1.0"

class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: str

class ChatRequest(BaseModel):
    """Chat request from client."""
    message: str
    session_id: str
    user_id: str = "default_user"
    project_id: str = "default_project"
    workspace_path: str = "/tmp/workspace"
    parameters: Dict[str, Any] = Field(default_factory=dict)
    stream: bool = False

class AsyncTaskResponse(BaseModel):
    """Response for async task creation."""
    task_id: str
    status: str
    estimated_duration: Optional[int] = None
    message: str = "Task started"

class TaskStatusResponse(BaseModel):
    """Task status response."""
    task_id: str
    status: TaskStatus
    progress: float = 0.0
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: str
    updated_at: str

class AgentListResponse(BaseModel):
    """List of available agents."""
    agents: List[Dict[str, Any]]
    total: int

class SessionContextResponse(BaseModel):
    """Session context response."""
    session_id: str
    conversation_history: List[Dict[str, Any]]
    project_context: Dict[str, Any]
    available_agents: List[str]
