# main.py
# Main FastAPI application for Backend API


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db, init_default_data

from app.routes import auth_router, agents_router, activity_router, alerts_router

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="PC Activity Monitoring & Alert System",
    version=settings.APP_VERSION
)

# CORS middleware
# Handle wildcard origin properly
if settings.CORS_ORIGINS == "*":
    origins = ["*"]
else:
    origins = settings.CORS_ORIGINS.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(auth_router)
app.include_router(agents_router)
app.include_router(activity_router)
app.include_router(alerts_router)


# Health check endpoint (no auth required)
@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {
        "message": "PC Activity Monitoring Backend is running",
        "version": settings.APP_VERSION,
        "status": "healthy"
    }


# Root endpoint
@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


# Create tables on startup
@app.on_event("startup")
def startup_event():
    """Initialize database tables on startup."""
    init_db()
    init_default_data()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
