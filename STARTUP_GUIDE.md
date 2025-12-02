# Infinite AI Security Platform

> Enterprise AI Security Platform with multi-agent intelligence and labyrinth defense mechanism

## 🚀 Quick Start

### 1. Setup Environment
```bash
bash setup_env.sh
```

This will create a `.env` file with default values if it doesn't exist.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Application
```bash
bash start_app.sh
# OR
python start_server.py
# OR
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the Application
- **API Root**: `http://localhost:8000/api/v1/`
- **Health Check**: `http://localhost:8000/api/health`
- **API Documentation**: `http://localhost:8000/api/docs`
- **ReDoc Documentation**: `http://localhost:8000/api/redoc`

## 🔐 Environment Variables

The following environment variables are required:

- `API_SECRET_KEY` - Secret key for API authentication
- `JWT_SECRET_KEY` - Secret key for JWT tokens
- `API_DEBUG` - Enable/disable debug mode (true/false)
- `API_HOST` - Host to bind to (default: 0.0.0.0)
- `API_PORT` - Port to run on (default: 8000)

## 🏗️ Architecture

### API Structure
```
api/
├── main.py          # Main FastAPI application
├── routers/         # API route modules
│   ├── users.py     # User management
│   ├── security.py  # Security analysis
│   ├── monitoring.py # Health and metrics
│   └── ...
├── schemas/         # Pydantic schemas
├── dependencies/    # FastAPI dependencies
└── ...
```

### Core Components
- **Multi-tenant Architecture**: Isolated data per organization
- **Security Engine**: Advanced threat detection and prevention
- **Subscription Management**: Tier-based features and limits
- **Monitoring & Observability**: Comprehensive metrics and logging
- **Rate Limiting**: Tier-based request limiting

## 🌐 API Endpoints

### Security Analysis
- `POST /api/v1/security/analyze` - Analyze content for security threats
- `POST /api/v1/security/detect-threats` - Bulk threat detection

### User Management
- `GET /api/v1/users` - List users in organization
- `POST /api/v1/users` - Create new user

### Organization & Subscription
- `GET /api/v1/organizations` - Manage organizations
- `GET /api/v1/usage` - Track usage metrics

## 🛡️ Security Features

- **Prompt Injection Detection**
- **Jailbreak Attempt Prevention** 
- **Malicious Code Detection**
- **Sensitive Data Protection**
- **Multi-Agent Orchestration**
- **Labyrinth Defense Mechanism**

## 📊 Monitoring

- **Health Check**: `/api/health`
- **Metrics**: `/api/metrics`
- **Agent Health**: `/api/agents`
- **Threat Monitoring**: `/api/threats`

## 🔧 Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
isort .
```

### Running in Development Mode
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload --debug
```

## 🚀 Production Deployment

For production, make sure to:
1. Set strong values for `API_SECRET_KEY` and `JWT_SECRET_KEY`
2. Configure a production database
3. Set `API_DEBUG=false`
4. Use a process manager like Gunicorn:

```bash
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📄 License

MIT License - See LICENSE file for details.