# AI Code Editor - Development Makefile

.PHONY: help setup install dev test lint clean test-models

help: ## Show this help
\t@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'

setup: ## Initial project setup
\tpython fixed_structure_generator.py
\tcp .env.example .env

install: ## Install dependencies
\tcd backend && pip install -r requirements/development.txt
\tcd frontend && npm install

test-models: ## Test Pydantic V2 models
\tcd backend && python test_models.py

dev: ## Start development servers
\tdocker-compose up -d redis
\tcd backend && uvicorn app.main:app --reload --port 8000 &
\tcd frontend && npm run dev

test: ## Run tests
\tcd backend && pytest
\tcd frontend && npm test

lint: ## Run linters
\tcd backend && black . && flake8 .
\tcd frontend && npm run lint

clean: ## Clean build artifacts
\tcd backend && find . -type d -name __pycache__ -delete
\tcd frontend && rm -rf node_modules dist
\tdocker-compose down -v
