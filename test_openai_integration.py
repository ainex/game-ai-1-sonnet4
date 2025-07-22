#!/usr/bin/env python3
"""
Test script for OpenAI integration in the Sims 4 AI Gaming Assistant.

This script tests the new OpenAI-powered endpoints:
1. /api/v1/openai/analyze-game-with-voice
2. /api/v1/openai/analyze-game-text-only

Usage:
    python test_openai_integration.py
"""

import requests
import tempfile
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import io

def create_test_screenshot():
    """Create a test screenshot for testing."""
    # Create a simple test image
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some text to simulate a game UI
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    draw.text((50, 50), "Test Game Screenshot", fill='black', font=font)
    draw.text((50, 100), "Sims 4 Game Interface", fill='blue', font=font)
    draw.text((50, 150), "Character Status: Happy", fill='green', font=font)
    draw.text((50, 200), "Energy: 75%", fill='orange', font=font)
    draw.text((50, 250), "Hunger: 60%", fill='red', font=font)
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def create_test_audio():
    """Create a test audio file for testing."""
    # Create a simple WAV file (1 second of silence)
    import wave
    import struct
    
    # Create a simple sine wave
    sample_rate = 44100
    duration = 1  # 1 second
    frequency = 440  # A4 note
    
    # Generate sine wave
    samples = []
    for i in range(sample_rate * duration):
        sample = int(32767 * 0.3 * (i * frequency * 2 * 3.14159 / sample_rate))
        samples.append(struct.pack('<h', sample))
    
    # Create WAV file in memory
    wav_bytes = io.BytesIO()
    with wave.open(wav_bytes, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(samples))
    
    wav_bytes.seek(0)
    return wav_bytes.getvalue()

def test_openai_text_only():
    """Test the text-only OpenAI analysis endpoint."""
    print("🧪 Testing OpenAI text-only analysis...")
    
    try:
        # Create test screenshot
        screenshot_bytes = create_test_screenshot()
        print(f"📸 Created test screenshot: {len(screenshot_bytes)} bytes")
        
        # Prepare request
        files = {
            "image": ("test_screenshot.png", io.BytesIO(screenshot_bytes), "image/png")
        }
        data = {
            "question": "What should I do next in this game situation?",
            "system_prompt": "You are a helpful game assistant. Analyze the screenshot and provide specific advice for the player."
        }
        
        # Send request
        response = requests.post(
            "http://localhost:8000/api/v1/openai/analyze-game-text-only",
            files=files,
            data=data,
            timeout=60
        )
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ OpenAI text analysis successful!")
            print(f"❓ Question: {result.get('question', 'N/A')}")
            print(f"🤖 Response: {result.get('response', 'N/A')}")
            print(f"🔧 System prompt: {result.get('system_prompt', 'N/A')}")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"❌ Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error in text-only test: {e}")

def test_openai_with_voice():
    """Test the OpenAI analysis with voice endpoint."""
    print("\n🧪 Testing OpenAI analysis with voice...")
    
    try:
        # Create test files
        screenshot_bytes = create_test_screenshot()
        audio_bytes = create_test_audio()
        print(f"📸 Created test screenshot: {len(screenshot_bytes)} bytes")
        print(f"🎵 Created test audio: {len(audio_bytes)} bytes")
        
        # Prepare request
        files = {
            "image": ("test_screenshot.png", io.BytesIO(screenshot_bytes), "image/png"),
            "audio": ("test_audio.wav", io.BytesIO(audio_bytes), "audio/wav")
        }
        data = {
            "system_prompt": "You are a helpful game assistant. Analyze the screenshot and answer the user's question about the game situation."
        }
        
        # Send request
        response = requests.post(
            "http://localhost:8000/api/v1/openai/analyze-game-with-voice",
            files=files,
            data=data,
            timeout=120
        )
        
        print(f"📡 Response status: {response.status_code}")
        print(f"📡 Response content length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ OpenAI voice analysis successful!")
            
            # Save audio response to file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(response.content)
                audio_path = tmp_file.name
            
            print(f"💾 Audio response saved to: {audio_path}")
            print("🔊 You can play this file to hear the AI response")
            
            # Try to play the audio if pygame is available
            try:
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
                print("🔊 Playing audio response...")
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                pygame.mixer.quit()
            except ImportError:
                print("⚠️ Pygame not available - audio saved to file only")
            
            # Clean up
            try:
                os.unlink(audio_path)
                print("🧹 Temporary audio file cleaned up")
            except:
                pass
                
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"❌ Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error in voice test: {e}")

def main():
    """Run all tests."""
    print("🤖 OpenAI Integration Test Suite")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        print("✅ Server is running")
    except:
        print("❌ Server is not running. Please start the server first:")
        print("   cd server && python -m uvicorn src.main:app --reload --port 8000")
        return
    
    # Run tests
    test_openai_text_only()
    test_openai_with_voice()
    
    print("\n🎉 Test suite completed!")

if __name__ == "__main__":
    main() 