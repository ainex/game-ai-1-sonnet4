"""Endpoints for image analysis."""

import logging
from fastapi import APIRouter, File, HTTPException, UploadFile

from ...services.image_analysis import get_image_analysis_service

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()
service = get_image_analysis_service()


@router.post("/image/analyze")
async def analyze_image(image: UploadFile = File(...)) -> dict[str, str]:
    """Analyze uploaded image and return description."""
    logger.info(f"🔍 Received image analysis request")
    logger.info(f"📸 Image file: {image.filename}, size: {image.size} bytes")
    
    try:
        data = await image.read()
        logger.info(f"📸 Read image data: {len(data)} bytes")
        
        logger.info("🔍 Starting image analysis...")
        description = service.analyze(data)
        logger.info(f"📝 Generated description: '{description}'")
        
        result = {"description": description}
        logger.info(f"✅ Returning analysis result: {result}")
        return result
        
    except Exception as exc:
        logger.error(f"❌ Error in image analysis: {exc}")
        raise HTTPException(status_code=500, detail=str(exc))
