"""Test environment setup and dependencies."""

import sys

import pytest  # type: ignore


def test_python_version() -> None:
    """Test that we're using Python 3.11+."""
    assert sys.version_info >= (3, 11)


def test_critical_imports() -> None:
    """Test that all critical packages can be imported."""
    try:
        import asyncio  # noqa: F401
        import json  # noqa: F401
        import os  # noqa: F401
        import sqlite3  # noqa: F401

        import aiohttp  # type: ignore # noqa: F401
        import fastapi  # type: ignore # noqa: F401
        import httpx  # type: ignore # noqa: F401
        import PIL  # type: ignore # noqa: F401
        import pydantic  # type: ignore # noqa: F401
        import requests  # noqa: F401
        import sounddevice  # noqa: F401
        import sqlalchemy  # type: ignore # noqa: F401
        import uvicorn  # type: ignore # noqa: F401
    except ImportError as e:
        pytest.fail(f"Critical import failed: {e}")


def test_audio_system() -> None:
    """Test audio system availability."""
    try:
        import sounddevice as sd  # noqa: F401

        # Just check if we can query devices without actually using audio
        devices = sd.query_devices()
        assert len(devices) > 0
    except Exception as e:
        pytest.skip(f"Audio system not available: {e}")


@pytest.mark.mock  # type: ignore
def test_mock_libraries() -> None:
    """Test that mocking libraries are available."""
    try:
        from unittest.mock import Mock, patch  # noqa: F401

        import faker  # type: ignore # noqa: F401
        import responses  # noqa: F401
    except ImportError as e:
        pytest.fail(f"Mock library import failed: {e}")
