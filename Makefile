# Makefile for Infinite AI Security Platform
# Simplifies common development tasks

.PHONY: help up down build test lint clean logs shell db-migrate db-reset install-dev

# Default target
help:
	@echo "🚀 Infinite AI Security - Development Commands"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make up          - Start all services"
	@echo "  make down        - Stop all services"
	@echo "  make build       - Build all Docker images"
	@echo "  make logs        - Show logs from all services"
	@echo "  make clean       - Remove all containers and volumes"
	@echo ""
	@echo "Development Commands:"
	@echo "  make install-dev - Install development dependencies"
	@echo "  make test        - Run all tests"
	@echo "  make lint        - Run linters (Python, Go, Rust)"
	@echo "  make format      - Auto-format code"
	@echo ""
	@echo "Database Commands:"
	@echo "  make db-migrate  - Run database migrations"
	@echo "  make db-reset    - Reset database (WARNING: deletes data)"
	@echo "  make db-shell    - Open PostgreSQL shell"
	@echo ""
	@echo "Service Commands:"
	@echo "  make shell-api   - Shell into API Gateway container"
	@echo "  make shell-hub   - Shell into AI Hub container"
	@echo ""

# Docker Commands
up:
	@echo "🚀 Starting all services..."
	cd infrastructure/docker && docker-compose -p aisec_v8 up -d

down:
	@echo "🛑 Stopping all services..."
	cd infrastructure/docker && docker-compose -p aisec_v8 down

build:
	@echo "🔨 Building all Docker images..."
	cd infrastructure/docker && docker-compose -p aisec_v8 build

logs:
	@echo "📋 Showing logs..."
	cd infrastructure/docker && docker-compose -p aisec_v8 logs -f

clean:
	@echo "🧹 Cleaning up containers and volumes..."
	cd infrastructure/docker && docker-compose -p aisec_v8 down -v
	docker system prune -f

# Development Commands
install-dev:
	@echo "📦 Installing development dependencies..."
	pip install -r requirements-dev.txt
	cd services/api-gateway && pip install -r requirements.txt
	cd services/ai-hub && pip install -r requirements.txt
	cd frontend && npm install

test:
	@echo "🧪 Running tests..."
	pytest tests/ -v --cov=services --cov-report=html --cov-report=term

test-unit:
	@echo "🧪 Running unit tests..."
	pytest tests/unit/ -v

test-integration:
	@echo "🧪 Running integration tests..."
	pytest tests/integration/ -v

lint:
	@echo "🔍 Running linters..."
	@echo "Python (flake8)..."
	flake8 services/api-gateway services/ai-hub security/
	@echo "Python (mypy)..."
	mypy services/api-gateway services/ai-hub --ignore-missing-imports
	@echo "Go (golangci-lint)..."
	cd services/scanner-go && golangci-lint run || echo "⚠️  Go linter not installed"
	@echo "Rust (clippy)..."
	cd services/labyrinth-rust && cargo clippy || echo "⚠️  Rust clippy not installed"

format:
	@echo "✨ Formatting code..."
	black services/api-gateway services/ai-hub security/
	isort services/api-gateway services/ai-hub security/
	cd services/scanner-go && go fmt ./... || true
	cd services/labyrinth-rust && cargo fmt || true

# Database Commands
db-migrate:
	@echo "🗄️  Running database migrations..."
	cd services/api-gateway && alembic upgrade head

db-reset:
	@echo "⚠️  Resetting database (this will delete all data)..."
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		cd infrastructure/docker && docker-compose -p aisec_v8 exec postgres psql -U admin -d ai_security -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"; \
		cd services/api-gateway && alembic upgrade head; \
		echo "✅ Database reset complete"; \
	fi

db-shell:
	@echo "🗄️  Opening PostgreSQL shell..."
	cd infrastructure/docker && docker-compose -p aisec_v8 exec postgres psql -U admin -d ai_security

# Service Shell Commands
shell-api:
	@echo "🐚 Opening shell in API Gateway..."
	cd infrastructure/docker && docker-compose -p aisec_v8 exec api-gateway /bin/bash

shell-hub:
	@echo "🐚 Opening shell in AI Hub..."
	cd infrastructure/docker && docker-compose -p aisec_v8 exec ai-hub /bin/bash

# Quick start for new developers
quickstart:
	@echo "🚀 Quick Start - Setting up development environment..."
	@echo "1️⃣  Copying .env.example to .env..."
	cp .env.example .env
	@echo "2️⃣  Building Docker images..."
	$(MAKE) build
	@echo "3️⃣  Starting services..."
	$(MAKE) up
	@echo "4️⃣  Running migrations..."
	sleep 5
	$(MAKE) db-migrate
	@echo ""
	@echo "✅ Setup complete! Services running at:"
	@echo "   API Gateway: http://localhost:8030"
	@echo "   AI Hub:      http://localhost:8031"
	@echo "   Grafana:     http://localhost:3000"
	@echo "   Prometheus:  http://localhost:9090"

# Health check
health:
	@echo "🏥 Checking service health..."
	@curl -s http://localhost:8040/ | jq . || echo "❌ API Gateway not responding"
	@curl -s http://localhost:8041/ | jq . || echo "❌ AI Hub not responding"
	@curl -s http://localhost:9090/-/healthy || echo "❌ Prometheus not responding"
