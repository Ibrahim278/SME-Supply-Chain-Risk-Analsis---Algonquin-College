# SME Supply Chain Risk Analysis - Development Commands
# Usage: make <target>

.PHONY: up down restart logs ps clean build rebuild \
        backend-logs frontend-logs db-logs redis-logs \
        shell-backend shell-frontend shell-db \
        migrate test lint format

# =============================================================================
# Docker Compose - Full Stack
# =============================================================================

up:
	sudo docker compose -f docker-compose.dev-full.yml up -d

down:
	sudo docker compose -f docker-compose.dev-full.yml down

restart:
	sudo docker compose -f docker-compose.dev-full.yml down
	sudo docker compose -f docker-compose.dev-full.yml up -d

build:
	sudo docker compose -f docker-compose.dev-full.yml build

rebuild:
	sudo docker compose -f docker-compose.dev-full.yml build --no-cache
	sudo docker compose -f docker-compose.dev-full.yml up -d

# =============================================================================
# Status & Logs
# =============================================================================

ps:
	sudo docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

logs:
	sudo docker compose -f docker-compose.dev-full.yml logs -f

backend-logs:
	sudo docker logs -f sme-backend-dev-full

frontend-logs:
	sudo docker logs -f sme-frontend-dev-full

db-logs:
	sudo docker logs -f sme-postgres-dev-full

redis-logs:
	sudo docker logs -f sme-redis-dev-full

# =============================================================================
# Shell Access
# =============================================================================

shell-backend:
	sudo docker exec -it sme-backend-dev-full /bin/bash

shell-frontend:
	sudo docker exec -it sme-frontend-dev-full /bin/sh

shell-db:
	sudo docker exec -it sme-postgres-dev-full psql -U sme -d sme

shell-redis:
	sudo docker exec -it sme-redis-dev-full redis-cli

# =============================================================================
# Database
# =============================================================================

migrate:
	sudo docker exec sme-backend-dev-full alembic upgrade head

migrate-new:
	@read -p "Migration message: " msg; \
	sudo docker exec sme-backend-dev-full alembic revision --autogenerate -m "$$msg"

# =============================================================================
# Testing & Quality
# =============================================================================

test-backend:
	sudo docker exec sme-backend-dev-full pytest -v

test-frontend:
	sudo docker exec sme-frontend-dev-full npm test

lint-backend:
	sudo docker exec sme-backend-dev-full ruff check app/

lint-frontend:
	sudo docker exec sme-frontend-dev-full npm run lint

format-backend:
	sudo docker exec sme-backend-dev-full black app/
	sudo docker exec sme-backend-dev-full ruff check --fix app/

format-frontend:
	cd frontend && npm run format

format: format-backend format-frontend

# =============================================================================
# Cleanup
# =============================================================================

clean:
	sudo docker compose -f docker-compose.dev-full.yml down -v --remove-orphans

prune:
	sudo docker system prune -f

# =============================================================================
# Help
# =============================================================================

help:
	@echo "SME Development Commands"
	@echo ""
	@echo "Stack:"
	@echo "  make up          - Start all containers"
	@echo "  make down        - Stop all containers"
	@echo "  make restart     - Restart all containers"
	@echo "  make ps          - Show container status"
	@echo ""
	@echo "Logs:"
	@echo "  make logs        - Follow all logs"
	@echo "  make backend-logs"
	@echo "  make frontend-logs"
	@echo ""
	@echo "Shell:"
	@echo "  make shell-backend"
	@echo "  make shell-frontend"
	@echo "  make shell-db"
	@echo "  make shell-redis"
	@echo ""
	@echo "Database:"
	@echo "  make migrate     - Run migrations"
	@echo "  make migrate-new - Create new migration"
	@echo ""
	@echo "Testing:"
	@echo "  make test-backend"
	@echo "  make test-frontend"
	@echo "  make lint-backend"
	@echo "  make lint-frontend"
	@echo ""
	@echo "Formatting:"
	@echo "  make format          - Format all code"
	@echo "  make format-backend"
	@echo "  make format-frontend"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean       - Remove containers and volumes"
	@echo "  make prune       - Docker system prune"
