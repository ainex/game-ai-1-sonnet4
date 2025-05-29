"""Endpoint for screenshot analysis placeholder."""

from fastapi import APIRouter, File, Form, UploadFile

router = APIRouter()


@router.post("/analyze_situation")
async def analyze_situation(
    image: UploadFile = File(...), query: str = Form(...)
) -> dict[str, str | int]:
    """Receive screenshot and query, return image size."""
    content = await image.read()
    size = len(content)
    return {
        "image_size_bytes": size,
        "message": (
            "Screenshot and query received successfully. LLM processing placeholder."
        ),
    }
