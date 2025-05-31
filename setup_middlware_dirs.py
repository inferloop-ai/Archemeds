#!/usr/bin/env python3
"""
Setup Script - Organize Agentic Middleware in Correct Directory Structure
This script takes the middleware files and organizes them properly within the project structure.
"""

import os
import shutil
from pathlib import Path

def setup_middleware_structure():
    """Setup the middleware in the correct directory structure."""
    
    # Base directory (assumes we're in the project root)
    base_dir = Path("ai-code-editor")
    backend_dir = base_dir / "backend"
    
    print("🏗️ Setting up Agentic Middleware directory structure...")
    
    # Create the directory structure if it doesn't exist
    directories_to_create = [
        # Core orchestration
        "core/orchestration",
        "core/memory", 
        "core/llm/providers",
        
        # Agent directories
        "agents/base",
        "agents/code/generators",
        "agents/code/parsers", 
        "agents/code/validators",
        "agents/infrastructure/cloud_providers",
        "agents/testing/generators",
        "agents/testing/runners",
        "agents/devops/ci_generators",
        "agents/devops/deployment",
        "agents/documentation/generators",
        "agents/documentation/parsers",
        "agents/security/scanners",
        "agents/security/policies",
        
        # API integration
        "api/v1",
        
        # Configuration
        "config"
    ]
    
    # Create directories
    for dir_path in directories_to_create:
        full_path = backend_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py files for Python packages
        init_file = full_path / "__init__.py"
        if not init_file.exists():
            init_file.touch()
        
        print(f"📁 Created: {full_path}")
    
    # Create the main middleware files
    create_middleware_files(backend_dir)
    
    print("✅ Middleware structure setup complete!")
    print("\n📋 Next steps:")
    print("1. cd ai-code-editor/backend")
    print("2. pip install -r requirements.txt")
    print("3. python -m app.main  # Start the server")

