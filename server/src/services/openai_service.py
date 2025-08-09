"""OpenAI API service for LLM integration."""

import logging
import base64
from functools import lru_cache
from typing import Optional, Dict, Any
import os
from pathlib import Path
import requests

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

# Import server config and web search service
from ..core import get_server_config
from .web_search_service import get_web_search_service


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
            
            # Get the appropriate model from config
            config = get_server_config()
            model_name = config.get_openai_model(model)
            
            # Check if this is the search-enabled model
            is_search_model = (model == "gpt-4o-search-preview" or model_name == "gpt-4o-search-preview")
            
            # Prepare user content - start with the question
            user_content = [
                {
                    "type": "text",
                    "text": question_text
                }
            ]
            
            # If using search model, perform web search and add results to context
            if is_search_model:
                try:
                    logger.info("🔍 Using search-enabled model - performing web search")
                    search_service = get_web_search_service()
                    
                    # Extract search queries from the user's question
                    search_queries = search_service.extract_search_queries_from_text(question_text)
                    
                    all_search_results = []
                    for query in search_queries:
                        search_results = search_service.search(query, max_results=3)
                        all_search_results.extend(search_results)
                    
                    if all_search_results:
                        # Format search results for LLM
                        formatted_results = search_service.format_search_results_for_llm(all_search_results)
                        
                        # Add search results to user content
                        user_content.insert(0, {
                            "type": "text", 
                            "text": f"Additional context from web search:\n\n{formatted_results}\n\nUser's question about the game screenshot:"
                        })
                        
                        logger.info(f"🔍 Added {len(all_search_results)} search results to context")
                    else:
                        logger.warning("🔍 No search results found")
                        
                except Exception as search_error:
                    logger.error(f"❌ Web search failed: {search_error}")
                    # Continue without search results rather than failing completely
            
            # Add the screenshot to user content
            # Add detail level for better image processing
            image_content = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                }
            }
            
            # Add high detail for game screenshots
            image_content["image_url"]["detail"] = "high"
            
            user_content.append(image_content)
            
            # Prepare the message for GPT-4 Vision
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ]
            
            logger.info(f"🤖 Sending request to OpenAI model: {model_name}...")
            
            # Log message structure for debugging GPT-4.1
            if "gpt-4.1" in model_name:
                logger.info(f"🔍 GPT-4.1 request - Message structure: System: {len(messages[0]['content'])} chars, User content items: {len(messages[1]['content'])}")
                for i, item in enumerate(messages[1]['content']):
                    if item['type'] == 'text':
                        logger.info(f"  - Item {i}: Text - {len(item['text'])} chars")
                    elif item['type'] == 'image_url':
                        logger.info(f"  - Item {i}: Image - base64 data present")
            
            # GPT-5 Responses API path (no fallback)
            if model_name == "gpt-5": 
                # Use Responses API for GPT-5
                logger.info(f"🧠 Using Responses API for {model_name} with web search enabled")
                
                # Format input for Responses API - combine text and image
                response_params = {
                    "model": model_name,  # Use model name directly (e.g., gpt-5)
                    "tools": [{"type": "web_search"}],
                    "max_output_tokens": 16000  # Responses API uses max_output_tokens
                }
                
                # Build input array with role and content structure for Responses API
                input_array = [{
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"{system_prompt}\n\n{question_text}"
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{base64_image}"
                        }
                    ]
                }]
                
                response_params["input"] = input_array
                
                # Create response using Responses API with requests library
                logger.info(f"📤 Sending request to Responses API with params: {response_params.keys()}")
                response = requests.post(
                    "https://api.openai.com/v1/responses",
                    headers={
                        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                        "Content-Type": "application/json"
                    },
                    json=response_params
                )
                
                # Log error details if request failed
                if response.status_code != 200:
                    logger.error(f"❌ Responses API error: {response.status_code}")
                    logger.error(f"❌ Error response: {response.text}")
                
                response.raise_for_status()  # Raise error for bad status codes
            else:
                # Use Chat Completions API for other models
                completion_params = {
                    "model": model_name,
                    "messages": messages,
                    "max_tokens": 1000,
                    "temperature": 0.7
                }
                response = self._client.chat.completions.create(**completion_params)
            
            # Handle different response formats
            if model_name == "gpt-5":
                # Handle Responses API format
                logger.info(f"🤖 Full Responses API response: {response}")
                
                if hasattr(response, 'json'):
                    response_data = response.json()
                else:
                    response_data = response
                
                # Extract text content from Responses API format
                ai_response = ""
                
                # Check if response has 'output' field (new Responses API format)
                if isinstance(response_data, dict) and "output" in response_data:
                    output_list = response_data["output"]
                    # Look for message type in the output array
                    for item in output_list:
                        if item.get("type") == "message" and item.get("content"):
                            for content_item in item["content"]:
                                if content_item.get("type") == "output_text":
                                    ai_response = content_item.get("text", "")
                                    break
                            if ai_response:
                                break
                elif isinstance(response_data, list):
                    # Fallback for list format
                    for item in response_data:
                        if item.get("type") == "message" and item.get("content"):
                            for content_item in item["content"]:
                                if content_item.get("type") == "output_text":
                                    ai_response = content_item.get("text", "")
                                    break
                            if ai_response:
                                break
                
                if not ai_response:
                    logger.error(f"❌ Could not extract text from response")
                    return "Error: Could not extract text from GPT-5 response"
            else:
                # Handle Chat Completions API format
                logger.info(f"🤖 Full OpenAI response object: {response}")
                
                # Check if response has content
                if not response.choices:
                    logger.error("❌ OpenAI returned no choices")
                    return "Error: OpenAI returned no response choices"
                
                ai_response = response.choices[0].message.content
                
                # Check for empty response
                if not ai_response:
                    logger.error(f"❌ OpenAI returned empty content. Full response: {response}")
                    # Log usage details
                    if hasattr(response, 'usage'):
                        usage = response.usage
                        logger.error(f"📊 Token usage - Total: {usage.total_tokens}, Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens}")
                    return "Error: OpenAI returned an empty response"
            
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