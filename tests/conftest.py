"""Pytest configuration and shared fixtures."""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mock_openai():
    """Mock OpenAI API."""
    with patch('openai.OpenAI') as mock:
        yield mock


@pytest.fixture
def mock_audio():
    """Mock audio recording."""
    with patch('sounddevice.rec') as mock:
        mock.return_value = b"mock_audio_data"
        yield mock


@pytest.fixture
def mock_screenshot():
    """Mock screenshot capture."""
    with patch('PIL.ImageGrab.grab') as mock:
        mock.return_value = Mock()
        yield mock


@pytest.fixture
def test_database_url():
    """Test database URL."""
    return "sqlite:///:memory:" 