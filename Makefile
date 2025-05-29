# Sims 4 AI Gaming Assistant - Development Makefile
# Provides convenient commands for common development tasks

.PHONY: help setup validate clean test lint format docs install dev-install

# Default target
help:
	@echo "🎮 Sims 4 AI Gaming Assistant - Development Commands"
	@echo "================================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  setup          - Run full development environment setup"
	@echo "  install        - Install Python dependencies only"
	@echo "  dev-install    - Install development dependencies"
	@echo "  validate       - Validate development environment setup"
	@echo ""
	@echo "Development Commands:"
	@echo "  test           - Run all tests"
	@echo "  test-unit      - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-cov       - Run tests with coverage report"
	@echo "  lint           - Run all linting tools"
	@echo "  format         - Format code with black and isort"
	@echo "  typecheck      - Run mypy type checking"
	@echo "  security       - Run security checks with bandit"
	@echo ""
	@echo "Server Commands:"
	@echo "  server         - Start FastAPI development server"
	@echo "  server-prod    - Start production server"
	@echo "  client         - Start desktop client"
	@echo ""
	@echo "Quality Commands:"
	@echo "  pre-commit     - Run pre-commit hooks on all files"
	@echo "  clean          - Clean temporary files and caches"
	@echo "  docs           - Generate documentation"
	@echo ""
	@echo "Quick Commands:"
	@echo "  check          - Run format + lint + test (quick validation)"
	@echo "  ci             - Run full CI pipeline locally"

# Setup and Installation
setup:
	@echo "🚀 Setting up development environment..."
	./setup.sh

install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt

dev-install:
	@echo "🛠️ Installing development dependencies..."
	pip install --upgrade pip setuptools wheel
	pip install black isort flake8 mypy bandit pytest pytest-cov pre-commit

validate:
	@echo "🔍 Validating setup..."
	./validate_setup.sh

# Testing Commands
test:
	@echo "🧪 Running all tests..."
	pytest tests/ -v

test-unit:
	@echo "🧪 Running unit tests..."
	pytest tests/unit/ -v

test-integration:
	@echo "🧪 Running integration tests..."
	pytest tests/integration/ -v

test-cov:
	@echo "🧪 Running tests with coverage..."
	pytest tests/ -v --cov=server/src --cov=client/src --cov=shared --cov-report=html --cov-report=term

test-fast:
	@echo "🧪 Running fast tests only..."
	pytest tests/ -v -m "not slow"

test-audio:
	@echo "🧪 Running audio system tests..."
	pytest tests/ -v -m "audio"

test-mock:
	@echo "🧪 Running mock tests..."
	pytest tests/ -v -m "mock"

# Code Quality Commands
lint:
	@echo "🔍 Running linting tools..."
	python -m flake8 server/ client/ shared/ tests/
	python -m mypy server/src/
	python -m bandit -r server/src/

format:
	@echo "✨ Formatting code..."
	python -m black server/ client/ shared/ tests/
	python -m isort server/ client/ shared/ tests/

typecheck:
	@echo "🔍 Running type checking..."
	python -m mypy server/src/

security:
	@echo "🔒 Running security checks..."
	python -m bandit -r server/src/

# Application Commands
server:
	@echo "🌐 Starting FastAPI development server..."
	cd server && python -m uvicorn src.main:app --reload --port 8000

server-prod:
	@echo "🌐 Starting production server..."
	cd server && python -m uvicorn src.main:app --port 8000

client:
	@echo "🖥️ Starting desktop client..."
	@if [ -f "client/src/main.py" ]; then \
		cd client && python src/main.py; \
	else \
		echo "Client not implemented yet"; \
	fi

# Pre-commit and Git Hooks
pre-commit:
	@echo "🔧 Running pre-commit hooks..."
	pre-commit run --all-files

pre-commit-install:
	@echo "🔧 Installing pre-commit hooks..."
	pre-commit install

# Documentation
docs:
	@echo "📚 Generating documentation..."
	@if [ -d "docs/" ]; then \
		echo "Building with MkDocs..."; \
		mkdocs build; \
	else \
		echo "Documentation directory not found"; \
	fi

docs-serve:
	@echo "📚 Serving documentation locally..."
	mkdocs serve

# Database Commands
db-create:
	@echo "🗄️ Creating database..."
	cd server && python -c "from src.core.database import create_tables; create_tables()"

db-migrate:
	@echo "🗄️ Running database migrations..."
	cd server && alembic upgrade head

db-reset:
	@echo "🗄️ Resetting database..."
	rm -f server/sims4_assistant.db
	$(MAKE) db-create

# Cleanup Commands
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf dist/
	rm -rf build/
	rm -rf .mypy_cache/
	rm -rf recordings/
	rm -rf screenshots/

clean-all: clean
	@echo "🧹 Deep cleaning (including virtual environment)..."
	rm -rf venv/
	rm -f *.db *.sqlite *.sqlite3

# Quick Validation Commands
check: format lint test-fast
	@echo "✅ Quick validation complete!"

ci: format lint typecheck security test test-cov
	@echo "✅ Full CI pipeline complete!"

# Development Environment
venv:
	@echo "🐍 Creating virtual environment..."
	python3 -m venv venv
	@echo "Activate with: source venv/bin/activate"

