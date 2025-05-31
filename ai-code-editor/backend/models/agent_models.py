"""
Core data models for the Agentic Middleware system - Pydantic V2 Compatible.
These models define the fundamental data structures used throughout the application.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator, ConfigDict


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


# ============================================================================
# Core Data Models
# ============================================================================

class ExecutionContext(BaseModel):
    """Context information for agent execution."""
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()},
        use_enum_values=True
    )
    
    session_id: str
    user_id: str
    project_id: str
    workspace_path: str
    environment: str = "development"
    language: Optional[str] = None
    framework: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @field_validator('workspace_path')
    @classmethod
    def validate_workspace_path(cls, v: str) -> str:
        """Ensure workspace path is not empty."""
        if not v or not v.strip():
            raise ValueError("Workspace path cannot be empty")
        return v.strip()

class TaskRequest(BaseModel):
    """Request to execute a task."""
    model_config = ConfigDict(
        use_enum_values=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
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
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Ensure description is not empty."""
        if not v or not v.strip():
            raise ValueError("Task description cannot be empty")
        return v.strip()
    
    @field_validator('timeout')
    @classmethod
    def validate_timeout(cls, v: int) -> int:
        """Ensure timeout is reasonable."""
        if v < 1:
            raise ValueError("Timeout must be at least 1 second")
        if v > 3600:  # 1 hour max
            raise ValueError("Timeout cannot exceed 1 hour")
        return v

class TaskResult(BaseModel):
    """Result of task execution."""
    model_config = ConfigDict(
        use_enum_values=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )
    
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
    
    @field_validator('execution_time')
    @classmethod
    def validate_execution_time(cls, v: float) -> float:
        """Ensure execution time is non-negative."""
        if v < 0:
            raise ValueError("Execution time cannot be negative")
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

class ChatMessage(BaseModel):
    """Chat message from user."""
    message: str
    session_id: str
    user_id: str = "default_user"
    project_id: str = "default_project" 
    workspace_path: str = "/tmp/workspace"
    parameters: Dict[str, Any] = Field(default_factory=dict)
    stream: bool = False
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
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

class SystemStatus(BaseModel):
    """Overall system status."""
    status: str
    active_sessions: int
    agents: List[Dict[str, Any]]
    uptime: float
    version: str = "0.1.0"
    total_requests: int = 0
    total_errors: int = 0
    average_response_time: float = 0.0


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
    
    @field_validator('provider')
    @classmethod
    def validate_provider(cls, v: str) -> str:
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
    log_level: str = Field(default="INFO", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    max_sessions: int = Field(default=1000, ge=1)
    session_timeout: int = Field(default=3600, ge=300)


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
# Test the Models
# ============================================================================

if __name__ == "__main__":
    """Test the data models to ensure they work correctly."""
    
    print("🧪 Testing Pydantic V2 Compatible Data Models...")
    
    try:
        # Test ExecutionContext
        context = create_execution_context(
            session_id="test-session-123",
            user_id="developer-1", 
            project_id="ai-editor-project",
            workspace_path="/tmp/test-workspace"
        )
        print(f"✅ ExecutionContext created: {context.session_id}")
        
        # Test TaskRequest
        task = create_task_request(
            description="Create a FastAPI application with JWT authentication",
            context=context,
            intent=IntentType.CODE_GENERATION,
            priority=Priority.HIGH
        )
        print(f"✅ TaskRequest created: {task.id}")
        
        # Test TaskResult
        result = create_task_result(
            task_id=task.id,
            agent_type=AgentType.CODE,
            status=TaskStatus.COMPLETED,
            result={"code": "print('Hello, World!')", "language": "python"}
        )
        print(f"✅ TaskResult created: {result.status}")
        
        # Test ChatMessage  
        chat_msg = ChatMessage(
            message="Generate a Python function to calculate fibonacci numbers",
            session_id="test-session",
            user_id="developer",
            project_id="fibonacci-project"
        )
        print(f"✅ ChatMessage created: {chat_msg.message[:50]}...")
        
        print("\n🎉 All tests passed! Pydantic V2 models are working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


# ============================================================================
# Export All Models
# ============================================================================

__all__ = [
    # Enums
    "AgentType", "TaskStatus", "IntentType", "Priority", "MessageType",
    
    # Core Models
    "ExecutionContext", "TaskRequest", "TaskResult",
    
    # Request/Response
    "ChatMessage", "ChatResponse", "SystemStatus",
    
    # Configuration
    "LLMConfig", "AgentConfig", "SystemConfig",
    
    # Utilities
    "create_execution_context", "create_task_request", "create_task_result",
]
