"""Text-to-speech service using Coqui TTS."""

from functools import lru_cache
from io import BytesIO

try:
    from TTS.api import TTS
except Exception:  # pragma: no cover - optional dependency
    TTS = None


class TTSService:
    """Service for generating speech from text."""

    def __init__(self) -> None:
        if TTS is None:
            self._tts = None
        else:
            try:
                self._tts = TTS(
                    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
                    progress_bar=False,
                    gpu=True,
                )
            except Exception:  # pragma: no cover - runtime failure
                self._tts = None

    def speak(self, text: str, language: str = "en") -> bytes:
        """Generate speech audio for the given text."""
        if self._tts is None:
            return b""

        wav = self._tts.tts(text=text, speaker_wav=None, language=language)
        buffer = BytesIO()
        self._tts.save_wav(wav, buffer)
        return buffer.getvalue()


@lru_cache(maxsize=1)
def get_tts_service() -> "TTSService":
    """Cached service instance."""
    return TTSService()
