"""Endpoints for image analysis."""

from fastapi import APIRouter, File, HTTPException, UploadFile

from ...services.image_analysis import get_image_analysis_service

router = APIRouter()
service = get_image_analysis_service()


@router.post("/image/analyze")
async def analyze_image(image: UploadFile = File(...)) -> dict[str, str]:
    """Analyze uploaded image and return description."""
    data = await image.read()
    try:
        description = service.analyze(data)
    except Exception as exc:  # pragma: no cover - runtime failure
        raise HTTPException(status_code=500, detail=str(exc))
    return {"description": description}
