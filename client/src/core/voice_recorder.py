"""Voice recording module with silence detection."""

import io
import logging
import numpy as np
import tempfile
import time
import threading
from typing import Optional

# Set up logging
logger = logging.getLogger(__name__)

try:
    import sounddevice as sd
    import soundfile as sf
    SOUNDDEVICE_AVAILABLE = True
    logger.info("✅ Sounddevice available for recording")
except ImportError:
    SOUNDDEVICE_AVAILABLE = False
    logger.warning("⚠️ Sounddevice not available for recording")

try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
    logger.info("✅ Pygame available for sound effects")
except ImportError:
    PYGAME_AVAILABLE = False
    logger.warning("⚠️ Pygame not available for sound effects")


class VoiceRecorder:
    """Voice recorder with silence detection and audio feedback."""
    
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        silence_threshold: float = 0.001,  # Lower threshold for better sensitivity
        silence_duration: float = 2.0,
        max_recording_time: float = 30.0,
        min_recording_time: float = 1.0  # Minimum recording time
    ):
        """Initialize voice recorder.
        
        Args:
            sample_rate: Audio sample rate in Hz
            channels: Number of audio channels (1=mono, 2=stereo)
            silence_threshold: Volume threshold below which audio is considered silence
            silence_duration: Seconds of silence before auto-stopping recording
            max_recording_time: Maximum recording time in seconds
            min_recording_time: Minimum recording time before allowing silence detection
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.max_recording_time = max_recording_time
        self.min_recording_time = min_recording_time
        
        self.is_recording = False
        self.audio_data = []
        self.recording_thread: Optional[threading.Thread] = None
        self.monitoring_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.stream = None
        
        # Generate pleasant audio feedback sounds
        self._generate_feedback_sounds()
    
    def _generate_feedback_sounds(self):
        """Generate pleasant start and stop recording sounds."""
        try:
            # Generate a pleasant "start recording" sound (ascending chime)
            duration = 0.3
            freq_start = 440  # A4
            freq_end = 660    # E5
            t = np.linspace(0, duration, int(self.sample_rate * duration))
            frequency = np.linspace(freq_start, freq_end, len(t))
            
            # Create ascending chime with fade in/out
            start_sound = np.sin(2 * np.pi * frequency * t)
            fade = np.linspace(0, 1, len(t)) * np.linspace(1, 0, len(t))
            self.start_sound = (start_sound * fade * 0.3).astype(np.float32)
            
            # Generate a pleasant "stop recording" sound (descending chime)
            freq_start = 660  # E5
            freq_end = 440    # A4
            frequency = np.linspace(freq_start, freq_end, len(t))
            stop_sound = np.sin(2 * np.pi * frequency * t)
            self.stop_sound = (stop_sound * fade * 0.3).astype(np.float32)
            
            logger.info("✅ Generated pleasant audio feedback sounds")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not generate feedback sounds: {e}")
            # Create silent fallback sounds
            self.start_sound = np.zeros(int(self.sample_rate * 0.1), dtype=np.float32)
            self.stop_sound = np.zeros(int(self.sample_rate * 0.1), dtype=np.float32)
    
    def _play_feedback_sound(self, sound: np.ndarray):
        """Play a feedback sound asynchronously."""
        try:
            if SOUNDDEVICE_AVAILABLE:
                # Play sound without blocking
                threading.Thread(
                    target=lambda: sd.play(sound, self.sample_rate),
                    daemon=True
                ).start()
                logger.info("🔊 Played feedback sound")
            else:
                logger.info("🔇 Feedback sound skipped (no audio device)")
        except Exception as e:
            logger.warning(f"⚠️ Could not play feedback sound: {e}")
    
    def _audio_callback(self, indata, frames, time, status):
        """Callback function for audio recording."""
        if status:
            logger.warning(f"⚠️ Audio callback status: {status}")
        
        if self.is_recording:
            # Convert to mono if stereo
            if indata.shape[1] > 1:
                audio_chunk = np.mean(indata, axis=1)
            else:
                audio_chunk = indata[:, 0]
            
            # Make a copy to avoid reference issues
            self.audio_data.append(audio_chunk.copy())
    
    def _monitor_silence(self):
        """Monitor for silence and auto-stop recording."""
        logger.info("🔍 Silence monitoring thread started")
        silence_start = None
        last_chunk_time = time.time()
        
        while self.is_recording and not self.stop_event.is_set():
            current_time = time.time()
            recording_duration = current_time - self.recording_start_time
            
            # Don't check for silence until minimum recording time has passed
            if recording_duration < self.min_recording_time:
                time.sleep(0.1)
                continue
            
            # Check if we have recent audio data
            if len(self.audio_data) > 0:
                # Get the most recent audio chunk
                recent_audio = self.audio_data[-1] if self.audio_data else np.array([])
                
                if len(recent_audio) > 0:
                    # Calculate volume (RMS)
                    volume = np.sqrt(np.mean(recent_audio ** 2))
                    
                    if volume < self.silence_threshold:
                        # Silence detected
                        if silence_start is None:
                            silence_start = current_time
                            logger.info(f"🔇 Silence detected (volume: {volume:.4f}) after {recording_duration:.1f}s")
                        elif current_time - silence_start >= self.silence_duration:
                            logger.info(f"🔇 Auto-stopping recording after {self.silence_duration}s of silence (total: {recording_duration:.1f}s)")
                            self.stop_event.set()  # Signal to stop instead of calling stop_recording
                            break
                    else:
                        # Sound detected, reset silence timer
                        if silence_start is not None:
                            logger.info(f"🔊 Sound detected, continuing recording (volume: {volume:.4f})")
                        silence_start = None
                    
                    last_chunk_time = current_time
            
            # Check maximum recording time
            if hasattr(self, 'recording_start_time'):
                if current_time - self.recording_start_time >= self.max_recording_time:
                    logger.info(f"⏰ Max recording time ({self.max_recording_time}s) reached")
                    self.stop_event.set()  # Signal to stop instead of calling stop_recording
                    break
            
            # Sleep briefly to avoid busy waiting
            time.sleep(0.1)
        
        logger.info("🔍 Silence monitoring thread ending")
    
    def start_recording(self):
        """Start voice recording with pleasant feedback sound."""
        if not SOUNDDEVICE_AVAILABLE:
            logger.error("❌ Cannot start recording - sounddevice not available")
            return False
        
        if self.is_recording:
            logger.warning("⚠️ Recording already in progress")
            logger.warning(f"⚠️ Current state: is_recording={self.is_recording}, thread_alive={self.monitoring_thread.is_alive() if self.monitoring_thread else 'None'}")
            return False
        
        try:
            logger.info("🎤 Starting voice recording...")
            
            # Play start sound
            self._play_feedback_sound(self.start_sound)
            
            # Wait briefly for start sound to play
            time.sleep(0.4)
            
            # Clean up any existing threads first
            if self.monitoring_thread is not None and self.monitoring_thread.is_alive():
                self.stop_event.set()
                self.monitoring_thread.join(timeout=1.0)
            
            # Reset recording state
            self.reset()
            self.is_recording = True
            self.recording_start_time = time.time()
            
            # Start recording stream
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self._audio_callback,
                dtype='float32'
            )
            self.stream.start()
            
            # Start silence monitoring in a separate thread
            self.monitoring_thread = threading.Thread(target=self._monitor_silence, daemon=True)
            self.monitoring_thread.start()
            
            logger.info("✅ Voice recording started with silence detection")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start recording: {e}")
            self.is_recording = False
            return False
    
    def reset(self):
        """Reset the recorder to a clean state."""
        logger.info("🔄 Resetting voice recorder state...")
        
        # Stop any active recording first
        if self.is_recording:
            self.is_recording = False
            self.stop_event.set()
        
        # Close stream if active
        if self.stream is not None:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                logger.warning(f"⚠️ Error closing stream during reset: {e}")
            self.stream = None
        
        # Wait for monitoring thread to finish
        if self.monitoring_thread is not None and self.monitoring_thread.is_alive():
            try:
                if self.monitoring_thread != threading.current_thread():
                    self.monitoring_thread.join(timeout=2.0)
                    if self.monitoring_thread.is_alive():
                        logger.warning("⚠️ Monitoring thread didn't terminate gracefully")
            except Exception as e:
                logger.warning(f"⚠️ Error joining monitoring thread: {e}")
        
        # Reset all state variables
        self.is_recording = False
        self.audio_data = []
        self.recording_thread = None
        self.monitoring_thread = None
        self.stop_event.clear()
        
        logger.info("✅ Voice recorder state reset complete")
    
    def stop_recording(self) -> Optional[bytes]:
        """Stop recording and return audio data as WAV bytes."""
        if not self.is_recording and len(self.audio_data) == 0:
            logger.warning("⚠️ No recording in progress")
            return None
        
        try:
            # Only stop if we're actually recording
            if self.is_recording:
                logger.info("🛑 Stopping voice recording...")
                
                # Signal stop
                self.is_recording = False
                self.stop_event.set()
                
                # Stop recording stream
                if self.stream is not None:
                    self.stream.stop()
                    self.stream.close()
                    self.stream = None
                
                # Play stop sound
                self._play_feedback_sound(self.stop_sound)
                
                # Wait for monitoring thread to finish (with timeout and proper thread check)
                if self.monitoring_thread is not None and self.monitoring_thread.is_alive():
                    try:
                        # Check if we're not trying to join the current thread
                        if self.monitoring_thread != threading.current_thread():
                            self.monitoring_thread.join(timeout=2.0)
                            if self.monitoring_thread.is_alive():
                                logger.warning("⚠️ Monitoring thread didn't terminate within timeout")
                        else:
                            logger.warning("⚠️ Skipping thread join - monitoring thread is current thread")
                    except Exception as e:
                        logger.warning(f"⚠️ Error joining monitoring thread: {e}")
                    finally:
                        # Clear the thread reference regardless
                        self.monitoring_thread = None
            else:
                logger.info("🛑 Recording already stopped, processing audio data...")
            
            # Process recorded audio
            if len(self.audio_data) == 0:
                logger.warning("⚠️ No audio data recorded")
                return None
            
            # Concatenate all audio chunks
            full_audio = np.concatenate(self.audio_data)
            logger.info(f"🎵 Recorded {len(full_audio)} samples ({len(full_audio)/self.sample_rate:.2f}s)")
            
            # Convert to WAV bytes
            buffer = io.BytesIO()
            sf.write(buffer, full_audio, self.sample_rate, format='WAV')
            buffer.seek(0)
            audio_bytes = buffer.getvalue()
            
            # Clear audio data after processing (but don't reset everything)
            self.audio_data = []
            
            logger.info(f"✅ Voice recording completed: {len(audio_bytes)} bytes")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"❌ Failed to stop recording: {e}")
            return None
    
    def is_recording_active(self) -> bool:
        """Check if recording is currently active."""
        return self.is_recording


# Global recorder instance
_recorder_instance: Optional[VoiceRecorder] = None


def get_voice_recorder() -> VoiceRecorder:
    """Get or create the global voice recorder instance."""
    global _recorder_instance
    if _recorder_instance is None:
        _recorder_instance = VoiceRecorder()
    return _recorder_instance 