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
from ui.overlay import get_overlay, get_root
from core.config import get_config

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
    config = get_config()
    
    logger.info(f"🎵 Audio file generated: {audio_path}")
    logger.info(f"📊 Audio file size: {os.path.getsize(audio_path)} bytes")
    
    # Check feature flag for TTS
    if not config.get_feature("use_tts"):
        logger.info(f"🔇 TTS disabled by feature flag. Audio saved to: {audio_path}")
        return
    
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


def capture_screenshot_and_record_voice_claude():
    """Capture screenshot AND record voice, then send both to Claude for analysis with overlay display."""
    try:
        logger.info("🤖 Starting Claude-powered screenshot + voice capture...")
        
        # Get overlay, voice recorder, and config
        overlay = get_overlay()
        recorder = get_voice_recorder()
        config = get_config()
        
        # Reset recorder to ensure clean state
        recorder.reset()
        
        _claude_analysis_main(overlay, recorder, config)
        
    except KeyboardInterrupt:
        logger.warning("⚠️ Claude analysis interrupted by KeyboardInterrupt")
        print("⚠️ Analysis interrupted - please try again")
    except Exception as e:
        logger.error(f"❌ Unexpected error in Claude analysis: {e}")
        print(f"❌ Analysis failed: {e}")
        try:
            overlay = get_overlay()
            overlay.display_error(f"Analysis failed: {e}")
        except:
            pass


