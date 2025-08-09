# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A **Windows desktop application that provides AI-powered gaming assistance for strategy and RPG games**. The system captures screenshots and voice input to provide intelligent gameplay advice using multiple LLM APIs (Anthropic Claude 3.5 Sonnet, OpenAI GPT-4o, Whisper) with local TTS capabilities and a beautiful sci-fi overlay UI.

## Architecture

**Client-Server Split:**
- **Client** (`client/src/`): Windows desktop app using Python/Tkinter with global hotkeys
- **Server** (`server/src/`): FastAPI backend with AI services (deployable locally or cloud)
- **Shared** (`shared/`): Common models and utilities
- **Database**: SQLite for local storage
- **Integration**: Anthropic Claude 3.5 Sonnet (primary), OpenAI GPT-4o + Whisper, local TTS
- **UI**: Sci-fi transparent overlay for displaying AI responses (always-on-top)

## Development Commands

### Environment Setup
```bash
# Setup development environment (Linux/WSL)
./setup.sh

# Windows setup (recommended)
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# SECURE API KEY SETUP (REQUIRED)
# 1. Copy the example environment file
cp .env.example .env

# 2. Edit .env file and add your real API keys
# ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
# OPENAI_API_KEY=sk-your-openai-key-here
# DEFAULT_MODEL=claude-4-sonnet  # Options: claude-3.5-sonnet, claude-4-sonnet, gpt-4o-mini, gpt-4o, gpt-4.1, o3

# 3. Install additional Windows-only dependencies if needed
pip install keyboard  # For global hotkeys on Windows
```

### Running the Application
```bash
# Start server (from project root)
cd server && python -m uvicorn src.main:app --reload --port 8000

# Start client (from project root)
cd client && python src/main.py
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=server/src --cov-report=html

# Run only unit tests
pytest tests/unit/ -v

# Run integration tests  
pytest tests/integration/ -v

# Skip slow tests
pytest tests/ -v -m "not slow"
```

### Code Quality
```bash
# Format code (uses pyproject.toml config)
python -m black server/ client/ tests/
python -m isort server/ client/ tests/

# Type checking (configured for Python 3.12)
python -m mypy server/src/

# Linting
python -m flake8 server/ client/ tests/

# Security checks
python -m bandit -r server/src/

# Run pre-commit hooks
pre-commit run --all-files
```

### Special Test Scripts
```bash
# Test Claude 4 models (including new reasoning models)
python test_claude4_models.py

# Test OpenAI integration
python test_openai_integration.py

# Test voice functionality
python test_voice_functionality.py

# Verify CUDA setup
python scripts/verify_cuda.py
```

## Key Architecture Patterns

### API Endpoint Structure
The server follows a modular endpoint pattern in `server/src/api/endpoints/`:
- `claude_analysis.py`: Anthropic Claude 3.5 Sonnet multimodal integration (primary)
- `openai_analysis.py`: OpenAI GPT-4o + Whisper integration (backup)
- `image_analysis.py`: Local image captioning using Transformers
- `stt.py`: Speech-to-text using local Whisper
- `tts.py`: Text-to-speech using local TTS models
- `game_analysis.py`: Combined analysis workflows
- `analyze.py`: General analysis endpoint

### Service Layer Pattern
Business logic is separated into `server/src/services/`:
- `claude_service.py`: Anthropic Claude API integration (supports Claude 3.5 Sonnet and Claude 4 Sonnet)
- `openai_service.py`: OpenAI API integration (supports GPT-4o-mini, GPT-4o, GPT-4.1 series, and o3 models)
- `image_analysis.py`: Local vision models (BLIP, etc.)
- `stt.py`: Local speech recognition
- `tts.py`: Local speech synthesis with GPU acceleration

### Model Configuration
The system supports multiple AI models with easy configuration:
- **Default Model**: Set via `DEFAULT_MODEL` environment variable or client config
- **Claude Models**: 
  - `claude-3.5-sonnet`: Claude 3.5 Sonnet
  - `claude-4-sonnet`: Claude 4 Sonnet (standard reasoning)
  - `claude-4-opus`: Claude 4 Opus (most powerful model)
  - `claude-4-sonnet-thinking`: Claude 4 Sonnet with extended thinking
  - `claude-4-opus-thinking`: Claude 4 Opus with extended thinking
- **OpenAI Models**: `gpt-4o-mini`, `gpt-4o`, `gpt-4.1` (latest, August 2025), `gpt-4.1-mini`, `gpt-4.1-nano`, `o3` (using gpt-4o until o3 is released)
- **Server Config**: `server/src/core/config.py` handles model mappings
- **Client Config**: `client/src/core/config.py` stores user preferences

### Client Hotkey System
The client uses global hotkeys for seamless gaming integration:
- **Ctrl+Shift+C**: Claude-powered analysis with sci-fi overlay (recommended)
- **Ctrl+Shift+V**: OpenAI-powered voice + screenshot analysis
- **Ctrl+Shift+S**: Screenshot + AI description + TTS
- **Ctrl+Shift+A**: Screenshot + text analysis only
- **Ctrl+Shift+T**: Test TTS service

