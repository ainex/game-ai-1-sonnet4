"""Endpoint combining image analysis and TTS."""

import logging
from io import BytesIO

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

from ...services.image_analysis import get_image_analysis_service
from ...services.stt import get_stt_service
from ...services.tts import get_tts_service

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()
image_service = get_image_analysis_service()
stt_service = get_stt_service()
tts_service = get_tts_service()


@router.post("/game/analyze-and-speak")
async def analyze_and_speak(
    image: UploadFile = File(...),
) -> StreamingResponse:
    """Analyze image then return spoken description."""
    logger.info(f"🎮 Received analyze-and-speak request")
    logger.info(f"📸 Image file: {image.filename}, size: {image.size} bytes")
    
    try:
        data = await image.read()
        logger.info(f"📸 Read image data: {len(data)} bytes")
        
        logger.info("🔍 Starting image analysis...")
        description = image_service.analyze(data)
        logger.info(f"📝 Generated description: '{description}'")
        
        logger.info("🔊 Starting TTS generation...")
        audio = tts_service.speak(description)
        logger.info(f"🔊 Generated audio: {len(audio)} bytes")
        
        if len(audio) == 0:
            logger.error("❌ TTS generated empty audio!")
            # Return a simple error message as audio
            error_text = "Sorry, I couldn't generate speech for this image."
            audio = tts_service.speak(error_text)
            logger.info(f"🔊 Generated error audio: {len(audio)} bytes")
        
        logger.info("✅ Successfully generated audio response")
        return StreamingResponse(content=BytesIO(audio), media_type="audio/wav")
        
    except Exception as e:
        logger.error(f"❌ Error in analyze_and_speak: {e}")
        # Try to return error audio
        try:
            error_text = "Sorry, there was an error processing your request."
            audio = tts_service.speak(error_text)
            return StreamingResponse(content=BytesIO(audio), media_type="audio/wav")
        except:
            # If even error audio fails, return empty response
            return StreamingResponse(content=BytesIO(b""), media_type="audio/wav")


@router.post("/game/analyze-image-and-voice")
async def analyze_image_and_voice(
    image: UploadFile = File(...),
    audio: UploadFile = File(...),
) -> StreamingResponse:
    """Analyze both image and voice, then return combined spoken response."""
    logger.info(f"🎮 Received combined image + voice analysis request")
    logger.info(f"📸 Image file: {image.filename}, size: {image.size} bytes")
    logger.info(f"🎵 Audio file: {audio.filename}, size: {audio.size} bytes")
    
    try:
        # Read both files
        image_data = await image.read()
        audio_data = await audio.read()
        logger.info(f"📸 Read image data: {len(image_data)} bytes")
        logger.info(f"🎵 Read audio data: {len(audio_data)} bytes")
        
        # Analyze image
        logger.info("🔍 Starting image analysis...")
        image_description = image_service.analyze(image_data)
        logger.info(f"📝 Image description: '{image_description}'")
        
        # Transcribe voice
        logger.info("🎤 Starting voice transcription...")
        voice_text = stt_service.transcribe(audio_data)
        logger.info(f"🎤 Voice text: '{voice_text}'")
        
        # Combine the information
        combined_text = f"I can see: {image_description}. You said: {voice_text}. Let me help you with this situation."
        logger.info(f"💬 Combined response: '{combined_text}'")
        
        # Generate spoken response
        logger.info("🔊 Starting TTS generation for combined response...")
        audio_response = tts_service.speak(combined_text)
        logger.info(f"🔊 Generated combined audio: {len(audio_response)} bytes")
        
        if len(audio_response) == 0:
            logger.error("❌ TTS generated empty audio!")
            # Return a simple error message as audio
            error_text = "Sorry, I couldn't generate a response for your image and voice."
            audio_response = tts_service.speak(error_text)
            logger.info(f"🔊 Generated error audio: {len(audio_response)} bytes")
        
        logger.info("✅ Successfully generated combined audio response")
        return StreamingResponse(content=BytesIO(audio_response), media_type="audio/wav")
        
    except Exception as e:
        logger.error(f"❌ Error in combined analysis: {e}")
        # Try to return error audio
        try:
            error_text = "Sorry, there was an error processing your image and voice."
            audio_response = tts_service.speak(error_text)
            return StreamingResponse(content=BytesIO(audio_response), media_type="audio/wav")
        except:
            # If even error audio fails, return empty response
            return StreamingResponse(content=BytesIO(b""), media_type="audio/wav")
