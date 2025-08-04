"""Anthropic Claude API service for multimodal LLM integration."""

import logging
import base64
from functools import lru_cache
from typing import Optional
import os
from pathlib import Path

# Set up logging first
logger = logging.getLogger(__name__)

# Secure environment loading
try:
    from dotenv import load_dotenv
    # Load .env from project root (3 levels up from this file)
    project_root = Path(__file__).parent.parent.parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=False)  # Don't override existing env vars
        logger.info(f"✅ Loaded environment from {env_path}")
    else:
        logger.info("ℹ️ No .env file found, using system environment variables")
except ImportError:
    logger.warning("⚠️ python-dotenv not available, using system environment variables only")

try:
    import anthropic
    logger.info("✅ Anthropic library available")
except ImportError:
    logger.warning("⚠️ Anthropic library not available")
    anthropic = None

# Import server config
from ..core import get_server_config


class ClaudeService:
    """Service for Anthropic Claude API integration."""

    def __init__(self) -> None:
        if anthropic is None:
            logger.warning("⚠️ Claude service initialized without Anthropic library")
            self._client = None
        else:
            try:
                api_key = os.getenv("ANTHROPIC_API_KEY")
                
                # Secure API key validation
                if not api_key:
                    logger.warning("⚠️ ANTHROPIC_API_KEY not found - using mock mode")
                    self._client = None
                elif api_key == "mock_key_for_testing":
                    logger.warning("⚠️ Using mock API key - using mock mode")
                    self._client = None
                elif len(api_key) < 20:  # Basic validation
                    logger.error("❌ ANTHROPIC_API_KEY appears invalid (too short) - using mock mode")
                    self._client = None
                elif not api_key.startswith("sk-ant-"):
                    logger.error("❌ ANTHROPIC_API_KEY appears invalid (wrong format) - using mock mode")
                    self._client = None
                else:
                    # Mask API key in logs for security
                    masked_key = f"{api_key[:10]}...{api_key[-4:]}"
                    logger.info(f"🔑 Using Anthropic API key: {masked_key}")
                    
                    self._client = anthropic.Anthropic(api_key=api_key)
                    logger.info("✅ Claude client initialized successfully")
                    
            except Exception as e:
                logger.error(f"❌ Claude client initialization failed: {e}")
                self._client = None

    def analyze_game_situation(
        self, 
        screenshot_bytes: bytes, 
        question_text: str, 
        system_prompt: str = "You are the greatest gamer and assistant. Here is my game situation screenshot and my question. Provide specific, actionable advice for the player.",
        model: Optional[str] = None
    ) -> str:
        """
        Analyze a game screenshot and answer a question using Claude's vision model.
        
        Args:
            screenshot_bytes: Screenshot image as bytes
            question_text: User's question (transcribed from audio)
            system_prompt: System prompt for the AI assistant
            model: Optional model name (e.g., "claude-3.5-sonnet", "claude-4-sonnet")
            
        Returns:
            AI response as text
        """
        logger.info(f"🤖 Analyzing game situation with Claude")
        logger.info(f"📸 Screenshot size: {len(screenshot_bytes)} bytes")
        logger.info(f"🎤 Question: '{question_text}'")
        logger.info(f"🤖 System prompt: '{system_prompt}'")
        
        if self._client is None:
            logger.warning("⚠️ Claude client not available - returning mock response")
            return f"Mock Claude response: Based on the screenshot, I can see a game situation. You asked: '{question_text}'. Here's some helpful gaming advice for your situation."
        
        try:
            # Encode screenshot as base64
            base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            # Prepare the message for Claude
            message = {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": base64_image
                        }
                    },
                    {
                        "type": "text",
                        "text": question_text
                    }
                ]
            }
            
            # Get the appropriate model from config
            config = get_server_config()
            model_name = config.get_claude_model(model)
            
            logger.info(f"🤖 Sending request to Claude model: {model_name}...")
            
            response = self._client.messages.create(
                model=model_name,
                max_tokens=1000,
                temperature=0.7,
                system=system_prompt,
                messages=[message]
            )
            
            ai_response = response.content[0].text
            logger.info(f"🤖 Claude response: '{ai_response}'")
            
            return ai_response
            
        except Exception as e:
            logger.error(f"❌ Claude API call failed: {e}")
            return f"Sorry, I couldn't analyze the game situation right now. Error: {str(e)}"


@lru_cache(maxsize=1)
def get_claude_service() -> "ClaudeService":
    """Cached service instance."""
    logger.info("🏭 Creating Claude service instance")
    return ClaudeService()