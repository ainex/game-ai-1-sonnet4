# API Documentation

This directory contains API documentation for the Sims 4 AI Gaming Assistant.

## Server API Endpoints

### Voice Processing
- `POST /api/voice/record` - Start voice recording
- `POST /api/voice/stop` - Stop recording and process audio
- `GET /api/voice/status` - Get recording status

### Screenshot Analysis
- `POST /api/screenshot/capture` - Capture and analyze screenshot
- `GET /api/screenshot/history` - Get screenshot history

### LLM Integration
- `POST /api/llm/chat` - Send message to LLM
- `GET /api/llm/models` - Get available LLM models

### Game Data
- `GET /api/game/status` - Get Sims 4 game status
- `POST /api/game/advice` - Get gameplay advice

Documentation is automatically generated from FastAPI schemas.
