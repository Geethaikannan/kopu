# models/alert.py
# Alert model for security alerts

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    alert_type = Column(String, nullable=False)  # high_risk, suspicious_activity, agent_offline, etc.
    message = Column(String, nullable=False)
    severity = Column(String, default="medium")  # low, medium, high, critical
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    agent = relationship("Agent", back_populates="alerts")
    user = relationship("User", back_populates="alerts")
    
    def __repr__(self):
        return f"<Alert(id={self.id}, type='{self.alert_type}', severity='{self.severity}', resolved={self.is_resolved})>"
    
    def resolve(self):
        """Mark the alert as resolved."""
        self.is_resolved = True
        self.resolved_at = datetime.utcnow()
    
    @property
    def is_critical(self) -> bool:
        """Check if this alert is critical."""
        return self.severity == "critical" and not self.is_resolved
