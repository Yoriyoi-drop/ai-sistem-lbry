# 🚀 INFINITE AI SECURITY - FULL STACK RUN GUIDE

Congratulations! The project is now fully implemented with both Frontend and Backend components.

---

## 🏗️ Architecture Overview

- **Frontend:** React + TypeScript + Vite (Port 5173)
- **Backend:** FastAPI + Python 3.11 (Port 8000)
- **Database:** PostgreSQL
- **Cache/Queue:** Redis + Celery

---

## 🛠️ Setup Instructions

### 1. Backend Setup

**Prerequisites:**
- Python 3.10+
- PostgreSQL (running locally or via Docker)
- Redis (running locally or via Docker)

**Steps:**
```bash
# 1. Navigate to project root
cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security

# 2. Create Virtual Environment (if not exists)
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Dependencies
pip install -r apps/api/requirements.txt

# 4. Configure Environment
# Make sure your .env file has the correct DATABASE_URL
# Example: postgresql://postgres:password@localhost/infinite_ai_security

# 5. Run Migrations (Initialize Database)
cd apps/api
alembic upgrade head
cd ../..

# 6. Start Backend Server
./START_BACKEND.sh
```

### 2. Frontend Setup

**Prerequisites:**
- Node.js 18+

**Steps:**
```bash
# 1. Open a NEW terminal
cd apps/dashboard

# 2. Install Dependencies
npm install

# 3. Configure Environment
# Edit .env to switch between Mock API and Real API
# VITE_USE_MOCK_API=false  <-- Set to false to use real backend

# 4. Start Frontend Server
npm run dev
```

---

## 🧪 Testing the Integration

1.  **Start Backend:** Ensure `./START_BACKEND.sh` is running on port 8000.
2.  **Start Frontend:** Ensure `npm run dev` is running on port 5173.
3.  **Open Browser:** Go to `http://localhost:5173`.
4.  **Register:** Create a new account. This will now hit the real FastAPI endpoint `/api/v1/auth/register`.
5.  **Login:** Log in with your new credentials.
6.  **Explore:** Navigate to Agents, Security, Scans pages.

---

## 🐛 Troubleshooting

-   **Database Connection Error:** Check `DATABASE_URL` in `.env` and ensure PostgreSQL is running.
-   **CORS Error:** Check `BACKEND_CORS_ORIGINS` in `apps/api/src/config/settings.py`.
-   **Import Errors:** Ensure you are running scripts from the project root and `PYTHONPATH` is set correctly (handled by `START_BACKEND.sh`).

---

## 📝 API Documentation

Once the backend is running, you can access the interactive API docs at:
**http://localhost:8000/docs**

---

**Enjoy building with Infinite AI Security!** 🛡️
