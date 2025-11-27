# 🎯 FOUNDATION PHASE - ACTION PLAN (Week 1-2)

## 📊 Overview
- **Current Progress:** 15-20%
- **Target Progress:** 40%
- **Duration:** 2 weeks
- **Focus:** Foundation components

---

## 🗓️ WEEK 1: INFRASTRUCTURE & DATABASE

### 🎯 Day 1-2: Project Setup & Environment
**Goal:** Basic project structure and configuration management

#### Tasks:
- [ ] **Create proper .gitignore** (Python, Go, Rust, Node.js, IDE)
- [ ] **Setup .env.example** with all required environment variables
- [ ] **Create configuration management system** for Python, Go, Rust, Node.js
- [ ] **Setup Docker base images** for all services
- [ ] **Initialize database schema** (SQLAlchemy models)

#### Deliverables:
- `.gitignore` with all relevant patterns
- `.env.example` with all required variables
- `config.py` for Python services
- `config.go` for Go services
- `config.rs` for Rust services
- `config.js` for Node.js services

---

### 🎯 Day 3-4: Database Design & Implementation
**Goal:** Complete database schema with migrations

#### Tasks:
- [ ] **Design database schema** (ERD + tables)
- [ ] **Create SQLAlchemy models** for all entities
- [ ] **Setup Alembic for migrations** 
- [ ] **Create seed data** for development
- [ ] **Setup database connection pool**
- [ ] **Create repository pattern** for data access

#### Database Entities to Create:
1. **Users** - Authentication & authorization
2. **Agents** - AI agents metadata
3. **Workflows** - 200 nodes workflow definitions
4. **Sessions** - User sessions & tokens
5. **Audit Logs** - Security logs
6. **Subscriptions** - Pricing & billing
7. **Scans** - Security scan results
8. **Incidents** - Security incidents
9. **Agents Status** - Agent health & status

---

### 🎯 Day 5: Docker & Deployment Setup
**Goal:** Working Docker Compose for local development

#### Tasks:
- [ ] **Create Dockerfile for API service**
- [ ] **Create Dockerfile for Dashboard**
- [ ] **Create Dockerfile for Scanner (Go)**
- [ ] **Create Dockerfile for Labyrinth (Rust)**
- [ ] **Setup docker-compose.yml** with all services
- [ ] **Configure network connections** between services
- [ ] **Setup volumes** for data persistence

---

## 🗓️ WEEK 2: AUTHENTICATION & CORE API

### 🎯 Day 6-7: Authentication System
**Goal:** Complete JWT-based authentication

#### Tasks:
- [ ] **Implement JWT token generation** (access & refresh tokens)
- [ ] **Create user registration/login API**
- [ ] **Implement JWT middleware** with proper validation
- [ ] **Create role-based access control (RBAC)**
- [ ] **Implement password hashing** (bcrypt)
- [ ] **Create user profile management**
- [ ] **Implement logout & token blacklist**
- [ ] **Add 2FA support** (optional for MVP)

#### Security Features:
- Password complexity validation
- Rate limiting for auth endpoints
- Session management
- JWT refresh mechanism
- Token expiration handling

---

### 🎯 Day 8-9: Core API Implementation
**Goal:** Basic API with authentication and key endpoints

#### Tasks:
- [ ] **Create FastAPI application** with proper structure
- [ ] **Implement API routes** for authentication
- [ ] **Create Pydantic schemas** for request/response validation
- [ ] **Implement error handling** middleware
- [ ] **Create API documentation** (OpenAPI/Swagger)
- [ ] **Add CORS configuration**
- [ ] **Implement logging middleware**
- [ ] **Add request/response validation**

#### Key API Endpoints:
```
POST   /auth/register     - User registration
POST   /auth/login        - User login
POST   /auth/refresh      - Token refresh
GET    /auth/profile      - Get user profile
PUT    /auth/profile      - Update user profile
GET    /agents/           - List all agents
POST   /agents/run        - Run AI agents
GET    /workflows/        - List workflows
GET    /dashboard/stats   - Dashboard statistics
POST   /scan/code         - Submit code for scanning
GET    /scan/results      - Get scan results
```

---

### 🎯 Day 10-11: Testing Setup
**Goal:** Basic testing infrastructure

#### Tasks:
- [ ] **Setup pytest configuration**
- [ ] **Create database fixtures** for testing
- [ ] **Implement unit tests** for authentication
- [ ] **Create API integration tests**
- [ ] **Setup test coverage reporting**
- [ ] **Create CI pipeline** basic configuration

---

## 🎯 WEEK 2 SUMMARY: 40% TARGET ACHIEVED

### ✅ By End of Week 2, You'll Have:
1. **Complete database schema** with migrations
2. **Working authentication system** (JWT)
3. **Functional API Gateway** with key endpoints
4. **Docker Compose setup** for local development
5. **Environment management** with proper configuration
6. **Basic testing infrastructure**
7. **API documentation** available

---

## 🏗️ TECHNICAL SPECIFICATIONS

### Database Schema (SQLAlchemy Models):
```python
# users.py
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default="user")  # user, admin, superadmin
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# agents.py
class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    status = Column(String, default="active")  # active, inactive, maintenance
    team = Column(String)  # A, B, C
    created_at = Column(DateTime, default=datetime.utcnow)
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
```

### Docker Compose Structure:
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: securityai
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build:
      context: .
      dockerfile: infrastructure/docker/api/Dockerfile
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/securityai
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    ports:
      - "8000:8000"

  dashboard:
    build:
      context: ./apps/dashboard
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - api

volumes:
  postgres_data:
```

---

## 📋 CHECKLIST FOR WEEK 1-2 COMPLETION

### Environment & Config:
- [ ] `.gitignore` created
- [ ] `.env.example` created with all variables
- [ ] Configuration management for all services
- [ ] Docker setup with multi-service compose

### Database:
- [ ] SQLAlchemy models created
- [ ] Alembic migrations configured
- [ ] Database connection pool setup
- [ ] Repository pattern implemented

### Authentication:
- [ ] JWT implementation
- [ ] User registration/login endpoints
- [ ] Authentication middleware
- [ ] RBAC system
- [ ] Password hashing

### API:
- [ ] FastAPI application structure
- [ ] Key endpoints implemented
- [ ] Pydantic schemas
- [ ] Error handling
- [ ] CORS configuration
- [ ] Logging middleware

### Testing:
- [ ] Pytest setup
- [ ] Basic unit tests
- [ ] API integration tests
- [ ] Coverage reporting

---

## 🚀 NEXT STEPS (Post Week 2)

After achieving 40% progress, the next phase will focus on:
1. **Week 3-4:** AI Hub core implementation
2. **Week 5-6:** Scanner and Labyrinth integration  
3. **Week 7-8:** Frontend implementation
4. **Week 9-10:** Advanced features and optimization

---

## 📈 PROGRESS TRACKING

**Week 1 Target:** 25% (Infrastructure & Database)
**Week 2 Target:** 40% (Auth & Core API)

**Milestones:**
- Day 2: Environment setup complete
- Day 4: Database schema complete
- Day 5: Docker compose working
- Day 7: Authentication system complete
- Day 9: Core API endpoints complete
- Day 11: Testing infrastructure complete

---

**Generated:** 2025-11-26
**Target:** 40% project completion
**Status:** 🚀 Ready to Execute