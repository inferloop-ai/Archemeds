# AI Code Editor - Development Makefile
# Provides convenient commands for setting up and developing the AI-powered code editor

.PHONY: help scaffold setup install dev test lint clean docker-build docker-up docker-down deploy

# Default target
help: ## Show this help message
	@echo "AI Code Editor - Development Commands"
	@echo "====================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Project Setup Commands
scaffold: ## Create project directory structure using Python script
	@echo "🚀 Creating project structure..."
	@python3 create_structure.py
	@echo "✅ Project structure created!"

scaffold-bash: ## Create project structure using Bash script (Linux/Mac)
	@echo "🚀 Creating project structure with Bash..."
	@chmod +x create_structure.sh
	@./create_structure.sh
	@echo "✅ Project structure created!"

scaffold-windows: ## Create project structure using Windows batch script
	@echo "🚀 Creating project structure with Batch..."
	@create_structure.bat
	@echo "✅ Project structure created!"

init: ## Initialize project after scaffolding (git, env files, etc.)
	@echo "🔧 Initializing project..."
	@cd ai-code-editor && git init
	@cd ai-code-editor && cp .env.example .env
	@cd ai-code-editor/frontend && cp .env.example .env
	@cd ai-code-editor/backend && cp .env.example .env
	@echo "✅ Project initialized!"

# Development Setup
install: ## Install all dependencies (frontend + backend)
	@echo "📦 Installing dependencies..."
	@cd ai-code-editor/frontend && npm install
	@cd ai-code-editor/backend && pip install -r requirements/development.txt
	@echo "✅ Dependencies installed!"

install-frontend: ## Install frontend dependencies only
	@echo "📦 Installing frontend dependencies..."
	@cd ai-code-editor/frontend && npm install

install-backend: ## Install backend dependencies only
	@echo "📦 Installing backend dependencies..."
	@cd ai-code-editor/backend && pip install -r requirements/development.txt

# Development Commands
dev: ## Start development servers (frontend + backend)
	@echo "🚀 Starting development servers..."
	@cd ai-code-editor && docker-compose -f docker-compose.yml up -d postgres redis vector-db
	@cd ai-code-editor/backend && uvicorn app.main:app --reload --port 8000 &
	@cd ai-code-editor/frontend && npm run dev

dev-frontend: ## Start frontend development server only
	@echo "🚀 Starting frontend development server..."
	@cd ai-code-editor/frontend && npm run dev

dev-backend: ## Start backend development server only
	@echo "🚀 Starting backend development server..."
	@cd ai-code-editor/backend && uvicorn app.main:app --reload --port 8000

# Testing Commands
test: ## Run all tests (frontend + backend)
	@echo "🧪 Running all tests..."
	@cd ai-code-editor/frontend && npm test
	@cd ai-code-editor/backend && pytest

test-frontend: ## Run frontend tests only
	@echo "🧪 Running frontend tests..."
	@cd ai-code-editor/frontend && npm test

test-backend: ## Run backend tests only
	@echo "🧪 Running backend tests..."
	@cd ai-code-editor/backend && pytest

test-e2e: ## Run end-to-end tests
	@echo "🧪 Running E2E tests..."
	@cd ai-code-editor && npm run test:e2e

# Code Quality Commands
lint: ## Run linting for all code
	@echo "🔍 Running linters..."
	@cd ai-code-editor/frontend && npm run lint
	@cd ai-code-editor/backend && flake8 . && black --check . && isort --check-only .

lint-fix: ## Fix linting issues automatically
	@echo "🔧 Fixing lint issues..."
	@cd ai-code-editor/frontend && npm run lint:fix
	@cd ai-code-editor/backend && black . && isort .

format: ## Format all code
	@echo "✨ Formatting code..."
	@cd ai-code-editor/frontend && npm run format
	@cd ai-code-editor/backend && black . && isort .

# Docker Commands
docker-build: ## Build Docker images
	@echo "🐳 Building Docker images..."
	@cd ai-code-editor && docker-compose build

docker-up: ## Start all services with Docker
	@echo "🐳 Starting services with Docker..."
	@cd ai-code-editor && docker-compose up -d

docker-down: ## Stop all Docker services
	@echo "🐳 Stopping Docker services..."
	@cd ai-code-editor && docker-compose down

docker-logs: ## View Docker logs
	@echo "📋 Showing Docker logs..."
	@cd ai-code-editor && docker-compose logs -f

# Database Commands
db-migrate: ## Run database migrations
	@echo "🗄️ Running database migrations..."
	@cd ai-code-editor/backend && alembic upgrade head

db-reset: ## Reset database (WARNING: destructive)
	@echo "⚠️ Resetting database..."
	@cd ai-code-editor/backend && alembic downgrade base
	@cd ai-code-editor/backend && alembic upgrade head

