# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A **Windows desktop application that provides AI-powered gaming assistance for strategy and RPG games**. The system captures screenshots and voice input to provide intelligent gameplay advice using multiple LLM APIs (OpenAI GPT-4 Vision, Whisper, Claude) with local TTS/STT capabilities.

## Architecture

**Client-Server Split:**
- **Client** (`client/src/`): Windows desktop app using Python/Tkinter with global hotkeys
- **Server** (`server/src/`): FastAPI backend with AI services (deployable locally or cloud)
- **Shared** (`shared/`): Common models and utilities
- **Database**: SQLite for local storage
- **Integration**: OpenAI (GPT-4 Vision + Whisper), Claude, local TTS/STT

## Development Commands

### Environment Setup
```bash
# Setup development environment (Linux/WSL)
./setup.sh

# Windows setup (manual)
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
pip install keyboard
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
# Format code
python -m black server/ client/ tests/
python -m isort server/ client/ tests/

# Type checking
python -m mypy server/src/

# Linting
python -m flake8 server/ client/ tests/

# Security checks
python -m bandit -r server/src/
```

### Special Test Scripts
```bash
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
- `openai_analysis.py`: OpenAI GPT-4 Vision + Whisper integration
- `image_analysis.py`: Local image captioning using Transformers
- `stt.py`: Speech-to-text using local Whisper
- `tts.py`: Text-to-speech using local TTS models
- `game_analysis.py`: Combined analysis workflows

### Service Layer Pattern
Business logic is separated into `server/src/services/`:
- `openai_service.py`: OpenAI API integration with error handling
- `image_analysis.py`: Local vision models (BLIP, etc.)
- `stt.py`: Local speech recognition
- `tts.py`: Local speech synthesis with GPU acceleration

### Client Hotkey System
The client uses global hotkeys for seamless gaming integration:
- **Ctrl+Shift+V**: Complete voice + screenshot analysis (recommended)
- **Ctrl+Shift+S**: Screenshot + AI description + TTS
- **Ctrl+Shift+A**: Screenshot + text analysis only
- **Ctrl+Shift+T**: Test TTS service

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

# API Keys (mocked by default)
OPENAI_API_KEY=your_actual_openai_api_key_here

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
- Python 3.11+ for server and client
- Audio system libraries (automatic fallback handling in client)

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
- OpenAI >= 1.0.0 for GPT-4 Vision + Whisper
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