**Note**: The client includes a transparent sci-fi overlay UI (`client/src/ui/overlay.py`) for displaying AI responses always-on-top during gameplay.

### Mock Strategy for Development
All external services are mocked by default using `pytest` and `responses`:
- OpenAI API calls are mocked in tests
- Audio/voice recording uses test files
- Screenshot capture uses sample images
- Enable live APIs only with explicit environment variables

## Critical Development Patterns

### AI-Assisted Workflow
This project follows the structured workflow in `AGENTS.md`:
1. Create detailed `IMPLEMENTATION_PLAN.md` before coding
2. Follow step-by-step implementation
3. Update module READMEs
4. Remove implementation plans after completion

### Error Handling
- All external API calls must have comprehensive error handling
- Graceful fallbacks for missing audio libraries (pygame, sounddevice, pyaudio)
- Windows-specific console encoding handling (`chcp 65001`)
- Logging to both console and files with UTF-8 encoding

### Testing Requirements
- Mock all external services by default
- Use environment variables to enable live API testing
- Audio tests use sample files, not actual recording
- Screenshot tests use fixture images

## Environment Configuration

### Required Environment Variables
```bash
# Development mode
DEBUG=true
ENVIRONMENT=development

# API Keys (SECURE .env SETUP REQUIRED)
# Copy .env.example to .env and add your real keys:
# ANTHROPIC_API_KEY=sk-ant-api03-your-key-here  
# OPENAI_API_KEY=sk-your-openai-key-here

# Model Configuration (choose one)
# DEFAULT_MODEL=claude-4-sonnet         # Standard Claude 4 Sonnet
# DEFAULT_MODEL=claude-4-opus           # Most powerful Claude 4 model
# DEFAULT_MODEL=claude-4-opus-thinking  # Claude 4 Opus with extended reasoning

# Database
DATABASE_URL=sqlite:///./game_assistant.db

# Audio settings
AUDIO_SAMPLE_RATE=44100
AUDIO_CHANNELS=1

# Screenshot settings  
SCREENSHOT_QUALITY=85
MAX_IMAGE_SIZE=1920x1080
```

### Windows-Specific Requirements
- Visual Studio Build Tools for TTS compilation
- Python 3.11+ for server and client (project configured for 3.12)
- Audio system libraries (automatic fallback handling in client)
- `keyboard` library for global hotkey support

## GPU Acceleration Support
The project supports NVIDIA CUDA for faster TTS generation:
- 10-20x speed improvement with RTX/GTX cards
- Automatic CPU fallback when CUDA unavailable
- Verify setup with: `python scripts/verify_cuda.py`

## Key Dependencies

### Core Framework
- FastAPI 0.104.1 + Uvicorn for REST API
- SQLAlchemy 2.0.23 for database ORM
- Pydantic 2.5.2 for data validation

### AI/ML Libraries
- Anthropic >= 0.18.0 for Claude 3.5 Sonnet multimodal
- OpenAI >= 1.0.0 for GPT-4o + Whisper
- Transformers >= 4.35.0 for local vision models
- TTS >= 0.19.0 for local speech synthesis
- Torch/TorchVision for GPU acceleration

### Audio/Visual Processing
- Pillow 10.1.0 for image processing
- sounddevice, pyaudio, pygame for audio (with fallbacks)
- keyboard for global hotkey handling

### Testing Stack
- pytest 7.4.3 with asyncio and mock support
- responses 0.24.1 for HTTP mocking
- pytest-cov for coverage reporting
- pytest-mock for advanced mocking capabilities
- faker for test data generation

### Development Tools
- black for code formatting (configured in pyproject.toml)
- isort for import sorting
- mypy for type checking (Python 3.12 target)
- flake8 for linting
- bandit for security analysis
- pre-commit for automated quality checks

## Common Tasks

### Adding New API Endpoints
1. Create endpoint in `server/src/api/endpoints/`
2. Create corresponding service in `server/src/services/`
3. Add route to `server/src/main.py`
4. Write tests in `tests/unit/` and `tests/integration/`
5. Update this CLAUDE.md if it's a major feature

### Adding New Hotkeys
1. Add hotkey handler function in `client/src/main.py`
2. Register with `keyboard.add_hotkey()` in `main()`
3. Update help text in console output
4. Test with the client application

### Working with Voice/Audio
- All audio operations must handle library unavailability gracefully
- Use the established fallback pattern: sounddevice → pygame → pyaudio
- Always log audio processing steps for debugging
- Clean up temporary audio files after playback

### Working with AI Models
- Always implement comprehensive error handling for API calls
- Use environment variables for API keys
- Mock external API calls in tests by default
- Follow the established service layer pattern for new integrations