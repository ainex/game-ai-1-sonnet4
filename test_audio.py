#!/usr/bin/env python3
"""Test script to verify audio playback functionality."""

import os
import tempfile
import logging
import numpy as np
import soundfile as sf

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_audio():
    """Create a simple test audio file."""
    # Generate a simple sine wave
    sample_rate = 22050
    duration = 2.0  # seconds
    frequency = 440.0  # Hz (A4 note)
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.3  # 30% volume
    
    logger.info(f"🎵 Generated test audio: {len(audio_data)} samples, {sample_rate} Hz")
    return audio_data, sample_rate

def test_audio_libraries():
    """Test all available audio libraries."""
    logger.info("🧪 Testing audio libraries...")
    
    # Create test audio
    audio_data, sample_rate = create_test_audio()
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        sf.write(tmp_file.name, audio_data, sample_rate, format='WAV')
        audio_path = tmp_file.name
    
    logger.info(f"💾 Test audio saved to: {audio_path}")
    logger.info(f"📊 File size: {os.path.getsize(audio_path)} bytes")
    
    # Test sounddevice
    try:
        import sounddevice as sd
        logger.info("🔊 Testing sounddevice...")
        data, sr = sf.read(audio_path)
        logger.info(f"📊 Loaded audio: {data.shape}, {sr} Hz")
        sd.play(data, sr)
        sd.wait()
        logger.info("✅ sounddevice test successful")
    except Exception as e:
        logger.error(f"❌ sounddevice test failed: {e}")
    
    # Test pygame
    try:
        import pygame
        pygame.mixer.init()
        logger.info("🔊 Testing pygame...")
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        logger.info("✅ pygame test successful")
    except Exception as e:
        logger.error(f"❌ pygame test failed: {e}")
    
    # Test pyaudio
    try:
        import pyaudio
        import wave
        logger.info("🔊 Testing pyaudio...")
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
        logger.info("✅ pyaudio test successful")
    except Exception as e:
        logger.error(f"❌ pyaudio test failed: {e}")
    
    # Clean up
    try:
        os.unlink(audio_path)
        logger.info("🧹 Test file cleaned up")
    except Exception as e:
        logger.warning(f"⚠️ Failed to clean up test file: {e}")

if __name__ == "__main__":
    test_audio_libraries() 