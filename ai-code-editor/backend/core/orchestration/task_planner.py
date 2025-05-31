"""
Task planning and decomposition.
"""

import logging
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime
from ...models.agent_models import TaskRequest

@dataclass
class ExecutionPlan:
    """Plan for executing a complex task."""
    id: str
    original_task: TaskRequest
    subtasks: List[TaskRequest]
    dependencies: Dict[str, List[str]]
    estimated_duration: int

class TaskPlanner:
    """Plans complex tasks by breaking them into subtasks."""
    
    def __init__(self, agent_registry):
        self.agent_registry = agent_registry
        self.logger = logging.getLogger("task_planner")
    
    async def create_plan(self, task: TaskRequest) -> ExecutionPlan:
        """Create an execution plan for a task."""
        # Simple planning for now
        return ExecutionPlan(
            id="plan-1",
            original_task=task,
            subtasks=[task],
            dependencies={},
            estimated_duration=60
        )
