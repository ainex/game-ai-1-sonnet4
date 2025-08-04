"""OpenAI-powered game analysis endpoint."""

import logging
from io import BytesIO

from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import StreamingResponse

from ...services.openai_service import get_openai_service
from ...services.tts import get_tts_service

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()
openai_service = get_openai_service()
tts_service = get_tts_service()


@router.post("/openai/analyze-game-with-voice")
async def analyze_game_with_openai_and_voice(
    image: UploadFile = File(...),
    audio: UploadFile = File(...),
    system_prompt: str = Form(
        default="You are a helpful game assistant. Analyze the screenshot and answer the user's question about the game situation. Provide specific, actionable advice for the player."
    ),
    model: str = Form(default=None)
) -> StreamingResponse:
    """
    Analyze game screenshot and voice question using OpenAI, then return spoken response.
    
    This endpoint:
    1. Transcribes the audio using OpenAI Whisper
    2. Analyzes the screenshot + question using GPT-4 Vision
    3. Converts the response to speech using local TTS
    """
    logger.info(f"🤖 Received OpenAI-powered game analysis request")
    logger.info(f"📸 Image file: {image.filename}, size: {image.size} bytes")
    logger.info(f"🎵 Audio file: {audio.filename}, size: {audio.size} bytes")
    logger.info(f"🤖 System prompt: '{system_prompt}'")
    logger.info(f"🤖 Model: '{model}' (None = use default)")
    
    try:
        # Read both files
        image_data = await image.read()
        audio_data = await audio.read()
        logger.info(f"📸 Read image data: {len(image_data)} bytes")
        logger.info(f"🎵 Read audio data: {len(audio_data)} bytes")
        
        # Step 1: Transcribe audio using OpenAI Whisper
        logger.info("🎤 Starting OpenAI Whisper transcription...")
        question_text = openai_service.transcribe_audio(audio_data)
        logger.info(f"🎤 Transcribed question: '{question_text}'")
        
        # Step 2: Analyze screenshot + question using OpenAI
        logger.info("🤖 Starting OpenAI analysis...")
        ai_response = openai_service.analyze_game_situation(
            screenshot_bytes=image_data,
            question_text=question_text,
            system_prompt=system_prompt,
            model=model
        )
        logger.info(f"🤖 OpenAI analysis response: '{ai_response}'")
        
        # Step 3: Convert response to speech using local TTS
        logger.info("🔊 Starting TTS generation for OpenAI response...")
        audio_response = tts_service.speak(ai_response)
        logger.info(f"🔊 Generated audio response: {len(audio_response)} bytes")
        
        if len(audio_response) == 0:
            logger.error("❌ TTS generated empty audio!")
            # Return a simple error message as audio
            error_text = "Sorry, I couldn't generate speech for the AI response."
            audio_response = tts_service.speak(error_text)
            logger.info(f"🔊 Generated error audio: {len(audio_response)} bytes")
        
        logger.info("✅ Successfully generated OpenAI-powered audio response")
        return StreamingResponse(content=BytesIO(audio_response), media_type="audio/wav")
        
    except Exception as e:
        logger.error(f"❌ Error in OpenAI analysis: {e}")
        # Try to return error audio
        try:
            error_text = "Sorry, there was an error processing your request with OpenAI."
            audio_response = tts_service.speak(error_text)
            return StreamingResponse(content=BytesIO(audio_response), media_type="audio/wav")
        except:
            # If even error audio fails, return empty response
            return StreamingResponse(content=BytesIO(b""), media_type="audio/wav")


@router.post("/openai/analyze-game-text-only")
async def analyze_game_with_openai_text_only(
    image: UploadFile = File(...),
    question: str = Form(...),
    system_prompt: str = Form(
        default="You are a helpful game assistant. Analyze the screenshot and answer the user's question about the game situation. Provide specific, actionable advice for the player."
    ),
    model: str = Form(default=None)
) -> dict:
    """
    Analyze game screenshot and text question using OpenAI (no audio processing).
    
    Returns JSON response with the AI analysis.
    """
    logger.info(f"🤖 Received OpenAI text-only game analysis request")
    logger.info(f"📸 Image file: {image.filename}, size: {image.size} bytes")
    logger.info(f"❓ Question: '{question}'")
    logger.info(f"🤖 System prompt: '{system_prompt}'")
    logger.info(f"🤖 Model: '{model}' (None = use default)")
    
    try:
        # Read image file
        image_data = await image.read()
        logger.info(f"📸 Read image data: {len(image_data)} bytes")
        
        # Analyze screenshot + question using OpenAI
        logger.info("🤖 Starting OpenAI analysis...")
        ai_response = openai_service.analyze_game_situation(
            screenshot_bytes=image_data,
            question_text=question,
            system_prompt=system_prompt,
            model=model
        )
        logger.info(f"🤖 OpenAI analysis response: '{ai_response}'")
        
        # Get actual model used
        from ...core import get_server_config
        config = get_server_config()
        actual_model = model or config._get_default_openai_model()
        
        return {
            "success": True,
            "question": question,
            "response": ai_response,
            "system_prompt": system_prompt,
            "model": actual_model
        }
        
    except Exception as e:
        logger.error(f"❌ Error in OpenAI text analysis: {e}")
        return {
            "success": False,
            "error": str(e),
            "question": question,
            "response": "Sorry, there was an error processing your request with OpenAI.",
            "model": model or "default"
        } 