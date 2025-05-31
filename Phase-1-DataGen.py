#!/usr/bin/env python3
"""
Phase 1: Data Models & Repository Structure Generator
Creates the complete foundation for the Agentic Middleware implementation.
"""

import os
import json
from pathlib import Path
from datetime import datetime

def create_repository_structure():
    """Create the complete repository structure for Phase 1."""
    
    print("🏗️ Creating AI Code Editor repository structure (Phase 1)...")
    
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
    create_data_models(base_dir)
    create_config_files(base_dir)
    create_requirements_files(base_dir)
    create_basic_structure_files(base_dir)
    
    print("✅ Repository structure created successfully!")
    print(f"📁 Project root: {base_dir.absolute()}")
    
    # Print next steps
    print_next_steps()

def create_core_files(base_dir: Path):
    """Create core project files."""
    
    # Root level files
    files = {
        ".gitignore": gitignore_content(),
        "README.md": readme_content(),
        "docker-compose.yml": docker_compose_content(),
        "Makefile": makefile_content(),
        ".env.example": env_example_content(),
        "VERSION": "0.1.0\n"
    }
    
    for filename, content in files.items():
        file_path = base_dir / filename
        file_path.write_text(content)
        print(f"📄 Created: {filename}")

def create_data_models(base_dir: Path):
    """Create the core data models."""
    
    # Core agent models
    agent_models_content = '''"""
Core data models for the Agentic Middleware system.
These models define the fundamental data structures used throughout the application.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


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
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
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
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
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
    message_type: str
    payload: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: str
    
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

class ChatResponse(BaseModel):
    """Response from the agentic system."""
    session_id: str
    response: Dict[str, Any]
    processing_time: float
    timestamp: str
    task_id: Optional[str] = None

class AgentStatus(BaseModel):
    """Status of an agent."""
    agent_type: str
    status: str
    capabilities: List[str]
    active_tasks: int = 0
    last_activity: Optional[datetime] = None

class SystemStatus(BaseModel):
    """Overall system status."""
    status: str
    active_sessions: int
    agents: List[AgentStatus]
    uptime: float
    version: str = "0.1.0"


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

class ExecutionPlan(BaseModel):
    """Plan for executing a complex task."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    original_task: TaskRequest
    steps: List[ExecutionStep]
    estimated_total_duration: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: TaskStatus = TaskStatus.PENDING


# ============================================================================
# Configuration Models
# ============================================================================

class LLMConfig(BaseModel):
    """Configuration for LLM providers."""
    provider: str = "openai"
    api_key: str
    model: str = "gpt-4"
    max_tokens: int = 4000
    temperature: float = 0.7
    timeout: int = 30

class AgentConfig(BaseModel):
    """Configuration for agents."""
    enabled_agents: List[AgentType] = Field(default_factory=lambda: [
        AgentType.CODE, 
        AgentType.INFRASTRUCTURE, 
        AgentType.TESTING
    ])
    max_concurrent_tasks: int = 10
    default_timeout: int = 300

class SystemConfig(BaseModel):
    """Overall system configuration."""
    redis_url: str = "redis://localhost:6379"
    llm: LLMConfig
    agents: AgentConfig = Field(default_factory=AgentConfig)
    debug: bool = False
    log_level: str = "INFO"


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

class ValidationError(AgentError):
    """Validation error details."""
    field: str
    value: Any
    constraint: str


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


# ============================================================================
# Export All Models
# ============================================================================

__all__ = [
    # Enums
    "AgentType",
    "TaskStatus", 
    "IntentType",
    "Priority",
    
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
    
    # Utilities
    "create_execution_context",
    "create_task_request",
]
'''
    
    models_file = base_dir / "backend/models/agent_models.py"
    models_file.write_text(agent_models_content)
    print(f"📄 Created: backend/models/agent_models.py")
    
    # API models
    api_models_content = '''"""
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
'''
    
    api_models_file = base_dir / "backend/models/api_models.py"
    api_models_file.write_text(api_models_content)
    print(f"📄 Created: backend/models/api_models.py")

def create_config_files(base_dir: Path):
    """Create configuration files."""
    
    # Backend configuration
    config_content = '''"""
Application configuration management.
"""

import os
from typing import Optional
from pydantic import BaseSettings
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
    config_init.write_text('from .settings import settings, get_settings\n\n__all__ = ["settings", "get_settings"]\n')

def create_requirements_files(base_dir: Path):
    """Create requirements files."""
    
    # Base requirements
    base_requirements = '''# Core dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
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
    
    print(f"📄 Created: requirements files")

