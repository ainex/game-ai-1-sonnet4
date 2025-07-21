import io
import tempfile
import os
import logging
import time
import sys

import keyboard
import requests
from PIL import ImageGrab

# Add the current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from core.voice_recorder import get_voice_recorder

# Set up logging for Windows compatibility
import sys
import os

# Configure console encoding for Windows
if sys.platform == "win32":
    # Set console to UTF-8 mode on Windows
    os.system("chcp 65001 > nul")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('client.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Try to import pygame for audio playback
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
    logger.info("✅ Pygame audio available")
except ImportError:
    PYGAME_AVAILABLE = False
    logger.warning("⚠️ Pygame not available")

# Try alternative audio libraries
try:
    import sounddevice as sd
    import soundfile as sf
    SOUNDDEVICE_AVAILABLE = True
    logger.info("✅ Sounddevice audio available")
except ImportError:
    SOUNDDEVICE_AVAILABLE = False
    logger.warning("⚠️ Sounddevice not available")

try:
    import pyaudio
    import wave
    PYAUDIO_AVAILABLE = True
    logger.info("✅ PyAudio available")
except ImportError:
    PYAUDIO_AVAILABLE = False
    logger.warning("⚠️ PyAudio not available")

if not (PYGAME_AVAILABLE or SOUNDDEVICE_AVAILABLE or PYAUDIO_AVAILABLE):
    logger.error("❌ No audio libraries available - audio playback disabled")
    AUDIO_AVAILABLE = False
else:
    AUDIO_AVAILABLE = True


def play_audio(audio_path):
    """Play audio using the best available library."""
    logger.info(f"🎵 Attempting to play audio: {audio_path}")
    logger.info(f"📊 Audio file size: {os.path.getsize(audio_path)} bytes")
    
    if not AUDIO_AVAILABLE:
        logger.warning(f"💾 Audio saved to: {audio_path}")
        return
    
    try:
        # Try sounddevice first (most compatible)
        if SOUNDDEVICE_AVAILABLE:
            logger.info("🔊 Using sounddevice for audio playback")
            data, samplerate = sf.read(audio_path)
            logger.info(f"📊 Audio data shape: {data.shape}, sample rate: {samplerate}")
            sd.play(data, samplerate)
            sd.wait()  # Wait until the audio is finished playing
            logger.info("✅ Audio playback finished (sounddevice)")
            return
    except Exception as e:
        logger.error(f"❌ sounddevice failed: {e}")
    
    try:
        # Try pygame second
        if PYGAME_AVAILABLE:
            logger.info("🔊 Using pygame for audio playback")
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            logger.info("✅ Audio playback finished (pygame)")
            return
    except Exception as e:
        logger.error(f"❌ pygame failed: {e}")
    
    try:
        # Try pyaudio last
        if PYAUDIO_AVAILABLE:
            logger.info("🔊 Using pyaudio for audio playback")
            wf = wave.open(audio_path, 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                          channels=wf.getnchannels(),
                          rate=wf.getframerate(),
                          output=True)
            
            chunk = 1024
            data = wf.readframes(chunk)
            while data:
                stream.write(data)
                data = wf.readframes(chunk)
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf.close()
            logger.info("✅ Audio playback finished (pyaudio)")
            return
    except Exception as e:
        logger.error(f"❌ pyaudio failed: {e}")
    
    logger.error(f"🔇 All audio libraries failed. Audio saved to: {audio_path}")


def capture_and_analyze_with_speech() -> None:
    """Capture screenshot, analyze it, and play the spoken description."""
    logger.info("📸 Capturing screenshot...")
    try:
        screenshot = ImageGrab.grab()
        logger.info(f"📸 Screenshot captured: {screenshot.size} pixels")
        
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        buffer.seek(0)
        image_size = len(buffer.getvalue())
        logger.info(f"📸 Screenshot saved to buffer: {image_size} bytes")
        
        files = {"image": ("screenshot.png", buffer, "image/png")}
        
        logger.info("🔍 Sending request to server for analysis and speech...")
        response = requests.post(
            "http://localhost:8000/api/v1/game/analyze-and-speak",
            files=files,
            timeout=30,  # Increased timeout for AI processing
        )
        
        logger.info(f"📡 Server response status: {response.status_code}")
        logger.info(f"📡 Server response headers: {dict(response.headers)}")
        logger.info(f"📡 Response content length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            logger.info("✅ Analysis complete! Processing audio...")
            
            # Save and play the audio response
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(response.content)
                audio_path = tmp_file.name
            
            logger.info(f"💾 Audio saved to temporary file: {audio_path}")
            
            # Use our improved audio playback function
            play_audio(audio_path)
            
            # Clean up temporary file
            try:
                os.unlink(audio_path)
                logger.info("🧹 Temporary audio file cleaned up")
            except Exception as e:
                logger.warning(f"⚠️ Failed to clean up temporary file: {e}")
        else:
            logger.error(f"❌ Request failed with status {response.status_code}")
            logger.error(f"❌ Response text: {response.text}")
            
    except requests.RequestException as exc:
        logger.error(f"❌ Request failed: {exc}")
    except Exception as exc:
        logger.error(f"❌ Unexpected error: {exc}")


def capture_and_analyze_text_only() -> None:
    """Capture screenshot and get text description only."""
    logger.info("📸 Capturing screenshot...")
    try:
        screenshot = ImageGrab.grab()
        logger.info(f"📸 Screenshot captured: {screenshot.size} pixels")
        
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        buffer.seek(0)
        image_size = len(buffer.getvalue())
        logger.info(f"📸 Screenshot saved to buffer: {image_size} bytes")
        
        files = {"image": ("screenshot.png", buffer, "image/png")}
        
        logger.info("🔍 Sending request to server for text analysis...")
        response = requests.post(
            "http://localhost:8000/api/v1/image/analyze",
            files=files,
            timeout=15,
        )
        
        logger.info(f"📡 Server response status: {response.status_code}")
        logger.info(f"📡 Response content length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            result = response.json()
            description = result.get('description', 'No description available')
            logger.info(f"📝 Server response JSON: {result}")
            logger.info(f"📝 Description: {description}")
        else:
            logger.error(f"❌ Request failed with status {response.status_code}")
            logger.error(f"❌ Response text: {response.text}")
            
    except requests.RequestException as exc:
        logger.error(f"❌ Request failed: {exc}")
    except Exception as exc:
        logger.error(f"❌ Unexpected error: {exc}")


def capture_screenshot_and_record_voice() -> None:
    """Capture screenshot AND record voice, then send both to server for analysis."""
    logger.info("🎮 Starting combined screenshot + voice capture...")
    
    try:
        # Get voice recorder
        recorder = get_voice_recorder()
        
        # Step 1: Capture screenshot
        logger.info("📸 Capturing screenshot...")
        screenshot = ImageGrab.grab()
        logger.info(f"📸 Screenshot captured: {screenshot.size} pixels")
        
        # Save screenshot to buffer
        screenshot_buffer = io.BytesIO()
        screenshot.save(screenshot_buffer, format="PNG")
        screenshot_buffer.seek(0)
        screenshot_size = len(screenshot_buffer.getvalue())
        logger.info(f"📸 Screenshot saved to buffer: {screenshot_size} bytes")
        
        # Step 2: Start voice recording
        logger.info("🎤 Starting voice recording (speak after the chime, it will auto-stop when you're done)...")
        print("🎤 Recording started! Speak after the chime. Recording will auto-stop after silence.")
        
        recording_success = recorder.start_recording()
        if not recording_success:
            logger.error("❌ Failed to start voice recording")
            print("❌ Voice recording failed. Using screenshot only.")
            # Fall back to screenshot-only mode
            capture_and_analyze_with_speech()
            return
        
        # Wait for recording to complete (it will auto-stop on silence)
        print("🎤 Recording... (will auto-stop after 2 seconds of silence)")
        while recorder.is_recording_active():
            time.sleep(0.1)
        
        # Get recorded audio
        audio_bytes = recorder.stop_recording()
        if audio_bytes is None:
            logger.warning("⚠️ No audio recorded, using screenshot only")
            print("⚠️ No voice recorded. Using screenshot only.")
            # Fall back to screenshot-only mode
            capture_and_analyze_with_speech()
            return
        
        logger.info(f"🎵 Voice recorded: {len(audio_bytes)} bytes")
        print(f"✅ Voice recording completed: {len(audio_bytes)} bytes")
        
        # Step 3: Send both to server
        logger.info("🔍 Sending screenshot + voice to server for combined analysis...")
        print("🔍 Analyzing screenshot and voice...")
        
        # Prepare files for upload
        screenshot_buffer.seek(0)
        files = {
            "image": ("screenshot.png", screenshot_buffer, "image/png"),
            "audio": ("voice.wav", io.BytesIO(audio_bytes), "audio/wav")
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/game/analyze-image-and-voice",
            files=files,
            timeout=60,  # Longer timeout for combined processing
        )
        
        logger.info(f"📡 Server response status: {response.status_code}")
        logger.info(f"📡 Server response headers: {dict(response.headers)}")
        logger.info(f"📡 Response content length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            logger.info("✅ Combined analysis complete! Processing audio response...")
            print("✅ Analysis complete! Playing AI response...")
            
            # Save and play the audio response
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(response.content)
                audio_path = tmp_file.name
            
            logger.info(f"💾 Response audio saved to temporary file: {audio_path}")
            
            # Use our improved audio playback function
            play_audio(audio_path)
            
            # Clean up temporary file
            try:
                os.unlink(audio_path)
                logger.info("🧹 Temporary audio file cleaned up")
            except Exception as e:
                logger.warning(f"⚠️ Failed to clean up temporary file: {e}")
        else:
            logger.error(f"❌ Request failed with status {response.status_code}")
            logger.error(f"❌ Response text: {response.text}")
            print(f"❌ Analysis failed: {response.status_code}")
            
    except requests.RequestException as exc:
        logger.error(f"❌ Request failed: {exc}")
        print(f"❌ Connection failed: {exc}")
    except Exception as exc:
        logger.error(f"❌ Unexpected error: {exc}")
        print(f"❌ Error: {exc}")


def test_tts_service() -> None:
    """Test the TTS service with a sample text."""
    test_text = "Hello! This is a test of the text-to-speech service."
    
    try:
        logger.info(f"🔊 Testing TTS with: '{test_text}'")
        response = requests.post(
            "http://localhost:8000/api/v1/tts/speak",
            json={"text": test_text, "language": "en"},
            timeout=15,
        )
        
        logger.info(f"📡 TTS response status: {response.status_code}")
        logger.info(f"📡 TTS response headers: {dict(response.headers)}")
        logger.info(f"📡 TTS response content length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            logger.info("✅ TTS generation successful! Processing audio...")
            
            # Save and play the audio response
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(response.content)
                audio_path = tmp_file.name
            
            logger.info(f"💾 TTS audio saved to temporary file: {audio_path}")
            
            # Use our improved audio playback function
            play_audio(audio_path)
            
            # Clean up
            try:
                os.unlink(audio_path)
                logger.info("🧹 Temporary TTS audio file cleaned up")
            except Exception as e:
                logger.warning(f"⚠️ Failed to clean up temporary TTS file: {e}")
        else:
            logger.error(f"❌ TTS test failed with status {response.status_code}")
            logger.error(f"❌ TTS response text: {response.text}")
            
    except requests.RequestException as exc:
        logger.error(f"❌ TTS test failed: {exc}")
    except Exception as exc:
        logger.error(f"❌ TTS unexpected error: {exc}")


def main() -> None:
    """Entry point for the client with updated hotkeys."""
    logger.info("🎮 Sims 4 AI Gaming Assistant Client Starting...")
    print("🎮 Sims 4 AI Gaming Assistant Client")
    print("📋 Available hotkeys:")
    print("  Ctrl+Shift+V: 🎤📸 NEW! Capture screenshot + record voice (with pleasant chimes)")
    print("  Ctrl+Shift+S: 📸🔊 Capture screenshot + AI analysis + speech")
    print("  Ctrl+Shift+A: 📸📝 Capture screenshot + text analysis only")
    print("  Ctrl+Shift+T: 🔊🧪 Test TTS service")
    print("  Esc: Quit")
    print()
    print("🎯 RECOMMENDED: Use Ctrl+Shift+V for the complete voice + screenshot experience!")
    print("🎤 Voice recording will auto-stop after 2 seconds of silence (no need to hold button)")
    print()
    
    # Register hotkeys for new functionality
    keyboard.add_hotkey("ctrl+shift+v", capture_screenshot_and_record_voice)  # NEW combined function
    keyboard.add_hotkey("ctrl+shift+s", capture_and_analyze_with_speech)      # Existing screenshot + TTS
    keyboard.add_hotkey("ctrl+shift+a", capture_and_analyze_text_only)        # Existing screenshot only
    keyboard.add_hotkey("ctrl+shift+t", test_tts_service)                     # Existing TTS test
    
    logger.info("✅ Client ready! Use the hotkeys above or press Esc to quit.")
    print("✅ Client ready! Use the hotkeys above or press Esc to quit.")
    keyboard.wait("esc")
    logger.info("👋 Client shutting down...")
    print("👋 Goodbye!")


if __name__ == "__main__":
    main()
