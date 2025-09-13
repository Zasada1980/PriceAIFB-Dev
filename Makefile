# Makefile for PriceAIFB-Dev development
.PHONY: help install install-dev clean lint format typecheck test coverage run build up logs compile docs

# Default Python interpreter
PYTHON := python
PIP := pip
DOCKER_COMPOSE := docker compose

help: ## Show this help message
	@echo "PriceAIFB-Dev Development Commands"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	$(PIP) install -r requirements.txt

install-dev: ## Install all dependencies including development tools
	$(PIP) install -r requirements.txt -e ".[dev]"

clean: ## Clean build artifacts and caches
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build dist .coverage htmlcov .pytest_cache .mypy_cache

lint: ## Run code linting with ruff
	ruff check src/ tests/

format: ## Format code with black and isort
	black src/ tests/
	isort src/ tests/

format-check: ## Check code formatting without making changes
	black --check src/ tests/
	isort --check-only src/ tests/

typecheck: ## Run type checking with mypy
	mypy src/

test: ## Run tests with pytest
	pytest tests/ -v

coverage: ## Run tests with coverage report
	pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

test-fast: ## Run tests without coverage (faster)
	pytest tests/ -v --tb=short

run: ## Run the demo pipeline locally
	$(PYTHON) -m src.app.pipelines.run

compile: ## Compile requirements.in to requirements.txt
	pip-compile requirements.in

compile-upgrade: ## Upgrade and compile requirements
	pip-compile --upgrade requirements.in

# Docker commands
build: ## Build Docker image
	$(DOCKER_COMPOSE) build

up: ## Start services with docker-compose
	$(DOCKER_COMPOSE) up -d

up-build: ## Build and start services
	$(DOCKER_COMPOSE) up -d --build

down: ## Stop services
	$(DOCKER_COMPOSE) down

logs: ## Show container logs
	$(DOCKER_COMPOSE) logs -f

# Development workflow
dev-setup: install-dev ## Set up development environment
	@echo "Development environment ready!"
	@echo "Run 'make run' to test the demo pipeline"

check: lint format-check typecheck test ## Run all checks (lint, format, type, test)

ci: lint format-check typecheck coverage ## Run CI pipeline locally

# Environment setup
env: ## Copy .env.example to .env
	cp .env.example .env
	@echo "Environment file created. Please review and modify .env as needed."

# Quick development commands
quick-test: test-fast lint ## Quick development test (no coverage)

fix: format lint ## Fix code formatting and linting issues

# Documentation
docs: ## Generate documentation (placeholder)
	@echo "Documentation generation not yet implemented"

# Release preparation
prepare-release: clean check ## Prepare for release (clean + full check)
	@echo "Release preparation complete"