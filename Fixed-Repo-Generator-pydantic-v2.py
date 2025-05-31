#!/usr/bin/env python3
"""
Fixed Repository Structure Generator - Pydantic V2 Compatible
Creates the complete foundation for the Agentic Middleware implementation with Pydantic V2 support.
"""

import os
import json
from pathlib import Path
from datetime import datetime

def create_repository_structure():
    """Create the complete repository structure for Phase 1 with Pydantic V2 compatibility."""
    
    print("🏗️ Creating AI Code Editor repository structure (Phase 1 - Pydantic V2)...")
    
    # Base directory
    base_dir = Path("ai-code-editor")
    base_dir.mkdir(exist_ok=True)
    
    # Define complete directory structure
    directories = [
        # Root level
        ".github/workflows",
        ".github/ISSUE_TEMPLATE",
        "docs/architecture",
        "docs/api", 
        "docs/deployment",
        
        # Frontend structure
        "frontend/public",
        "frontend/src/components/chat",
        "frontend/src/components/editor",
        "frontend/src/services/api",
        "frontend/src/types",
        "frontend/src/hooks",
        "frontend/src/utils",
        
        # Backend structure - Core
        "backend/app",
        "backend/models",
        "backend/core/orchestration",
        "backend/core/memory", 
        "backend/core/llm/providers",
        
        # Backend structure - Agents
        "backend/agents/base",
        "backend/agents/code/generators",
        "backend/agents/code/parsers",
        "backend/agents/code/validators",
        "backend/agents/infrastructure",
        "backend/agents/testing/generators",
        "backend/agents/testing/runners",
        "backend/agents/devops",
        "backend/agents/documentation",
        "backend/agents/security",
        
        # Backend structure - API & Services
        "backend/api/v1",
        "backend/services",
        "backend/database/repositories",
        "backend/utils",
        "backend/tests/unit",
        "backend/tests/integration",
        "backend/tests/e2e",
        "backend/config",
        "backend/requirements",
        
        # Infrastructure
        "infrastructure/docker",
        "infrastructure/kubernetes",
        "infrastructure/terraform",
        "infrastructure/scripts",
        
        # Shared
        "shared/types",
        "shared/constants",
        "shared/utils",
        
        # Tools & Examples
        "tools/scripts",
        "tools/generators",
        "examples/tutorials",
        "examples/sample-projects",
        
        # Tests
        "tests/integration",
        "tests/e2e",
    ]
    
    # Create all directories
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py for Python packages
        if "backend" in str(dir_path) and not str(dir_path).endswith(("scripts", "requirements", "tests")):
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                init_file.write_text('"""Package initialization."""\n')
        
        print(f"📁 Created: {dir_path}")
    
    # Create core files
    create_core_files(base_dir)
    create_pydantic_v2_data_models(base_dir)
    create_config_files(base_dir)
    create_requirements_files(base_dir)
    create_basic_structure_files(base_dir)
    
    print("✅ Repository structure created successfully!")
    print(f"📁 Project root: {base_dir.absolute()}")
    
    # Print next steps
    print_next_steps()

def create_pydantic_v2_data_models(base_dir: Path):
    """Create Pydantic V2 compatible data models."""
    
    # This is the fixed Pydantic V2 compatible version
    agent_models_content = '''"""
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
        
        print("\\n🎉 All tests passed! Pydantic V2 models are working correctly.")
        
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
'''
    
    models_file = base_dir / "backend/models/agent_models.py"
    models_file.write_text(agent_models_content)
    print(f"📄 Created: backend/models/agent_models.py (Pydantic V2 Compatible)")

def create_core_files(base_dir: Path):
    """Create core project files."""
    
    # Root level files
    files = {
        ".gitignore": gitignore_content(),
        "README.md": readme_content(),
        "docker-compose.yml": docker_compose_content(),
        "Makefile": makefile_content(),
        ".env.example": env_example_content(),
        "VERSION": "0.1.0\\n"
    }
    
    for filename, content in files.items():
        file_path = base_dir / filename
        file_path.write_text(content)
        print(f"📄 Created: {filename}")

