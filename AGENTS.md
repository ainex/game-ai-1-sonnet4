# AI Gaming Assistant - Agent Instructions

## Project Overview

Developing a **Windows desktop application that provides AI-powered gaming assistance for strategy and RPG games**. The system uses voice recording, screenshot capture, and LLM integration to help players with gameplay strategies, character development, and in-game decision making.

## Architecture

- **Client**: Windows desktop app (Python/Tkinter or C#)
- **Server**: Python FastAPI backend (cloud-deployable)
- **Database**: SQLite for local storage
- **Integration**: Multiple LLM APIs (OpenAI, Claude, etc.)

## Core Development Workflow

This project follows the **AI-Assisted Software Development Workflow** outlined in `context/detailed Software AI Workflow.md`:

1. **Feature Planning**: Create detailed `IMPLEMENTATION_PLAN.md` documents before coding
2. **Dependency Analysis**: AI-assisted identification of relevant code segments
3. **Step-by-Step Implementation**: Follow the detailed plan as single source of truth
4. **Documentation & Cleanup**: Update module READMEs and keep the  implementation plans

## File and Folder Structure

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
├── AGENTS.md                    # This file - agent guidelines
├── README.md                    # Project overview
└── setup.sh                    # Environment setup script
```

## Development Environment Setup

### Prerequisites
- Python 3.11+ for server and client
- SQLite3 for database
- Audio system support (portaudio/pulseaudio)
- Git for version control

### Quick Start Commands
```bash
# Setup development environment
./setup.sh

# Install Python dependencies
pip install -r requirements.txt

# Run server locally
cd server && python -m uvicorn src.main:app --reload --port 8000

# Run client (when implemented)
cd client && python src/main.py

# Run tests
pytest tests/ -v
```

## Development Guidelines

### Code Structure
- Follow clean architecture principles
- Separate client from server completely
- Use dependency injection for testability
- Keep methods focused (max 20-30 lines)
- Comment only complex logic, not obvious code

### Python Code Style
- Follow PEP 8 conventions
- Use Black formatter for code formatting
- Use isort for import sorting
- Use type hints for all function signatures
- Maximum line length: 88 characters (Black default)
- Use docstrings for all public functions and classes

### Testing Requirements
- **Write tests FIRST** for core functionality
- **Mock all external API calls** by default
- Use `pytest` with `pytest-asyncio` for async code
- Test coverage should be >80%
- Use `responses` library for HTTP mocking

### Mock Strategy for Offline Development

All external services MUST be mocked:
- OpenAI API calls
- Claude API calls
- Speech-to-text services
- Text-to-speech services
- Any HTTP requests
- Screenshot capture (use test images)
- Audio recording (use test audio files)

## Critical Dependencies

### Core Framework
- **FastAPI** - REST API framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Audio/Visual Processing
- **sounddevice** - Audio capture
- **Pillow** - Image processing
- **pygame** - Additional audio support

### HTTP & APIs
- **requests** - HTTP client
- **aiohttp** - Async HTTP client
- **httpx** - Modern HTTP client

### Testing & Mocking
- **pytest** - Testing framework
- **responses** - HTTP mocking
- **faker** - Test data generation

## Implementation Plan Workflow

### Before Starting Any Feature:
1. **Create Implementation Plan**: Generate `IMPLEMENTATION_PLAN.md` with:
   - General solution description (`sd` section)
   - Dependencies and dependants investigation
   - Detailed step-by-step action plan
   - Test and documentation planning (optional)

2. **Review and Validate Plan**: Ensure the plan is comprehensive before implementation

3. **Follow the Plan**: Use `IMPLEMENTATION_PLAN.md` as single source of truth during development

4. **Post-Implementation Cleanup**:
   - Update relevant module `README.md` files
   - Delete `IMPLEMENTATION_PLAN.md` after successful implementation

## Validation and Testing

### Pre-Commit Checks
Run these commands before committing code:
```bash
# Code formatting and linting
python -m black server/ client/ tests/
python -m isort server/ client/ tests/
python -m flake8 server/ client/ tests/

# Type checking
python -m mypy server/src/

# Run all tests
python -m pytest tests/ -v --cov=server/src/

# Security checks
python -m bandit -r server/src/
```

### Test Commands
```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=server/src --cov-report=html

# Run only unit tests
pytest tests/unit/ -v

# Run integration tests
pytest tests/integration/ -v
```

## AI Agent Instructions

### Code Analysis and Understanding
- Read `context/detailed Software AI Workflow.md` to understand the project methodology
- Check for existing `IMPLEMENTATION_PLAN.md` files before starting work
- Always analyze dependencies and related code before making changes
- Focus on the client-server architecture separation

### Implementation Approach
- **Always create or update `IMPLEMENTATION_PLAN.md` first** before coding
- Start with server-side API endpoints
- Create comprehensive mocks for external services
- Build client after server API is stable
- Test each component thoroughly before integration

### Before Starting Implementation
1. Verify all dependencies are installed: `python -c "import fastapi, sqlalchemy, pytest, sounddevice, PIL"`
2. Create basic project structure
3. Set up pytest configuration
4. Write failing tests for core features first

### Testing and Validation
- Run the full test suite after any changes: `pytest tests/ -v`
- Ensure code formatting: `python -m black server/ client/ tests/`
- Check imports: `python -m isort server/ client/ tests/`
- Validate with linter: `python -m flake8 server/ client/ tests/`
- Verify type hints: `python -m mypy server/src/`

### Documentation Updates
- Update module `README.md` files when functionality changes
- Add docstrings to all new functions and classes
- Include usage examples in documentation
- Update the main `README.md` if adding major features

## Pull Request Guidelines

### PR Title Format
`[component] Brief description of changes`

Examples:
- `[server] Add screenshot analysis endpoint`
- `[client] Implement voice recording UI`
- `[tests] Add unit tests for LLM integration`

### PR Description Template
```markdown
## Summary
Brief description of what this PR does.

## Implementation Plan Reference
Link to the IMPLEMENTATION_PLAN.md that guided this work (if applicable).

## Changes Made
- List of specific changes
- Files modified or added
- New dependencies introduced

## Testing
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] External APIs properly mocked
- [ ] Code coverage maintained or improved
- [ ] Manual testing completed

