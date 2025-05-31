"""
Registry for managing available agents.
"""

import logging
from typing import Dict, List, Optional
from ...models.agent_models import AgentType, TaskRequest

class AgentRegistry:
    """Registry for managing available agents."""
    
    def __init__(self):
        self.agents: Dict[AgentType, 'BaseAgent'] = {}
        self.logger = logging.getLogger("agent_registry")
    
    def register_agent(self, agent):
        """Register an agent."""
        self.agents[agent.agent_type] = agent
        self.logger.info(f"Registered agent: {agent.agent_type.value}")
    
    def get_agent(self, agent_type: AgentType):
        """Get an agent by type."""
        return self.agents.get(agent_type)
    
    async def find_capable_agents(self, task: TaskRequest) -> List:
        """Find agents capable of handling a task."""
        capable_agents = []
        for agent in self.agents.values():
            if await agent.can_handle(task):
                capable_agents.append(agent)
        return capable_agents
    
    def get_all_capabilities(self):
        """Get capabilities of all agents."""
        capabilities = {}
        for agent_type, agent in self.agents.items():
            capabilities[agent_type] = agent.get_capabilities()
        return capabilities