def create_config_files(base_dir: Path):
    """Create configuration files."""
    
    # Backend configuration with Pydantic V2 compatibility
    config_content = '''"""
Application configuration management - Pydantic V2 Compatible.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from .models.agent_models import LLMConfig, AgentConfig, SystemConfig, AgentType


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Server settings
    app_name: str = "AI Code Editor"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    
    # Redis settings
    redis_url: str = "redis://localhost:6379"
    redis_max_connections: int = 10
    
    # LLM settings
    llm_provider: str = "openai"
    llm_api_key: str = ""
    llm_model: str = "gpt-4"
    llm_max_tokens: int = 4000
    llm_temperature: float = 0.7
    llm_timeout: int = 30
    
    # Agent settings
    max_concurrent_agents: int = 10
    agent_timeout: int = 300
    default_workspace_path: str = "/tmp/workspaces"
    
    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False

    def get_llm_config(self) -> LLMConfig:
        """Get LLM configuration."""
        return LLMConfig(
            provider=self.llm_provider,
            api_key=self.llm_api_key,
            model=self.llm_model,
            max_tokens=self.llm_max_tokens,
            temperature=self.llm_temperature,
            timeout=self.llm_timeout
        )
    
    def get_agent_config(self) -> AgentConfig:
        """Get agent configuration."""
        return AgentConfig(
            enabled_agents=[
                AgentType.CODE,
                AgentType.INFRASTRUCTURE, 
                AgentType.TESTING
            ],
            max_concurrent_tasks=self.max_concurrent_agents,
            default_timeout=self.agent_timeout
        )
    
    def get_system_config(self) -> SystemConfig:
        """Get complete system configuration."""
        return SystemConfig(
            redis_url=self.redis_url,
            llm=self.get_llm_config(),
            agents=self.get_agent_config(),
            debug=self.debug,
            log_level=self.log_level
        )


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings
'''
    
    config_file = base_dir / "backend/config/settings.py"
    config_file.write_text(config_content)
    print(f"📄 Created: backend/config/settings.py")
    
    # Create __init__.py for config
    config_init = base_dir / "backend/config/__init__.py"
    config_init.write_text('from .settings import settings, get_settings\\n\\n__all__ = ["settings", "get_settings"]\\n')

def create_requirements_files(base_dir: Path):
    """Create requirements files with Pydantic V2."""
    
    # Base requirements with Pydantic V2
    base_requirements = '''# Core dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.2
pydantic-settings==2.1.0
redis==5.0.1
python-dotenv==1.0.0

# LLM integrations
openai==1.3.7
anthropic==0.7.8

# Agent orchestration
langchain==0.0.340
langgraph==0.0.19

# Data handling
httpx==0.25.2
aiofiles==23.2.1

# Utilities
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
'''
    
    base_req_file = base_dir / "backend/requirements/base.txt"
    base_req_file.write_text(base_requirements)
    
    # Development requirements
    dev_requirements = '''-r base.txt

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2

# Code quality
black==23.11.0
isort==5.12.0
flake8==6.1.0
mypy==1.7.1

# Development tools
watchdog==3.0.0
pre-commit==3.5.0
'''
    
    dev_req_file = base_dir / "backend/requirements/development.txt"
    dev_req_file.write_text(dev_requirements)
    
    # Production requirements
    prod_requirements = '''-r base.txt

# Production server
gunicorn==21.2.0

# Monitoring
prometheus-client==0.19.0

# Production utilities
sentry-sdk[fastapi]==1.38.0
'''
    
    prod_req_file = base_dir / "backend/requirements/production.txt"
    prod_req_file.write_text(prod_requirements)
    
    print(f"📄 Created: requirements files (Pydantic V2 compatible)")

