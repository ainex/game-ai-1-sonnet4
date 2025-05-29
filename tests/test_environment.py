"""Test environment setup and dependencies."""

import pytest


def test_python_version():
    """Test that we're using Python 3.11+."""
    import sys
    assert sys.version_info >= (3, 11)


def test_critical_imports():
    """Test that all critical packages can be imported."""
    try:
        import fastapi
        import uvicorn
        import pydantic
        import sqlalchemy
        import PIL
        import requests
        import aiohttp
        import httpx
        import pytest
        import sqlite3
        import json
        import os
        import asyncio
    except ImportError as e:
        pytest.fail(f"Critical import failed: {e}")


def test_audio_system():
    """Test audio system availability."""
    try:
        import sounddevice as sd
        # Just check if we can query devices without actually using audio
        devices = sd.query_devices()
        assert len(devices) > 0
    except Exception as e:
        pytest.skip(f"Audio system not available: {e}")


@pytest.mark.mock
def test_mock_libraries():
    """Test that mocking libraries are available."""
    try:
        import responses
        import faker
        from unittest.mock import Mock, patch
    except ImportError as e:
        pytest.fail(f"Mock library import failed: {e}")


def test_database_connection():
    """Test that SQLite database connection works."""
    import sqlite3
    
    # Test in-memory database
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO test (name) VALUES (?)", ("test_value",))
    result = cursor.execute("SELECT name FROM test WHERE id = 1").fetchone()
    conn.close()
    
    assert result[0] == "test_value"


def test_fastapi_import():
    """Test that FastAPI can be imported and basic app created."""
    from fastapi import FastAPI
    
    app = FastAPI()
    assert app is not None


def test_async_support():
    """Test that async/await works properly."""
    import asyncio
    
    async def test_async_function():
        return "async_result"
    
    result = asyncio.run(test_async_function())
    assert result == "async_result" 