## Documentation
- [ ] Code is properly documented
- [ ] README.md updated if needed
- [ ] API documentation updated

## Checklist
- [ ] Code follows project style guidelines
- [ ] Linting passes without errors
- [ ] Type hints are included
- [ ] Security considerations addressed
- [ ] External dependencies mocked for testing
```

## Architecture Notes

### Current State
- Project is for AI gaming assistance
- Client-server architecture with clear separation
- Designed for offline development with comprehensive mocking
- Focus on voice recording, screenshot capture, and LLM integration

### Key Features to Implement
- Voice recording and processing
- Screenshot capture and analysis
- LLM integration (OpenAI, Claude)
- Local data storage with SQLite
- REST API for client-server communication
- Desktop UI for user interaction

## Troubleshooting

### Common Issues
1. **Audio Issues**: Check portaudio/pulseaudio installation
2. **Import Errors**: Ensure virtual environment is activated
3. **API Mock Failures**: Verify `responses` library setup
4. **Database Issues**: Check SQLite installation and permissions

### Getting Help
- Check existing documentation in `context/` directory
- Review the detailed workflow documentation
- Look for similar patterns in existing codebase
- Create detailed issue descriptions with error logs

## Security Considerations

- Never commit API keys or sensitive credentials
- Use environment variables for LLM API configurations
- Mock all external API calls in tests
- Implement input validation for voice/image data
- Secure local SQLite database access
- Validate all user inputs before processing

## Environment Variables

```bash
# Development settings
DEBUG=true
LOG_LEVEL=INFO
ENVIRONMENT=development

# API Keys (use mocks in development)
OPENAI_API_KEY=mock_key_for_testing
CLAUDE_API_KEY=mock_key_for_testing
GITHUB_API_KEY=mock_key_for_testing

# Database
DATABASE_URL=sqlite:///./game_assistant.db

# Server settings
HOST=localhost
PORT=8000

# Audio settings
AUDIO_SAMPLE_RATE=44100
AUDIO_CHANNELS=1

# Screenshot settings
SCREENSHOT_QUALITY=85
MAX_IMAGE_SIZE=1920x1080
```
