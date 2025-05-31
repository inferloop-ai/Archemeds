# Agentic Middleware - Deployment and Usage Guide

## 🏗️ Architecture Overview

The Agentic Middleware provides a complete orchestration layer for AI-powered development tools. It consists of:

### Core Components

1. **AgenticMiddleware** - Main orchestrator
2. **Agent Registry** - Manages available agents
3. **Intent Classifier** - Understands user requests
4. **Task Planner** - Breaks complex tasks into subtasks
5. **Execution Engine** - Runs agent workflows
6. **Memory Management** - Context and conversation history
7. **Communication Bus** - Inter-agent messaging

### Specialized Agents

- **Code Generation Agent** - Creates code from natural language
- **Infrastructure Agent** - Generates Docker, K8s, Terraform configs
- **Testing Agent** - Creates comprehensive test suites
- **DevOps Agent** - Sets up CI/CD pipelines
- **Documentation Agent** - Generates docs and comments
- **Security Agent** - Performs security scans and reviews

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install fastapi uvicorn redis langchain langgraph pydantic

# Start Redis (required for memory and communication)
docker run -d --name redis -p 6379:6379 redis:alpine

# Clone and setup
git clone <your-repo>
cd agentic-middleware
```

### 2. Configuration

Create `config.yaml`:

```yaml
# Agentic Middleware Configuration
redis:
  url: "redis://localhost:6379"
  
llm:
  provider: "openai"  # or "claude", "deepseek"
  api_key: "${LLM_API_KEY}"
  model: "gpt-4"
  
agents:
  enabled:
    - code
    - infrastructure  
    - testing
    - devops
    - documentation
    - security
  
server:
  host: "0.0.0.0"
  port: 8000
  workers: 1
  
logging:
  level: "INFO"
  format: "json"
```

### 3. Environment Variables

```bash
# .env file
LLM_API_KEY=your_openai_or_claude_api_key
REDIS_URL=redis://localhost:6379
WORKSPACE_PATH=/tmp/workspaces
LOG_LEVEL=INFO
```

### 4. Start the Server

```bash
# Development
uvicorn middleware_integration:app --reload --host 0.0.0.0 --port 8000

# Production
gunicorn middleware_integration:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔧 Usage Examples

### REST API Usage

```python
import httpx
import asyncio

async def demo_rest_api():
    async with httpx.AsyncClient() as client:
        # Send a code generation request
        response = await client.post("http://localhost:8000/chat", json={
            "message": "Create a FastAPI app with user authentication",
            "session_id": "demo-session",
            "user_id": "developer",
            "project_id": "my-project",
            "workspace_path": "/tmp/my-project",
            "parameters": {
                "language": "python",
                "framewor