# schemas/activity_log.py
# Pydantic schemas for ActivityLog

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ActivityLogBase(BaseModel):
    """Base activity log schema with common fields."""
    activity_type: str
    description: Optional[str] = None


class ActivityLogCreate(ActivityLogBase):
    """Schema for creating a new activity log."""
    agent_id: Optional[int] = None
    risk_level: str = "low"


class ActivityLogResponse(ActivityLogBase):
    """Schema for activity log response."""
    id: int
    agent_id: Optional[int] = None
    user_id: Optional[str] = None
    app_name: Optional[str] = None
    risk_level: str
    risk_score: float
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Backward compatible schema for agent data format
# Agent sends: {userId, appName, eventType, riskScore}
class AgentActivityCreate(BaseModel):
    """Schema for agent activity data - backward compatible with existing agent."""
    userId: str
    appName: Optional[str] = None
    eventType: str
    riskScore: float
    
    model_config = ConfigDict(from_attributes=True)


class ActivityLogListResponse(BaseModel):
    """Schema for list of activity logs."""
    id: int
    agent_id: Optional[int] = None
    activity_type: str
    app_name: Optional[str] = None
    risk_level: str
    risk_score: float
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)
