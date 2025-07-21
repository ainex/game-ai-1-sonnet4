"""Endpoints for speech-to-text."""

import logging
from fastapi import APIRouter, File, UploadFile, HTTPException

from ...services.stt import get_stt_service

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()
service = get_stt_service()


@router.post("/stt/transcribe")
async def stt_transcribe(audio: UploadFile = File(...)) -> dict[str, str]:
    """Transcribe uploaded audio to text."""
    logger.info(f"🎤 Received STT request")
    logger.info(f"🎵 Audio file: {audio.filename}, size: {audio.size} bytes")
    
    try:
        # Read audio data
        audio_data = await audio.read()
        logger.info(f"🎵 Read audio data: {len(audio_data)} bytes")
        
        logger.info("🎤 Starting speech-to-text transcription...")
        transcription = service.transcribe(audio_data)
        logger.info(f"🎤 Transcribed text: '{transcription}'")
        
        result = {"transcription": transcription}
        logger.info("✅ Successfully transcribed audio")
        return result
        
    except Exception as e:
        logger.error(f"❌ Error in STT transcription: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stt/test")
async def stt_test() -> dict[str, str]:
    """Test endpoint that returns STT service status."""
    logger.info("🧪 Received STT test request")
    
    try:
        # Check if STT service is available
        if service._processor is None or service._model is None:
            return {
                "status": "unavailable",
                "message": "STT service is not properly initialized"
            }
        
        return {
            "status": "available", 
            "message": "STT service is ready for transcription"
        }
        
    except Exception as e:
        logger.error(f"❌ Error in STT test: {e}")
        return {
            "status": "error",
            "message": f"STT test failed: {str(e)}"
        } 