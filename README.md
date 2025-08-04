# AI Gaming Assistant

A **Windows desktop application that provides AI-powered gaming assistance for strategy and RPG games**. The system uses voice recording, screenshot capture, and LLM integration to help players with gameplay strategies, character development, and in-game decision making.

## 🏗️ Architecture

- **Client**: Windows desktop app (Python/Tkinter or C#)
- **Server**: Python FastAPI backend (cloud-deployable)
- **Database**: SQLite for local storage
- **Integration**: Multiple LLM APIs (OpenAI, Claude, etc.)

## 🚀 Quick Start

1. **Setup the development environment:**
   ```bash
   ./setup.sh
   ```

2. **Activate the virtual environment:**
   
   **Linux/macOS:**
   ```bash
   source venv/bin/activate
   ```
   
   **Windows (PowerShell):**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   venv\Scripts\activate
   ```

3. **Start the server:**
   ```bash
   cd server && python -m uvicorn src.main:app --reload --port 8000
   ```

4. **Run the client:**
   ```bash
   cd client && python src/main.py
   ```

## 🎮 How to Use

### Voice + Screenshot Analysis with OpenAI (Recommended)
Press **Ctrl+Shift+V** for the complete experience:
1. 📸 **Automatic screenshot capture** of your game
2. 🎵 **Pleasant chime sound** indicates recording start
3. 🎤 **Speak your question** (e.g., "What should I do in this situation?")
4. 🔇 **Auto-stop** after 2 seconds of silence (no need to hold keys!)
5. 🎵 **Pleasant chime** confirms recording ended
6. 🤖 **OpenAI analyzes both** your screenshot and voice using GPT-4 Vision
7. 🔊 **Spoken response** with helpful advice

### Alternative Hotkeys
- **Ctrl+Shift+S**: Screenshot + AI description (no voice input)
- **Ctrl+Shift+A**: Screenshot + text analysis only
- **Ctrl+Shift+T**: Test text-to-speech service

5. **Verify the setup:**
   ```bash
   pytest tests/ -v
   ```

### Local AI Features

The server includes offline image captioning and text-to-speech services with GPU acceleration support.

**API Endpoints:**
- `POST /api/v1/image/analyze` - describe uploaded screenshot
- `POST /api/v1/stt/transcribe` - transcribe audio to text
- `POST /api/v1/tts/speak` - synthesize speech from text
- `POST /api/v1/game/analyze-and-speak` - analyze screenshot and return spoken description
- `POST /api/v1/game/analyze-image-and-voice` - analyze both screenshot + voice and return intelligent response
- `POST /api/v1/openai/analyze-game-with-voice` - **NEW!** OpenAI-powered analysis with GPT-4 Vision + Whisper
- `POST /api/v1/openai/analyze-game-text-only` - **NEW!** OpenAI-powered analysis with text input

**GPU Acceleration:**
- Supports NVIDIA RTX/GTX graphics cards
- 10-20x faster TTS generation with CUDA
- See [CUDA Setup Guide](docs/cuda-setup-guide.md) for installation instructions

**Quick GPU Check:**
```bash
python scripts/verify_cuda.py
```

### Windows 11 Setup Notes

The `setup.sh` script targets Linux environments. On Windows 11:

1. Install **Python 3.11** from [python.org](https://www.python.org/).
2. **Install Visual Studio Build Tools** (required for TTS):
   ```powershell
   winget install --id=Microsoft.VisualStudio.2022.BuildTools -e
   ```
   **Restart your computer after installation.**

3. Create a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
4. Install dependencies manually:
   ```powershell
   pip install -r requirements.txt
   pip install keyboard
   ```

**Troubleshooting**: If you encounter TTS installation errors, see our [Windows Troubleshooting Guide](docs/troubleshooting-windows-installation.md).

## 📁 Project Structure

```
game-ai-1-sonnet4/
├── server/src/                  # Backend FastAPI code
│   ├── api/                     # API endpoints and middleware
│   │   ├── endpoints/           # REST API endpoints
│   │   └── middleware/          # Request/response middleware
│   ├── core/                    # Core business logic
│   ├── models/                  # Database models
│   ├── services/                # Business services
│   └── utils/                   # Server utilities
├── client/src/                  # Desktop client code
│   ├── core/                    # Core client logic
│   ├── ui/                      # User interface components
│   └── utils/                   # Client utilities
├── shared/                      # Shared models/utilities
├── tests/                       # All tests
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── mocks/                   # Mock implementations
├── config/                      # Configuration files
│   ├── development/             # Development configs
│   ├── production/              # Production configs
│   └── test/                    # Test configs
├── docs/                        # Documentation
├── context/                     # Project documentation and manuals
├── AGENTS.md                    # Codex agent guidelines
├── setup.sh                    # Environment setup script
└── requirements.txt             # Python dependencies
```

## 🎮 Key Features

### Voice Processing
- **NEW!** Real-time voice recording with pleasant audio feedback (like Alexa)
- **NEW!** Automatic silence detection (no push-to-talk required)
- **NEW!** Local speech-to-text using Whisper AI
- Natural language processing for game commands
- Voice-activated assistance during gameplay

### Screenshot Analysis
- Automatic game screen capture
- AI-powered image analysis of game UI
- Context-aware gameplay suggestions

### LLM Integration
- **OpenAI GPT-4 Vision** for screenshot analysis and question answering
- **OpenAI Whisper** for high-quality audio transcription
- **Customizable system prompts** for different game scenarios
- Multiple LLM provider support (OpenAI, Claude)
- Intelligent gameplay advice and strategies
- Character development recommendations

### Local Data Storage
- SQLite database for user preferences
- Gameplay history and analytics
- Offline functionality support

## 🤖 AI-Assisted Development Workflow

This project follows a structured AI-assisted software development workflow:

1. **Feature Planning**: Create detailed `IMPLEMENTATION_PLAN.md` documents before coding
2. **Dependency Analysis**: AI-assisted identification of relevant code segments
3. **Step-by-Step Implementation**: Follow the detailed plan as single source of truth
4. **Documentation & Cleanup**: Update module READMEs and remove implementation plans

For complete details, see [`AGENTS.md`](AGENTS.md) and [`context/detailed Software AI Workflow.md`](context/detailed%20Software%20AI%20Workflow.md).

## 🛠️ Development Tools

The project comes pre-configured with:

- **FastAPI**: Modern REST API framework
- **SQLAlchemy**: Database ORM with SQLite
- **Pydantic**: Data validation and serialization
- **Audio Processing**: sounddevice, pyaudio, pygame
- **Image Processing**: Pillow for screenshot analysis
- **Testing**: pytest with comprehensive mocking
- **Code Quality**: Black, isort, flake8, mypy, bandit
- **Pre-commit Hooks**: Automated code quality checks

## 🧪 Testing & Mocking

All external services are mocked for offline development:

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

### Mock Strategy
- OpenAI and Claude API calls
- Voice recording and audio processing
- Screenshot capture and image analysis
- All HTTP requests and external services

## 📝 Code Quality

Ensure code quality with automated tools:

```bash
# Format code
python -m black server/ client/ tests/
python -m isort server/ client/ tests/

# Lint code
python -m flake8 server/ client/ tests/
python -m mypy server/src/

# Security checks
python -m bandit -r server/src/

# Run pre-commit hooks
pre-commit run --all-files
```

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:

```bash
# Development settings
DEBUG=true
ENVIRONMENT=development

# API Keys (use mocks in development)
OPENAI_API_KEY=your_actual_openai_api_key_here
CLAUDE_API_KEY=mock_key_for_testing
GITHUB_API_KEY=mock_key_for_testing

# Database
DATABASE_URL=sqlite:///./game_assistant.db

# Audio settings
AUDIO_SAMPLE_RATE=44100
AUDIO_CHANNELS=1

# Screenshot settings
SCREENSHOT_QUALITY=85
MAX_IMAGE_SIZE=1920x1080
```

### Dependencies
- **Python 3.11+** for server and client
- **SQLite3** for database
- **Audio system** support (portaudio/pulseaudio)
- **System packages** for audio/visual processing

## 📚 Documentation

- [`AGENTS.md`](AGENTS.md) - Complete contributor guide for AI agents
- [`context/`](context/) - Project methodology and Codex documentation
- [`docs/api/`](docs/api/) - API documentation and schemas
- [`docs/`](docs/) - User guides and examples

## 🚀 Ready for OpenAI Codex

This repository is fully prepared for OpenAI Codex agent work:

- ✅ **AGENTS.md** file with comprehensive guidelines
- ✅ **Setup script** with all dependencies and system packages
- ✅ **Client-server architecture** with clear separation
- ✅ **Comprehensive mocking** for offline development
- ✅ **Testing framework** with audio/visual test support
- ✅ **Environment configuration** for game integration
- ✅ **Pre-commit hooks** for code quality

The Codex agent will automatically read the `AGENTS.md` file and use the setup script to prepare the development environment with all necessary audio, visual, and LLM integration tools.

## 🎯 Next Steps

1. **Set up OpenAI API Key**: Add your OpenAI API key to the environment variables
2. **Install OpenAI dependency**: Run `pip install openai>=1.0.0`
3. **Test the integration**: Run `python test_openai_integration.py`
4. **Start using**: Press **Ctrl+Shift+V** for OpenAI-powered game assistance!

### OpenAI Setup
```bash
# Add your OpenAI API key to environment
export OPENAI_API_KEY="your_actual_openai_api_key_here"

# Or create a .env file
echo "OPENAI_API_KEY=your_actual_openai_api_key_here" > .env
```

## 🔒 Security & Privacy

- All API keys use mock values in development
- External API calls are mocked by default
- Voice and screenshot data processed locally
- SQLite database for secure local storage
- Input validation for all user data

## 📄 License

This project follows enterprise-scale development practices. See individual files for specific licensing terms.

---

*Built with ❤️ using AI-assisted development practices for the gaming community*
