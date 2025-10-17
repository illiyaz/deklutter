# Deklutter Dev Makefile
SHELL := /bin/bash

PROJECT := deklutter
PY      ?= python3
PORT    ?= 8000
VENV    := .venv
ACTIVATE := source $(VENV)/bin/activate

DC := docker compose -f infra/docker-compose.yml

.PHONY: help env install up down logs dev server api freeze clean env-file reset-db db-shell test lint format

help:
	@echo "Deklutter - Available commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make env         - Create venv & install requirements"
	@echo "  make install     - Alias for 'make env'"
	@echo "  make env-file    - Create .env from .env.example if missing"
	@echo ""
	@echo "Docker Services:"
	@echo "  make up          - Start Postgres & Redis via Docker"
	@echo "  make down        - Stop Docker services"
	@echo "  make logs        - Tail Docker logs"
	@echo "  make reset-db    - Stop & remove DB volume (⚠️ destructive)"
	@echo ""
	@echo "Development:"
	@echo "  make dev         - Start DB + FastAPI server"
	@echo "  make server      - Start FastAPI server only"
	@echo "  make api         - Open API docs in browser"
	@echo "  make db-shell    - Open PostgreSQL interactive shell"
	@echo ""
	@echo "Code Quality:"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code with black"
	@echo "  make freeze      - Update requirements.txt with current deps"
	@echo "  make clean       - Remove caches & build artifacts"

env: env-file
	@echo "Creating virtual environment..."
	@$(PY) -m venv $(VENV)
	@$(ACTIVATE) && pip install --upgrade pip
	@$(ACTIVATE) && pip install -r requirements.txt
	@echo "✅ Virtualenv ready. Activate with: 'source $(VENV)/bin/activate'"

install: env
	@true

env-file:
	@if [ ! -f .env ]; then \
		cp .env.example .env && echo "📝 Created .env from .env.example"; \
	else \
		echo "ℹ️  .env already exists"; \
	fi

up:
	@echo "Starting Postgres & Redis..."
	@$(DC) up -d
	@echo "✅ Database (port 5433) & Redis (port 6379) are up."

down:
	@echo "Stopping Docker services..."
	@$(DC) down
	@echo "🛑 Docker services stopped."

logs:
	@$(DC) logs -f

dev: up
	@echo "Waiting for database to be ready..."
	@sleep 3
	@echo "Starting FastAPI server on http://localhost:$(PORT)"
	@echo "API docs available at http://localhost:$(PORT)/docs"
	@$(ACTIVATE) && uvicorn services.gateway.main:app --reload --port $(PORT)

server:
	@echo "Starting FastAPI server on http://localhost:$(PORT)"
	@echo "API docs available at http://localhost:$(PORT)/docs"
	@$(ACTIVATE) && uvicorn services.gateway.main:app --reload --port $(PORT)

api:
	@python3 -c "import webbrowser; webbrowser.open('http://localhost:8000/docs')"

db-shell:
	@echo "Opening PostgreSQL shell..."
	@docker exec -it infra-db-1 psql -U deklutter_user -d deklutter

reset-db: down
	@echo "⚠️  This will remove the Postgres volume and all data."
	@read -p "Type 'YES' to confirm: " ans; \
	if [ "$$ans" = "YES" ]; then \
		$(DC) down -v; \
		echo "🗑️  Volume removed."; \
		$(DC) up -d; \
		echo "✅ Database recreated."; \
	else \
		echo "❌ Skipped."; \
	fi

test:
	@echo "Running tests..."
	@$(ACTIVATE) && pytest -v

lint:
	@echo "Running linters..."
	@$(ACTIVATE) && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	@$(ACTIVATE) && flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	@echo "Formatting code with black..."
	@$(ACTIVATE) && black . --exclude .venv
	@echo "✅ Code formatted."

freeze:
	@echo "Updating requirements.txt..."
	@$(ACTIVATE) && pip freeze > requirements.txt
	@echo "📌 requirements.txt updated."

clean:
	@echo "Cleaning up..."
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name "*.coverage" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "🧹 Cleanup complete."
