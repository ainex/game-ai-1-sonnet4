"""Image analysis service using transformer pipeline."""

from functools import lru_cache
from io import BytesIO

from PIL import Image

try:
    from transformers import pipeline
except Exception:  # pragma: no cover - optional dependency
    pipeline = None  # type: ignore


class ImageAnalysisService:
    """Service for generating descriptions from images."""

    def __init__(self) -> None:
        if pipeline is None:
            self._captioner = None
        else:
            try:
                self._captioner = pipeline(
                    "image-to-text",
                    model="nlpconnect/vit-gpt2-image-captioning",
                )
            except Exception:  # pragma: no cover - runtime failure
                self._captioner = None

    def analyze(self, image_bytes: bytes) -> str:
        """Return a caption for the given image bytes."""
        if self._captioner is None:
            return "Image analysis unavailable"

        image = Image.open(BytesIO(image_bytes))
        result = self._captioner(image)
        if result:
            return result[0].get("generated_text", "")
        return ""


@lru_cache(maxsize=1)
def get_image_analysis_service() -> "ImageAnalysisService":
    """Cached service instance."""
    return ImageAnalysisService()
