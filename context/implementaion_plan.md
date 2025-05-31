# Implementation Plan: Game AI Assistant for Sims 4

## Executive Summary

This implementation plan outlines the development of a Windows 11 desktop application that provides AI-powered gaming assistance for The Sims 4 and other strategy/RPG games. The system uses hotkey activation, voice recording, screenshot capture, and multimodal LLM integration to provide contextual gaming advice.

## Architecture Overview

### System Components
- **Client Application** (Windows Desktop - C#/WPF or Python/Tkinter)
- **Server Backend** (Python FastAPI - cloud-deployable)
- **Integration Layer** (APIs for speech, vision, and LLM services)
- **Data Layer** (SQLite for local history, future vector DB integration)

### C4 Architecture Diagrams Required
1. **Context Diagram**: User, Game AI Assistant, External APIs (OpenAI, Claude, etc.)
2. **Container Diagram**: Client App, Backend Server, Database, External Services
3. **Component Diagram**: Internal modules and their interactions

## Technical Requirements Analysis

### Core Functionality
1. **Hotkey System**: Global hotkey registration (Ctrl+Shift+I)
2. **Screen Capture**: Multi-monitor support with ultrawide (3440x1440) optimization
3. **Voice Recording**: VAD (Voice Activity Detection) with silence timeout
4. **Speech-to-Text**: Russian language support via API
5. **Multimodal LLM Integration**: Screenshot + transcribed text processing
6. **Response Handling**: Text-to-speech output and text display
7. **History Management**: Local storage with copy functionality

### Environment Configuration for Codex

#### Container Setup Script
```bash
# Python environment setup
apt-get update && apt-get install -y \
    python3.11 python3-pip \
    portaudio19-dev \
    xvfb \
    ffmpeg \
    sqlite3

# Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Test environment verification
python -c "import sounddevice, PIL, requests, sqlite3; print('Environment OK')"
```

#### Dependencies (requirements.txt)
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
sounddevice>=0.4.6
pillow>=10.1.0
requests>=2.31.0
aiohttp>=3.9.0
python-multipart>=0.0.6
sqlalchemy>=2.0.23
alembic>=1.13.0
pytest>=7.4.3
pytest-asyncio>=0.21.1
httpx>=0.25.2
python-dotenv>=1.0.0
keyboard>=0.13.5  # for Windows client
pyaudio>=0.2.11   # for Windows client
pygame>=2.5.2     # for audio feedback
tkinter-tooltip>=2.0.0  # for UI
```

#### Test Configuration
- **Mocked Tests**: Mock all external API calls (OpenAI, speech services)
- **Integration Tests**: Use test API keys with rate limiting safeguards
- **Production Mode**: Full API integration without mocks

## Implementation Structure

### Client Application (Windows Desktop)
```
client/
├── src/
│   ├── core/
│   │   ├── hotkey_manager.py
│   │   ├── screen_capture.py
│   │   ├── voice_recorder.py
│   │   └── api_client.py
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── history_panel.py
│   │   └── settings_dialog.py
│   ├── utils/
│   │   ├── audio_utils.py
│   │   ├── config_manager.py
│   │   └── visual_feedback.py
│   └── main.py
├── tests/
├── config/
└── assets/
```

### Server Backend (Python FastAPI)
```
server/
├── src/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── assistant.py
│   │   │   └── health.py
│   │   └── middleware/
│   ├── core/
│   │   ├── llm_router.py
│   │   ├── speech_service.py
│   │   ├── image_processor.py
│   │   └── memory_manager.py  # Future vector DB integration
│   ├── models/
│   │   ├── request_models.py
│   │   └── response_models.py
│   ├── services/
│   │   ├── openai_service.py
│   │   ├── claude_service.py
│   │   ├── huggingface_service.py
│   │   └── perplexity_service.py
│   └── utils/
├── tests/
├── alembic/
└── config/
```

## Detailed Component Specifications

### 1. Hotkey System
- **Technology**: `keyboard` library for global hotkey detection
- **Implementation**: Background thread monitoring Ctrl+Shift+I
- **Error Handling**: Permission checks, conflict detection

### 2. Screen Capture Module
- **Primary**: PIL/Pillow for cross-platform compatibility
- **Optimization**: Ultrawide support (3440x1440) with region detection
- **Output**: PNG format with compression for API efficiency

### 3. Voice Recording System
- **Library**: `sounddevice` for audio capture
- **VAD**: Silence detection with configurable timeout (2-3 seconds)
- **Format**: WAV/MP3 for API compatibility
- **Feedback**: Audio cues (beep sounds) using `pygame`

### 4. Speech-to-Text Integration
- **Primary**: Hugging Face Whisper API (Russian support)
- **Fallback**: OpenAI Whisper API
- **Local Option**: whisper-cpp for offline processing

### 5. LLM Router and Integration
```python
class LLMRouter:
    def __init__(self):
        self.providers = {
            'openai': OpenAIService(),
            'claude': ClaudeService(),
            'google': GoogleAIService(),
            'huggingface': HuggingFaceService()
        }

    async def process_request(self, text: str, image: bytes, provider: str):
        # Route to appropriate LLM service
        # Handle multimodal input
        # Return structured response
```

### 6. Visual Feedback System
- **Recording Indicator**: Screen border overlay (red frame)
- **Processing Indicator**: Animated border or LED keyboard integration
- **Technology**: Tkinter overlay or Windows API direct calls

### 7. History Management
- **Database**: SQLite for local storage
- **Schema**:
  ```sql
  CREATE TABLE interactions (
      id INTEGER PRIMARY KEY,
      timestamp DATETIME,
      screenshot_path TEXT,
      question_text TEXT,
      question_audio_path TEXT,
      response_text TEXT,
      response_audio_path TEXT,
      llm_provider TEXT
  );
  ```

## Testing Strategy

### Unit Tests
- Mock all external API calls
- Test core functionality in isolation
- Coverage target: >80%

### Integration Tests
- Test API integrations with real services (rate-limited)
- End-to-end workflow testing
- Screenshot processing validation

### Performance Tests
- Response time benchmarks
- Memory usage profiling
- Audio quality validation

## Deployment Configuration

### Local Development
```yaml
# docker-compose.yml
version: '3.8'
services:
  game-ai-backend:
    build: ./server
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
    volumes:
      - ./data:/app/data
```

### Production Deployment
- **Backend**: Cloud deployment (AWS/Azure/GCP)
- **Client**: Windows installer with auto-update capability
- **Configuration**: Environment-based API key management

## API Integration Specifications

### LLM Services Configuration
```python
LLM_CONFIGS = {
    'openai': {
        'model': 'gpt-4-vision-preview',
        'max_tokens': 1000,
        'temperature': 0.7
    },
    'claude': {
        'model': 'claude-3-sonnet-20240229',
        'max_tokens': 1000
    },
    'google': {
        'model': 'gemini-pro-vision'
    }
}
```

### Speech Services
- **Primary**: Hugging Face Transformers (whisper-large-v3)
- **Backup**: OpenAI Whisper API
- **TTS**: OpenAI TTS or Azure Speech Services

## Security Considerations

### API Key Management
- Local secure storage (Windows Credential Manager)
- Environment variable fallbacks
- Key rotation support

### Data Privacy
- Local screenshot storage with cleanup
- Audio recording deletion after processing
- GDPR-compliant data handling

## Future Extensibility

### Memory Integration Placeholder
```python
class MemoryManager:
    """Placeholder for future vector database integration"""

    def __init__(self):
        self.vector_db = None  # Future: ChromaDB, Pinecone, etc.

    async def store_interaction(self, interaction: dict):
        # Future: Store embeddings for context retrieval
        pass

    async def retrieve_context(self, query: str) -> List[dict]:
        # Future: Semantic search for relevant past interactions
        return []
```

### Mobile Client Preparation
- RESTful API design for future Android client
- Shared authentication system
- Cross-platform data synchronization

## Success Metrics

### Performance Targets
- **Activation Time**: <2 seconds from hotkey to recording
- **Processing Time**: <10 seconds for complete request cycle
- **Accuracy**: >90% speech recognition accuracy for Russian
- **Reliability**: 99%+ uptime for local components

### User Experience Goals
- Intuitive single-hotkey activation
- Clear visual/audio feedback
- Accurate game-specific advice
- Seamless history access and management

This implementation plan provides a comprehensive roadmap for developing the Game AI Assistant while maintaining clean architecture, testability, and future extensibility.
