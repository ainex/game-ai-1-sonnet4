# Codex Container Environment Setup

## Overview
This setup script ensures Codex can execute the Game AI Assistant implementation plan without dependency issues during the coding session (when internet is disabled). All dependencies must be installed during the setup phase.

## Setup Script for Codex

### Primary Setup Script (setup.sh)
```bash
#!/bin/bash
set -e

echo "=== Game AI Assistant - Codex Environment Setup ==="

# System packages and dependencies
apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
    python3-venv \
    build-essential \
    pkg-config \
    portaudio19-dev \
    libasound2-dev \
    libpulse-dev \
    ffmpeg \
    sqlite3 \
    libsqlite3-dev \
    git \
    curl \
    wget \
    unzip \
    xvfb \
    libgtk-3-dev \
    libx11-dev \
    libxext-dev \
    libxrandr-dev \
    libxss1 \
    libgconf-2-4 \
    libnss3 \
    libxss1

# Python environment setup
python3.11 -m pip install --upgrade pip setuptools wheel

# Core Python packages - install in specific order to avoid conflicts
echo "Installing core dependencies..."
pip install --no-cache-dir \
    numpy==1.24.3 \
    pillow==10.1.0 \
    requests==2.31.0 \
    aiohttp==3.9.1 \
    pydantic==2.5.2

# FastAPI ecosystem
echo "Installing FastAPI ecosystem..."
pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    python-multipart==0.0.6 \
    python-jose[cryptography]==3.3.0

# Database packages
echo "Installing database packages..."
pip install --no-cache-dir \
    sqlalchemy==2.0.23 \
    alembic==1.13.1 \
    sqlite3

# Audio processing packages
echo "Installing audio packages..."
pip install --no-cache-dir \
    sounddevice==0.4.6 \
    pyaudio==0.2.13 \
    wave \
    pygame==2.5.2

# Testing framework
echo "Installing testing packages..."
pip install --no-cache-dir \
    pytest==7.4.3 \
    pytest-asyncio==0.21.1 \
    pytest-mock==3.12.0 \
    httpx==0.25.2

# Configuration and utilities
echo "Installing utilities..."
pip install --no-cache-dir \
    python-dotenv==1.0.0 \
    pyyaml==6.0.1 \
    click==8.1.7 \
    rich==13.7.0

# Mock packages for testing (essential for offline development)
pip install --no-cache-dir \
    responses==0.24.1 \
    faker==20.1.0

# Verify installation
echo "Verifying Python environment..."
python3.11 -c "
import sys
print(f'Python version: {sys.version}')

# Test critical imports
try:
    import fastapi, uvicorn, pydantic, sqlalchemy
    import sounddevice, PIL, requests, aiohttp
    import pytest, httpx
    import sqlite3, json, os, asyncio
    print('✅ All critical packages imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

# Create project structure
echo "Creating project structure..."
mkdir -p /workspace/{client,server,shared,tests,docs,config}
mkdir -p /workspace/server/src/{api,core,models,services,utils}
mkdir -p /workspace/server/src/api/{endpoints,middleware}
mkdir -p /workspace/client/src/{core,ui,utils}
mkdir -p /workspace/tests/{unit,integration,mocks}
mkdir -p /workspace/config/{development,production,test}

echo "✅ Codex environment setup completed successfully"
```

## Requirements File (requirements.txt)
```txt
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.2
python-multipart==0.0.6

# HTTP Client
requests==2.31.0
aiohttp==3.9.1
httpx==0.25.2

# Database
sqlalchemy==2.0.23
alembic==1.13.1

# Audio Processing
sounddevice==0.4.6
pyaudio==0.2.13
pygame==2.5.2

# Image Processing
pillow==10.1.0
numpy==1.24.3

# Configuration
python-dotenv==1.0.0
pyyaml==6.0.1
click==8.1.7

# Development & Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-mock==3.12.0
responses==0.24.1
faker==20.1.0

# Utilities
rich==13.7.0
```

## AGENTS.md Configuration for Codex

