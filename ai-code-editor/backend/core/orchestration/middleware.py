"""
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
