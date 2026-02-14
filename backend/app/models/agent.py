# models/agent.py
# Agent model for PC monitoring agents

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    api_key = Column(String, unique=True, index=True, nullable=True)
    status = Column(String, default="active")
    last_seen = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    activity_logs = relationship("ActivityLog", back_populates="agent")
    alerts = relationship("Alert", back_populates="agent")
    
    def __repr__(self):
        return f"<Agent(id={self.id}, name='{self.name}', status='{self.status}')>"
    
    def update_last_seen(self):
        """Update the last_seen timestamp to current time."""
        self.last_seen = datetime.utcnow()