```markdown
# Game AI Assistant - Agent Instructions

## Project Overview
Developing a Windows desktop application that provides AI-powered gaming assistance for strategy and RPG games. The system uses voice recording, screenshot capture, and LLM integration.

## Architecture
- **Client**: Windows desktop app (Python/Tkinter or C#)
- **Server**: Python FastAPI backend (cloud-deployable)
- **Database**: SQLite for local storage
- **Integration**: Multiple LLM APIs (OpenAI, Claude, etc.)

## Development Guidelines

### Code Structure
- Follow clean architecture principles
- Separate client from server completely
- Use dependency injection for testability
- Keep methods focused (max 20-30 lines)
- Comment only complex logic, not obvious code

### Testing Requirements
- Write tests FIRST for core functionality
- Mock all external API calls by default
- Use `pytest` with `pytest-asyncio` for async code
- Test coverage should be >80%
- Use `responses` library for HTTP mocking

### Key Commands
```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run server locally
cd server && python -m uvicorn src.main:app --reload --port 8000

# Run client (when implemented)
cd client && python src/main.py
```

### Mock Strategy for Offline Development
All external services MUST be mocked:
- OpenAI API calls
- Claude API calls
- Speech-to-text services
- Text-to-speech services
- Any HTTP requests

### Critical Dependencies
- FastAPI for REST API
- SQLAlchemy for database ORM
- Pydantic for data validation
- sounddevice for audio capture
- Pillow for image processing
- pytest for testing

### File Organization
```
/workspace/
├── server/src/           # Backend FastAPI code
├── client/src/           # Desktop client code
├── shared/               # Shared models/utilities
├── tests/                # All tests
├── config/               # Configuration files
└── docs/                 # Documentation
```

### Before Starting Implementation
1. Verify all dependencies are installed: `python -c "import fastapi, sqlalchemy, pytest, sounddevice, PIL"`
2. Create basic project structure
3. Set up pytest configuration
4. Write failing tests for core features first

### When Implementing
- Start with server-side API endpoints
- Create comprehensive mocks for external services
- Build client after server API is stable
- Test each component thoroughly before integration

### PR Preparation
- Ensure all tests pass: `pytest tests/`
- Verify no dependency issues
- Include C4 architecture diagrams in docs/
- Update README.md with setup instructions
```

## Environment Variables Setup
```bash
# Add to ~/.bashrc for persistence
echo 'export PYTHONPATH="/workspace:$PYTHONPATH"' >> ~/.bashrc
echo 'export ENVIRONMENT="development"' >> ~/.bashrc
echo 'export DATABASE_URL="sqlite:///./game_ai_assistant.db"' >> ~/.bashrc
echo 'export GITHUB_API_KEY="mock_key_for_testing"' >> ~/.bashrc

# Reload environment
source ~/.bashrc
```

## Verification Script
```bash
#!/bin/bash
echo "=== Environment Verification ==="

# Check Python and packages
python3.11 -c "
import fastapi, uvicorn, pydantic, sqlalchemy, alembic
import sounddevice, PIL, requests, aiohttp, httpx
import pytest, responses, faker
import sqlite3, asyncio, json, os, sys
print('✅ All Python packages available')
print(f'Python path: {sys.executable}')
"

# Check system tools
which sqlite3 && echo "✅ SQLite3 available"
which ffmpeg && echo "✅ FFmpeg available"
python3.11 -c "import sounddevice; print('✅ Audio system configured')"

# Check project structure
ls -la /workspace/ && echo "✅ Project structure created"

echo "🚀 Codex environment ready for development"
```

## Key Points for Codex Success

1. **All dependencies pre-installed**: No pip installs during coding session
2. **Comprehensive mocking**: All external APIs mocked for offline development
3. **Clear project structure**: Organized directories for easy navigation
4. **Testing first**: Pytest configured and ready for TDD approach
5. **Environment isolation**: All paths and configurations pre-set

This setup ensures Codex can implement the complete Game AI Assistant without any dependency or internet connectivity issues during the coding phase.
