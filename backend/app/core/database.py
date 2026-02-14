# core/database.py
# Database configuration and session management

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings, is_postgresql

# Create engine based on database URL
connect_args = {}
if not is_postgresql():
    # SQLite needs check_same_thread=False
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Database dependency for FastAPI.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables.
    Called on application startup.
    """
    # Import all models to ensure they are registered
    from app.models import user, agent, activity_log, alert
    Base.metadata.create_all(bind=engine)


def init_default_data():
    """
    Initialize default data.
    Called after database tables are created.
    """
    from app.models.user import User
    from app.models.agent import Agent
    from app.models.activity_log import ActivityLog
    from app.models.alert import Alert
    from app.core.security import get_password_hash
    from datetime import datetime, timedelta
    import random
    
    db = SessionLocal()
    try:
        # Create default admin user if not exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@local.local",
                password=get_password_hash("admin123"),
                role="admin"
            )
            db.add(admin)
            print("Created default admin user (admin/admin123)")
        
        # Create default agent if not exists
        default_agent = db.query(Agent).filter(Agent.name == "default-agent").first()
        if not default_agent:
            default_agent = Agent(
                name="default-agent",
                api_key="agent-key-001",
                status="active"
            )
            db.add(default_agent)
            print("Created default agent with API key: agent-key-001")
        
        db.commit()
        
        # Create sample activity logs for demo purposes
        agent = db.query(Agent).filter(Agent.name == "default-agent").first()
        if agent:
            # Check if we already have sample data
            existing_logs = db.query(ActivityLog).count()
            if existing_logs < 5:
                sample_activities = [
                    ("chrome.exe", "Browser Activity", "User accessed work portal", "low", 15.5),
                    ("chrome.exe", "Browser Activity", "Visited social media site", "medium", 45.2),
                    ("notepad.exe", "Application Usage", "Created new document", "low", 5.0),
                    ("chrome.exe", "Browser Activity", "Accessed banking website", "high", 78.5),
                    ("chrome.exe", "Browser Activity", "Searched for job opportunities", "medium", 52.3),
                    ("outlook.exe", "Email Activity", "Sent email to external domain", "medium", 48.7),
                    ("chrome.exe", "Browser Activity", "Downloaded file from unknown source", "high", 85.0),
                    ("teams.exe", "Application Usage", "Video call with team", "low", 12.0),
                    ("chrome.exe", "Browser Activity", "Accessed cloud storage", "low", 22.4),
                    ("cmd.exe", "System Activity", "Command prompt opened", "high", 72.8),
                ]
                
                for i, (app, activity_type, desc, risk_level, risk_score) in enumerate(sample_activities):
                    # Create timestamps spread over last 24 hours
                    timestamp = datetime.utcnow() - timedelta(hours=random.randint(1, 24), minutes=random.randint(0, 59))
                    
                    log = ActivityLog(
                        agent_id=agent.id,
                        user_id="user-001",
                        activity_type=activity_type,
                        description=desc,
                        app_name=app,
                        risk_level=risk_level,
                        risk_score=risk_score,
                        timestamp=timestamp
                    )
                    db.add(log)
                
                print(f"Created {len(sample_activities)} sample activity logs")
        
        # Create sample alerts for demo purposes
        existing_alerts = db.query(Alert).count()
        if existing_alerts < 3:
            sample_alerts = [
                ("suspicious_activity", "High risk activity detected on workstation", "high", False),
                ("agent_offline", "Agent connection lost temporarily", "medium", True),
                ("data_exfiltration", "Large file upload detected", "critical", False),
                ("unauthorized_access", "After hours login attempt", "medium", False),
                ("malware_detected", "Suspicious process execution blocked", "critical", True),
            ]
            
            for alert_type, message, severity, is_resolved in sample_alerts:
                # Random timestamp within last 48 hours
                created_at = datetime.utcnow() - timedelta(hours=random.randint(1, 48))
                resolved_at = created_at + timedelta(minutes=random.randint(5, 30)) if is_resolved else None
                
                alert = Alert(
                    agent_id=agent.id if agent else None,
                    user_id=admin.id if admin else None,
                    alert_type=alert_type,
                    message=message,
                    severity=severity,
                    is_resolved=is_resolved,
                    resolved_at=resolved_at,
                    created_at=created_at
                )
                db.add(alert)
            
            print(f"Created {len(sample_alerts)} sample alerts")
        
        db.commit()
        print("Sample data initialization complete!")
        
    except Exception as e:
        print(f"Error initializing default data: {e}")
        db.rollback()
    finally:
        db.close()