def _claude_analysis_main(overlay, recorder, config):
    """Main Claude analysis logic separated for better error handling."""
    try:
        # Show processing status in overlay
        overlay.set_processing_status()
        
        # Step 1: Capture screenshot
        logger.info("📸 Capturing screenshot...")
        try:
            screenshot = ImageGrab.grab()
            logger.info(f"📸 Screenshot captured: {screenshot.size} pixels")
        except Exception as e:
            logger.error(f"❌ Screenshot capture failed: {e}")
            overlay.display_error(f"Screenshot capture failed: {e}")
            return
        
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
            overlay.display_error("Voice recording failed. Please check your microphone.")
            return
        
        # Wait for recording to complete (it will auto-stop on silence)
        print("🎤 Recording... (speak for at least 1 second, then auto-stops after 2 seconds of silence)")
        wait_start_time = time.time()
        max_wait_time = 35.0  # Maximum time to wait for recording to complete
        
        while recorder.is_recording_active():
            # Check if auto-stop was triggered
            if recorder.stop_event.is_set():
                break
            
            # Check for timeout
            if time.time() - wait_start_time > max_wait_time:
                logger.warning("⚠️ Recording wait timeout - forcing stop")
                recorder.stop_event.set()
                break
                
            time.sleep(0.1)
        
        # Get recorded audio (stop_recording will handle the cleanup)
        audio_bytes = recorder.stop_recording()
        if audio_bytes is None:
            logger.warning("⚠️ No audio recorded, aborting")
            print("⚠️ No voice recorded. Please try again.")
            overlay.display_error("No voice recorded. Please speak louder or check your microphone.")
            return
        
        logger.info(f"🎵 Voice recorded: {len(audio_bytes)} bytes")
        print(f"✅ Voice recording completed: {len(audio_bytes)} bytes")
        
        # Step 3: First transcribe the audio to get the question text
        logger.info("🎤 Transcribing voice to text...")
        try:
            # Call transcription endpoint first
            transcribe_response = requests.post(
                "http://localhost:8000/api/v1/stt/transcribe",
                files={"audio": ("voice.wav", io.BytesIO(audio_bytes), "audio/wav")},
                timeout=30
            )
            
            if transcribe_response.status_code != 200:
                logger.error(f"❌ Transcription failed: {transcribe_response.status_code}")
                overlay.display_error("Failed to transcribe voice. Please try again.")
                return
                
            transcription_result = transcribe_response.json()
            user_question = transcription_result.get('transcription', '').strip()
            logger.info(f"📝 Transcribed question: '{user_question}'")
            
            # Check if transcription is empty
            if not user_question:
                logger.warning("⚠️ No speech detected in audio")
                overlay.display_error("No speech detected. Please speak louder and try again.")
                return
            
        except Exception as e:
            logger.error(f"❌ Transcription error: {e}")
            overlay.display_error(f"Transcription error: {e}")
            return
        
        # Step 4: Send to Claude for analysis
        logger.info("🤖 Sending to Claude for analysis...")
        print("🤖 Analyzing with Claude...")
        
        # Prepare system prompt
        system_prompt = "You are the greatest gamer and assistant. Here is my game situation screenshot and my question. Provide specific, actionable advice for the player."
        
        # Get the default model from config
        default_model = config.get_model("default")
        
        # Check if we need TTS or just text
        use_tts = config.get_feature("use_tts")
        
        if use_tts:
            # Call the voice endpoint that returns audio
            screenshot_buffer.seek(0)
            files = {
                "image": ("screenshot.png", screenshot_buffer, "image/png"),
                "audio": ("voice.wav", io.BytesIO(audio_bytes), "audio/wav")
            }
            data = {
                "system_prompt": system_prompt,
                "model": default_model
            }
            
            response = requests.post(
                "http://localhost:8000/api/v1/claude/analyze-game-with-voice",
                files=files,
                data=data,
                timeout=120
            )
        else:
            # TTS disabled - only get text response
            screenshot_buffer.seek(0)
            files = {"image": ("screenshot.png", screenshot_buffer, "image/png")}
            data = {
                "question": user_question,
                "system_prompt": system_prompt,
                "model": default_model
            }
            
            response = requests.post(
                "http://localhost:8000/api/v1/claude/analyze-game-text-only",
                files=files,
                data=data,
                timeout=120
            )
        
        logger.info(f"📡 Server response status: {response.status_code}")
        
        if response.status_code == 200:
            if use_tts:
                # Handle audio response
                logger.info("✅ Claude analysis complete! Processing audio response...")
                print("✅ Analysis complete! Response will be shown in overlay and played as audio.")
                
                # Save audio response
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    tmp_file.write(response.content)
                    audio_path = tmp_file.name
                
                logger.info(f"💾 Audio response saved: {audio_path}")
                
                # Also get text for overlay (make text-only call)
                screenshot_buffer.seek(0)
                text_response = requests.post(
                    "http://localhost:8000/api/v1/claude/analyze-game-text-only",
                    files={"image": ("screenshot.png", screenshot_buffer, "image/png")},
                    data={"question": user_question, "system_prompt": system_prompt, "model": default_model},
                    timeout=60
                )
                
                if text_response.status_code == 200:
                    text_result = text_response.json()
                    ai_text = text_result.get('response', 'Analysis completed.')
                    overlay.display_response(ai_text)
                else:
                    overlay.display_response("Analysis completed. Audio response is ready.")
                
                # Play audio
                play_audio(audio_path)
                
                # Clean up audio file
                try:
                    os.unlink(audio_path)
                except Exception as e:
                    logger.warning(f"⚠️ Failed to clean up audio: {e}")
            else:
                # Handle text-only response
                logger.info("✅ Claude analysis complete!")
                print("✅ Analysis complete! Response displayed in overlay.")
                
                result = response.json()
                ai_text = result.get('response', 'Analysis completed.')
                model_used = result.get('model', default_model)
                logger.info(f"🤖 Claude response ({model_used}): {ai_text[:200]}...")
                overlay.display_response(f"[{model_used}] {ai_text}")
        else:
            logger.error(f"❌ Request failed with status {response.status_code}")
            logger.error(f"❌ Response text: {response.text}")
            print(f"❌ Analysis failed: {response.status_code}")
            overlay.display_error(f"Analysis failed: {response.status_code}\n{response.text}")
            
    except requests.RequestException as exc:
        logger.error(f"❌ Request failed: {exc}")
        print(f"❌ Connection failed: {exc}")
        overlay.display_error(f"Connection failed: {exc}")
    except Exception as exc:
        logger.error(f"❌ Unexpected error: {exc}")
        print(f"❌ Error: {exc}")
        overlay.display_error(f"Unexpected error: {exc}")


def capture_and_analyze_with_speech() -> None:
    """Capture screenshot, analyze it, and play the spoken description."""
    logger.info("📸 Capturing screenshot...")
    
    # Get overlay and config
    overlay = get_overlay()
    config = get_config()
    
    try:
        # Show processing status
        overlay.set_processing_status()
        
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
            logger.info("✅ Analysis complete!")
            
            # Get the text description from server (need to make another call for JSON response)
            buffer.seek(0)
            text_response = requests.post(
                "http://localhost:8000/api/v1/image/analyze",
                files={"image": ("screenshot.png", buffer, "image/png")},
                timeout=15
            )
            
            description = "Game scene analyzed successfully."
            if text_response.status_code == 200:
                result = text_response.json()
                description = result.get('description', description)
            
            # Display in overlay
            overlay.display_response(description)
            
            # Handle audio if TTS is enabled
            if config.get_feature("use_tts"):
                # Save and play the audio response
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                    tmp_file.write(response.content)
                    audio_path = tmp_file.name
                
                logger.info(f"💾 Audio saved to temporary file: {audio_path}")
                play_audio(audio_path)
                
                # Clean up temporary file
                try:
                    os.unlink(audio_path)
                    logger.info("🧹 Temporary audio file cleaned up")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to clean up temporary file: {e}")
            else:
                logger.info("🔇 TTS disabled - showing text only")
                print("✅ Analysis complete! Response displayed in overlay.")
        else:
            logger.error(f"❌ Request failed with status {response.status_code}")
            logger.error(f"❌ Response text: {response.text}")
            overlay.display_error(f"Analysis failed: {response.status_code}\n{response.text}")
            
    except requests.RequestException as exc:
        logger.error(f"❌ Request failed: {exc}")
        overlay.display_error(f"Connection failed: {exc}")
    except Exception as exc:
        logger.error(f"❌ Unexpected error: {exc}")
        overlay.display_error(f"Unexpected error: {exc}")