activate:
	@echo "🐍 To activate virtual environment, run:"
	@echo "source venv/bin/activate"

# Project Structure
structure:
	@echo "📁 Project structure:"
	@tree -I '__pycache__|*.pyc|venv|.git|recordings|screenshots' -a

# Git Commands
git-status:
	@echo "📊 Git status and info:"
	@git status
	@echo ""
	@echo "Recent commits:"
	@git log --oneline -5

# Installation Verification
verify:
	@echo "🔍 Verifying installation..."
	@python --version
	@pip --version
	@echo "Critical packages:"
	@python -c "import fastapi, sqlalchemy, pytest, sounddevice, PIL; print('✅ All critical packages available')"

# Development Info
info:
	@echo "📋 Sims 4 AI Assistant Development Environment Info:"
	@echo "=================================================="
	@echo "Python: $(shell python --version 2>&1)"
	@echo "Pip: $(shell pip --version 2>&1)"
	@echo "Virtual Env: $(VIRTUAL_ENV)"
	@echo "Working Dir: $(shell pwd)"
	@echo "Git Branch: $(shell git branch --show-current 2>/dev/null || echo 'Not a git repo')"
	@echo "Last Commit: $(shell git log -1 --format='%h %s' 2>/dev/null || echo 'No commits')"
	@echo "Server Status: $(shell curl -s http://localhost:8000/health 2>/dev/null || echo 'Not running')"

# Implementation Plan Helpers
plan:
	@echo "📝 Creating new implementation plan..."
	@read -p "Enter feature name: " feature_name; \
	echo "# Implementation Plan: $$feature_name" > IMPLEMENTATION_PLAN.md; \
	echo "" >> IMPLEMENTATION_PLAN.md; \
	echo "## General Solution (sd)" >> IMPLEMENTATION_PLAN.md; \
	echo "" >> IMPLEMENTATION_PLAN.md; \
	echo "Describe the general solution approach for $$feature_name in the Sims 4 AI Assistant." >> IMPLEMENTATION_PLAN.md; \
	echo "" >> IMPLEMENTATION_PLAN.md; \
	echo "## Dependencies and Dependants Investigation" >> IMPLEMENTATION_PLAN.md; \
	echo "" >> IMPLEMENTATION_PLAN.md; \
	echo "List relevant files and their relationships:" >> IMPLEMENTATION_PLAN.md; \
	echo "- server/src/..." >> IMPLEMENTATION_PLAN.md; \
	echo "- client/src/..." >> IMPLEMENTATION_PLAN.md; \
	echo "- shared/..." >> IMPLEMENTATION_PLAN.md; \
	echo "- tests/..." >> IMPLEMENTATION_PLAN.md; \
	echo "" >> IMPLEMENTATION_PLAN.md; \
	echo "## Implementation Plan, Finally" >> IMPLEMENTATION_PLAN.md; \
	echo "" >> IMPLEMENTATION_PLAN.md; \
	echo "Step-by-step action plan:" >> IMPLEMENTATION_PLAN.md; \
	echo "1. Server-side implementation" >> IMPLEMENTATION_PLAN.md; \
	echo "2. Client-side implementation" >> IMPLEMENTATION_PLAN.md; \
	echo "3. Testing with mocks" >> IMPLEMENTATION_PLAN.md; \
	echo "4. Integration testing" >> IMPLEMENTATION_PLAN.md; \
	echo "5. Documentation update" >> IMPLEMENTATION_PLAN.md; \
	echo "" >> IMPLEMENTATION_PLAN.md; \
	echo "✅ Created IMPLEMENTATION_PLAN.md for $$feature_name"

clean-plan:
	@echo "🧹 Removing implementation plan..."
	@if [ -f "IMPLEMENTATION_PLAN.md" ]; then \
		rm IMPLEMENTATION_PLAN.md; \
		echo "✅ IMPLEMENTATION_PLAN.md removed"; \
	else \
		echo "No IMPLEMENTATION_PLAN.md found"; \
	fi

# Audio/Visual Testing
test-audio-system:
	@echo "🔊 Testing audio system..."
	@python -c "import sounddevice as sd; print('Audio devices:'); print(sd.query_devices())"

test-screenshot-system:
	@echo "📸 Testing screenshot system..."
	@python -c "from PIL import ImageGrab; img = ImageGrab.grab(); print(f'Screenshot captured: {img.size}')"

# Mock Server for Development
mock-server:
	@echo "🎭 Starting mock server for LLM APIs..."
	@python -c "print('Mock server functionality to be implemented')"

# Environment Health Check
health:
	@echo "🏥 Checking environment health..."
	@echo "Python version:"
	@python --version
	@echo ""
	@echo "Critical imports:"
	@python -c "import fastapi, sqlalchemy, pytest, sounddevice, PIL, sqlite3; print('✅ All imports successful')"
	@echo ""
	@echo "Audio system:"
	@python -c "import sounddevice as sd; devices = sd.query_devices(); print(f'✅ {len(devices)} audio devices found')" 2>/dev/null || echo "⚠️ Audio system issues"
	@echo ""
	@echo "Database:"
	@python -c "import sqlite3; conn = sqlite3.connect(':memory:'); print('✅ SQLite working')" 