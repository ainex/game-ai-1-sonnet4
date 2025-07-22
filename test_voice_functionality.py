#!/usr/bin/env python3
"""Test script for voice recording functionality."""

import sys
import os
import time
import logging

# Add the client directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
client_dir = os.path.join(current_dir, 'client', 'src')
if client_dir not in sys.path:
    sys.path.insert(0, client_dir)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_audio_devices():
    """Test audio device availability."""
    logger.info("🔍 Testing audio device availability...")
    
    try:
        import sounddevice as sd
        logger.info("✅ Sounddevice imported successfully")
        
        # List available devices
        devices = sd.query_devices()
        logger.info(f"📊 Found {len(devices)} audio devices:")
        
        for i, device in enumerate(devices):
            # Handle different device structures
            name = device.get('name', 'Unknown')
            max_inputs = device.get('max_inputs', 0)
            max_outputs = device.get('max_outputs', 0)
            logger.info(f"  Device {i}: {name} (inputs: {max_inputs}, outputs: {max_outputs})")
        
        # Get default devices
        try:
            default_input = sd.query_devices(kind='input')
            logger.info(f"🎤 Default input device: {default_input.get('name', 'Unknown')}")
        except Exception as e:
            logger.warning(f"⚠️ Could not get default input device: {e}")
        
        try:
            default_output = sd.query_devices(kind='output')
            logger.info(f"🔊 Default output device: {default_output.get('name', 'Unknown')}")
        except Exception as e:
            logger.warning(f"⚠️ Could not get default output device: {e}")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Sounddevice not available: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error testing audio devices: {e}")
        return False

def test_voice_recorder():
    """Test the voice recorder functionality."""
    logger.info("🎤 Testing voice recorder...")
    
    try:
        from core.voice_recorder import get_voice_recorder
        
        recorder = get_voice_recorder()
        logger.info("✅ Voice recorder created successfully")
        
        # Test recording start
        logger.info("🎤 Starting test recording (speak for a few seconds)...")
        success = recorder.start_recording()
        
        if not success:
            logger.error("❌ Failed to start recording")
            return False
        
        logger.info("✅ Recording started successfully")
        logger.info("🎤 Please speak for a few seconds...")
        
        # Wait for recording to complete
        start_time = time.time()
        while recorder.is_recording_active():
            time.sleep(0.1)
            if time.time() - start_time > 30:  # Max 30 seconds
                logger.warning("⏰ Recording timeout, stopping manually")
                # Only call stop_recording if still active
                audio_bytes = recorder.stop_recording()
                break
        else:
            # Recording stopped naturally, get the audio
            audio_bytes = recorder.stop_recording()
        
        if audio_bytes is None:
            logger.error("❌ No audio recorded")
            return False
        
        logger.info(f"✅ Recording completed: {len(audio_bytes)} bytes")
        
        # Save audio to file for inspection
        test_file = "test_recording.wav"
        with open(test_file, "wb") as f:
            f.write(audio_bytes)
        
        logger.info(f"💾 Test recording saved to: {test_file}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error testing voice recorder: {e}")
        return False

def main():
    """Main test function."""
    logger.info("🧪 Starting voice functionality tests...")
    
    # Test 1: Audio devices
    logger.info("\n" + "="*50)
    logger.info("TEST 1: Audio Device Detection")
    logger.info("="*50)
    audio_ok = test_audio_devices()
    
    if not audio_ok:
        logger.error("❌ Audio device test failed - cannot proceed with recording test")
        return
    
    # Test 2: Voice recorder
    logger.info("\n" + "="*50)
    logger.info("TEST 2: Voice Recording")
    logger.info("="*50)
    recording_ok = test_voice_recorder()
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("TEST SUMMARY")
    logger.info("="*50)
    logger.info(f"Audio devices: {'✅ PASS' if audio_ok else '❌ FAIL'}")
    logger.info(f"Voice recording: {'✅ PASS' if recording_ok else '❌ FAIL'}")
    
    if audio_ok and recording_ok:
        logger.info("🎉 All tests passed! Voice functionality should work.")
    else:
        logger.error("❌ Some tests failed. Check the logs above for details.")

if __name__ == "__main__":
    main() 