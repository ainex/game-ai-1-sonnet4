"""OpenAI API service for LLM integration."""

import logging
import base64
from functools import lru_cache
from typing import Optional, Dict, Any
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
    from openai import OpenAI
    logger.info("✅ OpenAI library available")
except ImportError:
    logger.warning("⚠️ OpenAI library not available")
    OpenAI = None

# Import server config
from ..core import get_server_config


class OpenAIService:
    """Service for OpenAI API integration."""

    def __init__(self) -> None:
        if OpenAI is None:
            logger.warning("⚠️ OpenAI service initialized without OpenAI library")
            self._client = None
        else:
            try:
                api_key = os.getenv("OPENAI_API_KEY")
                
                # Secure API key validation
                if not api_key:
                    logger.warning("⚠️ OPENAI_API_KEY not found - using mock mode")
                    self._client = None
                elif api_key == "mock_key_for_testing":
                    logger.warning("⚠️ Using mock API key - using mock mode")
                    self._client = None
                elif len(api_key) < 20:  # Basic validation
                    logger.error("❌ OPENAI_API_KEY appears invalid (too short) - using mock mode")
                    self._client = None
                elif not api_key.startswith("sk-"):
                    logger.error("❌ OPENAI_API_KEY appears invalid (wrong format) - using mock mode")
                    self._client = None
                else:
                    # Mask API key in logs for security
                    masked_key = f"{api_key[:10]}...{api_key[-4:]}"
                    logger.info(f"🔑 Using OpenAI API key: {masked_key}")
                    
                    self._client = OpenAI(api_key=api_key)
                    logger.info("✅ OpenAI client initialized successfully")
                    
            except Exception as e:
                logger.error(f"❌ OpenAI client initialization failed: {e}")
                self._client = None

    def analyze_game_situation(
        self, 
        screenshot_bytes: bytes, 
        question_text: str, 
        system_prompt: str = "You are a helpful game assistant. Analyze the screenshot and answer the user's question about the game situation.",
        model: Optional[str] = None
    ) -> str:
        """
        Analyze a game screenshot and answer a question using OpenAI's vision model.
        
        Args:
            screenshot_bytes: Screenshot image as bytes
            question_text: User's question (transcribed from audio)
            system_prompt: System prompt for the AI assistant
            model: Optional model name (e.g., "gpt-4o-mini", "gpt-4o", "o3")
            
        Returns:
            AI response as text
        """
        logger.info(f"🤖 Analyzing game situation with OpenAI")
        logger.info(f"📸 Screenshot size: {len(screenshot_bytes)} bytes")
        logger.info(f"🎤 Question: '{question_text}'")
        logger.info(f"🤖 System prompt: '{system_prompt}'")
        
        if self._client is None:
            logger.warning("⚠️ OpenAI client not available - returning mock response")
            return f"Mock response: Based on the screenshot, I can see a game situation. You asked: '{question_text}'. Here's some helpful advice for your game."
        
        try:
            # Encode screenshot as base64
            base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            # Prepare the message for GPT-4 Vision
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
            
            # Get the appropriate model from config
            config = get_server_config()
            model_name = config.get_openai_model(model)
            
            logger.info(f"🤖 Sending request to OpenAI model: {model_name}...")
            
            response = self._client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            logger.info(f"🤖 OpenAI response: '{ai_response}'")
            
            return ai_response
            
        except Exception as e:
            logger.error(f"❌ OpenAI API call failed: {e}")
            return f"Sorry, I couldn't analyze the game situation right now. Error: {str(e)}"

    def transcribe_audio(self, audio_bytes: bytes) -> str:
        """
        Transcribe audio using OpenAI's Whisper API.
        
        Args:
            audio_bytes: Audio file as bytes
            
        Returns:
            Transcribed text
        """
        logger.info(f"🎤 Transcribing audio with OpenAI Whisper: {len(audio_bytes)} bytes")
        
        if self._client is None:
            logger.warning("⚠️ OpenAI client not available - returning mock transcription")
            return "Mock transcription: What should I do in this game situation?"
        
        try:
            # Create a temporary file for the audio
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_bytes)
                audio_path = tmp_file.name
            
            try:
                with open(audio_path, "rb") as audio_file:
                    response = self._client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="text"
                    )
                
                transcription = response.strip()
                logger.info(f"🎤 OpenAI Whisper transcription: '{transcription}'")
                return transcription
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(audio_path)
                except Exception as cleanup_error:
                    logger.warning(f"⚠️ Failed to clean up temporary audio file: {cleanup_error}")
                    
        except Exception as e:
            logger.error(f"❌ OpenAI Whisper transcription failed: {e}")
            return f"Error transcribing audio: {str(e)}"


@lru_cache(maxsize=1)
def get_openai_service() -> "OpenAIService":
    """Cached service instance."""
    logger.info("🏭 Creating OpenAI service instance")
    return OpenAIService() 