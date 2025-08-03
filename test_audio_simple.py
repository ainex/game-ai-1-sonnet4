#!/usr/bin/env python3
"""Simple audio test script."""

import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🔊 Testing audio libraries...")

# Test pygame
try:
    import pygame
    pygame.mixer.init()
    print("✅ Pygame available")
except ImportError as e:
    print(f"❌ Pygame not available: {e}")

# Test sounddevice
try:
    import sounddevice as sd
    import soundfile as sf
    print("✅ Sounddevice available")
except ImportError as e:
    print(f"❌ Sounddevice not available: {e}")

# Test pyaudio
try:
    import pyaudio
    print("✅ PyAudio available")
except ImportError as e:
    print(f"❌ PyAudio not available: {e}")

print("\n🔊 Audio test complete. At least one library should be available for sound to work.")