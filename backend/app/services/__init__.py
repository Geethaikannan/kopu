# services/__init__.py
# Services module initialization

from app.services.risk_service import (
    calculate_risk_level,
    evaluate_activity_risk,
    get_recent_high_risk_activities,
    get_risk_statistics,
)
from app.services.alert_service import (
    create_alert,
    create_high_risk_alert,
    get_active_alerts,
    get_all_alerts,
    resolve_alert,
    get_alert_statistics,
    ALERT_TYPES,
)

__all__ = [
    # Risk service
    "calculate_risk_level",
    "evaluate_activity_risk",
    "get_recent_high_risk_activities",
    "get_risk_statistics",
    # Alert service
    "create_alert",
    "create_high_risk_alert",
    "get_active_alerts",
    "get_all_alerts",
    "resolve_alert",
    "get_alert_statistics",
    "ALERT_TYPES",
]