def create_middleware_files(backend_dir: Path):
    """Create the core middleware files with proper imports."""
    
    # 1. Main middleware file
    middleware_file = backend_dir / "core/orchestration/middleware.py"
    middleware_content = '''"""
Main Agentic Middleware class - orchestrates all AI agents.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .intent_classifier import IntentClassifier
from .task_planner import TaskPlanner
from .execution_engine import ExecutionEngine
from .agent_registry import AgentRegistry
from ..memory.context_manager import ContextMemory
from ..llm.gateway import LLMGateway
from ...models.agent_models import ExecutionContext, TaskRequest

class AgenticMiddleware:
    """Main orchestrator class that coordinates all agents."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.logger = logging.getLogger("agentic_middleware")
        
        # Initialize components
        self.agent_registry = AgentRegistry()
        self.intent_classifier = IntentClassifier()
        self.task_planner = TaskPlanner(self.agent_registry)
        self.memory = ContextMemory(redis_url)
        self.execution_engine = ExecutionEngine(
            self.agent_registry,
            self.memory
        )
        
        self.sessions = {}
    
    async def initialize(self):
        """Initialize the middleware."""
        self.logger.info("Initializing Agentic Middleware...")
        await self.memory.initialize()
        self.logger.info("Agentic Middleware initialized successfully")
    
    async def process_request(self, user_input: str, context: ExecutionContext) -> Dict[str, Any]:
        """Process a user request through the agentic system."""
        try:
            # Classify intent
            intent = await self.intent_classifier.classify(user_input, context)
            self.logger.info(f"Classified intent: {intent.value}")
            
            # Create task request
            task = TaskRequest(
                intent=intent,
                description=user_input,
                context=context
            )
            
            # Execute task
            if await self._needs_planning(task):
                plan = await self.task_planner.create_plan(task)
                results = await self.execution_engine.execute_plan(plan)
                response = await self._aggregate_results(results, plan)
            else:
                result = await self.execution_engine.execute_task(task)
                response = await self._format_single_result(result)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return {
                "error": str(e),
                "status": "failed",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def register_agent(self, agent):
        """Register a new agent with the middleware."""
        self.agent_registry.register_agent(agent)
    
    async def _needs_planning(self, task: TaskRequest) -> bool:
        """Determine if a task needs complex planning."""
        # Implementation here
        return False
    
    async def _aggregate_results(self, results, plan) -> Dict[str, Any]:
        """Aggregate results from multiple tasks."""
        return {"status": "completed", "results": results}
    
    async def _format_single_result(self, result) -> Dict[str, Any]:
        """Format a single task result."""
        return {"status": result.status.value, "result": result.result}
'''
    
    with open(middleware_file, 'w') as f:
        f.write(middleware_content)
    
    # 2. Intent classifier
    intent_file = backend_dir / "core/orchestration/intent_classifier.py"
    intent_content = '''"""
Intent classification for understanding user requests.
"""

from typing import Dict, Any
from enum import Enum
from ...models.agent_models import ExecutionContext

class IntentType(str, Enum):
    """Types of user intents."""
    CODE_GENERATION = "code_generation"
    INFRASTRUCTURE_SETUP = "infrastructure_setup"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    SECURITY_SCAN = "security_scan"

class IntentClassifier:
    """Classifies user intents from natural language."""
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.intent_examples = {
            IntentType.CODE_GENERATION: [
                "create a function", "write code for", "implement", "generate"
            ],
            IntentType.INFRASTRUCTURE_SETUP: [
                "deploy to", "create dockerfile", "setup kubernetes"
            ],
            IntentType.TESTING: [
                "write tests", "create unit tests", "test coverage"
            ]
        }
    
    async def classify(self, user_input: str, context: ExecutionContext) -> IntentType:
        """Classify user intent from input."""
        user_input_lower = user_input.lower()
        
        # Simple keyword-based classification
        for intent, keywords in self.intent_examples.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return intent
        
        return IntentType.CODE_GENERATION
'''
    
    with open(intent_file, 'w') as f:
        f.write(intent_content)
    
    # 3. Agent registry
    registry_file = backend_dir / "core/orchestration/agent_registry.py"
    registry_content = '''"""
Registry for managing available agents.
"""

import logging
from typing import Dict, List, Optional
from ...models.agent_models import AgentType, TaskRequest

class AgentRegistry:
    """Registry for managing available agents."""
    
    def __init__(self):
        self.agents: Dict[AgentType, 'BaseAgent'] = {}
        self.logger = logging.getLogger("agent_registry")
    
    def register_agent(self, agent):
        """Register an agent."""
        self.agents[agent.agent_type] = agent
        self.logger.info(f"Registered agent: {agent.agent_type.value}")
    
    def get_agent(self, agent_type: AgentType):
        """Get an agent by type."""
        return self.agents.get(agent_type)
    
    async def find_capable_agents(self, task: TaskRequest) -> List:
        """Find agents capable of handling a task."""
        capable_agents = []
        for agent in self.agents.values():
            if await agent.can_handle(task):
                capable_agents.append(agent)
        return capable_agents
    
    def get_all_capabilities(self):
        """Get capabilities of all agents."""
        capabilities = {}
        for agent_type, agent in self.agents.items():
            capabilities[agent_type] = agent.get_capabilities()
        return capabilities
'''
    
    with open(registry_file, 'w') as f:
        f.write(registry_content)
    
    # 4. Task planner
    planner_file = backend_dir / "core/orchestration/task_planner.py"
    planner_content = '''"""
Task planning and decomposition.
"""

import logging
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime
from ...models.agent_models import TaskRequest

@dataclass
class ExecutionPlan:
    """Plan for executing a complex task."""
    id: str
    original_task: TaskRequest
    subtasks: List[TaskRequest]
    dependencies: Dict[str, List[str]]
    estimated_duration: int

class TaskPlanner:
    """Plans complex tasks by breaking them into subtasks."""
    
    def __init__(self, agent_registry):
        self.agent_registry = agent_registry
        self.logger = logging.getLogger("task_planner")
    
    async def create_plan(self, task: TaskRequest) -> ExecutionPlan:
        """Create an execution plan for a task."""
        # Simple planning for now
        return ExecutionPlan(
            id="plan-1",
            original_task=task,
            subtasks=[task],
            dependencies={},
            estimated_duration=60
        )
'''
    
    with open(planner_file, 'w') as f:
        f.write(planner_content)
    
    # 5. Execution engine
    execution_file = backend_dir / "core/orchestration/execution_engine.py"
    execution_content = '''"""
Execution engine for running agent workflows.
"""

import logging
from datetime import datetime
from typing import List
from ...models.agent_models import TaskRequest, TaskResult, TaskStatus

class ExecutionEngine:
    """Executes agent workflows."""
    
    def __init__(self, agent_registry, memory):
        self.agent_registry = agent_registry
        self.memory = memory
        self.logger = logging.getLogger("execution_engine")
    
    async def execute_task(self, task: TaskRequest) -> TaskResult:
        """Execute a single task."""
        start_time = datetime.utcnow()
        
        try:
            # Find capable agents
            capable_agents = await self.agent_registry.find_capable_agents(task)
            
            if not capable_agents:
                return TaskResult(
                    task_id=task.id,
                    agent_type="unknown",
                    status=TaskStatus.FAILED,
                    error="No capable agents found"
                )
            
            # Execute with first capable agent
            selected_agent = capable_agents[0]
            result = await selected_agent.execute(task)
            
            return result
            
        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            return TaskResult(
                task_id=task.id,
                agent_type="unknown",
                status=TaskStatus.FAILED,
                error=str(e),
                execution_time=execution_time
            )
    
    async def execute_plan(self, plan) -> List[TaskResult]:
        """Execute a complex plan."""
        results = []
        for task in plan.subtasks:
            result = await self.execute_task(task)
            results.append(result)
        return results
'''
    
    with open(execution_file, 'w') as f:
        f.write(execution_content)
    
    # 6. Create package __init__.py files
    init_files = [
        backend_dir / "core/__init__.py",
        backend_dir / "core/orchestration/__init__.py",
        backend_dir / "core/memory/__init__.py", 
        backend_dir / "core/llm/__init__.py",
        backend_dir / "agents/__init__.py",
        backend_dir / "agents/base/__init__.py"
    ]
    
    for init_file in init_files:
        if not init_file.exists():
            with open(init_file, 'w') as f:
                f.write('"""Package initialization."""\n')
    
    # Main orchestration __init__.py with exports
    orchestration_init = backend_dir / "core/orchestration/__init__.py"
    with open(orchestration_init, 'w') as f:
        f.write('''"""
Core orchestration components for the Agentic Middleware.
"""

from .middleware import AgenticMiddleware
from .intent_classifier import IntentClassifier, IntentType
from .agent_registry import AgentRegistry
from .task_planner import TaskPlanner, ExecutionPlan
from .execution_engine import ExecutionEngine

__all__ = [
    'AgenticMiddleware',
    'IntentClassifier',
    'IntentType', 
    'AgentRegistry',
    'TaskPlanner',
    'ExecutionPlan',
    'ExecutionEngine'
]
''')
    
    print("📝 Created core middleware files")

