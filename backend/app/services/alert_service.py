# services/alert_service.py
# Alert generation service

from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.models.activity_log import ActivityLog
from datetime import datetime, timedelta
from typing import List, Optional


# Alert types
ALERT_TYPES = {
    "HIGH_RISK": "high_risk",
    "SUSPICIOUS_ACTIVITY": "suspicious_activity",
    "AGENT_OFFLINE": "agent_offline",
    "MULTIPLE_FAILED_LOGINS": "multiple_failed_logins",
    "CRITICAL_KEYWORD": "critical_keyword",
}


def create_alert(
    db: Session,
    alert_type: str,
    message: str,
    severity: str = "medium",
    agent_id: Optional[int] = None,
    user_id: Optional[int] = None
) -> Alert:
    """
    Create a new alert.
    
    Args:
        db: Database session
        alert_type: Type of alert
        message: Alert message
        severity: Alert severity (low, medium, high, critical)
        agent_id: Optional agent ID
        user_id: Optional user ID
        
    Returns:
        Created Alert object
    """
    alert = Alert(
        alert_type=alert_type,
        message=message,
        severity=severity,
        agent_id=agent_id,
        user_id=user_id
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def create_high_risk_alert(
    db: Session,
    activity: ActivityLog,
    risk_score: float
) -> Optional[Alert]:
    """
    Create an alert for high-risk activity.
    
    Args:
        db: Database session
        activity: The activity log that triggered the alert
        risk_score: The risk score that triggered the alert
        
    Returns:
        Created Alert object or None
    """
    severity = "critical" if risk_score >= 8.0 else "high"
    
    message = (
        f"High-risk activity detected: {activity.activity_type} "
        f"(Risk Score: {risk_score}, Level: {activity.risk_level})"
    )
    
    return create_alert(
        db=db,
        alert_type=ALERT_TYPES["HIGH_RISK"],
        message=message,
        severity=severity,
        agent_id=activity.agent_id
    )


def get_active_alerts(
    db: Session,
    severity: Optional[str] = None,
    limit: int = 100
) -> List[Alert]:
    """
    Get active (unresolved) alerts.
    
    Args:
        db: Database session
        severity: Optional filter by severity
        limit: Maximum number of alerts to return
        
    Returns:
        List of active alerts
    """
    query = db.query(Alert).filter(Alert.is_resolved == False)
    
    if severity:
        query = query.filter(Alert.severity == severity)
    
    return query.order_by(Alert.created_at.desc()).limit(limit).all()


def get_all_alerts(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    is_resolved: Optional[bool] = None,
    severity: Optional[str] = None
) -> List[Alert]:
    """
    Get all alerts with optional filters.
    
    Args:
        db: Database session
        skip: Number of alerts to skip
        limit: Maximum number of alerts to return
        is_resolved: Filter by resolved status
        severity: Filter by severity
        
    Returns:
        List of alerts
    """
    query = db.query(Alert)
    
    if is_resolved is not None:
        query = query.filter(Alert.is_resolved == is_resolved)
    
    if severity:
        query = query.filter(Alert.severity == severity)
    
    return query.order_by(Alert.created_at.desc()).offset(skip).limit(limit).all()


def resolve_alert(db: Session, alert_id: int) -> Optional[Alert]:
    """
    Resolve an alert.
    
    Args:
        db: Database session
        alert_id: ID of the alert to resolve
        
    Returns:
        Updated Alert object or None if not found
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.resolve()
        db.commit()
        db.refresh(alert)
    return alert


def get_alert_statistics(db: Session) -> dict:
    """
    Get alert statistics.
    
    Args:
        db: Database session
        
    Returns:
        Dictionary with alert statistics
    """
    total = db.query(Alert).count()
    active = db.query(Alert).filter(Alert.is_resolved == False).count()
    resolved = db.query(Alert).filter(Alert.is_resolved == True).count()
    
    critical = db.query(Alert).filter(
        Alert.severity == "critical",
        Alert.is_resolved == False
    ).count()
    
    high = db.query(Alert).filter(
        Alert.severity == "high",
        Alert.is_resolved == False
    ).count()
    
    return {
        "total": total,
        "active": active,
        "resolved": resolved,
        "by_severity": {
            "critical": critical,
            "high": high
        }
    }