def create_basic_structure_files(base_dir: Path):
    """Create basic structure files for immediate use."""
    
    # Backend __init__.py files with proper imports
    backend_init_files = {
        "backend/__init__.py": '"""AI Code Editor Backend Package."""\n',
        "backend/models/__init__.py": '''"""Data models package."""

from .agent_models import *
from .api_models import *

__all__ = [
    # Re-export all model classes
    "AgentType", "TaskStatus", "IntentType", "Priority",
    "ExecutionContext", "TaskRequest", "TaskResult", 
    "ChatMessage", "ChatResponse", "SystemStatus"
]
''',
        "backend/core/__init__.py": '"""Core system components."""\n',
        "backend/agents/__init__.py": '"""Agent implementations."""\n',
        "backend/api/__init__.py": '"""API endpoints."""\n',
        "backend/services/__init__.py": '"""Business services."""\n',
        "backend/utils/__init__.py": '"""Utility functions."""\n',
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
    
    # Basic README for immediate setup
    readme_phase1 = f'''# AI Code Editor - Phase 1 Setup Complete

## 🎯 Current Status: Foundation Ready

You now have the complete repository structure and data models for the AI Code Editor.

## 📁 Structure Created

```
ai-code-editor/
├── backend/                    # Python FastAPI backend
│   ├── models/                # ✅ Data models (COMPLETE)
│   ├── config/                # ✅ Configuration (COMPLETE)
│   ├── core/orchestration/    # 🔄 Next: Basic middleware
│   ├── agents/                # 🔄 Next: Simple agents
│   └── api/                   # 🔄 Next: REST endpoints
├── frontend/                  # React frontend
└── infrastructure/            # Docker, K8s configs
```

## 🚀 Next Steps (Phase 1 continues)

### Day 1 Remaining: Basic FastAPI App
```bash
cd ai-code-editor/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements/development.txt
```

### Day 2-3: Implement Base Agent Classes
- Create BaseAgent abstract class
- Implement simple CodeGenerationAgent
- Add mock LLM client

### Day 4-7: Basic Middleware & API
- Agent registry for managing agents
- Intent classifier for routing requests
- Basic middleware orchestration
- REST API endpoints

## 📋 What's Ready to Use

### ✅ Data Models
All core models are implemented in `backend/models/agent_models.py`:
- `TaskRequest`, `TaskResult`, `ExecutionContext`
- `AgentType`, `IntentType`, `TaskStatus` enums
- Configuration and error models

### ✅ Configuration System
Environment-based configuration in `backend/config/settings.py`

### ✅ Requirements
All dependencies defined in `backend/requirements/`

## 🧪 Test the Foundation

```python
# Test the data models
from backend.models.agent_models import *

# Create a sample task
context = create_execution_context("test-session", "user-1")
task = create_task_request("Create a Python function", context)
print(f"Task ID: {{task.id}}")
print(f"Intent: {{task.intent}}")
```

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
'''
    
    readme_file = base_dir / "README.md"
    readme_file.write_text(readme_phase1)

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
    return '''# AI Code Editor

An AI-powered code editor with multi-agent system for intelligent development assistance.

## 🚀 Quick Start

```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt

# Frontend setup
cd frontend
npm install
npm run dev
```

## 📖 Documentation

See `docs/` directory for detailed documentation.

## 🏗️ Architecture

- **Backend**: FastAPI with agentic middleware
- **Frontend**: React with Monaco Editor
- **Agents**: Specialized AI agents for different tasks
- **Infrastructure**: Docker, Kubernetes deployment ready

## 🧪 Development

```bash
# Run backend
cd backend && python -m app.main

# Run frontend  
cd frontend && npm run dev

# Run tests
make test
```

## 📝 License

MIT License - see LICENSE file for details.
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

.PHONY: help setup install dev test lint clean

help: ## Show this help
\t@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'

setup: ## Initial project setup
\tpython setup_structure.py
\tcp .env.example .env

install: ## Install dependencies
\tcd backend && pip install -r requirements/development.txt
\tcd frontend && npm install

dev: ## Start development servers
\tdocker-compose up -d redis
\tcd backend && uvicorn app.main:app --reload --port 8000 &
\tcd frontend && npm run dev

test: ## Run tests
\tcd backend && pytest
\tcd frontend && npm test

lint: ## Run linters
\tcd backend && black . && flake8 .
\tcd frontend && npm run lint

clean: ## Clean build artifacts
\tcd backend && find . -type d -name __pycache__ -delete
\tcd frontend && rm -rf node_modules dist
\tdocker-compose down -v
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
🎉 Phase 1 Foundation Complete!

📋 Next Steps:

1. **Setup Environment**:
   cd ai-code-editor
   cp .env.example .env
   # Edit .env with your LLM API keys

2. **Install Dependencies**:
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   pip install -r requirements/development.txt

3. **Test the Foundation**:
   python -c "from models.agent_models import *; print('✅ Models imported successfully')"

4. **Start Day 2 Implementation**:
   - Create BaseAgent class in agents/base/
   - Implement mock LLM client
   - Build simple CodeGenerationAgent

📁 Everything is ready in: ai-code-editor/
🔄 Continue with Phase 1, Day 2: Base Agent Classes
""")

if __name__ == "__main__":
    create_repository_structure()