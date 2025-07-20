"""Endpoint combining image analysis and TTS."""

from io import BytesIO

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

from ...services.image_analysis import get_image_analysis_service
from ...services.tts import get_tts_service

router = APIRouter()
image_service = get_image_analysis_service()
tts_service = get_tts_service()


@router.post("/game/analyze-and-speak")
async def analyze_and_speak(
    image: UploadFile = File(...),
) -> StreamingResponse:
    """Analyze image then return spoken description."""
    data = await image.read()
    description = image_service.analyze(data)
    audio = tts_service.speak(description)
    return StreamingResponse(content=BytesIO(audio), media_type="audio/wav")
