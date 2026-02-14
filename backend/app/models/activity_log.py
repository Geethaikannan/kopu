# models/activity_log.py
# ActivityLog model for storing PC activity data

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    user_id = Column(String, nullable=True)  # For backward compatibility with agent
    activity_type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    app_name = Column(String, nullable=True)  # From agent
    risk_level = Column(String, default="low")  # low, medium, high, critical
    risk_score = Column(Float, default=0.0)  # Numeric risk score from agent
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    agent = relationship("Agent", back_populates="activity_logs")
    
    def __repr__(self):
        return f"<ActivityLog(id={self.id}, type='{self.activity_type}', risk='{self.risk_level}')>"
    
    @property
    def is_suspicious(self) -> bool:
        """Check if this activity is suspicious based on risk level."""
        return self.risk_level in ["high", "critical"]
