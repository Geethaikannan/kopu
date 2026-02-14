# schemas/__init__.py
# Schemas module initialization

from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    TokenData,
)
from app.schemas.agent import (
    AgentBase,
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentListResponse,
)
from app.schemas.activity_log import (
    ActivityLogBase,
    ActivityLogCreate,
    ActivityLogResponse,
    AgentActivityCreate,
    ActivityLogListResponse,
)
from app.schemas.alert import (
    AlertBase,
    AlertCreate,
    AlertUpdate,
    AlertResponse,
    AlertListResponse,
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData",
    # Agent schemas
    "AgentBase",
    "AgentCreate",
    "AgentUpdate",
    "AgentResponse",
    "AgentListResponse",
    # Activity log schemas
    "ActivityLogBase",
    "ActivityLogCreate",
    "ActivityLogResponse",
    "AgentActivityCreate",
    "ActivityLogListResponse",
    # Alert schemas
    "AlertBase",
    "AlertCreate",
    "AlertUpdate",
    "AlertResponse",
    "AlertListResponse",
]
