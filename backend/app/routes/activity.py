# routes/activity.py
# Activity log routes

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user, get_api_key, get_optional_api_key
from app.models.user import User
from app.models.agent import Agent
from app.models.activity_log import ActivityLog
from app.schemas.activity_log import (
    ActivityLogCreate,
    ActivityLogResponse,
    AgentActivityCreate,
    ActivityLogListResponse
)
from app.services.risk_service import (
    evaluate_activity_risk,
    calculate_risk_level,
    get_risk_statistics
)
from app.services.alert_service import create_high_risk_alert

router = APIRouter(prefix="/api/activity", tags=["Activity"])


# ============== BACKWARD COMPATIBLE ENDPOINT FOR AGENTS ==============
@router.post("/log", status_code=status.HTTP_201_CREATED)
def log_activity_from_agent(
    activity_data: AgentActivityCreate,
    db: Session = Depends(get_db),
    api_key: Optional[str] = Depends(get_optional_api_key)
):
    """
    BACKWARD COMPATIBLE: Receive activity from agent (uses API key auth).
    
    This endpoint accepts the original agent data format:
    {
        "userId": "string",
        "appName": "string",
        "eventType": "string", 
        "riskScore": float
    }
    
    Auto-creates agent if not exists (including API key auto-registration).
    """
    # Try to find agent by name first
    agent = db.query(Agent).filter(Agent.name == activity_data.userId).first()
    
    # If agent doesn't exist, create it automatically with optional API key
    if not agent:
        agent = Agent(
            name=activity_data.userId, 
            status="active",
            api_key=api_key if api_key else None
        )
        db.add(agent)
        db.commit()
        db.refresh(agent)
        print(f"Auto-created new agent: {activity_data.userId}")
    else:
        # Update API key if provided and agent doesn't have one
        if api_key and not agent.api_key:
            agent.api_key = api_key
            db.commit()
    
    # Update agent's last_seen
    agent.update_last_seen()
    db.commit()

    
    # Calculate risk level from score
    risk_level = calculate_risk_level(activity_data.riskScore)
    
    # Create activity log
    activity = ActivityLog(
        agent_id=agent.id,
        user_id=activity_data.userId,
        activity_type=activity_data.eventType,
        app_name=activity_data.appName,
        risk_score=activity_data.riskScore,
        risk_level=risk_level,
        description=f"Activity in {activity_data.appName}" if activity_data.appName else None
    )
    
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    # Evaluate risk and create alert if needed
    risk_evaluation = evaluate_activity_risk(activity_data, db)
    
    if risk_evaluation["should_alert"]:
        create_high_risk_alert(db, activity, activity_data.riskScore)
    
    return {
        "message": "Activity logged successfully",
        "activity_id": activity.id,
        "risk_level": risk_level
    }


# ============== ADMIN ROUTES (JWT AUTH REQUIRED) ==============

@router.post("/", response_model=ActivityLogResponse, status_code=status.HTTP_201_CREATED)
def create_activity_log(
    activity: ActivityLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new activity log (admin only).
    """
    new_activity = ActivityLog(**activity.dict())
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity


@router.get("/", response_model=List[ActivityLogListResponse])
def get_activity_logs(
    skip: int = 0,
    limit: int = 100,
    risk_level: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get activity logs (admin only).
    """
    query = db.query(ActivityLog)
    
    if risk_level:
        query = query.filter(ActivityLog.risk_level == risk_level)
    
    activities = query.order_by(ActivityLog.timestamp.desc()).offset(skip).limit(limit).all()
    return activities


@router.get("/stats")
def get_activity_statistics(
    hours: int = 24,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get activity statistics (admin only).
    """
    return get_risk_statistics(db, hours)


@router.get("/{activity_id}", response_model=ActivityLogResponse)
def get_activity_log(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific activity log (admin only).
    """
    activity = db.query(ActivityLog).filter(ActivityLog.id == activity_id).first()
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    return activity
