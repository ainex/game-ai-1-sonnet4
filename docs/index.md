# AI Gaming Assistant Documentation

Welcome to the AI Gaming Assistant project documentation.

## Overview

This project is a Windows desktop application that provides AI-powered gaming assistance for strategy and RPG games. The system uses voice recording, screenshot capture, and LLM integration to help players with gameplay strategies, character development, and in-game decision making.

## Architecture

- **Client**: Windows desktop app (Python/Tkinter or C#)
- **Server**: Python FastAPI backend (cloud-deployable)
- **Database**: SQLite for local storage
- **Integration**: Multiple LLM APIs (OpenAI, Claude, etc.)

## Quick Start

1. Set up the development environment: `./setup.sh`
2. Activate the virtual environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests: `pytest tests/ -v`
5. Start the server: `cd server && python -m uvicorn src.main:app --reload`

## Development Workflow

This project follows the AI-Assisted Software Development Workflow:

1. Create detailed `IMPLEMENTATION_PLAN.md` documents
2. Analyze dependencies and related code
3. Implement features following the plan
4. Update documentation and clean up

For more details, see the [AGENTS.md](../AGENTS.md) file.
