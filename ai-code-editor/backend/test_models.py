#!/usr/bin/env python3
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
        
        print("\n🎉 All models working correctly with Pydantic V2!")
        return True
    
    if __name__ == "__main__":
        test_models()
        
except Exception as e:
    print(f"❌ Error testing models: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
