# routes/__init__.py
# Routes module initialization

from app.routes.auth import router as auth_router
from app.routes.agents import router as agents_router
from app.routes.activity import router as activity_router
from app.routes.alerts import router as alerts_router

__all__ = [
    "auth_router",
    "agents_router",
    "activity_router",
    "alerts_router",
]
