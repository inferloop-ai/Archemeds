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
                "framework": "fastapi"
            }
        })
        
        result = response.json()
        print(f"Response: {result}")

# Run the demo
asyncio.run(demo_rest_api())
```

### WebSocket Usage

```python
import asyncio
import websockets
import json

async def demo_websocket():
    uri = "ws://localhost:8000/ws/demo-session"
    
    async with websockets.connect(uri) as websocket:
        # Send a message
        await websocket.send(json.dumps({
            "type": "chat_message",
            "message": "Generate Docker configuration for my app",
            "user_id": "developer",
            "project_id": "my-project",
            "workspace_path": "/tmp/my-project"
        }))
        
        # Listen for responses
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print(f"Received: {data}")
            
            if data.get("type") == "task_completed":
                break

# Run the demo
asyncio.run(demo_websocket())
```

### Python Client

```python
from agentic_client import AgenticClient

async def demo_client():
    client = AgenticClient("http://localhost:8000")
    
    # Send various requests
    responses = []
    
    # 1. Code generation
    response = await client.send_message(
        "Create a REST API for a todo application",
        language="python",
        framework="fastapi"
    )
    responses.append(response)
    
    # 2. Infrastructure setup
    response = await client.send_message(
        "Create Docker configuration for the todo API"
    )
    responses.append(response)
    
    # 3. Testing
    response = await client.send_message(
        "Generate comprehensive tests for the todo API"
    )
    responses.append(response)
    
    return responses
```

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Create workspace directory
RUN mkdir -p /app/workspaces

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start server
CMD ["uvicorn", "middleware_integration:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  agentic-middleware:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
      - LLM_API_KEY=${LLM_API_KEY}
      - WORKSPACE_PATH=/app/workspaces
    volumes:
      - ./workspaces:/app/workspaces
      - ./logs:/app/logs
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - agentic-middleware
    restart: unless-stopped

volumes:
  redis_data:
```

## ☸️ Kubernetes Deployment

### deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agentic-middleware
  labels:
    app: agentic-middleware
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agentic-middleware
  template:
    metadata:
      labels:
        app: agentic-middleware
    spec:
      containers:
      - name: agentic-middleware
        image: agentic-middleware:latest
        ports:
        - containerPort: 8000
        env:
        - name: REDIS_URL
          value: "redis://redis-service:6379"
        - name: LLM_API_KEY
          valueFrom:
            secretKeyRef:
              name: llm-secrets
              key: api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: agentic-middleware-service
spec:
  selector:
    app: agentic-middleware
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379

---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
  - protocol: TCP
    port: 6379
    targetPort: 6379
```

## 📊 Monitoring and Observability

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'agentic-middleware'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Agentic Middleware Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "Requests/sec"
          }
        ]
      },
      {
        "title": "Agent Execution Time",
        "type": "graph", 
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(agent_execution_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Active Sessions",
        "type": "stat",
        "targets": [
          {
            "expr": "active_sessions_total",
            "legendFormat": "Sessions"
          }
        ]
      }
    ]
  }
}
```

## 🔒 Security Configuration

### Authentication

```python
# auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# Add to endpoints
@app.post("/chat")
async def process_chat_message(
    message: ChatMessage,
    user: dict = Depends(verify_token)
):
    # Process with user context
    pass
```

### Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/chat")
@limiter.limit("10/minute")
async def process_chat_message(request: Request, message: ChatMessage):
    # Process message with rate limiting
    pass
```

## 🧪 Testing

### Unit Tests

```python
import pytest
from agentic_middleware import AgenticMiddleware
from concrete_agents import CodeGenerationAgent, MockLLMClient

@pytest.fixture
async def middleware():
    middleware = AgenticMiddleware("redis://localhost:6379")
    await middleware.initialize()
    
    # Register test agents
    llm_client = MockLLMClient()
    code_agent = CodeGenerationAgent(llm_client)
    middleware.register_agent(code_agent)
    
    return middleware

@pytest.mark.asyncio
async def test_code_generation(middleware):
    context = ExecutionContext(
        session_id="test",
        user_id="test",
        project_id="test",
        workspace_path="/tmp/test"
    )
    
    response = await middleware.process_request(
        "Create a Python function to calculate fibonacci numbers",
        context
    )
    
    assert response["status"] == "completed"
    assert "code" in response["result"]
```

### Integration Tests

```python
import httpx
import pytest

@pytest.mark.asyncio
async def test_api_endpoints():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        # Test health endpoint
        response = await client.get("/health")
        assert response.status_code == 200
        
        # Test chat endpoint
        response = await client.post("/chat", json={
            "message": "Create a simple function",
            "session_id": "test-session",
            "user_id": "test-user",
            "project_id": "test-project",
            "workspace_path": "/tmp/test"
        })
        assert response.status_code == 200
        assert "response" in response.json()
```

## 🔧 Customization

### Adding New Agents

```python
from agentic_middleware import LLMAgent, AgentType, AgentCapability

class CustomAgent(LLMAgent):
    def __init__(self, llm_client=None):
        capabilities = [
            AgentCapability(
                name="custom_capability",
                description="Does something custom",
                required_context=["input"],
                outputs=["output"]
            )
        ]
        super().__init__(AgentType.CUSTOM, capabilities, llm_client)
    
    def _get_system_prompt(self) -> str:
        return "You are a custom agent that..."
    
    async def can_handle(self, task: TaskRequest) -> bool:
        return "custom" in task.description.lower()
    
    async def execute(self, task: TaskRequest) -> TaskResult:
        # Custom execution logic
        pass

# Register the agent
middleware.register_agent(CustomAgent(llm_client))
```

### Custom Intent Classification

```python
class CustomIntentClassifier(IntentClassifier):
    async def classify(self, user_input: str, context: ExecutionContext) -> IntentType:
        # Custom classification logic
        if "deploy" in user_input.lower():
            return IntentType.DEPLOYMENT
        elif "test" in user_input.lower():
            return IntentType.TESTING
        else:
            return await super().classify(user_input, context)

# Use custom classifier
middleware.intent_classifier = CustomIntentClassifier(llm_client)
```

## 📈 Performance Tuning

### Redis Configuration

```ini
# redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### Application Settings

```python
# config.py
class Settings:
    redis_pool_size: int = 20
    max_concurrent_tasks: int = 100
    task_timeout: int = 300
    agent_timeout: int = 60
    llm_timeout: int = 30
    max_context_length: int = 8000
```

## 🚨 Troubleshooting

### Common Issues

1. **Redis Connection Failed**
   ```bash
   # Check Redis status
   redis-cli ping
   
   # Check connection
   telnet localhost 6379
   ```

2. **LLM API Errors**
   ```python
   # Check API key
   import openai
   openai.api_key = "your-key"
   response = openai.ChatCompletion.create(...)
   ```

3. **High Memory Usage**
   ```bash
   # Monitor memory
   docker stats
   
   # Check Redis memory
   redis-cli info memory
   ```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with profiling
python -m cProfile -o profile.out middleware_integration.py
```

This deployment guide provides everything needed to run the Agentic Middleware in production environments, from local development to cloud-scale Kubernetes deployments.