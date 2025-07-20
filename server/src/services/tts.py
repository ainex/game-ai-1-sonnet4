"""Text-to-speech service using Coqui TTS."""

import logging
import torch
from functools import lru_cache
from io import BytesIO

# Set up logging
logger = logging.getLogger(__name__)

try:
    from TTS.api import TTS
    # Fix PyTorch 2.6 weights_only security issue
    torch.serialization.add_safe_globals([])
    logger.info("✅ Coqui TTS available")
except Exception as e:  # pragma: no cover - optional dependency
    logger.warning(f"⚠️ Coqui TTS not available: {e}")
    TTS = None


class TTSService:
    """Service for generating speech from text."""

    def __init__(self) -> None:
        if TTS is None:
            logger.warning("⚠️ TTS service initialized without TTS library")
            self._tts = None
        else:
            try:
                logger.info("🔧 Loading TTS model...")
                # Use a simpler, more reliable TTS model that doesn't require GPU
                self._tts = TTS(
                    model_name="tts_models/en/ljspeech/tacotron2-DDC",
                    progress_bar=False,
                    gpu=False,
                )
                logger.info("✅ TTS model loaded successfully")
            except Exception as e:
                logger.error(f"❌ TTS model loading failed: {e}")
                self._tts = None

    def speak(self, text: str, language: str = "en") -> bytes:
        """Generate speech audio for the given text."""
        logger.info(f"🔊 Generating speech for text: '{text}' (language: {language})")
        
        if self._tts is None:
            logger.warning("⚠️ TTS unavailable - no TTS model loaded")
            return b""

        try:
            logger.info("🔊 Starting TTS generation...")
            # Generate audio and save to buffer
            wav = self._tts.tts(text=text)
            logger.info(f"🔊 TTS generated audio data: {type(wav)}, length: {len(wav) if hasattr(wav, '__len__') else 'unknown'}")
            
            # Create a BytesIO buffer and save the WAV file to it
            buffer = BytesIO()
            
            # Save the audio to the buffer in WAV format
            import soundfile as sf
            import numpy as np
            
            # Convert to numpy array if needed
            if isinstance(wav, list):
                wav = np.array(wav)
                logger.info(f"🔊 Converted list to numpy array: {wav.shape}")
            
            logger.info(f"🔊 Audio data type: {type(wav)}, shape: {wav.shape if hasattr(wav, 'shape') else 'unknown'}")
            sample_rate = self._tts.synthesizer.output_sample_rate if self._tts and self._tts.synthesizer else 22050
            logger.info(f"🔊 Sample rate: {sample_rate}")
            
            # Save as WAV using soundfile
            sf.write(buffer, wav, sample_rate, format='WAV')
            buffer.seek(0)
            
            audio_bytes = buffer.getvalue()
            logger.info(f"🔊 Generated audio: {len(audio_bytes)} bytes")
            
            return audio_bytes
            
        except Exception as e:
            logger.error(f"❌ TTS generation failed: {e}")
            return b""


@lru_cache(maxsize=1)
def get_tts_service() -> "TTSService":
    """Cached service instance."""
    logger.info("🏭 Creating TTS service instance")
    return TTSService()
