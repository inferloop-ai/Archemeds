# File: ai-code-editor/backend/agents/base/agent.py
"""
Base agent class for all AI agents.
"""

from abc import ABC, abstractmethod
from typing import List
from ...models.agent_models import TaskRequest, TaskResult, AgentType

class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.capabilities = []
    
    @abstractmethod
    async def execute(self, task: TaskRequest) -> TaskResult:
        """Execute a task and return results."""
        pass
    
    @abstractmethod
    async def can_handle(self, task: TaskRequest) -> bool:
        """Check if this agent can handle the given task."""
        pass
    
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities."""
        return self.capabilities


# File: ai-code-editor/backend/core/llm/mock_client.py
"""
Mock LLM client for testing without API calls.
"""

import json
from typing import List, Dict

class MockLLMClient:
    """Mock LLM client that returns predefined responses."""
    
    async def chat_completion(self, messages: List[Dict[str, str]]):
        """Mock chat completion."""
        user_message = messages[-1]["content"].lower()
        
        # Simple pattern matching for different code requests
        if "fastapi" in user_message:
            code = '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/items/")
async def create_item(item: Item):
    return item'''
            
            return MockResponse(json.dumps({
                "code": code,
                "language": "python",
                "explanation": "Created a basic FastAPI application with a root endpoint and item creation endpoint."
            }))
        
        elif "react" in user_message:
            code = '''import React, { useState } from 'react';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="App">
      <h1>React Counter</h1>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}

export default App;'''
            
            return MockResponse(json.dumps({
                "code": code,
                "language": "javascript",
                "explanation": "Created a basic React component with state management."
            }))
        
        elif "function" in user_message and "python" in user_message:
            code = '''def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)

# Example usage
if __name__ == "__main__":
    for i in range(10):
        print(f"F({i}) = {calculate_fibonacci(i)}")'''
            
            return MockResponse(json.dumps({
                "code": code,
                "language": "python",
                "explanation": "Created a recursive Fibonacci function with example usage."
            }))
        
        else:
            return MockResponse(json.dumps({
                "code": "# Generated code based on your request\nprint('Hello, AI-generated code!')",
                "language": "python",
                "explanation": "Generated a simple Python script based on your request."
            }))

class MockResponse:
    """Mock response object."""
    
    def __init__(self, content: str):
        self.content = content


# File: ai-code-editor/backend/agents/code/code_agent.py
"""
Code generation agent.
"""

import json
import uuid
from ...agents.base.agent import BaseAgent
from ...models.agent_models import AgentType, TaskRequest, TaskResult, TaskStatus, IntentType

class CodeGenerationAgent(BaseAgent):
    """Agent specialized in code generation."""
    
    def __init__(self, llm_client=None):
        super().__init__(AgentType.CODE)
        self.llm_client = llm_client
        self.capabilities = [
            "Generate Python code",
            "Generate JavaScript/TypeScript code", 
            "Generate API endpoints",
            "Generate React components",
            "Code refactoring"
        ]
    
    async def can_handle(self, task: TaskRequest) -> bool:
        """Check if this agent can handle the task."""
        return task.intent == IntentType.CODE_GENERATION
    
    async def execute(self, task: TaskRequest) -> TaskResult:
        """Execute code generation task."""
        try:
            # Build prompt with context
            messages = [
                {
                    "role": "system",
                    "content": "You are a code generation expert. Generate clean, well-documented code based on user requests."
                },
                {
                    "role": "user", 
                    "content": task.description
                }
            ]
            
            # Get response from LLM
            response = await self.llm_client.chat_completion(messages)
            
            # Parse response
            try:
                result_data = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback if response isn't JSON
                result_data = {
                    "code": response.content,
                    "language": "python",
                    "explanation": "Generated code based on your request."
                }
            
            return TaskResult(
                task_id=task.id,
                agent_type=self.agent_type,
                status=TaskStatus.COMPLETED,
                result=result_data,
                execution_time=1.5  # Mock execution time
            )
            
        except Exception as e:
            return TaskResult(
                task_id=task.id,
                agent_type=self.agent_type,
                status=TaskStatus.FAILED,
                error=str(e)
            )


# File: ai-code-editor/backend/agents/factory.py
"""
Agent factory for creating and configuring agents.
"""

from .code.code_agent import CodeGenerationAgent
from ..core.llm.mock_client import MockLLMClient

class AgentFactory:
    """Factory for creating pre-configured agents."""
    
    @staticmethod
    def create_all_agents(llm_client=None):
        """Create all available agents."""
        if llm_client is None:
            llm_client = MockLLMClient()
        
        return [
            CodeGenerationAgent(llm_client)
        ]
    
    @staticmethod
    def create_code_agent(llm_client=None):
        """Create a code generation agent."""
        if llm_client is None:
            llm_client = MockLLMClient()
        return CodeGenerationAgent(llm_client)


# File: ai-code-editor/backend/api/v1/middleware_api.py
"""
API endpoints for the agentic middleware.
"""

import logging
from fastapi import APIRouter, HTTPException
from ...models.agent_models import ChatMessage, ExecutionContext
from ...core.orchestration.middleware import AgenticMiddleware

logger = logging.getLogger("middleware_api")
router = APIRouter()

# Global middleware instance (will be set by main app)
middleware = None

@router.post("/chat")
async def chat(message: ChatMessage):
    """Process a chat message through the agentic system."""
    global middleware
    
    if not middleware:
        raise HTTPException(status_code=503, detail="Middleware not initialized")
    
    try:
        # Create execution context
        context = ExecutionContext(
            session_id=message.session_id,
            user_id=message.user_id,
            project_id=message.project_id,
            workspace_path=message.workspace_path
        )
        
        # Process through middleware
        response = await middleware.process_request(message.message, context)
        
        return {
            "session_id": message.session_id,
            "response": response,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agents")
async def list_agents():
    """List available agents and their capabilities."""
    global middleware
    
    if not middleware:
        return {"agents": []}
    
    capabilities = middleware.agent_registry.get_all_capabilities()
    
    agents = []
    for agent_type, caps in capabilities.items():
        agents.append({
            "type": agent_type.value,
            "capabilities": caps
        })
    
    return {"agents": agents}

@router.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "middleware_active": middleware is not None
    }


# File: ai-code-editor/backend/app/main.py (Updated)
"""
Main FastAPI application.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..core.orchestration.middleware import AgenticMiddleware
from ..agents.factory import AgentFactory
from ..api.v1.middleware_api import router as middleware_router
from ..api.v1 import middleware_api

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# Create FastAPI app
app = FastAPI(
    title="AI Code Editor",
    description="AI-powered code editor with agentic middleware",
    version="0.1.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize the agentic middleware."""
    logger.info("Starting AI Code Editor API...")
    
    try:
        # Initialize middleware
        middleware = AgenticMiddleware()
        await middleware.initialize()
        
        # Create and register agents
        agents = AgentFactory.create_all_agents()
        for agent in agents:
            middleware.register_agent(agent)
        
        # Make middleware available to API routes
        middleware_api.middleware = middleware
        
        logger.info(f"✅ Initialized with {len(agents)} agents")
        
    except Exception as e:
        logger.error(f"❌ Failed to start: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "AI Code Editor API", "status": "running"}

# Include API routes
app.include_router(middleware_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)