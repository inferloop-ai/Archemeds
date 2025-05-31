# Complete Data Models Implementation
# backend/models/agent_models.py

"""
Core data models for the Agentic Middleware system.
These models define the fundamental data structures used throughout the application.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator


# ============================================================================
# Enums
# ============================================================================

class AgentType(str, Enum):
    """Types of available agents in the system."""
    CODE = "code"
    INFRASTRUCTURE = "infrastructure" 
    TESTING = "testing"
    DEVOPS = "devops"
    DOCUMENTATION = "documentation"
    SECURITY = "security"
    PLANNING = "planning"
    REVIEW = "review"

class TaskStatus(str, Enum):
    """Task execution statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class IntentType(str, Enum):
    """Types of user intents that can be classified."""
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    CODE_REFACTORING = "refactoring"
    INFRASTRUCTURE_SETUP = "infrastructure_setup"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    DOCUMENTATION = "documentation"
    DEBUGGING = "debugging"
    SECURITY_SCAN = "security_scan"
    EXPLANATION = "explanation"
    PROJECT_SETUP = "project_setup"

class Priority(int, Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 5
    HIGH = 8
    CRITICAL = 10

class MessageType(str, Enum):
    """Types of messages in the system."""
    USER_INPUT = "user_input"
    AGENT_RESPONSE = "agent_response"
    SYSTEM_NOTIFICATION = "system_notification"
    ERROR = "error"
    STATUS_UPDATE = "status_update"

class ContextType(str, Enum):
    """Types of context data."""
    PROJECT = "project"
    FILE = "file"
    CONVERSATION = "conversation"
    AGENT_STATE = "agent_state"
    USER_PREFERENCE = "user_preference"


# ============================================================================
# Core Data Models
# ============================================================================

class ExecutionContext(BaseModel):
    """Context information for agent execution."""
    session_id: str
    user_id: str
    project_id: str
    workspace_path: str
    environment: str = "development"
    language: Optional[str] = None
    framework: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('workspace_path')
    def validate_workspace_path(cls, v):
        """Ensure workspace path is not empty."""
        if not v or not v.strip():
            raise ValueError("Workspace path cannot be empty")
        return v.strip()
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AgentCapability(BaseModel):
    """Represents what an agent can do."""
    name: str
    description: str
    required_context: List[str] = Field(default_factory=list)
    outputs: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    estimated_duration: int = 60  # seconds
    complexity_level: int = Field(default=1, ge=1, le=10)
    
    @validator('name')
    def validate_name(cls, v):
        """Ensure capability name is valid."""
        if not v or not v.strip():
            raise ValueError("Capability name cannot be empty")
        return v.strip().lower()

class TaskRequest(BaseModel):
    """Request to execute a task."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    intent: IntentType
    description: str
    context: ExecutionContext
    parameters: Dict[str, Any] = Field(default_factory=dict)
    priority: Priority = Priority.MEDIUM
    timeout: int = Field(default=300, description="Timeout in seconds")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    parent_task_id: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    
    @validator('description')
    def validate_description(cls, v):
        """Ensure description is not empty."""
        if not v or not v.strip():
            raise ValueError("Task description cannot be empty")
        return v.strip()
    
    @validator('timeout')
    def validate_timeout(cls, v):
        """Ensure timeout is reasonable."""
        if v < 1:
            raise ValueError("Timeout must be at least 1 second")
        if v > 3600:  # 1 hour max
            raise ValueError("Timeout cannot exceed 1 hour")
        return v
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TaskResult(BaseModel):
    """Result of task execution."""
    task_id: str
    agent_type: AgentType
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    tokens_used: int = 0
    cost: float = 0.0
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    @validator('execution_time')
    def validate_execution_time(cls, v):
        """Ensure execution time is non-negative."""
        if v < 0:
            raise ValueError("Execution time cannot be negative")
        return v
    
    @validator('tokens_used')
    def validate_tokens_used(cls, v):
        """Ensure tokens used is non-negative."""
        if v < 0:
            raise ValueError("Tokens used cannot be negative")
        return v
    
    def mark_completed(self, result: Dict[str, Any] = None):
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        if result:
            self.result = result
    
    def mark_failed(self, error: str):
        """Mark the task as failed."""
        self.status = TaskStatus.FAILED
        self.error = error
        self.completed_at = datetime.utcnow()
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AgentMessage(BaseModel):
    """Message between agents or from user."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    from_agent: Optional[AgentType] = None
    to_agent: Optional[AgentType] = None
    message_type: MessageType
    content: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: str
    priority: Priority = Priority.MEDIUM
    requires_response: bool = False
    
    @validator('content')
    def validate_content(cls, v):
        """Ensure message content is not empty."""
        if not v or not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# ============================================================================
# Request/Response Models
# ============================================================================

class ChatMessage(BaseModel):
    """Chat message from user."""
    message: str
    session_id: str
    user_id: str = "default_user"
    project_id: str = "default_project" 
    workspace_path: str = "/tmp/workspace"
    parameters: Dict[str, Any] = Field(default_factory=dict)
    stream: bool = False
    
    @validator('message')
    def validate_message(cls, v):
        """Ensure message is not empty."""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()

class ChatResponse(BaseModel):
    """Response from the agentic system."""
    session_id: str
    response: Dict[str, Any]
    processing_time: float
    timestamp: str
    task_id: Optional[str] = None
    agent_type: Optional[AgentType] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

class AgentStatus(BaseModel):
    """Status of an agent."""
    agent_type: AgentType
    status: str
    capabilities: List[str]
    active_tasks: int = 0
    total_tasks_completed: int = 0
    average_execution_time: float = 0.0
    success_rate: float = Field(default=1.0, ge=0.0, le=1.0)
    last_activity: Optional[datetime] = None

class SystemStatus(BaseModel):
    """Overall system status."""
    status: str
    active_sessions: int
    agents: List[AgentStatus]
    uptime: float
    version: str = "0.1.0"
    total_requests: int = 0
    total_errors: int = 0
    average_response_time: float = 0.0


# ============================================================================
# Planning Models
# ============================================================================

class ExecutionStep(BaseModel):
    """A single step in an execution plan."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_type: AgentType
    task: TaskRequest
    dependencies: List[str] = Field(default_factory=list)
    estimated_duration: int = 60
    status: TaskStatus = TaskStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    
    def can_execute(self, completed_steps: set) -> bool:
        """Check if this step can be executed based on dependencies."""
        return all(dep_id in completed_steps for dep_id in self.dependencies)

class ExecutionPlan(BaseModel):
    """Plan for executing a complex task."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    original_task: TaskRequest
    steps: List[ExecutionStep]
    estimated_total_duration: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    
    def get_ready_steps(self, completed_step_ids: set) -> List[ExecutionStep]:
        """Get steps that are ready to execute."""
        ready_steps = []
        for step in self.steps:
            if step.status == TaskStatus.PENDING and step.can_execute(completed_step_ids):
                ready_steps.append(step)
        return ready_steps
    
    def get_progress(self) -> float:
        """Get execution progress as percentage."""
        if not self.steps:
            return 0.0
        
        completed = len([s for s in self.steps if s.status == TaskStatus.COMPLETED])
        return (completed / len(self.steps)) * 100.0


# ============================================================================
# Configuration Models
# ============================================================================

class LLMConfig(BaseModel):
    """Configuration for LLM providers."""
    provider: str = "openai"
    api_key: str
    model: str = "gpt-4"
    max_tokens: int = 4000
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    timeout: int = Field(default=30, ge=1, le=300)
    max_retries: int = Field(default=3, ge=0, le=10)
    
    @validator('provider')
    def validate_provider(cls, v):
        """Validate LLM provider."""
        valid_providers = ["openai", "anthropic", "claude", "deepseek", "mock"]
        if v.lower() not in valid_providers:
            raise ValueError(f"Provider must be one of: {valid_providers}")
        return v.lower()

class AgentConfig(BaseModel):
    """Configuration for agents."""
    enabled_agents: List[AgentType] = Field(default_factory=lambda: [
        AgentType.CODE, 
        AgentType.INFRASTRUCTURE, 
        AgentType.TESTING
    ])
    max_concurrent_tasks: int = Field(default=10, ge=1, le=100)
    default_timeout: int = Field(default=300, ge=30, le=3600)
    retry_enabled: bool = True
    max_retries: int = Field(default=3, ge=0, le=10)

class SystemConfig(BaseModel):
    """Overall system configuration."""
    redis_url: str = "redis://localhost:6379"
    llm: LLMConfig
    agents: AgentConfig = Field(default_factory=AgentConfig)
    debug: bool = False
    log_level: str = Field(default="INFO", regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    max_sessions: int = Field(default=1000, ge=1)
    session_timeout: int = Field(default=3600, ge=300)  # 1 hour default


# ============================================================================
# Error Models
# ============================================================================

class AgentError(BaseModel):
    """Error information from agent execution."""
    error_type: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    recoverable: bool = True
    error_code: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ValidationError(AgentError):
    """Validation error details."""
    field: str
    value: Any
    constraint: str
    
    def __init__(self, field: str, value: Any, constraint: str, **kwargs):
        super().__init__(
            error_type="validation_error",
            message=f"Validation failed for field '{field}': {constraint}",
            details={"field": field, "value": value, "constraint": constraint},
            **kwargs
        )
        self.field = field
        self.value = value
        self.constraint = constraint

class TimeoutError(AgentError):
    """Timeout error details."""
    timeout_duration: int
    
    def __init__(self, timeout_duration: int, **kwargs):
        super().__init__(
            error_type="timeout_error",
            message=f"Operation timed out after {timeout_duration} seconds",
            details={"timeout_duration": timeout_duration},
            recoverable=True,
            **kwargs
        )
        self.timeout_duration = timeout_duration

class LLMError(AgentError):
    """LLM-specific error details."""
    provider: str
    model: str
    tokens_used: int = 0
    
    def __init__(self, provider: str, model: str, message: str, tokens_used: int = 0, **kwargs):
        super().__init__(
            error_type="llm_error",
            message=message,
            details={"provider": provider, "model": model, "tokens_used": tokens_used},
            **kwargs
        )
        self.provider = provider
        self.model = model
        self.tokens_used = tokens_used


# ============================================================================
# Session Models
# ============================================================================

class SessionContext(BaseModel):
    """Session context information."""
    session_id: str
    user_id: str
    project_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    message_count: int = 0
    active_agents: List[AgentType] = Field(default_factory=list)
    context_data: Dict[str, Any] = Field(default_factory=dict)
    
    def update_activity(self):
        """Update last activity timestamp."""
        self.last_activity = datetime.utcnow()
        self.message_count += 1

class ConversationHistory(BaseModel):
    """Conversation history for a session."""
    session_id: str
    messages: List[AgentMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def add_message(self, message: AgentMessage):
        """Add a message to the conversation."""
        self.messages.append(message)
        self.updated_at = datetime.utcnow()
    
    def get_recent_messages(self, limit: int = 10) -> List[AgentMessage]:
        """Get recent messages."""
        return self.messages[-limit:] if self.messages else []


# ============================================================================
# Utility Functions
# ============================================================================

def create_execution_context(
    session_id: str,
    user_id: str = "default_user",
    project_id: str = "default_project",
    workspace_path: str = "/tmp/workspace",
    **metadata
) -> ExecutionContext:
    """Create an execution context with defaults."""
    return ExecutionContext(
        session_id=session_id,
        user_id=user_id,
        project_id=project_id,
        workspace_path=workspace_path,
        metadata=metadata
    )

def create_task_request(
    description: str,
    context: ExecutionContext,
    intent: IntentType = IntentType.CODE_GENERATION,
    priority: Priority = Priority.MEDIUM,
    **parameters
) -> TaskRequest:
    """Create a task request with defaults."""
    return TaskRequest(
        intent=intent,
        description=description,
        context=context,
        parameters=parameters,
        priority=priority
    )

def create_agent_message(
    content: str,
    session_id: str,
    message_type: MessageType = MessageType.AGENT_RESPONSE,
    from_agent: Optional[AgentType] = None,
    to_agent: Optional[AgentType] = None,
    **payload
) -> AgentMessage:
    """Create an agent message with defaults."""
    return AgentMessage(
        content=content,
        session_id=session_id,
        message_type=message_type,
        from_agent=from_agent,
        to_agent=to_agent,
        payload=payload
    )

def create_task_result(
    task_id: str,
    agent_type: AgentType,
    status: TaskStatus = TaskStatus.COMPLETED,
    result: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
    execution_time: float = 0.0
) -> TaskResult:
    """Create a task result with defaults."""
    task_result = TaskResult(
        task_id=task_id,
        agent_type=agent_type,
        status=status,
        result=result,
        error=error,
        execution_time=execution_time
    )
    
    if status == TaskStatus.COMPLETED:
        task_result.completed_at = datetime.utcnow()
    
    return task_result


# ============================================================================
# Model Validation Utilities
# ============================================================================

def validate_task_request(task: TaskRequest) -> List[str]:
    """Validate a task request and return any validation errors."""
    errors = []
    
    if not task.description.strip():
        errors.append("Task description cannot be empty")
    
    if task.timeout < 1 or task.timeout > 3600:
        errors.append("Timeout must be between 1 and 3600 seconds")
    
    if not task.context.workspace_path.strip():
        errors.append("Workspace path cannot be empty")
    
    return errors

def validate_execution_context(context: ExecutionContext) -> List[str]:
    """Validate an execution context and return any validation errors."""
    errors = []
    
    if not context.session_id.strip():
        errors.append("Session ID cannot be empty")
    
    if not context.user_id.strip():
        errors.append("User ID cannot be empty")
    
    if not context.project_id.strip():
        errors.append("Project ID cannot be empty")
    
    if not context.workspace_path.strip():
        errors.append("Workspace path cannot be empty")
    
    return errors


# ============================================================================
# Export All Models
# ============================================================================

__all__ = [
    # Enums
    "AgentType",
    "TaskStatus", 
    "IntentType",
    "Priority",
    "MessageType",
    "ContextType",
    
    # Core Models
    "ExecutionContext",
    "AgentCapability",
    "TaskRequest",
    "TaskResult",
    "AgentMessage",
    
    # Request/Response
    "ChatMessage",
    "ChatResponse", 
    "AgentStatus",
    "SystemStatus",
    
    # Planning
    "ExecutionStep",
    "ExecutionPlan",
    
    # Configuration
    "LLMConfig",
    "AgentConfig",
    "SystemConfig",
    
    # Errors
    "AgentError",
    "ValidationError",
    "TimeoutError",
    "LLMError",
    
    # Session
    "SessionContext",
    "ConversationHistory",
    
    # Utilities
    "create_execution_context",
    "create_task_request",
    "create_agent_message",
    "create_task_result",
    "validate_task_request",
    "validate_execution_context",
]