# Build Commands
build: ## Build production bundles
	@echo "🔨 Building production bundles..."
	@cd ai-code-editor/frontend && npm run build
	@cd ai-code-editor/backend && python -m build

build-frontend: ## Build frontend for production
	@echo "🔨 Building frontend..."
	@cd ai-code-editor/frontend && npm run build

# Deployment Commands
deploy-dev: ## Deploy to development environment
	@echo "🚀 Deploying to development..."
	@cd ai-code-editor && kubectl apply -f infrastructure/kubernetes/ -n ai-editor-dev

deploy-staging: ## Deploy to staging environment
	@echo "🚀 Deploying to staging..."
	@cd ai-code-editor && kubectl apply -f infrastructure/kubernetes/ -n ai-editor-staging

deploy-prod: ## Deploy to production environment
	@echo "🚀 Deploying to production..."
	@cd ai-code-editor && kubectl apply -f infrastructure/kubernetes/ -n ai-editor-prod

# Monitoring Commands
logs: ## View application logs
	@echo "📋 Viewing logs..."
	@cd ai-code-editor && kubectl logs -f deployment/ai-editor-backend

monitor: ## Open monitoring dashboard
	@echo "📊 Opening monitoring dashboard..."
	@open http://localhost:3000 # Grafana
	@open http://localhost:9090 # Prometheus

# Cleanup Commands
clean: ## Clean build artifacts and dependencies
	@echo "🧹 Cleaning build artifacts..."
	@cd ai-code-editor/frontend && rm -rf node_modules dist .next
	@cd ai-code-editor/backend && rm -rf __pycache__ .pytest_cache dist build *.egg-info
	@cd ai-code-editor && docker-compose down -v --remove-orphans

clean-docker: ## Clean Docker images and volumes
	@echo "🧹 Cleaning Docker resources..."
	@docker system prune -f
	@docker volume prune -f

# Utility Commands
docs: ## Generate and serve documentation
	@echo "📚 Generating documentation..."
	@cd ai-code-editor && mkdocs serve

backup: ## Backup database and important files
	@echo "💾 Creating backup..."
	@cd ai-code-editor && ./infrastructure/scripts/backup.sh

update-deps: ## Update all dependencies
	@echo "⬆️ Updating dependencies..."
	@cd ai-code-editor/frontend && npm update
	@cd ai-code-editor/backend && pip install --upgrade -r requirements/development.txt

security-scan: ## Run security scans
	@echo "🔒 Running security scans..."
	@cd ai-code-editor/frontend && npm audit
	@cd ai-code-editor/backend && safety check
	@cd ai-code-editor && trivy fs .

# Quick Setup Command
quick-setup: scaffold init install ## Complete project setup in one command
	@echo "🎉 Quick setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. cd ai-code-editor"
	@echo "2. Edit .env files with your API keys"
	@echo "3. make dev  # Start development servers"
	@echo ""

# Development workflow
workflow: ## Common development workflow (install, test, lint)
	@make install
	@make test
	@make lint
	@echo "✅ Development workflow complete!"

# Status check
status: ## Check status of all services
	@echo "📊 Service Status:"
	@echo "Frontend: $(shell cd ai-code-editor/frontend 2>/dev/null && npm list --depth=0 2>/dev/null | head -1 || echo 'Not installed')"
	@echo "Backend: $(shell cd ai-code-editor/backend 2>/dev/null && python --version 2>/dev/null || echo 'Not installed')"
	@echo "Docker: $(shell docker --version 2>/dev/null || echo 'Not installed')"
	@echo "Git: $(shell cd ai-code-editor 2>/dev/null && git status --porcelain 2>/dev/null | wc -l || echo 'Not initialized') uncommitted files"

# Project info
info: ## Show project information
	@echo "AI Code Editor Project Information"
	@echo "=================================="
	@echo "Project: AI-Powered Code Editor with Multi-Agent System"
	@echo "Frontend: React + TypeScript + Monaco Editor + Tailwind CSS"
	@echo "Backend: FastAPI + Python + LangGraph + AI Agents"
	@echo "Database: PostgreSQL + Redis + Vector DB (Weaviate/Chroma)"
	@echo "Infrastructure: Docker + Kubernetes + Terraform"
	@echo "AI: OpenAI GPT-4, Anthropic Claude, DeepSeek"
	@echo ""
	@echo "Key Features:"
	@echo "- Monaco Editor with AI-powered code generation"
	@echo "- Multi-agent system for specialized tasks"
	@echo "- Real-time collaborative editing"
	@echo "- Infrastructure as code generation"
	@echo "- Automated testing and CI/CD"
	@echo "- Security scanning and compliance"