def create_example_main_app(backend_dir: Path):
    """Create an example main application file."""
    
    main_file = backend_dir / "app/main.py"
    main_content = '''"""
Main FastAPI application with Agentic Middleware integration.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..core.orchestration import AgenticMiddleware
from ..agents.factory import AgentFactory
from ..api.v1.middleware_api import router as middleware_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# Create FastAPI app
app = FastAPI(
    title="AI Code Editor with Agentic Middleware",
    description="AI-powered code editor with multi-agent system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global middleware instance
middleware = None

@app.on_event("startup")
async def startup_event():
    """Initialize the agentic middleware on startup."""
    global middleware
    
    logger.info("Starting AI Code Editor API...")
    
    try:
        # Initialize middleware
        middleware = AgenticMiddleware()
        await middleware.initialize()
        
        # Register agents
        agents = AgentFactory.create_all_agents()
        for agent in agents:
            middleware.register_agent(agent)
        
        logger.info(f"Initialized with {len(agents)} agents")
        logger.info("AI Code Editor API started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start API: {e}")
        raise

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "middleware_active": middleware is not None}

# Include middleware API routes
app.include_router(middleware_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    with open(main_file, 'w') as f:
        f.write(main_content)
    
    print("📝 Created main application file")

if __name__ == "__main__":
    setup_middleware_structure()