"""Database model for image analysis records."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .base import Base


class ImageAnalysis(Base):
    """Persisted image analysis result."""

    __tablename__ = "image_analysis"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    image_hash = Column(String, nullable=False)
    description = Column(String, nullable=False)
