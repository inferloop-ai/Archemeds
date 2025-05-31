#!/bin/bash
# File Creation Script - AI Code Editor Phase 2
# Creates all necessary files with proper directory structure

set -e
echo "🏗️ Creating AI Code Editor Phase 2 files..."

# Ensure we're in the right directory
if [ ! -d "ai-code-editor" ]; then
    echo "❌ Please run this from the directory containing 'ai-code-editor' folder"
    exit 1
fi

cd ai-code-editor

# =============================================================================
# BACKEND FILES
# =============================================================================

echo "📁 Creating backend directory structure..."

# Create necessary directories
mkdir -p backend/agents/base
mkdir -p backend/agents/code
mkdir -p backend/core/llm
mkdir -p backend/api/v1
mkdir -p backend/app

# File 1: Backend Base Agent
echo "📄 Creating: backend/agents/base/agent.py"
cat > backend/agents/base/agent.py << 'EOF'
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
EOF

# File 2: Mock LLM Client
echo "📄 Creating: backend/core/llm/mock_client.py"
cat > backend/core/llm/mock_client.py << 'EOF'
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
EOF

# File 3: Code Agent
echo "📄 Creating: backend/agents/code/code_agent.py"
cat > backend/agents/code/code_agent.py << 'EOF'
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
EOF

# File 4: Agent Factory
echo "📄 Creating: backend/agents/factory.py"
cat > backend/agents/factory.py << 'EOF'
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
EOF

# File 5: API Routes
echo "📄 Creating: backend/api/v1/middleware_api.py"
cat > backend/api/v1/middleware_api.py << 'EOF'
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
EOF

# File 6: Updated Main App
echo "📄 Creating: backend/app/main.py"
cat > backend/app/main.py << 'EOF'
# File: ai-code-editor/backend/app/main.py
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
EOF

# Create necessary __init__.py files
echo "📄 Creating __init__.py files..."
touch backend/agents/__init__.py
touch backend/agents/base/__init__.py
touch backend/agents/code/__init__.py
touch backend/core/__init__.py
touch backend/core/llm/__init__.py
touch backend/api/__init__.py
touch backend/api/v1/__init__.py

# =============================================================================
# FRONTEND FILES
# =============================================================================

echo "📁 Creating frontend directory structure..."

# Create necessary directories
mkdir -p frontend/src/services/api
mkdir -p frontend/src/components/editor
mkdir -p frontend/src/components/chat
mkdir -p frontend/public

# File 1: API Client
echo "📄 Creating: frontend/src/services/api/client.ts"
cat > frontend/src/services/api/client.ts << 'EOF'
// File: ai-code-editor/frontend/src/services/api/client.ts
export interface ChatMessage {
  message: string;
  session_id: string;
  user_id?: string;
  project_id?: string;
  workspace_path?: string;
}

export interface ChatResponse {
  session_id: string;
  response: {
    status: string;
    result?: {
      code: string;
      language: string;
      explanation: string;
    };
  };
  timestamp: string;
}

class APIClient {
  private baseURL: string;

  constructor(baseURL: string = 'http://localhost:8000') {
    this.baseURL = baseURL;
  }

