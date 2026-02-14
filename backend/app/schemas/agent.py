# schemas/agent.py
# Pydantic schemas for Agent

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class AgentBase(BaseModel):
    """Base agent schema with common fields."""
    name: str


class AgentCreate(AgentBase):
    """Schema for creating a new agent."""
    api_key: Optional[str] = None


class AgentUpdate(BaseModel):
    """Schema for updating agent information."""
    name: Optional[str] = None
    status: Optional[str] = None


class AgentResponse(AgentBase):
    """Schema for agent response."""
    id: int
    api_key: Optional[str] = None
    status: str
    last_seen: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AgentListResponse(BaseModel):
    """Schema for list of agents."""
    id: int
    name: str
    status: str
    last_seen: datetime
    
    model_config = ConfigDict(from_attributes=True)