def capture_and_analyze_text_only() -> None:
    """Capture screenshot and get text description only."""
    logger.info("📸 Capturing screenshot...")
    
    # Get overlay
    overlay = get_overlay()
    
    try:
        # Show processing status
        overlay.set_processing_status()
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
            
            # Display in overlay
            overlay.display_response(description)
            print("✅ Analysis complete! Response displayed in overlay.")
        else:
            logger.error(f"❌ Request failed with status {response.status_code}")
            logger.error(f"❌ Response text: {response.text}")
            overlay.display_error(f"Analysis failed: {response.status_code}\n{response.text}")
            
    except requests.RequestException as exc:
        logger.error(f"❌ Request failed: {exc}")
        overlay.display_error(f"Connection failed: {exc}")
    except Exception as exc:
        logger.error(f"❌ Unexpected error: {exc}")
        overlay.display_error(f"Unexpected error: {exc}")


def capture_screenshot_and_record_voice() -> None:
    """Capture screenshot AND record voice, then send both to OpenAI for analysis."""
    logger.info("🎮 Starting OpenAI-powered screenshot + voice capture...")
    
    # Get overlay and config
    overlay = get_overlay()
    config = get_config()
    
    # Get voice recorder and reset state
    recorder = get_voice_recorder()
    recorder.reset()
    
    try:
        # Show processing status
        overlay.set_processing_status()
        
        
        # Step 1: Capture screenshot
        logger.info("📸 Capturing screenshot...")
        try:
            screenshot = ImageGrab.grab()
            logger.info(f"📸 Screenshot captured: {screenshot.size} pixels")
        except Exception as e:
            logger.error(f"❌ Screenshot capture failed: {e}")
            overlay.display_error(f"Screenshot capture failed: {e}")
            return
        
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
            overlay.display_error("Voice recording failed. Please check your microphone.")
            # Fall back to screenshot-only mode
            capture_and_analyze_with_speech()
            return
        
        # Wait for recording to complete (it will auto-stop on silence)
        print("🎤 Recording... (speak for at least 1 second, then auto-stops after 2 seconds of silence)")
        wait_start_time = time.time()
        max_wait_time = 35.0  # Maximum time to wait for recording to complete
        
        while recorder.is_recording_active():
            # Check for timeout
            if time.time() - wait_start_time > max_wait_time:
                logger.warning("⚠️ Recording wait timeout - forcing stop")
                recorder.stop_event.set()
                break
                
            time.sleep(0.1)
        
        # Get recorded audio
        audio_bytes = recorder.stop_recording()
        if audio_bytes is None:
            logger.warning("⚠️ No audio recorded, using screenshot only")
            print("⚠️ No voice recorded. Using screenshot only.")
            overlay.display_error("No voice recorded. Please speak louder or check your microphone.")
            # Fall back to screenshot-only mode
            capture_and_analyze_with_speech()
            return
        
        logger.info(f"🎵 Voice recorded: {len(audio_bytes)} bytes")
        print(f"✅ Voice recording completed: {len(audio_bytes)} bytes")
        
        # Step 3: Send both to OpenAI server
        logger.info("🤖 Sending screenshot + voice to OpenAI for analysis...")
        print("🤖 Analyzing screenshot and voice with OpenAI...")
        
        # Get the default model from config (will use OpenAI default if it's not an OpenAI model)
        default_model = config.get_model("default")
        if default_model not in config.get_available_models("openai"):
            # Use OpenAI default if configured model is not an OpenAI model
            openai_model = None
        else:
            openai_model = default_model
        
        # Prepare files for upload with system prompt
        screenshot_buffer.seek(0)
        files = {
            "image": ("screenshot.png", screenshot_buffer, "image/png"),
            "audio": ("voice.wav", io.BytesIO(audio_bytes), "audio/wav")
        }
        data = {
            "system_prompt": "You are a helpful game assistant. Analyze the screenshot and answer the user's question about the game situation. Provide specific, actionable advice for the player."
        }
        if openai_model:
            data["model"] = openai_model
        
        response = requests.post(
            "http://localhost:8000/api/v1/openai/analyze-game-with-voice",
            files=files,
            data=data,
            timeout=120,  # Longer timeout for OpenAI processing
        )
        
        logger.info(f"📡 Server response status: {response.status_code}")
        logger.info(f"📡 Server response headers: {dict(response.headers)}")
        logger.info(f"📡 Response content length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            logger.info("✅ Combined analysis complete!")
            
            # Display a message in the overlay (OpenAI returns audio, not text)
            overlay.display_response("Analysis complete! OpenAI has generated a response.")
            
            # Handle audio if TTS is enabled
            if config.get_feature("use_tts"):
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
                logger.info("🔇 TTS disabled - OpenAI response received but not played")
                print("✅ Analysis complete! (TTS disabled - check logs for details)")
        else:
            logger.error(f"❌ Request failed with status {response.status_code}")
            logger.error(f"❌ Response text: {response.text}")
            print(f"❌ Analysis failed: {response.status_code}")
            overlay.display_error(f"Analysis failed: {response.status_code}\n{response.text}")
            
    except requests.RequestException as exc:
        logger.error(f"❌ Request failed: {exc}")
        print(f"❌ Connection failed: {exc}")
        overlay.display_error(f"Connection failed: {exc}")
    except Exception as exc:
        logger.error(f"❌ Unexpected error: {exc}")
        print(f"❌ Error: {exc}")
        overlay.display_error(f"Unexpected error: {exc}")


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
    logger.info("🎮 AI Gaming Assistant Client Starting...")
    
    # Initialize Tkinter root window early
    root = get_root()
    
    # Get config to show current settings
    config = get_config()
    tts_status = "enabled" if config.get_feature("use_tts") else "disabled"
    
    print("AI Gaming Assistant Client - Phase 1")
    print(f"Configuration: TTS is {tts_status} (default: disabled)")
    print("Available hotkeys:")
    print("  Ctrl+Shift+C: Claude analysis with voice + overlay display")
    print("  Ctrl+Shift+V: OpenAI voice + screenshot analysis")
    print("  Ctrl+Shift+S: Screenshot + AI analysis")
    print("  Ctrl+Shift+A: Screenshot + text analysis only")
    print("  Ctrl+Shift+T: Test TTS service")
    print("  Esc: Quit")
    print()
    print("Phase 1 Features:")
    print("  - Voice questions are transcribed and analyzed")
    print("  - AI responses shown in transparent overlay window")
    print("  - Audio responses saved but not played (TTS disabled)")
    print("  - All responses logged to console and files")
    print()
    print("RECOMMENDED: Use Ctrl+Shift+C for Claude-powered analysis!")
    print("Voice recording: speak for 1+ seconds, then auto-stops after 2s silence")
    print()
    
    # Register hotkeys for new functionality
    keyboard.add_hotkey("ctrl+shift+c", capture_screenshot_and_record_voice_claude)  # NEW Claude with overlay
    keyboard.add_hotkey("ctrl+shift+v", capture_screenshot_and_record_voice)         # OpenAI combined function
    keyboard.add_hotkey("ctrl+shift+s", capture_and_analyze_with_speech)             # Existing screenshot + TTS
    keyboard.add_hotkey("ctrl+shift+a", capture_and_analyze_text_only)               # Existing screenshot only
    keyboard.add_hotkey("ctrl+shift+t", test_tts_service)                            # Existing TTS test
    
    # Flag to control main loop
    running = True
    
    def quit_app():
        nonlocal running
        running = False
        root.quit()
    
    keyboard.add_hotkey("esc", quit_app)
    
    logger.info("Client ready! Use the hotkeys above or press Esc to quit.")
    print("Client ready! Use the hotkeys above or press Esc to quit.")
    
    # Run Tkinter event loop with periodic updates
    while running:
        try:
            root.update()
            # Use root.after instead of time.sleep to avoid KeyboardInterrupt issues
            root.update_idletasks()
            time.sleep(0.01)  # Small delay to prevent high CPU usage
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully - but continue running for hotkeys
            logger.info("KeyboardInterrupt caught in main loop - continuing...")
            continue
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            break
    
    logger.info("Client shutting down...")
    print("Goodbye!")


if __name__ == "__main__":
    main()
