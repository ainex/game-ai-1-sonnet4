"""Test environment setup and dependencies."""

import pytest


def test_python_version() -> None:
    """Test that we're using Python 3.11+."""
    import sys

    assert sys.version_info >= (3, 11)


def test_critical_imports() -> None:
    """Test that all critical packages can be imported."""
    # Standard library imports
    import_tests = [
        "asyncio",
        "json",
        "os",
        "sqlite3",
    ]

    for module in import_tests:
        try:
            __import__(module)
        except ImportError as e:
            pytest.fail(f"Standard library import failed for {module}: {e}")

    # Third party imports
    third_party_tests = [
        "aiohttp",
        "fastapi",
        "httpx",
        "PIL",
        "pydantic",
        "pytest",
        "requests",
        "sounddevice",
        "sqlalchemy",
        "uvicorn",
    ]

    for module in third_party_tests:
        try:
            __import__(module)
        except ImportError as e:
            pytest.fail(f"Third party import failed for {module}: {e}")


def test_audio_system() -> None:
    """Test audio system availability."""
    try:
        import sounddevice as sd

        # Just check if we can query devices without actually using audio
        devices = sd.query_devices()
        assert len(devices) > 0
    except Exception as e:
        pytest.skip(f"Audio system not available: {e}")


@pytest.mark.mock
def test_mock_libraries() -> None:
    """Test that mocking libraries are available."""
    mock_tests = [
        "unittest.mock",
        "faker",
        "responses",
    ]

    for module in mock_tests:
        try:
            __import__(module)
        except ImportError as e:
            pytest.fail(f"Mock library import failed for {module}: {e}")