def create_basic_structure_files(base_dir: Path):
    """Create basic structure files for immediate use."""
    
    # Backend __init__.py files with proper imports
    backend_init_files = {
        "backend/__init__.py": '"""AI Code Editor Backend Package."""\\n',
        "backend/models/__init__.py": '''"""Data models package."""

from .agent_models import *

__all__ = [
    # Re-export all model classes
    "AgentType", "TaskStatus", "IntentType", "Priority",
    "ExecutionContext", "TaskRequest", "TaskResult", 
    "ChatMessage", "ChatResponse", "SystemStatus",
    "create_execution_context", "create_task_request", "create_task_result"
]
''',
        "backend/core/__init__.py": '"""Core system components."""\\n',
        "backend/agents/__init__.py": '"""Agent implementations."""\\n',
        "backend/api/__init__.py": '"""API endpoints."""\\n',
        "backend/services/__init__.py": '"""Business services."""\\n',
        "backend/utils/__init__.py": '"""Utility functions."""\\n',
    }
    
    for file_path, content in backend_init_files.items():
        full_path = base_dir / file_path
        full_path.write_text(content)
    
    # Frontend package.json
    frontend_package = {
        "name": "ai-code-editor-frontend",
        "version": "0.1.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "@monaco-editor/react": "^4.6.0",
            "tailwindcss": "^3.3.0",
            "typescript": "^5.0.0",
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0"
        },
        "scripts": {
            "dev": "vite",
            "build": "tsc && vite build",
            "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
            "preview": "vite preview"
        },
        "devDependencies": {
            "@types/node": "^20.0.0",
            "@vitejs/plugin-react": "^4.0.0",
            "vite": "^4.4.0",
            "eslint": "^8.45.0"
        }
    }
    
    package_file = base_dir / "frontend/package.json"
    package_file.write_text(json.dumps(frontend_package, indent=2))
    print(f"📄 Created: frontend/package.json")
    
    # Test script to verify models work
    test_script = base_dir / "backend/test_models.py"
    test_script_content = '''#!/usr/bin/env python3
"""
Test script to verify Pydantic V2 models work correctly.
"""

import sys
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

try:
    from models.agent_models import *
    
    def test_models():
        print("🧪 Testing Pydantic V2 models...")
        
        # Test ExecutionContext
        context = create_execution_context(
            session_id="test-session",
            user_id="developer", 
            project_id="test-project",
            workspace_path="/tmp/test"
        )
        print(f"✅ ExecutionContext: {context.session_id}")
        
        # Test TaskRequest
        task = create_task_request(
            description="Create a Python function",
            context=context,
            intent=IntentType.CODE_GENERATION
        )
        print(f"✅ TaskRequest: {task.id}")
        
        # Test TaskResult
        result = create_task_result(
            task_id=task.id,
            agent_type=AgentType.CODE,
            status=TaskStatus.COMPLETED,
            result={"code": "def hello(): return 'world'"}
        )
        print(f"✅ TaskResult: {result.status}")
        
        # Test ChatMessage
        chat = ChatMessage(
            message="Hello AI",
            session_id="test",
            user_id="user"
        )
        print(f"✅ ChatMessage: {chat.message}")
        
        print("\\n🎉 All models working correctly with Pydantic V2!")
        return True
    
    if __name__ == "__main__":
        test_models()
        
except Exception as e:
    print(f"❌ Error testing models: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
    
    test_script.write_text(test_script_content)
    print(f"📄 Created: backend/test_models.py")

def gitignore_content():
    """Generate .gitignore content."""
    return '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Frontend build
frontend/dist/
frontend/build/

# Logs
*.log
logs/

# Database
*.db
*.sqlite

# Redis dump
dump.rdb

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
.pytest_cache/
htmlcov/

# Temporary files
tmp/
temp/
.tmp/

# Workspace files
workspaces/
'''

