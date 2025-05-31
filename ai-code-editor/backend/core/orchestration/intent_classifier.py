"""
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
