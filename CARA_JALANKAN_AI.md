# 🚀 PANDUAN LENGKAP MENJALANKAN AI

**Last Updated**: 2025-11-28  
**Status**: Ready to Deploy

---

## 📋 RINGKASAN SISTEM

Project **Infinite AI Security** adalah platform keamanan berbasis Multi-Agent AI dengan komponen:

### AI Agents:
- 🧠 **AI Hub** - Orchestrator utama (LangGraph)
- 🎯 **AstraMind** - Strategist
- 🔍 **SpectraLogic** - Analyzer
- ⚡ **ForgeRun** - Executor
- 🛡️ **GuardianOS** - Validator
- 💾 **ChronaCore** - Memory Manager
- 🌊 **NexaFlow** - Workflow Orchestrator

### Infrastructure:
- PostgreSQL (Database)
- Redis (Cache)
- n8n (Workflow Automation)
- Scanner (Go)
- Labyrinth Defense (Rust)

---

## 🎯 OPSI 1: DOCKER COMPOSE (RECOMMENDED)

### Langkah 1: Persiapan Environment

```bash
# Masuk ke direktori project
cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security

# Copy environment template
cp .env.example .env

# Edit .env dan tambahkan API keys (jika diperlukan)
nano .env
```

**Konfigurasi penting di `.env`:**
```bash
# AI Configuration
OPENAI_API_KEY=your_openai_key_here  # Jika menggunakan OpenAI
MODEL_NAME=Qwen/Qwen2.5-7B-Instruct
TEMPERATURE=0.3
MAX_TOKENS=2000

# Database
DATABASE_URL=postgresql://admin:admin@postgres:5432/ai_security

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Langkah 2: Start dengan Docker Compose (Clean Setup)

```bash
# Masuk ke direktori infrastructure/docker
cd infrastructure/docker

# Start services dengan konfigurasi final (Port 8200+)
docker-compose -f docker-compose-final.yml -p aisec_final up -d
```

### Langkah 3: Verifikasi Services

```bash
# Check status containers
docker-compose -f docker-compose-final.yml -p aisec_final ps

# Test API Gateway
curl http://localhost:8200/api/v1/health/

# Test AI Hub
curl http://localhost:8201/

# Check logs
docker-compose -f docker-compose-final.yml -p aisec_final logs ai-hub
```

### Langkah 4: Access Interfaces

- **API Gateway**: http://localhost:8200
- **API Gateway Docs**: http://localhost:8200/docs
- **AI Hub**: http://localhost:8201
- **AI Hub Docs**: http://localhost:8201/docs
- **Scanner**: http://localhost:8202
- **n8n Workflow**: http://localhost:8204 (user: admin, pass: admin)
- **PostgreSQL**: localhost:8205
- **Redis**: localhost:8206

---

## 🎯 OPSI 2: MANUAL START (Development)

Jika ingin menjalankan secara manual untuk development:

### Terminal 1 - PostgreSQL & Redis

```bash
# Start PostgreSQL
docker run -d --name postgres \
  -e POSTGRES_DB=ai_security \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -p 5432:5432 \
  postgres:15-alpine

# Start Redis
docker run -d --name redis \
  -p 6379:6379 \
  redis:7-alpine
```

### Terminal 2 - AI Hub

```bash
cd services/ai-hub

# Install dependencies
pip install -r requirements.txt

# Run AI Hub
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Terminal 3 - API Gateway

```bash
cd services/api-gateway

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Run API Gateway
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 4 - Scanner (Optional)

```bash
cd services/scanner-go

# Build and run
go run cmd/scanner/main.go
```

### Terminal 5 - Frontend Dashboard (Optional)

```bash
cd dashboard-react

# Install dependencies
npm install

# Start dev server
npm run dev
```

---

## 🎯 OPSI 3: OLLAMA LOCAL AI (Tanpa OpenAI)

Jika ingin menggunakan AI lokal dengan Ollama:

### Langkah 1: Start Ollama

```bash
# Start Ollama container
docker-compose up -d ollama

# Atau manual
docker run -d --name ollama \
  -p 11434:11434 \
  -v ollama_models:/root/.ollama \
  ollama/ollama:latest
```

### Langkah 2: Download Model

```bash
# Pull model Qwen
docker exec -it ollama ollama pull qwen2.5:7b

# Atau model lain
docker exec -it ollama ollama pull llama3.1:8b
docker exec -it ollama ollama pull mistral:7b
```

### Langkah 3: Configure Environment

Edit `.env`:
```bash
# Ganti dengan Ollama
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=qwen2.5:7b
USE_OLLAMA=true
```

### Langkah 4: Start Services

```bash
# Start dengan konfigurasi Ollama
docker-compose -f docker-compose.ollama.yml up -d
```

---

## 🔧 MANAGEMENT COMMANDS

### Menggunakan manage.sh

```bash
# Start semua services
./manage.sh start