def readme_content():
    """Generate README content."""
    return f'''# AI Code Editor - Pydantic V2 Compatible

An AI-powered code editor with multi-agent system for intelligent development assistance.

## ✅ Pydantic V2 Ready

This project uses **Pydantic V2** for all data models with proper validation and type safety.

## 🚀 Quick Start

```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements/development.txt

# Test the models
python test_models.py

# Frontend setup (optional)
cd frontend
npm install
npm run dev
```

## 🧪 Test Data Models

```bash
cd backend
python test_models.py
```

Expected output:
```
🧪 Testing Pydantic V2 models...
✅ ExecutionContext: test-session
✅ TaskRequest: [uuid]
✅ TaskResult: completed
✅ ChatMessage: Hello AI
🎉 All models working correctly with Pydantic V2!
```

## 📖 What's Fixed

- ✅ **Pydantic V2 compatibility**: Updated all `@validator` to `@field_validator`
- ✅ **Pattern instead of regex**: Fixed `Field(regex=...)` to `Field(pattern=...)`
- ✅ **ConfigDict**: Using Pydantic V2 configuration style
- ✅ **Type safety**: Full type hints and validation

## 🏗️ Architecture

- **Backend**: FastAPI with agentic middleware
- **Frontend**: React with Monaco Editor
- **Agents**: Specialized AI agents for different tasks
- **Infrastructure**: Docker, Kubernetes deployment ready

## 📝 Generated on

{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 🎯 Next Steps

1. Test the foundation: `cd backend && python test_models.py`
2. Install dependencies: `pip install -r requirements/development.txt`
3. Start building Phase 1: BaseAgent classes
4. Continue with middleware implementation

Ready to build the future of AI-powered development! 🚀
'''

def docker_compose_content():
    """Generate docker-compose.yml content."""
    return '''version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
      - LLM_API_KEY=${LLM_API_KEY}
    volumes:
      - ./backend:/app
      - ./workspaces:/app/workspaces
    depends_on:
      - redis
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
'''

def makefile_content():
    """Generate Makefile content."""
    return '''# AI Code Editor - Development Makefile

.PHONY: help setup install dev test lint clean test-models

help: ## Show this help
\\t@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\\\033[36m%-20s\\\\033[0m %s\\\\n", $$1, $$2}'

setup: ## Initial project setup
\\tpython fixed_structure_generator.py
\\tcp .env.example .env

install: ## Install dependencies
\\tcd backend && pip install -r requirements/development.txt
\\tcd frontend && npm install

test-models: ## Test Pydantic V2 models
\\tcd backend && python test_models.py

dev: ## Start development servers
\\tdocker-compose up -d redis
\\tcd backend && uvicorn app.main:app --reload --port 8000 &
\\tcd frontend && npm run dev

test: ## Run tests
\\tcd backend && pytest
\\tcd frontend && npm test

lint: ## Run linters
\\tcd backend && black . && flake8 .
\\tcd frontend && npm run lint

clean: ## Clean build artifacts
\\tcd backend && find . -type d -name __pycache__ -delete
\\tcd frontend && rm -rf node_modules dist
\\tdocker-compose down -v
'''

def env_example_content():
    """Generate .env.example content."""
    return '''# AI Code Editor Environment Variables

# LLM Configuration
LLM_PROVIDER=openai
LLM_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4
LLM_MAX_TOKENS=4000

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
LOG_LEVEL=INFO

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-change-in-production

# Agent Configuration
MAX_CONCURRENT_AGENTS=10
AGENT_TIMEOUT=300
DEFAULT_WORKSPACE_PATH=/tmp/workspaces

# Development
WORKSPACE_PATH=./workspaces
'''

def print_next_steps():
    """Print next steps for the user."""
    print(f"""
🎉 Fixed Repository Structure Complete! (Pydantic V2 Compatible)

📋 Next Steps:

1. **Navigate to Project**:
   cd ai-code-editor

2. **Setup Backend Environment**:
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   pip install -r requirements/development.txt

3. **Test the Fixed Models**:
   python test_models.py
   # Should show: "🎉 All models working correctly with Pydantic V2!"

4. **Configure Environment**:
   cd ..  # back to project root
   cp .env.example .env
   # Edit .env with your LLM API keys

5. **Ready for Phase 1 Development**:
   # All Pydantic V2 issues are now fixed!
   # Continue with base agent classes

📁 Everything is ready in: ai-code-editor/
🔄 No more Pydantic V2 errors!
🚀 Ready to build your agentic middleware!
""")

if __name__ == "__main__":
    create_repository_structure()