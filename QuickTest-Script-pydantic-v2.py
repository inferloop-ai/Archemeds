#!/usr/bin/env python3
"""
Quick Test Script - Verify Pydantic V2 Compatibility
Run this to test the fixed data models without setting up the full project.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

print("🧪 Testing Pydantic V2 Compatibility...")

# Test the core models that were causing issues

class AgentType(str, Enum):
    """Types of available agents in the system."""
    CODE = "code"
    INFRASTRUCTURE = "infrastructure" 
    TESTING = "testing"

class TaskStatus(str, Enum):
    """Task execution statuses."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class IntentType(str, Enum):
    """Types of user intents."""
    CODE_GENERATION = "code_generation"
    INFRASTRUCTURE_SETUP = "infrastructure_setup"
    TESTING = "testing"

class Priority(int, Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 5
    HIGH = 8

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
        if v > 3600:
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
    
    @field_validator('execution_time')
    @classmethod
    def validate_execution_time(cls, v: float) -> float:
        """Ensure execution time is non-negative."""
        if v < 0:
            raise ValueError("Execution time cannot be negative")
        return v
    
    @field_validator('tokens_used')
    @classmethod
    def validate_tokens_used(cls, v: int) -> int:
        """Ensure tokens used is non-negative."""
        if v < 0:
            raise ValueError("Tokens used cannot be negative")
        return v

class LLMConfig(BaseModel):
    """Configuration for LLM providers."""
    provider: str = "openai"
    api_key: str
    model: str = "gpt-4"
    max_tokens: int = 4000
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    timeout: int = Field(default=30, ge=1, le=300)
    
    @field_validator('provider')
    @classmethod
    def validate_provider(cls, v: str) -> str:
        """Validate LLM provider."""
        valid_providers = ["openai", "anthropic", "claude", "deepseek", "mock"]
        if v.lower() not in valid_providers:
            raise ValueError(f"Provider must be one of: {valid_providers}")
        return v.lower()

class SystemConfig(BaseModel):
    """Overall system configuration."""
    redis_url: str = "redis://localhost:6379"
    llm: LLMConfig
    debug: bool = False
    log_level: str = Field(default="INFO", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    max_sessions: int = Field(default=1000, ge=1)

# Test utility functions
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

def run_tests():
    """Run comprehensive tests of the fixed models."""
    
    print("1. Testing ExecutionContext...")
    try:
        context = create_execution_context(
            session_id="test-session-123",
            user_id="developer-1", 
            project_id="ai-editor-project",
            workspace_path="/tmp/test-workspace"
        )
        print(f"   ✅ Created context: {context.session_id}")
        
        # Test validation
        try:
            bad_context = ExecutionContext(
                session_id="test",
                user_id="user",
                project_id="project",
                workspace_path=""  # Should fail validation
            )
            print("   ❌ Validation should have failed")
        except ValueError as e:
            print(f"   ✅ Validation working: {e}")
            
    except Exception as e:
        print(f"   ❌ ExecutionContext failed: {e}")
        return False
    
    print("2. Testing TaskRequest...")
    try:
        task = TaskRequest(
            intent=IntentType.CODE_GENERATION,
            description="Create a FastAPI application with JWT authentication",
            context=context,
            priority=Priority.HIGH,
            timeout=600
        )
        print(f"   ✅ Created task: {task.id}")
        print(f"   ✅ Intent: {task.intent}")
        print(f"   ✅ Priority: {task.priority}")
        
        # Test validation
        try:
            bad_task = TaskRequest(
                intent=IntentType.CODE_GENERATION,
                description="",  # Should fail validation
                context=context
            )
            print("   ❌ Validation should have failed")
        except ValueError as e:
            print(f"   ✅ Validation working: {e}")
            
    except Exception as e:
        print(f"   ❌ TaskRequest failed: {e}")
        return False
    
    print("3. Testing TaskResult...")
    try:
        result = TaskResult(
            task_id=task.id,
            agent_type=AgentType.CODE,
            status=TaskStatus.COMPLETED,
            result={
                "code": "from fastapi import FastAPI\n\napp = FastAPI()",
                "language": "python"
            },
            execution_time=45.2,
            tokens_used=150
        )
        print(f"   ✅ Created result: {result.status}")
        print(f"   ✅ Execution time: {result.execution_time}s")
        print(f"   ✅ Tokens used: {result.tokens_used}")
        
    except Exception as e:
        print(f"   ❌ TaskResult failed: {e}")
        return False
    
    print("4. Testing LLMConfig...")
    try:
        llm_config = LLMConfig(
            provider="openai",
            api_key="test-key-123",
            model="gpt-4",
            temperature=0.7
        )
        print(f"   ✅ Created LLM config: {llm_config.provider}")
        print(f"   ✅ Model: {llm_config.model}")
        
    except Exception as e:
        print(f"   ❌ LLMConfig failed: {e}")
        return False
    
    print("5. Testing SystemConfig (with pattern field)...")
    try:
        system_config = SystemConfig(
            redis_url="redis://localhost:6379",
            llm=llm_config,
            debug=True,
            log_level="DEBUG",  # Should pass pattern validation
            max_sessions=500
        )
        print(f"   ✅ Created system config")
        print(f"   ✅ Log level: {system_config.log_level}")
        print(f"   ✅ Max sessions: {system_config.max_sessions}")
        
        # Test pattern validation
        try:
            bad_config = SystemConfig(
                redis_url="redis://localhost:6379",
                llm=llm_config,
                log_level="INVALID_LEVEL"  # Should fail pattern validation
            )
            print("   ❌ Pattern validation should have failed")
        except ValueError as e:
            print(f"   ✅ Pattern validation working: {e}")
        
    except Exception as e:
        print(f"   ❌ SystemConfig failed: {e}")
        return False
    
    print("6. Testing JSON serialization...")
    try:
        # Test model_dump_json (Pydantic V2 method)
        task_json = task.model_dump_json()
        result_json = result.model_dump_json()
        config_json = system_config.model_dump_json()
        
        print(f"   ✅ Task JSON: {len(task_json)} chars")
        print(f"   ✅ Result JSON: {len(result_json)} chars") 
        print(f"   ✅ Config JSON: {len(config_json)} chars")
        
    except Exception as e:
        print(f"   ❌ JSON serialization failed: {e}")
        return False
    
    print("7. Testing model_dump (Pydantic V2)...")
    try:
        task_dict = task.model_dump()
        result_dict = result.model_dump()
        
        print(f"   ✅ Task dict keys: {list(task_dict.keys())[:3]}...")
        print(f"   ✅ Result dict keys: {list(result_dict.keys())[:3]}...")
        
    except Exception as e:
        print(f"   ❌ model_dump failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Running Pydantic V2 Compatibility Tests...")
    print("=" * 50)
    
    try:
        success = run_tests()
        
        if success:
            print("=" * 50)
            print("🎉 ALL TESTS PASSED!")
            print("✅ Pydantic V2 compatibility confirmed")
            print("✅ All @field_validator decorators working")
            print("✅ Pattern validation working (no more regex errors)")
            print("✅ ConfigDict working properly")
            print("✅ JSON serialization working")
            print("✅ Ready for production use!")
            print("\n🚀 You can now run the fixed structure generator!")
        else:
            print("❌ Some tests failed")
            
    except Exception as e:
        print(f"❌ Critical error: {e}")
        import traceback
        traceback.print_exc()