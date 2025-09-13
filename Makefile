# Market Scout Israel Makefile

.PHONY: help install test lint format clean ollama-up ollama-down ollama-pull

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -e .
	pip install pytest pytest-asyncio black mypy ruff httpx

test:  ## Run tests (excluding ollama tests)
	python -m pytest tests/ -v -m "not ollama"

test-all:  ## Run all tests including ollama integration tests
	python -m pytest tests/ -v

lint:  ## Run linting checks
	python -m ruff check .
	python -m black --check .

format:  ## Format code
	python -m black .
	python -m ruff check . --fix

clean:  ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf *.egg-info/

# Ollama commands
ollama-up:  ## Start Ollama service
	docker compose up -d ollama
	@echo "Waiting for Ollama service to be ready..."
	@timeout 60 bash -c 'until curl -s http://localhost:11434/api/tags >/dev/null 2>&1; do sleep 2; done'
	@echo "Ollama service is ready!"

ollama-down:  ## Stop Ollama service
	docker compose down ollama

ollama-pull:  ## Pull an Ollama model (usage: make ollama-pull MODEL=llama3)
	@if [ -z "$(MODEL)" ]; then \
		echo "Usage: make ollama-pull MODEL=<model_name>"; \
		echo "Example: make ollama-pull MODEL=llama3"; \
		exit 1; \
	fi
	docker compose exec ollama ollama pull $(MODEL)

ollama-models:  ## List available Ollama models
	docker compose exec ollama ollama list

ollama-logs:  ## Show Ollama logs
	docker compose logs -f ollama