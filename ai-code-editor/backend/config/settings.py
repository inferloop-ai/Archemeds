"""
Application configuration management - Pydantic V2 Compatible.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from .models.agent_models import LLMConfig, AgentConfig, SystemConfig, AgentType


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Server settings
    app_name: str = "AI Code Editor"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    
    # Redis settings
    redis_url: str = "redis://localhost:6379"
    redis_max_connections: int = 10
    
    # LLM settings
    llm_provider: str = "openai"
    llm_api_key: str = ""
    llm_model: str = "gpt-4"
    llm_max_tokens: int = 4000
    llm_temperature: float = 0.7
    llm_timeout: int = 30
    
    # Agent settings
    max_concurrent_agents: int = 10
    agent_timeout: int = 300
    default_workspace_path: str = "/tmp/workspaces"
    
    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False

    def get_llm_config(self) -> LLMConfig:
        """Get LLM configuration."""
        return LLMConfig(
            provider=self.llm_provider,
            api_key=self.llm_api_key,
            model=self.llm_model,
            max_tokens=self.llm_max_tokens,
            temperature=self.llm_temperature,
            timeout=self.llm_timeout
        )
    
    def get_agent_config(self) -> AgentConfig:
        """Get agent configuration."""
        return AgentConfig(
            enabled_agents=[
                AgentType.CODE,
                AgentType.INFRASTRUCTURE, 
                AgentType.TESTING
            ],
            max_concurrent_tasks=self.max_concurrent_agents,
            default_timeout=self.agent_timeout
        )
    
    def get_system_config(self) -> SystemConfig:
        """Get complete system configuration."""
        return SystemConfig(
            redis_url=self.redis_url,
            llm=self.get_llm_config(),
            agents=self.get_agent_config(),
            debug=self.debug,
            log_level=self.log_level
        )


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings
