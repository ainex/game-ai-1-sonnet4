"""Main entry for FastAPI server."""

import logging
from fastapi import FastAPI

from .api.endpoints.analyze import router as analyze_router
from .api.endpoints.game_analysis import router as game_router
from .api.endpoints.image_analysis import router as image_router
from .api.endpoints.stt import router as stt_router
from .api.endpoints.tts import router as tts_router

# Configure logging for Windows compatibility
import sys
import os

# Configure console encoding for Windows
if sys.platform == "win32":
    # Set console to UTF-8 mode on Windows
    os.system("chcp 65001 > nul")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('server.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)
logger.info("🚀 Starting Sims 4 AI Gaming Assistant Server...")

app = FastAPI()

app.include_router(analyze_router, prefix="/api/v1")
app.include_router(image_router, prefix="/api/v1")
app.include_router(stt_router, prefix="/api/v1")
app.include_router(tts_router, prefix="/api/v1")
app.include_router(game_router, prefix="/api/v1")

logger.info("✅ Server routes configured successfully")
