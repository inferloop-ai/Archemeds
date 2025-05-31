# Quick Setup Guide - Phase 1 Implementation

## 🚀 **Get Started in 5 Minutes**

### **Step 1: Generate Structure & Models**
```bash
# Create the complete structure
python phase1_structure_generator.py

# Navigate to project
cd ai-code-editor
```

### **Step 2: Setup Backend Environment**
```bash
# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements/development.txt
```

### **Step 3: Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# At minimum, add your LLM API key:
LLM_API_KEY=your_openai_api_key_here
```

### **Step 4: Test the Foundation**
```python
# Test data models work
cd backend
python -c "
from models.agent_models import *
print('✅ All models imported successfully!')

# Create sample data
context = create_execution_context('test-session', 'user-1')
task = create_task_request('Create a Python function', context)
print(f'✅ Created task: {task.id}')
print(f'✅ Intent: {task.intent}')
"
```

## 📋 **What You Have Now**

### **✅ Complete Data Models**
All models are ready to use in `backend/models/agent_models.py`:

```python
# Core models available:
from backend.models.agent_models import (
    # Enums
    AgentType, TaskStatus, IntentType, Priority,
    
    # Core models
    ExecutionContext, TaskRequest, TaskResult, AgentMessage,
    
    # Request/Response
    ChatMessage, ChatResponse, SystemStatus,
    
    # Configuration
    LLMConfig, AgentConfig, SystemConfig,
    
    # Utilities
    create_execution_context, create_task_request
)
```

### **✅ Configuration System**
Environment-based config in `backend/config/settings.py`:

```python
from backend.config import settings

# Access configuration
print(f"LLM Provider: {settings.llm_provider}")
print(f"Redis URL: {settings.redis_url}")
print(f"Debug Mode: {settings.debug}")

# Get typed configs
llm_config = settings.get_llm_config()
agent_config = settings.get_agent_config()
```

### **✅ Project Structure**
```
ai-code-editor/
├── backend/
│   ├── models/                # ✅ COMPLETE - All data models
│   ├── config/                # ✅ COMPLETE - Configuration system
│   ├── core/orchestration/    # 🔄 NEXT - Middleware components
│   ├── agents/                # 🔄 NEXT - Agent implementations
│   ├── api/                   # 🔄 NEXT - REST endpoints
│   ├── requirements/          # ✅ COMPLETE - Dependencies
│   └── tests/                 # 🔄 Ready for tests
├── frontend/                  # 🔄 React structure ready
├── infrastructure/            # 🔄 Docker configs ready
└── docs/                      # 📚 Documentation structure
```

## 🧪 **Test Your Setup**

### **Test 1: Import Models**
```python
# backend/test_models.py
from models.agent_models import *

def test_basic_models():
    # Test ExecutionContext
    context = create_execution_context(
        session_id="test-123",
        user_id="developer-1",
        project_id="my-project",
        workspace_path="/tmp/test-project"
    )
    print(f"✅ Context created: {context.session_id}")
    
    # Test TaskRequest
    task = create_task_request(
        description="Create a FastAPI app with authentication",
        context=context,
        intent=IntentType.CODE_GENERATION,
        priority=Priority.HIGH
    )
    print(f"✅ Task created: {task.id}")
    print(f"   Intent: {task.intent}")
    print(f"   Priority: {task.priority}")
    
    # Test TaskResult
    result = create_task_result(
        task_id=task.id,
        agent_type=AgentType.CODE,
        status=TaskStatus.COMPLETED,
        result={"code": "print('Hello, World!')", "language": "python"}
    )
    print(f"✅ Result created: {result.status}")
    
    # Test ChatMessage
    chat_msg = ChatMessage(
        message="Generate a Python function to calculate fibonacci numbers",
        session_id="test-session",
        user_id="developer",
        project_id="fibonacci-project"
    )
    print(f"✅ Chat message: {chat_msg.message[:50]}...")
    
    print("\n🎉 All tests passed! Models are working correctly.")

if __name__ == "__main__":
    test_basic_models()
```

Run the test:
```bash
cd backend
python test_models.py
```

### **Test 2: Configuration**
```python
# backend/test_config.py
from config.settings import settings

