.PHONY: help install dev prod test clean db-migrate db-upgrade db-downgrade

# Infinite AI Security Platform - Makefile

# Default target
help:
	@echo "Infinite AI Security Platform - Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make install          Install dependencies"
	@echo "  make dev              Start development server"
	@echo "  make prod             Start production server"
	@echo "  make test             Run tests"
	@echo "  make clean            Clean temporary files"
	@echo "  make db-migrate       Create database migration"
	@echo "  make db-upgrade       Upgrade database to latest"
	@echo "  make db-downgrade     Downgrade database"
	@echo ""

# Install dependencies
install:
	pip install -r requirements.txt

# Start development server with auto-reload
dev:
	bash setup_env.sh
	python start_server.py

# Start production server (this would use gunicorn in real production)
prod:
	bash setup_env.sh
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4

# Run tests
test:
	pytest tests/ -v

# Clean temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name ".coverage" -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/

# Database management (these would work with alembic)
db-migrate:
	alembic revision --autogenerate

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

# Quick start command
start: dev