# Stop semua services
./manage.sh stop

# Restart services
./manage.sh restart

# Check status
./manage.sh status

# View logs
./manage.sh logs              # All services
./manage.sh logs ai-hub       # Specific service

# Rebuild containers
./manage.sh build
```

### Docker Compose Manual

```bash
# Start services
docker-compose -p aisec_v4 up -d

# Stop services
docker-compose -p aisec_v4 down

# View logs
docker-compose -p aisec_v4 logs -f ai-hub

# Rebuild specific service
docker-compose -p aisec_v4 up -d --build ai-hub

# Scale services
docker-compose -p aisec_v4 up -d --scale ai-hub=3
```

---

## 🧪 TESTING AI

### Test AI Hub Endpoint

```bash
# Health check
curl http://localhost:9001/health

# Test graph building (200 nodes)
curl -X POST http://localhost:9001/api/v1/graph/build \
  -H "Content-Type: application/json" \
  -d '{"node_count": 200}'

# Test AI orchestration
curl -X POST http://localhost:9001/api/v1/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "analyze_security",
    "target": "example.com"
  }'
```

### Test dengan Python

```python
import requests

# Test AI Hub
response = requests.post(
    "http://localhost:9001/api/v1/orchestrate",
    json={
        "task": "security_scan",
        "target": "192.168.1.1"
    }
)
print(response.json())
```

---

## 🐛 TROUBLESHOOTING

### Docker Permission Denied

```bash
# Tambahkan user ke docker group
sudo usermod -aG docker $USER

# Logout dan login kembali, atau:
newgrp docker

# Test tanpa sudo
docker ps
```

### Port Already in Use

```bash
# Check port yang digunakan
sudo lsof -i :9000
sudo lsof -i :9001

# Kill process
sudo kill -9 <PID>

# Atau ubah port di docker-compose.yml
```

### Container Won't Start

```bash
# Check logs
docker-compose -p aisec_v4 logs ai-hub

# Restart specific service
docker-compose -p aisec_v4 restart ai-hub

# Remove and recreate
docker-compose -p aisec_v4 rm -f ai-hub
docker-compose -p aisec_v4 up -d ai-hub
```

### Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose -p aisec_v4 ps postgres

# Run migrations
cd services/api-gateway
alembic upgrade head

# Or recreate database
docker-compose -p aisec_v4 down -v
docker-compose -p aisec_v4 up -d
```

### AI Model Not Found (Ollama)

```bash
# List available models
docker exec -it ollama ollama list

# Pull model
docker exec -it ollama ollama pull qwen2.5:7b

# Test model
docker exec -it ollama ollama run qwen2.5:7b "Hello"
```

---

## 📊 MONITORING

### Check Service Health

```bash
# All services status
docker-compose -p aisec_v4 ps

# Resource usage
docker stats

# Logs real-time
docker-compose -p aisec_v4 logs -f
```

### Access Monitoring Tools

- **n8n Workflows**: http://localhost:9004
- **PostgreSQL**: Use pgAdmin or DBeaver on port 9005
- **Redis**: Use Redis Commander or redis-cli

```bash
# Redis CLI
docker exec -it redis redis-cli
> PING
> KEYS *
```

---

## 🚀 QUICK START COMMANDS

### Fastest Way to Start Everything:

```bash
# 1. Setup environment
cd /home/whale-d/Unduhan/backup/ai-p/infinite_ai_security
cp .env.example .env

# 2. Start all services
cd infrastructure/docker
docker-compose -p aisec_v4 up -d

# 3. Wait 30 seconds for services to initialize
sleep 30

# 4. Test
curl http://localhost:9001/health
```

### Stop Everything:

```bash
cd infrastructure/docker
docker-compose -p aisec_v4 down
```

---

## 📚 NEXT STEPS

Setelah AI berjalan:

1. **Configure AI Agents** - Edit konfigurasi di `ai_config.json`
2. **Setup Workflows** - Buat workflow di n8n (http://localhost:9004)
3. **Test Security Scans** - Jalankan security scan pertama
4. **Monitor Logs** - Pantau logs untuk memastikan AI berjalan dengan baik
5. **Scale Services** - Scale AI Hub jika diperlukan lebih banyak workers

---

## 🔗 DOKUMENTASI LANJUTAN

- **QUICK_START.md** - Quick start guide
- **DEPLOYMENT_GUIDE.md** - Deployment details
- **ARCHITECTURE.md** - System architecture
- **ROADMAP.md** - Development roadmap
- **API Documentation** - http://localhost:9001/docs

---

**Status**: ✅ Ready to Deploy  
**Last Tested**: 2025-11-28  
**Recommended**: Opsi 1 (Docker Compose)
