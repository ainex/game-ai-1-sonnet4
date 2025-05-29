# Sims 4 AI Gaming Assistant

A **Windows desktop application that provides AI-powered gaming assistance for The Sims 4**. The system uses voice recording, screenshot capture, and LLM integration to help players with gameplay strategies, character development, and in-game decision making.

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
   ```bash
   source venv/bin/activate
   ```

3. **Start the server:**
   ```bash
   cd server && python -m uvicorn src.main:app --reload --port 8000
   ```

4. **Run the client (when implemented):**
   ```bash
   cd client && python src/main.py
   ```

5. **Verify the setup:**
   ```bash
   pytest tests/ -v
   ```

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
- Real-time voice recording and transcription
- Natural language processing for game commands
- Voice-activated assistance during gameplay

### Screenshot Analysis
- Automatic game screen capture
- AI-powered image analysis of Sims 4 UI
- Context-aware gameplay suggestions

### LLM Integration
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
OPENAI_API_KEY=mock_key_for_testing
CLAUDE_API_KEY=mock_key_for_testing

# Database
DATABASE_URL=sqlite:///./sims4_assistant.db

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
- ✅ **Environment configuration** for Sims 4 integration
- ✅ **Pre-commit hooks** for code quality

The Codex agent will automatically read the `AGENTS.md` file and use the setup script to prepare the development environment with all necessary audio, visual, and LLM integration tools.

## 🎯 Next Steps

1. Review the [`AGENTS.md`](AGENTS.md) file to understand the development workflow
2. Run `./setup.sh` to prepare your development environment
3. Create your first `IMPLEMENTATION_PLAN.md` for new features
4. Start building the Sims 4 AI assistant with voice and visual capabilities!

## 🔒 Security & Privacy

- All API keys use mock values in development
- External API calls are mocked by default
- Voice and screenshot data processed locally
- SQLite database for secure local storage
- Input validation for all user data

## 📄 License

This project follows enterprise-scale development practices. See individual files for specific licensing terms.

---

*Built with ❤️ using AI-assisted development practices for The Sims 4 gaming community*
