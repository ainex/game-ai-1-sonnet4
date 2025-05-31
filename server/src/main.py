"""Main entry for FastAPI server."""

from fastapi import FastAPI

from .api.endpoints.analyze import router as analyze_router
from .api.endpoints.game_analysis import router as game_router
from .api.endpoints.image_analysis import router as image_router
from .api.endpoints.tts import router as tts_router

app = FastAPI()

app.include_router(analyze_router, prefix="/api/v1")
app.include_router(image_router, prefix="/api/v1")
app.include_router(tts_router, prefix="/api/v1")
app.include_router(game_router, prefix="/api/v1")
