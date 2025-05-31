class APIClient {
  async healthCheck() {
    return { status: 'ok' };
  }
}

export const apiClient = new APIClient();
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
      error?: string;
    };
    timestamp: string;
  }
  
  export interface AgentInfo {
    type: string;
    capabilities: string[];
  }
  
  export interface AgentsResponse {
    agents: AgentInfo[];
  }
  
  class APIClient {
    private baseURL: string;
  
    constructor(baseURL: string = 'http://localhost:8000') {
      this.baseURL = baseURL;
    }
  
    async sendChatMessage(message: ChatMessage): Promise<ChatResponse> {
      try {
        const response = await fetch(`${this.baseURL}/api/v1/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(message),
        });
  
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
  
        const data = await response.json();
        return data;
      } catch (error) {
        console.error('API Error:', error);
        throw new Error(`Failed to send message: ${error instanceof Error ? error.message : 'Unknown error'}`);
      }
    }
  
    async getAgents(): Promise<AgentsResponse> {
      try {
        const response = await fetch(`${this.baseURL}/api/v1/agents`);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
      } catch (error) {
        console.error('Failed to fetch agents:', error);
        return { agents: [] };
      }
    }
  
    async healthCheck(): Promise<{ status: string; middleware_active: boolean }> {
      try {
        const response = await fetch(`${this.baseURL}/api/v1/health`);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
      } catch (error) {
        console.error('Health check failed:', error);
        throw error;
      }
    }
  
    // Test the root endpoint
    async testConnection(): Promise<any> {
      try {
        const response = await fetch(`${this.baseURL}/`);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return await response.json();
      } catch (error) {
        console.error('Connection test failed:', error);
        throw error;
      }
    }
  }
  
  export const apiClient = new APIClient();
  
  // File: ai-code-editor/frontend/src/components/chat/ChatInterface.tsx
  import React, { useState, useRef, useEffect } from 'react';
  import { apiClient, ChatMessage, ChatResponse } from '../../services/api/client';
  
  interface Message {
    id: string;
    type: 'user' | 'assistant' | 'error';
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
    isBackendConnected: boolean;
  }
  
  const ChatInterface: React.FC<ChatInterfaceProps> = ({ onCodeGenerated, isBackendConnected }) => {
    const [messages, setMessages] = useState<Message[]>([
      {
        id: '1',
        type: 'assistant',
        content: '👋 Hello! I\'m your AI coding assistant. I can help you generate code, create APIs, build React components, and more. What would you like to build?',
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
  
      if (!isBackendConnected) {
        const errorMessage: Message = {
          id: Date.now().toString(),
          type: 'error',
          content: '⚠️ Backend not connected. Please start the backend server first.',
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, errorMessage]);
        return;
      }
  
      const userMessage: Message = {
        id: Date.now().toString(),
        type: 'user',
        content: input,
        timestamp: new Date(),
      };
  
      setMessages(prev => [...prev, userMessage]);
      const currentInput = input;
      setInput('');
      setIsLoading(true);
  
      try {
        const chatMessage: ChatMessage = {
          message: currentInput,
          session_id: 'demo-session',
          user_id: 'demo-user',
          project_id: 'demo-project',
          workspace_path: '/tmp/demo'
        };
  
        console.log('Sending message to backend:', chatMessage);
        const response: ChatResponse = await apiClient.sendChatMessage(chatMessage);
        console.log('Backend response:', response);
  
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
        } else if (response.response.error) {
          assistantMessage.type = 'error';
          assistantMessage.content = `Error: ${response.response.error}`;
        }
  
        setMessages(prev => [...prev, assistantMessage]);
      } catch (error) {
        console.error('Error sending message:', error);
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: 'error',
          content: `❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}. Make sure the backend is running on port 8000.`,
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
  
    const getMessageBgColor = (type: string) => {
      switch (type) {
        case 'user': return 'bg-blue-600';
        case 'error': return 'bg-red-600';
        default: return 'bg-gray-700';
      }
    };
  
    return (
      <div className="flex flex-col h-full bg-gray-900 text-white">
        {/* Header */}
        <div className="p-4 border-b border-gray-700">
          <h2 className="text-lg font-semibold">AI Assistant</h2>
          <div className="text-xs text-gray-400 mt-1">
            {isBackendConnected ? '✅ Connected to backend' : '❌ Backend disconnected'}
          </div>
        </div>
  
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${getMessageBgColor(message.type)} text-white`}
              >
                <p className="text-sm">{message.content}</p>
                {message.code && (
                  <div className="mt-2 p-2 bg-gray-800 rounded text-xs">
                    <div className="text-green-400 mb-1 flex items-center">
                      <span>✨ Generated {message.code.language} code</span>
                    </div>
                    <pre className="text-gray-300 overflow-x-auto whitespace-pre-wrap">
                      {message.code.content.length > 200 
                        ? message.code.content.substring(0, 200) + '\n... (truncated, see editor for full code)'
                        : message.code.content
                      }
                    </pre>
                  </div>
                )}
                <div className="text-xs text-gray-300 mt-1">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-700 text-gray-100 px-4 py-2 rounded-lg">
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span className="text-sm">🤖 AI is thinking...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
  
        {/* Quick Actions */}
        <div className="px-4 pb-2">
          <div className="flex gap-2 text-xs">
            <button
              onClick={() => setInput('Create a Python function to calculate fibonacci numbers')}
              className="px-2 py-1 bg-gray-700 hover:bg-gray-600 rounded text-gray-300"
              disabled={isLoading}
            >
              Python Function
            </button>
            <button
              onClick={() => setInput('Create a FastAPI app with authentication')}
              className="px-2 py-1 bg-gray-700 hover:bg-gray-600 rounded text-gray-300"
              disabled={isLoading}
            >
              FastAPI App
            </button>
            <button
              onClick={() => setInput('Generate a React component with state')}
              className="px-2 py-1 bg-gray-700 hover:bg-gray-600 rounded text-gray-300"
              disabled={isLoading}
            >
              React Component
            </button>
          </div>
        </div>
  
        {/* Input */}
        <div className="p-4 border-t border-gray-700">
          <div className="flex space-x-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={isBackendConnected ? "Ask me to generate code..." : "Start backend first: cd backend && python -m app.main"}
              className="flex-1 p-3 bg-gray-800 text-white rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              rows={2}
              disabled={isLoading || !isBackendConnected}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !input.trim() || !isBackendConnected}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? '...' : 'Send'}
            </button>
          </div>
        </div>
      </div>
    );
  };
  
  export default ChatInterface;
  
  // File: ai-code-editor/frontend/src/App.tsx
  import React, { useState, useEffect } from 'react';
  import { apiClient } from './services/api/client';
  import ChatInterface from './components/chat/ChatInterface';
  import './App.css';
  
  function App() {
    const [code, setCode] = useState('# Welcome to AI Code Editor\n# Ask the AI to generate code for you!\n\nprint("Hello, World!")');
    const [language, setLanguage] = useState('python');
    const [isBackendConnected, setIsBackendConnected] = useState(false);
    const [agents, setAgents] = useState<any[]>([]);
    const [connectionStatus, setConnectionStatus] = useState<string>('Checking...');
  
    // Check backend connection on startup and periodically
    useEffect(() => {
      checkBackendConnection();
      const interval = setInterval(checkBackendConnection, 10000); // Check every 10 seconds
      return () => clearInterval(interval);
    }, []);
  
    const checkBackendConnection = async () => {
      try {
        setConnectionStatus('Connecting...');
        
        // First test basic connection
        await apiClient.testConnection();
        
        // Then check health
        const health = await apiClient.healthCheck();
        
        // Get available agents
        const agentsData = await apiClient.getAgents();
        
        setIsBackendConnected(true);
        setAgents(agentsData.agents);
        setConnectionStatus(`Connected • ${agentsData.agents.length} agents`);
        
        console.log('✅ Backend connected:', health);
        console.log('📋 Available agents:', agentsData.agents);
        
      } catch (error) {
        setIsBackendConnected(false);
        setAgents([]);
        setConnectionStatus('Disconnected');
        console.error('❌ Backend connection failed:', error);
      }
    };
  
    const handleCodeGenerated = (generatedCode: string, generatedLanguage: string) => {
      setCode(generatedCode);
      setLanguage(generatedLanguage);
      console.log(`📝 Code updated: ${generatedLanguage} (${generatedCode.length} chars)`);
    };
  
    const handleCodeChange = (newCode: string) => {
      setCode(newCode);
    };
  
    return (
      <div className="h-screen bg-gray-900 text-white">
        {/* Header */}
        <header className="h-12 bg-gray-800 border-b border-gray-700 flex items-center px-4">
          <h1 className="text-xl font-bold">🤖 AI Code Editor</h1>
          <div className="ml-auto flex items-center space-x-4">
            <div className="text-sm">
              Language: <span className="font-mono text-blue-400">{language}</span>
            </div>
            <div className={`flex items-center space-x-2 text-sm ${isBackendConnected ? 'text-green-400' : 'text-red-400'}`}>
              <div className={`w-2 h-2 rounded-full ${isBackendConnected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`}></div>
              <span>{connectionStatus}</span>
            </div>
            <button
              onClick={checkBackendConnection}
              className="px-3 py-1 bg-gray-700 hover:bg-gray-600 rounded text-sm transition-colors"
            >
              🔄 Refresh
            </button>
          </div>
        </header>
  
        {/* Main Content */}
        <div className="h-[calc(100vh-3rem)] flex">
          {/* Editor */}
          <div className="flex-1 min-w-0 bg-gray-800 p-4">
            <div className="h-full bg-gray-900 rounded p-4">
              <div className="flex justify-between items-center mb-3">
                <h3 className="text-lg text-gray-300">Generated Code</h3>
                <div className="text-sm text-gray-400">
                  {code.split('\n').length} lines • {code.length} chars
                </div>
              </div>
              <textarea
                value={code}
                onChange={(e) => handleCodeChange(e.target.value)}
                className="w-full h-[calc(100%-3rem)] bg-black text-green-400 p-4 font-mono text-sm resize-none border border-gray-600 rounded focus:outline-none focus:border-blue-500"
                placeholder="Generated code will appear here..."
                spellCheck={false}
              />
            </div>
          </div>
  
          {/* Chat Sidebar */}
          <div className="w-80 border-l border-gray-700">
            <ChatInterface 
              onCodeGenerated={handleCodeGenerated} 
              isBackendConnected={isBackendConnected}
            />
          </div>
        </div>
  
        {/* Status Bar */}
        <div className="h-6 bg-gray-800 border-t border-gray-700 flex items-center px-4 text-xs text-gray-400">
          <span>Ready</span>
          <span className="mx-2">•</span>
          <span>Backend: {isBackendConnected ? '✅ Online' : '❌ Offline'}</span>
          {agents.length > 0 && (
            <>
              <span className="mx-2">•</span>
              <span>Agents: {agents.map(a => a.type).join(', ')}</span>
            </>
          )}
        </div>
  
        {/* Connection Warning */}
        {!isBackendConnected && (
          <div className="fixed bottom-4 left-4 bg-red-600 text-white p-4 rounded-lg shadow-lg max-w-md">
            <p className="text-sm font-semibold mb-2">
              ⚠️ Backend Server Required
            </p>
            <p className="text-xs mb-2">
              Start the backend server to enable AI code generation:
            </p>
            <code className="text-xs bg-red-700 px-2 py-1 rounded block">
              cd backend && python -m app.main
            </code>
            <button
              onClick={checkBackendConnection}
              className="mt-2 px-3 py-1 bg-red-700 hover:bg-red-800 rounded text-xs"
            >
              Try Again
            </button>
          </div>
        )}
      </div>
    );
  }
  
  export default App;