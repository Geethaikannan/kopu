# services/risk_service.py
# Risk evaluation service

from sqlalchemy.orm import Session
from app.models.activity_log import ActivityLog
from app.models.alert import Alert
from app.schemas.activity_log import AgentActivityCreate
from datetime import datetime
from typing import Optional


# Risk thresholds
RISK_LEVELS = {
    "low": 0.0,
    "medium": 3.0,
    "high": 6.0,
    "critical": 8.0,
}

# Suspicious keywords for additional risk assessment
SUSPICIOUS_KEYWORDS = [
    "hack",
    "password",
    "admin",
    "cheat",
    "malware",
    "virus",
    "trojan",
    "keylogger",
    "credential",
    "breach",
]


def calculate_risk_level(risk_score: float) -> str:
    """
    Calculate risk level based on risk score.
    
    Args:
        risk_score: Numeric risk score (0-10)
        
    Returns:
        Risk level string: low, medium, high, critical
    """
    if risk_score >= RISK_LEVELS["critical"]:
        return "critical"
    elif risk_score >= RISK_LEVELS["high"]:
        return "high"
    elif risk_score >= RISK_LEVELS["medium"]:
        return "medium"
    else:
        return "low"


def evaluate_activity_risk(
    activity_data: AgentActivityCreate,
    db: Session
) -> dict:
    """
    Evaluate risk for an activity and create alert if needed.
    
    Args:
        activity_data: Activity data from agent
        db: Database session
        
    Returns:
        Dictionary with risk evaluation results
    """
    risk_score = activity_data.riskScore
    risk_level = calculate_risk_level(risk_score)
    
    # Check for high-risk activities
    should_alert = risk_level in ["high", "critical"]
    
    result = {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "should_alert": should_alert,
        "alert_message": None
    }
    
    if should_alert:
        if risk_level == "critical":
            result["alert_message"] = f"CRITICAL: High risk activity detected - Score: {risk_score}"
        else:
            result["alert_message"] = f"HIGH: Elevated risk activity detected - Score: {risk_score}"
    
    return result


def get_recent_high_risk_activities(db: Session, hours: int = 24) -> list:
    """
    Get recent high-risk activities within specified hours.
    
    Args:
        db: Database session
        hours: Number of hours to look back
        
    Returns:
        List of high-risk activities
    """
    from datetime import timedelta
    
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    activities = db.query(ActivityLog).filter(
        ActivityLog.timestamp >= cutoff_time,
        ActivityLog.risk_level.in_(["high", "critical"])
    ).all()
    
    return activities


def get_risk_statistics(db: Session, hours: int = 24) -> dict:
    """
    Get risk statistics for the specified time period.
    
    Args:
        db: Database session
        hours: Number of hours to look back
        
    Returns:
        Dictionary with risk statistics
    """
    from datetime import timedelta
    
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    
    total = db.query(ActivityLog).filter(
        ActivityLog.timestamp >= cutoff_time
    ).count()
    
    low = db.query(ActivityLog).filter(
        ActivityLog.timestamp >= cutoff_time,
        ActivityLog.risk_level == "low"
    ).count()
    
    medium = db.query(ActivityLog).filter(
        ActivityLog.timestamp >= cutoff_time,
        ActivityLog.risk_level == "medium"
    ).count()
    
    high = db.query(ActivityLog).filter(
        ActivityLog.timestamp >= cutoff_time,
        ActivityLog.risk_level == "high"
    ).count()
    
    critical = db.query(ActivityLog).filter(
        ActivityLog.timestamp >= cutoff_time,
        ActivityLog.risk_level == "critical"
    ).count()
    
    avg_risk_score = db.query(ActivityLog).filter(
        ActivityLog.timestamp >= cutoff_time
    ).with_entities(ActivityLog.risk_score).all()
    
    avg_score = 0.0
    if avg_risk_score:
        scores = [s[0] for s in avg_risk_score]
        avg_score = sum(scores) / len(scores) if scores else 0.0
    
    return {
        "total_activities": total,
        "risk_distribution": {
            "low": low,
            "medium": medium,
            "high": high,
            "critical": critical,
        },
        "average_risk_score": round(avg_score, 2),
        "period_hours": hours
    }
