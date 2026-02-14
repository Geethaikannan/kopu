# Backend Development TODO

## Phase 1: Project Structure & Configuration
- [ ] Update requirements.txt with PostgreSQL support and other deps
- [ ] Create .env.example file
- [ ] Create backend/app/core/config.py - Configuration management
- [ ] Create backend/app/core/security.py - JWT and API key utilities
- [ ] Create backend/app/core/database.py - Database setup

## Phase 2: Models (SQLAlchemy)
- [ ] Create backend/app/models/__init__.py
- [ ] Create backend/app/models/user.py
- [ ] Create backend/app/models/agent.py
- [ ] Create backend/app/models/activity_log.py
- [ ] Create backend/app/models/alert.py

## Phase 3: Schemas (Pydantic)
- [ ] Create backend/app/schemas/__init__.py
- [ ] Create backend/app/schemas/user.py
- [ ] Create backend/app/schemas/agent.py
- [ ] Create backend/app/schemas/activity_log.py
- [ ] Create backend/app/schemas/alert.py

## Phase 4: Services (Business Logic)
- [ ] Create backend/app/services/__init__.py
- [ ] Create backend/app/services/risk_service.py - Risk evaluation
- [ ] Create backend/app/services/alert_service.py - Alert generation
- [ ] Create backend/app/services/agent_service.py - Agent management

## Phase 5: Routes (API Endpoints)
- [ ] Create backend/app/routes/__init__.py
- [ ] Create backend/app/routes/auth.py - JWT authentication
- [ ] Create backend/app/routes/agents.py - Agent management
- [ ] Create backend/app/routes/activity.py - Activity logs
- [ ] Create backend/app/routes/alerts.py - Alert management

## Phase 6: Main Application
- [ ] Update backend/app/main.py to use modular structure
- [ ] Add startup event for table creation
- [ ] Ensure backward compatibility with /api/activity/log

## Phase 7: Integration Testing
- [ ] Test /api/activity/log endpoint with agent data format
- [ ] Test JWT authentication on admin routes
- [ ] Test API key validation for agents
- [ ] Verify PostgreSQL connection (if configured)
