"""Speech-to-text service using Whisper."""

import logging
import torch
from functools import lru_cache
from io import BytesIO
import tempfile
import os

# Set up logging
logger = logging.getLogger(__name__)

try:
    from transformers import WhisperProcessor, WhisperForConditionalGeneration
    import librosa
    logger.info("✅ Whisper STT available")
except Exception as e:  # pragma: no cover - optional dependency
    logger.warning(f"⚠️ Whisper STT not available: {e}")
    WhisperProcessor = None
    WhisperForConditionalGeneration = None


class STTService:
    """Service for converting speech audio to text."""

    def __init__(self) -> None:
        if WhisperProcessor is None or WhisperForConditionalGeneration is None:
            logger.warning("⚠️ STT service initialized without Whisper libraries")
            self._processor = None
            self._model = None
        else:
            try:
                logger.info("🔧 Loading Whisper STT model...")
                # Use a smaller, faster Whisper model for real-time processing
                model_name = "openai/whisper-base"
                self._processor = WhisperProcessor.from_pretrained(model_name)
                self._model = WhisperForConditionalGeneration.from_pretrained(model_name)
                
                # Move to GPU if available
                if torch.cuda.is_available():
                    self._model = self._model.cuda()
                    logger.info("✅ Whisper STT model loaded on GPU")
                else:
                    logger.info("✅ Whisper STT model loaded on CPU")
            except Exception as e:
                logger.error(f"❌ Whisper STT model loading failed: {e}")
                self._processor = None
                self._model = None

    def transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe speech audio to text."""
        logger.info(f"🎤 Transcribing audio of {len(audio_bytes)} bytes")
        
        if self._processor is None or self._model is None:
            logger.warning("⚠️ STT unavailable - no Whisper model loaded")
            return "Speech recognition unavailable"

        try:
            logger.info("🎤 Starting speech-to-text transcription...")
            
            # Save audio bytes to temporary file for librosa
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_bytes)
                audio_path = tmp_file.name
            
            try:
                # Load audio with librosa
                audio, sampling_rate = librosa.load(audio_path, sr=16000)  # Whisper expects 16kHz
                logger.info(f"🎤 Loaded audio: {len(audio)} samples at {sampling_rate}Hz")
                
                # Process audio for Whisper
                inputs = self._processor(audio, sampling_rate=sampling_rate, return_tensors="pt")
                
                # Move inputs to GPU if model is on GPU
                if torch.cuda.is_available() and next(self._model.parameters()).is_cuda:
                    inputs = {k: v.cuda() for k, v in inputs.items()}
                
                # Generate transcription
                with torch.no_grad():
                    predicted_ids = self._model.generate(
                        inputs.input_features,
                        max_new_tokens=200,  # Limit output length
                        do_sample=False,     # Use greedy decoding for consistency
                    )
                
                # Decode the transcription
                transcription = self._processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
                logger.info(f"🎤 Transcribed text: '{transcription}'")
                
                return transcription.strip()
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(audio_path)
                except Exception as cleanup_error:
                    logger.warning(f"⚠️ Failed to clean up temporary audio file: {cleanup_error}")
                    
        except Exception as e:
            logger.error(f"❌ STT transcription failed: {e}")
            return f"Error transcribing audio: {str(e)}"


@lru_cache(maxsize=1)
def get_stt_service() -> "STTService":
    """Cached service instance."""
    logger.info("🏭 Creating STT service instance")
    return STTService() 