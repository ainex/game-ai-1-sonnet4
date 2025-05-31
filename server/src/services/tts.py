"""Text-to-speech service using Coqui TTS."""

import torch
from functools import lru_cache
from io import BytesIO

try:
    from TTS.api import TTS
    # Fix PyTorch 2.6 weights_only security issue
    torch.serialization.add_safe_globals([])
except Exception:  # pragma: no cover - optional dependency
    TTS = None


class TTSService:
    """Service for generating speech from text."""

    def __init__(self) -> None:
        if TTS is None:
            self._tts = None
        else:
            try:
                # Use a simpler, more reliable TTS model that doesn't require GPU
                self._tts = TTS(
                    model_name="tts_models/en/ljspeech/tacotron2-DDC",
                    progress_bar=False,
                    gpu=False,
                )
            except Exception as e:
                print(f"TTS model loading failed: {e}")
                self._tts = None

    def speak(self, text: str, language: str = "en") -> bytes:
        """Generate speech audio for the given text."""
        if self._tts is None:
            return b""

        try:
            # Generate audio and save to buffer
            wav = self._tts.tts(text=text)
            
            # Create a BytesIO buffer and save the WAV file to it
            buffer = BytesIO()
            
            # Save the audio to the buffer in WAV format
            import soundfile as sf
            import numpy as np
            
            # Convert to numpy array if needed
            if isinstance(wav, list):
                wav = np.array(wav)
            
            # Save as WAV using soundfile
            sf.write(buffer, wav, self._tts.synthesizer.output_sample_rate, format='WAV')
            buffer.seek(0)
            
            return buffer.getvalue()
        except Exception as e:
            print(f"TTS generation failed: {e}")
            return b""


@lru_cache(maxsize=1)
def get_tts_service() -> "TTSService":
    """Cached service instance."""
    return TTSService()
