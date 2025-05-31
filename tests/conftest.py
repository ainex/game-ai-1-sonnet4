"""Pytest configuration and shared fixtures."""

import tempfile
from typing import Generator
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mock_openai() -> Generator[Mock, None, None]:
    """Mock OpenAI API."""
    with patch("openai.OpenAI") as mock:
        yield mock


@pytest.fixture
def mock_audio() -> Generator[Mock, None, None]:
    """Mock audio recording."""
    with patch("sounddevice.rec") as mock:
        mock.return_value = b"mock_audio_data"
        yield mock


@pytest.fixture
def mock_screenshot() -> Generator[Mock, None, None]:
    """Mock screenshot capture."""
    with patch("PIL.ImageGrab.grab") as mock:
        mock.return_value = Mock()
        yield mock


@pytest.fixture
def test_database_url() -> str:
    """Test database URL."""
    return "sqlite:///:memory:"
