#!/usr/bin/env python3
"""
Test script for backend API endpoints.
"""

import sys
import asyncio
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_api():
    """Test all API endpoints."""
    print("🧪 Testing backend API endpoints...")
    
    try:
        from models.agent_models import (
            ChatMessage, ExecutionContext, 
            create_execution_context, create_task_request
        )
        from core.orchestration.middleware import AgenticMiddleware
        from agents.factory import AgentFactory
        
        print("✅ All imports successful")
        
        # Test middleware initialization
        middleware = AgenticMiddleware()
        await middleware.initialize()
        print("✅ Middleware initialized")
        
        # Register agents
        agents = AgentFactory.create_all_agents()
        for agent in agents:
            middleware.register_agent(agent)
        print(f"✅ Registered {len(agents)} agents")
        
        # Test context creation
        context = create_execution_context(
            session_id="test-session",
            user_id="test-user",
            project_id="test-project",
            workspace_path="/tmp/test"
        )
        print("✅ Context creation works")
        
        # Test chat message processing
        test_messages = [
            "Create a Python function to calculate fibonacci numbers",
            "Generate a FastAPI app with authentication",
            "Write a React component with state management"
        ]
        
        for msg in test_messages:
            print(f"\n🤖 Testing: '{msg}'")
            
            response = await middleware.process_request(msg, context)
            print(f"   Status: {response.get('status', 'unknown')}")
            
            if 'result' in response and response['result']:
                result = response['result']
                if 'code' in result:
                    code_preview = result['code'][:100] + '...' if len(result['code']) > 100 else result['code']
                    print(f"   Generated: {result.get('language', 'unknown')} code")
                    print(f"   Preview: {code_preview}")
                else:
                    print(f"   Result: {result}")
            
            if 'error' in response:
                print(f"   Error: {response['error']}")
        
        print("\n🎉 Backend API test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_api())
    if not success:
        sys.exit(1)
