#!/usr/bin/env python3
"""Test script to verify server endpoints are working."""

import requests
import tempfile
import os
import logging
from PIL import ImageGrab
import io

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_tts_endpoint():
    """Test the TTS endpoint."""
    logger.info("🧪 Testing TTS endpoint...")
    
    try:
        response = requests.get("http://localhost:8000/api/v1/tts/test", timeout=30)
        logger.info(f"📡 TTS test response status: {response.status_code}")
        logger.info(f"📡 TTS test response headers: {dict(response.headers)}")
        logger.info(f"📡 TTS test response size: {len(response.content)} bytes")
        
        if response.status_code == 200:
            logger.info("✅ TTS test successful!")
            
            # Save the audio for inspection
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(response.content)
                audio_path = tmp_file.name
            
            logger.info(f"💾 TTS test audio saved to: {audio_path}")
            logger.info(f"📊 Audio file size: {os.path.getsize(audio_path)} bytes")
            
            return audio_path
        else:
            logger.error(f"❌ TTS test failed: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"❌ TTS test error: {e}")
        return None

def test_image_analysis_endpoint():
    """Test the image analysis endpoint."""
    logger.info("🧪 Testing image analysis endpoint...")
    
    try:
        # Capture a screenshot
        screenshot = ImageGrab.grab()
        logger.info(f"📸 Captured screenshot: {screenshot.size} pixels")
        
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        buffer.seek(0)
        image_size = len(buffer.getvalue())
        logger.info(f"📸 Screenshot size: {image_size} bytes")
        
        files = {"image": ("screenshot.png", buffer, "image/png")}
        
        response = requests.post(
            "http://localhost:8000/api/v1/image/analyze",
            files=files,
            timeout=30
        )
        
        logger.info(f"📡 Image analysis response status: {response.status_code}")
        logger.info(f"📡 Image analysis response size: {len(response.content)} bytes")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ Image analysis successful!")
            logger.info(f"📝 Analysis result: {result}")
            return result
        else:
            logger.error(f"❌ Image analysis failed: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Image analysis error: {e}")
        return None

def test_game_analysis_endpoint():
    """Test the game analysis endpoint."""
    logger.info("🧪 Testing game analysis endpoint...")
    
    try:
        # Capture a screenshot
        screenshot = ImageGrab.grab()
        logger.info(f"📸 Captured screenshot: {screenshot.size} pixels")
        
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG")
        buffer.seek(0)
        image_size = len(buffer.getvalue())
        logger.info(f"📸 Screenshot size: {image_size} bytes")
        
        files = {"image": ("screenshot.png", buffer, "image/png")}
        
        response = requests.post(
            "http://localhost:8000/api/v1/game/analyze-and-speak",
            files=files,
            timeout=60  # Longer timeout for AI processing
        )
        
        logger.info(f"📡 Game analysis response status: {response.status_code}")
        logger.info(f"📡 Game analysis response headers: {dict(response.headers)}")
        logger.info(f"📡 Game analysis response size: {len(response.content)} bytes")
        
        if response.status_code == 200:
            logger.info("✅ Game analysis successful!")
            
            # Save the audio for inspection
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(response.content)
                audio_path = tmp_file.name
            
            logger.info(f"💾 Game analysis audio saved to: {audio_path}")
            logger.info(f"📊 Audio file size: {os.path.getsize(audio_path)} bytes")
            
            return audio_path
        else:
            logger.error(f"❌ Game analysis failed: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Game analysis error: {e}")
        return None

def main():
    """Run all tests."""
    logger.info("🚀 Starting server tests...")
    
    # Test TTS endpoint
    tts_audio = test_tts_endpoint()
    
    # Test image analysis endpoint
    image_result = test_image_analysis_endpoint()
    
    # Test game analysis endpoint
    game_audio = test_game_analysis_endpoint()
    
    logger.info("🏁 Server tests completed!")
    
    if tts_audio:
        logger.info(f"✅ TTS test passed - audio saved to: {tts_audio}")
    else:
        logger.error("❌ TTS test failed")
    
    if image_result:
        logger.info(f"✅ Image analysis test passed - result: {image_result}")
    else:
        logger.error("❌ Image analysis test failed")
    
    if game_audio:
        logger.info(f"✅ Game analysis test passed - audio saved to: {game_audio}")
    else:
        logger.error("❌ Game analysis test failed")

if __name__ == "__main__":
    main() 