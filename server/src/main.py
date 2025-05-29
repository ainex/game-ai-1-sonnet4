"""Main entry for FastAPI server."""

from fastapi import FastAPI

from .api.endpoints.analyze import router as analyze_router

app = FastAPI()

app.include_router(analyze_router, prefix="/api/v1")
