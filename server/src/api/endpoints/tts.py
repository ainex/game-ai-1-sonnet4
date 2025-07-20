"""Endpoints for text-to-speech."""

from io import BytesIO

from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse

from ...services.tts import get_tts_service

router = APIRouter()
service = get_tts_service()


@router.post("/tts/speak")
async def tts_speak(
    text: str = Body(...), language: str = Body("en")
) -> StreamingResponse:
    """Return spoken audio for the provided text."""
    audio = service.speak(text=text, language=language)
    return StreamingResponse(content=BytesIO(audio), media_type="audio/wav")
