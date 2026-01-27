.PHONY: help up down down-volumes migration migrate logs shell db-shell redis-cli clean

help:
	@echo "ScholarPASS Backend - Available Commands"
	@echo "========================================"
	@echo "make up                    - Start all services (db, redis, app)"
	@echo "make down                  - Stop all services"
	@echo "make down-volumes          - Stop services and remove volumes"
	@echo "make migration msg=\"...\"   - Create a new migration with message"
	@echo "make migrate               - Run pending migrations"
	@echo "make logs                  - View application logs"
	@echo "make shell                 - Open Python shell with app context"
	@echo "make db-shell              - Open PostgreSQL shell"
	@echo "make redis-cli             - Open Redis CLI"
	@echo "make clean                 - Remove containers, volumes, and cache"
	@echo "make build                 - Build Docker images"
	@echo "make test                  - Run tests"
	@echo "make lint                  - Run code linting"
	@echo "make format                - Format code with black"

# Docker Compose Commands
up:
	@echo "Starting ScholarPASS services..."
	docker-compose up -d
	@echo "Services started successfully!"
	@echo "API available at: http://localhost:8000"
	@echo "API docs at: http://localhost:8000/docs"

down:
	@echo "Stopping ScholarPASS services..."
	docker-compose down

down-volumes:
	@echo "Stopping services and removing volumes..."
	docker-compose down -v
	@echo "All services and volumes removed!"

build:
	@echo "Building Docker images..."
	docker-compose build

# Database Migration Commands
migration:
	@if [ -z "$(msg)" ]; then \
		echo "Error: Please provide a migration message"; \
		echo "Usage: make migration msg=\"your migration message\""; \
		exit 1; \
	fi
	@echo "Creating migration: $(msg)"
	docker-compose exec app alembic revision --autogenerate -m "$(msg)"

migrate:
	@echo "Running pending migrations..."
	docker-compose exec app alembic upgrade head
	@echo "Migrations completed!"

# Utility Commands
logs:
	docker-compose logs -f app

logs-db:
	docker-compose logs -f db

logs-redis:
	docker-compose logs -f redis

shell:
	docker-compose exec app python

db-shell:
	docker-compose exec db psql -U scholarpass_user -d scholarpass_db

redis-cli:
	docker-compose exec redis redis-cli

# Development Commands
clean:
	@echo "Cleaning up..."
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup completed!"

# Health Check
health:
	@echo "Checking service health..."
	@docker-compose ps
	@echo ""
	@echo "Testing API health..."
	@curl -s http://localhost:8000/health | python -m json.tool || echo "API not responding"

# Database Commands
db-reset:
	@echo "Resetting database..."
	docker-compose down -v
	docker-compose up -d db redis
	@sleep 5
	docker-compose exec app alembic upgrade head
	@echo "Database reset completed!"

db-seed:
	@echo "Seeding database..."
	docker-compose exec app python -m scripts.seed_data
	@echo "Database seeded!"

# Development Setup
setup:
	@echo "Setting up development environment..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env file created from .env.example"; \
	fi
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Setup completed!"

# Code Quality
lint:
	@echo "Running linting..."
	docker-compose exec app flake8 src/
	@echo "Linting completed!"

format:
	@echo "Formatting code..."
	docker-compose exec app black src/
	@echo "Code formatted!"

# Testing
test:
	@echo "Running tests..."
	docker-compose exec app pytest tests/ -v
	@echo "Tests completed!"

test-coverage:
	@echo "Running tests with coverage..."
	docker-compose exec app pytest tests/ --cov=src --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

# Info Commands
info:
	@echo "ScholarPASS Backend Information"
	@echo "================================"
	@echo "Database: PostgreSQL 15"
	@echo "Cache: Redis 7"
	@echo "API Framework: FastAPI"
	@echo "ORM: SQLAlchemy"
	@echo "Migrations: Alembic"
	@echo ""
	@echo "Running Services:"
	@docker-compose ps
