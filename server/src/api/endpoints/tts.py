"""Endpoints for text-to-speech."""

import logging
from io import BytesIO

from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse

from ...services.tts import get_tts_service

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()
service = get_tts_service()


@router.post("/tts/speak")
async def tts_speak(
    text: str = Body(...), language: str = Body("en")
) -> StreamingResponse:
    """Return spoken audio for the provided text."""
    logger.info(f"🔊 Received TTS request")
    logger.info(f"📝 Text: '{text}'")
    logger.info(f"🌍 Language: {language}")
    
    try:
        logger.info("🔊 Starting TTS generation...")
        audio = service.speak(text=text, language=language)
        logger.info(f"🔊 Generated audio: {len(audio)} bytes")
        
        if len(audio) == 0:
            logger.error("❌ TTS generated empty audio!")
            # Return a simple error message as audio
            error_text = "Sorry, I couldn't generate speech for this text."
            audio = service.speak(text=error_text, language=language)
            logger.info(f"🔊 Generated error audio: {len(audio)} bytes")
        
        logger.info("✅ Successfully generated TTS response")
        return StreamingResponse(content=BytesIO(audio), media_type="audio/wav")
        
    except Exception as e:
        logger.error(f"❌ Error in TTS generation: {e}")
        # Try to return error audio
        try:
            error_text = "Sorry, there was an error generating speech."
            audio = service.speak(text=error_text, language=language)
            return StreamingResponse(content=BytesIO(audio), media_type="audio/wav")
        except:
            # If even error audio fails, return empty response
            return StreamingResponse(content=BytesIO(b""), media_type="audio/wav")


@router.get("/tts/test")
async def tts_test() -> StreamingResponse:
    """Test endpoint that returns a simple spoken message."""
    logger.info("🧪 Received TTS test request")
    
    test_text = "Hello! This is a test of the text to speech service. If you can hear this, the TTS is working correctly."
    
    try:
        logger.info(f"🔊 Generating test speech for: '{test_text}'")
        audio = service.speak(text=test_text, language="en")
        logger.info(f"🔊 Generated test audio: {len(audio)} bytes")
        
        if len(audio) == 0:
            logger.error("❌ TTS test generated empty audio!")
            return StreamingResponse(content=BytesIO(b""), media_type="audio/wav")
        
        logger.info("✅ Successfully generated TTS test response")
        return StreamingResponse(content=BytesIO(audio), media_type="audio/wav")
        
    except Exception as e:
        logger.error(f"❌ Error in TTS test: {e}")
        return StreamingResponse(content=BytesIO(b""), media_type="audio/wav")