def test_configuration():
    print("Configuration Test:")
    print(f"✅ App Name: {settings.app_name}")
    print(f"✅ Version: {settings.app_version}")
    print(f"✅ Debug: {settings.debug}")
    print(f"✅ LLM Provider: {settings.llm_provider}")
    print(f"✅ Redis URL: {settings.redis_url}")
    
    # Test typed configs
    llm_config = settings.get_llm_config()
    print(f"✅ LLM Model: {llm_config.model}")
    print(f"✅ Max Tokens: {llm_config.max_tokens}")
    
    agent_config = settings.get_agent_config()
    print(f"✅ Enabled Agents: {[a.value for a in agent_config.enabled_agents]}")
    print(f"✅ Max Concurrent: {agent_config.max_concurrent_tasks}")
    
    print("\n🎉 Configuration working correctly!")

if __name__ == "__main__":
    test_configuration()
```

## 🔄 **Next Steps - Continue Phase 1**

Now you're ready for the remaining Phase 1 steps:

### **Day 2: Base Agent Classes**
Create `backend/agents/base/agent.py`:
```python
from abc import ABC, abstractmethod
from typing import List
from ...models.agent_models import TaskRequest, TaskResult, AgentCapability, AgentType

class BaseAgent(ABC):
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.capabilities: List[AgentCapability] = []
    
    @abstractmethod
    async def execute(self, task: TaskRequest) -> TaskResult:
        """Execute a task and return the result."""
        pass
    
    @abstractmethod
    async def can_handle(self, task: TaskRequest) -> bool:
        """Check if this agent can handle the given task."""
        pass
    
    def get_capabilities(self) -> List[AgentCapability]:
        """Get agent capabilities."""
        return self.capabilities
```

### **Day 3: Mock LLM Client**
Create `backend/core/llm/mock_client.py`:
```python
import json
from typing import List, Dict, Any

class MockLLMClient:
    """Mock LLM client for testing and development."""
    
    async def chat_completion(self, messages: List[Dict[str, str]]):
        user_message = messages[-1]["content"].lower()
        
        # Simple pattern matching for responses
        if "fastapi" in user_message:
            return MockResponse(json.dumps({
                "code": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'Hello': 'World'}",
                "explanation": "Basic FastAPI application with a root endpoint",
                "dependencies": ["fastapi", "uvicorn"]
            }))
        
        return MockResponse("Mock response for: " + user_message)

class MockResponse:
    def __init__(self, content: str):
        self.content = content
```

### **Day 4-7: Complete Basic System**
- Agent registry
- Intent classifier  
- Basic middleware
- REST API endpoints

## 💡 **Pro Tips**

### **Development Workflow**
```bash
# Start Redis for testing
docker run -d --name redis -p 6379:6379 redis:alpine

# Run tests as you develop
cd backend && python -m pytest tests/

# Use hot reload during development
cd backend && uvicorn app.main:app --reload
```

### **Debugging**
```python
# Enable debug mode in .env
DEBUG=true
LOG_LEVEL=DEBUG

# Use this in your code for debugging
from config.settings import settings
if settings.debug:
    print(f"Debug: Task created with ID {task.id}")
```

### **Best Practices**
1. **Always validate data** using the built-in Pydantic validators
2. **Use type hints** - all models support full typing
3. **Handle errors gracefully** using the error models
4. **Test incrementally** - verify each component before moving on

## 🎯 **Success Criteria for Phase 1**

By end of Phase 1 (Day 7), you should have:
- ✅ All data models working and tested
- ✅ Basic FastAPI server running
- ✅ Simple agent that can execute tasks
- ✅ Basic middleware routing requests
- ✅ REST API accepting chat messages
- ✅ End-to-end test: User message → Agent → Response

**Ready to continue?** You now have a rock-solid foundation to build upon! 🚀

## 📞 **Need Help?**

Common issues and solutions:

**Import Errors:**
```bash
# Make sure you're in the backend directory
cd backend
# And virtual environment is activated
source venv/bin/activate
```

**Missing Dependencies:**
```bash
# Reinstall requirements
pip install -r requirements/development.txt
```

**Configuration Issues:**
```bash
# Check .env file exists and has LLM_API_KEY
cat .env | grep LLM_API_KEY
```

Your foundation is now complete and ready for building the actual agentic middleware! 🎉