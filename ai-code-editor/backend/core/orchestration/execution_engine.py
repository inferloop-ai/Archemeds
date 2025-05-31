"""
Execution engine for running agent workflows.
"""

import logging
from datetime import datetime
from typing import List
from ...models.agent_models import TaskRequest, TaskResult, TaskStatus

class ExecutionEngine:
    """Executes agent workflows."""
    
    def __init__(self, agent_registry, memory):
        self.agent_registry = agent_registry
        self.memory = memory
        self.logger = logging.getLogger("execution_engine")
    
    async def execute_task(self, task: TaskRequest) -> TaskResult:
        """Execute a single task."""
        start_time = datetime.utcnow()
        
        try:
            # Find capable agents
            capable_agents = await self.agent_registry.find_capable_agents(task)
            
            if not capable_agents:
                return TaskResult(
                    task_id=task.id,
                    agent_type="unknown",
                    status=TaskStatus.FAILED,
                    error="No capable agents found"
                )
            
            # Execute with first capable agent
            selected_agent = capable_agents[0]
            result = await selected_agent.execute(task)
            
            return result
            
        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            return TaskResult(
                task_id=task.id,
                agent_type="unknown",
                status=TaskStatus.FAILED,
                error=str(e),
                execution_time=execution_time
            )
    
    async def execute_plan(self, plan) -> List[TaskResult]:
        """Execute a complex plan."""
        results = []
        for task in plan.subtasks:
            result = await self.execute_task(task)
            results.append(result)
        return results