  async sendChatMessage(message: ChatMessage): Promise<ChatResponse> {
    const response = await fetch(`${this.baseURL}/api/v1/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(message),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  async getAgents() {
    const response = await fetch(`${this.baseURL}/api/v1/agents`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  }

  async healthCheck() {
    const response = await fetch(`${this.baseURL}/api/v1/health`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  }
}

export const apiClient = new APIClient();
EOF

# File 2: Monaco Editor Component
echo "📄 Creating: frontend/src/components/editor/MonacoEditor.tsx"
cat > frontend/src/components/editor/MonacoEditor.tsx << 'EOF'
// File: ai-code-editor/frontend/src/components/editor/MonacoEditor.tsx
import React, { useRef } from 'react';
import Editor from '@monaco-editor/react';

interface MonacoEditorProps {
  value: string;
  onChange: (value: string) => void;
  language: string;
  theme?: string;
}

const MonacoEditor: React.FC<MonacoEditorProps> = ({
  value,
  onChange,
  language,
  theme = 'vs-dark'
}) => {
  const editorRef = useRef(null);

  function handleEditorDidMount(editor: any, monaco: any) {
    editorRef.current = editor;
  }

  function handleEditorChange(value: string | undefined) {
    onChange(value || '');
  }

  return (
    <div className="h-full w-full">
      <Editor
        height="100%"
        defaultLanguage={language}
        value={value}
        theme={theme}
        onMount={handleEditorDidMount}
        onChange={handleEditorChange}
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          lineNumbers: 'on',
          roundedSelection: false,
          scrollBeyondLastLine: false,
          automaticLayout: true,
        }}
      />
    </div>
  );
};

export default MonacoEditor;
EOF

# File 3: Chat Interface
echo "📄 Creating: frontend/src/components/chat/ChatInterface.tsx"
cat > frontend/src/components/chat/ChatInterface.tsx << 'EOF'
// File: ai-code-editor/frontend/src/components/chat/ChatInterface.tsx
import React, { useState, useRef, useEffect } from 'react';
import { apiClient, ChatMessage, ChatResponse } from '../../services/api/client';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  code?: {
    content: string;
    language: string;
    explanation: string;
  };
}

interface ChatInterfaceProps {
  onCodeGenerated: (code: string, language: string) => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ onCodeGenerated }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: 'Hello! I\'m your AI coding assistant. I can help you generate code, create APIs, build React components, and more. What would you like to build?',
      timestamp: new Date(),
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const chatMessage: ChatMessage = {
        message: input,
        session_id: 'demo-session',
        user_id: 'demo-user',
        project_id: 'demo-project',
        workspace_path: '/tmp/demo'
      };

      const response: ChatResponse = await apiClient.sendChatMessage(chatMessage);

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: response.response.result?.explanation || 'I generated some code for you!',
        timestamp: new Date(),
      };

      if (response.response.result?.code) {
        assistantMessage.code = {
          content: response.response.result.code,
          language: response.response.result.language,
          explanation: response.response.result.explanation
        };
        
        // Update the editor with generated code
        onCodeGenerated(response.response.result.code, response.response.result.language);
      }

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: 'Sorry, I encountered an error. Please make sure the backend server is running.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-900 text-white">
      {/* Header */}
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-lg font-semibold">AI Assistant</h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.type === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-100'
              }`}
            >
              <p className="text-sm">{message.content}</p>
              {message.code && (
                <div className="mt-2 p-2 bg-gray-800 rounded text-xs">
                  <div className="text-green-400 mb-1">
                    Generated {message.code.language} code:
                  </div>
                  <pre className="text-gray-300 overflow-x-auto">
                    {message.code.content.length > 100 
                      ? message.code.content.substring(0, 100) + '...'
                      : message.code.content
                    }
                  </pre>
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-700 text-gray-100 px-4 py-2 rounded-lg">
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span className="text-sm">Generating...</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-700">
        <div className="flex space-x-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me to generate code..."
            className="flex-1 p-3 bg-gray-800 text-white rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={1}
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
EOF

# File 4: Main App Component
echo "📄 Creating: frontend/src/App.tsx"
cat > frontend/src/App.tsx << 'EOF'
// File: ai-code-editor/frontend/src/App.tsx
import React, { useState, useEffect } from 'react';
import MonacoEditor from './components/editor/MonacoEditor';
import ChatInterface from './components/chat/ChatInterface';
import { apiClient } from './services/api/client';
import './App.css';

function App() {
  const [code, setCode] = useState('# Welcome to AI Code Editor\n# Ask the AI to generate code for you!\n\nprint("Hello, World!")');
  const [language, setLanguage] = useState('python');
  const [isBackendConnected, setIsBackendConnected] = useState(false);

  // Check backend connection on startup
  useEffect(() => {
    checkBackendConnection();
  }, []);

  const checkBackendConnection = async () => {
    try {
      await apiClient.healthCheck();
      setIsBackendConnected(true);
    } catch (error) {
      setIsBackendConnected(false);
      console.error('Backend connection failed:', error);
    }
  };

  const handleCodeGenerated = (generatedCode: string, generatedLanguage: string) => {
    setCode(generatedCode);
    setLanguage(generatedLanguage);
  };

  const handleCodeChange = (newCode: string) => {
    setCode(newCode);
  };

  return (
    <div className="h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="h-12 bg-gray-800 border-b border-gray-700 flex items-center px-4">
        <h1 className="text-xl font-bold">AI Code Editor</h1>
        <div className="ml-auto flex items-center space-x-4">
          <div className="text-sm">
            Language: <span className="font-mono text-blue-400">{language}</span>
          </div>
          <div className={`flex items-center space-x-2 text-sm ${isBackendConnected ? 'text-green-400' : 'text-red-400'}`}>
            <div className={`w-2 h-2 rounded-full ${isBackendConnected ? 'bg-green-400' : 'bg-red-400'}`}></div>
            <span>{isBackendConnected ? 'Connected' : 'Disconnected'}</span>
          </div>
          <button
            onClick={checkBackendConnection}
            className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm"
          >
            Refresh
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className="h-[calc(100vh-3rem)] flex">
        {/* Editor */}
        <div className="flex-1 min-w-0">
          <MonacoEditor
            value={code}
            onChange={handleCodeChange}
            language={language}
            theme="vs-dark"
          />
        </div>

        {/* Chat Sidebar */}
        <div className="w-80 border-l border-gray-700">
          <ChatInterface onCodeGenerated={handleCodeGenerated} />
        </div>
      </div>

      {/* Connection Warning */}
      {!isBackendConnected && (
        <div className="fixed bottom-4 left-4 bg-red-600 text-white p-3 rounded-lg shadow-lg">
          <p className="text-sm">
            ⚠️ Backend not connected. Start the backend server:
          </p>
          <code className="text-xs bg-red-700 px-2 py-1 rounded mt-1 block">
            cd backend && python -m app.main
          </code>
        </div>
      )}
    </div>
  );
}

export default App;
EOF

# File 5: Package.json
echo "📄 Creating: frontend/package.json"
cat > frontend/package.json << 'EOF'
{
  "name": "ai-code-editor-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@monaco-editor/react": "^4.6.0",
    "typescript": "^5.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview",
    "start": "vite"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^4.4.0",
    "eslint": "^8.45.0",
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.24",
    "tailwindcss": "^3.3.0"
  }
}
EOF

# File 6: Other necessary files
echo "📄 Creating: frontend/vite.config.ts"
cat > frontend/vite.config.ts << 'EOF'
// File: ai-code-editor/frontend/vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true
  }
})
EOF

