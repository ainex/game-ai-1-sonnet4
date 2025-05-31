import io
import tempfile
import os

import keyboard
import requests
from PIL import ImageGrab

# Try to import pygame for audio playback
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

# Try alternative audio libraries
try:
    import sounddevice as sd
    import soundfile as sf
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False

try:
    import pyaudio
    import wave
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False

if not (PYGAME_AVAILABLE or SOUNDDEVICE_AVAILABLE or PYAUDIO_AVAILABLE):
    print("⚠️  No audio libraries available - audio playback disabled")
    AUDIO_AVAILABLE = False
else:
    AUDIO_AVAILABLE = True


def play_audio(audio_path):
    """Play audio using the best available library."""
    if not AUDIO_AVAILABLE:
        print(f"💾 Audio saved to: {audio_path}")
        return
    
    try:
        # Try sounddevice first (most compatible)
        if SOUNDDEVICE_AVAILABLE:
            data, samplerate = sf.read(audio_path)
            sd.play(data, samplerate)
            sd.wait()  # Wait until the audio is finished playing
            print("🔊 Audio playback finished (sounddevice)")
            return
    except Exception as e:
        print(f"sounddevice failed: {e}")
    
    try:
        # Try pygame second
        if PYGAME_AVAILABLE:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            print("🔊 Audio playback finished (pygame)")
            return
    except Exception as e:
        print(f"pygame failed: {e}")
    
    try:
        # Try pyaudio last
        if PYAUDIO_AVAILABLE:
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
            print("🔊 Audio playback finished (pyaudio)")
            return
    except Exception as e:
        print(f"pyaudio failed: {e}")
    
    print(f"🔇 All audio libraries failed. Audio saved to: {audio_path}")


def capture_and_analyze_with_speech() -> None:
    """Capture screenshot, analyze it, and play the spoken description."""
    print("📸 Capturing screenshot...")
    screenshot = ImageGrab.grab()
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    buffer.seek(0)
    files = {"image": ("screenshot.png", buffer, "image/png")}
    
    try:
        print("🔍 Analyzing image and generating speech...")
        response = requests.post(
            "http://localhost:8000/api/v1/game/analyze-and-speak",
            files=files,
            timeout=30,  # Increased timeout for AI processing
        )
        
        if response.status_code == 200:
            print("✅ Analysis complete! Playing audio...")
            # Save and play the audio response
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(response.content)
                audio_path = tmp_file.name
            
            # Use our improved audio playback function
            play_audio(audio_path)
            
            # Clean up temporary file
            try:
                os.unlink(audio_path)
            except Exception:
                pass
        else:
            print(f"❌ Request failed with status {response.status_code}: {response.text}")
            
    except requests.RequestException as exc:
        print(f"❌ Request failed: {exc}")


def capture_and_analyze_text_only() -> None:
    """Capture screenshot and get text description only."""
    print("📸 Capturing screenshot...")
    screenshot = ImageGrab.grab()
    buffer = io.BytesIO()
    screenshot.save(buffer, format="PNG")
    buffer.seek(0)
    files = {"image": ("screenshot.png", buffer, "image/png")}
    
    try:
        print("🔍 Analyzing image...")
        response = requests.post(
            "http://localhost:8000/api/v1/image/analyze",
            files=files,
            timeout=15,
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"📝 Description: {result.get('description', 'No description available')}")
        else:
            print(f"❌ Request failed with status {response.status_code}: {response.text}")
            
    except requests.RequestException as exc:
        print(f"❌ Request failed: {exc}")


def test_tts_service() -> None:
    """Test the TTS service with a sample text."""
    test_text = "Hello! This is a test of the text-to-speech service."
    
    try:
        print(f"🔊 Testing TTS with: '{test_text}'")
        response = requests.post(
            "http://localhost:8000/api/v1/tts/speak",
            json={"text": test_text, "language": "en"},
            timeout=15,
        )
        
        if response.status_code == 200:
            print("✅ TTS generation successful! Playing audio...")
            # Save and play the audio response
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(response.content)
                audio_path = tmp_file.name
            
            # Use our improved audio playback function
            play_audio(audio_path)
            
            # Clean up
            try:
                os.unlink(audio_path)
            except Exception:
                pass
        else:
            print(f"❌ TTS test failed with status {response.status_code}: {response.text}")
            
    except requests.RequestException as exc:
        print(f"❌ TTS test failed: {exc}")


def main() -> None:
    """Entry point for the client with updated hotkeys."""
    print("🎮 Sims 4 AI Gaming Assistant Client")
    print("📋 Available hotkeys:")
    print("  Ctrl+Shift+S: Capture screenshot + AI analysis + speech")
    print("  Ctrl+Shift+A: Capture screenshot + text analysis only")
    print("  Ctrl+Shift+T: Test TTS service")
    print("  Esc: Quit")
    print()
    
    # Register hotkeys for new functionality
    keyboard.add_hotkey("ctrl+shift+s", capture_and_analyze_with_speech)
    keyboard.add_hotkey("ctrl+shift+a", capture_and_analyze_text_only)
    keyboard.add_hotkey("ctrl+shift+t", test_tts_service)
    
    print("✅ Client ready! Use the hotkeys above or press Esc to quit.")
    keyboard.wait("esc")
    print("👋 Goodbye!")


if __name__ == "__main__":
    main()
