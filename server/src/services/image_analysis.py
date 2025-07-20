"""Image analysis service using transformer pipeline."""

import logging
from functools import lru_cache
from io import BytesIO

from PIL import Image

# Set up logging
logger = logging.getLogger(__name__)

try:
    from transformers import pipeline
    logger.info("✅ Transformers pipeline available")
except Exception as e:  # pragma: no cover - optional dependency
    logger.warning(f"⚠️ Transformers pipeline not available: {e}")
    pipeline = None  # type: ignore


class ImageAnalysisService:
    """Service for generating descriptions from images."""

    def __init__(self) -> None:
        if pipeline is None:
            logger.warning("⚠️ Image analysis service initialized without pipeline")
            self._captioner = None
        else:
            try:
                logger.info("🔧 Loading image captioning model...")
                self._captioner = pipeline(
                    "image-to-text",
                    model="nlpconnect/vit-gpt2-image-captioning",
                )
                logger.info("✅ Image captioning model loaded successfully")
            except Exception as e:  # pragma: no cover - runtime failure
                logger.error(f"❌ Failed to load image captioning model: {e}")
                self._captioner = None

    def analyze(self, image_bytes: bytes) -> str:
        """Return a caption for the given image bytes."""
        logger.info(f"🔍 Analyzing image of {len(image_bytes)} bytes")
        
        if self._captioner is None:
            logger.warning("⚠️ Image analysis unavailable - no captioner loaded")
            return "Image analysis unavailable"

        try:
            image = Image.open(BytesIO(image_bytes))
            logger.info(f"📸 Opened image: {image.size} pixels, mode: {image.mode}")
            
            result = self._captioner(image)
            logger.info(f"🔍 Captioner result: {result}")
            
            if result:
                caption = result[0].get("generated_text", "")
                logger.info(f"📝 Generated caption: '{caption}'")
                return caption
            else:
                logger.warning("⚠️ Captioner returned empty result")
                return "No description available"
                
        except Exception as e:
            logger.error(f"❌ Error in image analysis: {e}")
            return f"Error analyzing image: {str(e)}"


@lru_cache(maxsize=1)
def get_image_analysis_service() -> "ImageAnalysisService":
    """Cached service instance."""
    logger.info("🏭 Creating image analysis service instance")
    return ImageAnalysisService()