echo "📄 Creating: frontend/tailwind.config.js"
cat > frontend/tailwind.config.js << 'EOF'
// File: ai-code-editor/frontend/tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOF

echo "📄 Creating: frontend/src/index.tsx"
cat > frontend/src/index.tsx << 'EOF'
// File: ai-code-editor/frontend/src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF

echo "📄 Creating: frontend/src/index.css"
cat > frontend/src/index.css << 'EOF'
/* File: ai-code-editor/frontend/src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

html, body, #root {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

* {
  box-sizing: border-box;
}
EOF

echo "📄 Creating: frontend/src/App.css"
cat > frontend/src/App.css << 'EOF'
/* File: ai-code-editor/frontend/src/App.css */
.App {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.monaco-editor {
  background-color: #1e1e1e !important;
}

/* Custom scrollbar for chat */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #374151;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #6b7280;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
EOF

echo "📄 Creating: frontend/public/index.html"
cat > frontend/public/index.html << 'EOF'
<!-- File: ai-code-editor/frontend/public/index.html -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="AI-powered code editor with intelligent agents" />
    <title>AI Code Editor</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
    <script type="module" src="/src/index.tsx"></script>
  </body>
</html>
EOF

echo ""
echo "✅ All files created successfully!"
echo ""
echo "📋 File Summary:"
echo "   Backend: 6 Python files + __init__.py files"
echo "   Frontend: 9 TypeScript/JavaScript/CSS/HTML files"
echo ""
echo "🚀 Next Steps:"
echo "1. Install backend dependencies:"
echo "   cd backend && pip install fastapi uvicorn pydantic python-dotenv"
echo ""
echo "2. Install frontend dependencies:"
echo "   cd frontend && npm install"
echo ""
echo "3. Start backend:"
echo "   cd backend && python -m app.main"
echo ""
echo "4. Start frontend:"
echo "   cd frontend && npm run dev"
echo ""
echo "5. Open http://localhost:3000 and test!"
echo ""
echo "🎉 Your AI Code Editor is ready!"
