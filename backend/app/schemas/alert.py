# schemas/alert.py
# Pydantic schemas for Alert

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class AlertBase(BaseModel):
    """Base alert schema with common fields."""
    alert_type: str
    message: str
    severity: str = "medium"


class AlertCreate(AlertBase):
    """Schema for creating a new alert."""
    agent_id: Optional[int] = None
    user_id: Optional[int] = None


class AlertUpdate(BaseModel):
    """Schema for updating an alert."""
    is_resolved: Optional[bool] = None
    severity: Optional[str] = None
    message: Optional[str] = None


class AlertResponse(AlertBase):
    """Schema for alert response."""
    id: int
    agent_id: Optional[int] = None
    user_id: Optional[int] = None
    is_resolved: bool
    resolved_at: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AlertListResponse(BaseModel):
    """Schema for list of alerts."""
    id: int
    alert_type: str
    message: str
    severity: str
    is_resolved: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
