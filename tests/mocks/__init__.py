"""Mock implementations for external services."""

from unittest.mock import Mock


class MockOpenAI:
    """Mock OpenAI API client."""

    def __init__(self) -> None:
        """Initialize the mock OpenAI client."""
        self.chat = Mock()
        self.chat.completions = Mock()
        self.chat.completions.create = Mock()


class MockClaude:
    """Mock Claude API client."""

    def __init__(self) -> None:
        """Initialize the mock Claude client."""
        self.messages = Mock()
        self.messages.create = Mock()


# Common mock responses
MOCK_AUDIO_DATA = b"mock_audio_data"
MOCK_IMAGE_DATA = b"mock_image_data"
MOCK_LLM_RESPONSE = "This is a mock LLM response for testing."
