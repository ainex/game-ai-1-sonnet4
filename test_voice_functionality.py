#!/usr/bin/env python3
"""Test script for voice recording and STT functionality."""

import requests
import time
import io
from PIL import Image, ImageDraw, ImageFont

def create_test_image():
    """Create a simple test image for testing."""
    # Create a test image
    img = Image.new('RGB', (800, 600))
    img.paste((173, 216, 230), [0, 0, 800, 600])  # lightblue background
    draw = ImageDraw.Draw(img)
    
    # Draw some test content
    draw.rectangle([50, 50, 750, 550], fill='white', outline='black', width=3)
    draw.text((100, 100), "TEST SCREENSHOT", fill='black')
    draw.text((100, 150), "This is a test image for", fill='black')
    draw.text((100, 200), "the AI gaming assistant", fill='black')
    draw.ellipse([350, 300, 450, 400], fill='red', outline='darkred', width=3)  # circle using ellipse
    draw.text((350, 450), "Test Element", fill='black')
    
    # Save to buffer
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

def test_server_health():
    """Test if server is running."""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print(f"❌ Server returned status {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Server is not accessible: {e}")
        return False

def test_image_analysis():
    """Test image analysis endpoint."""
    print("\n🧪 Testing image analysis...")
    
    try:
        test_image = create_test_image()
        files = {"image": ("test.png", test_image, "image/png")}
        
        response = requests.post(
            "http://localhost:8000/api/v1/image/analyze",
            files=files,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            description = result.get('description', 'No description')
            print(f"✅ Image analysis works: '{description}'")
            return True
        else:
            print(f"❌ Image analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Image analysis error: {e}")
        return False

def test_stt_service():
    """Test STT service availability."""
    print("\n🧪 Testing STT service availability...")
    
    try:
        response = requests.get(
            "http://localhost:8000/api/v1/stt/test",
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            status = result.get('status', 'unknown')
            message = result.get('message', 'No message')
            
            if status == 'available':
                print(f"✅ STT service is ready: {message}")
                return True
            else:
                print(f"⚠️ STT service status: {status} - {message}")
                return False
        else:
            print(f"❌ STT test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ STT test error: {e}")
        return False

def test_tts_service():
    """Test TTS service."""
    print("\n🧪 Testing TTS service...")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/tts/speak",
            json={"text": "Hello! This is a test of the text to speech service.", "language": "en"},
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ TTS service works: {len(response.content)} bytes of audio generated")
            return True
        else:
            print(f"❌ TTS service failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ TTS service error: {e}")
        return False

def test_voice_recorder():
    """Test the voice recorder module."""
    print("\n🧪 Testing voice recorder...")
    
    try:
        # Import the voice recorder
        import sys
        import os
        client_src_path = os.path.join(os.path.dirname(__file__), 'client', 'src')
        if client_src_path not in sys.path:
            sys.path.append(client_src_path)
        
        # Try to import with exception handling
        try:
            from core.voice_recorder import get_voice_recorder  # type: ignore
        except ImportError as ie:
            print(f"⚠️ Could not import voice recorder module: {ie}")
            print("This is expected if running from a different location.")
            return False
        
        recorder = get_voice_recorder()
        print("✅ Voice recorder module imported successfully")
        
        # Test recorder initialization
        if hasattr(recorder, 'start_recording') and hasattr(recorder, 'stop_recording'):
            print("✅ Voice recorder has required methods")
            return True
        else:
            print("❌ Voice recorder missing required methods")
            return False
            
    except Exception as e:
        print(f"❌ Voice recorder test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Voice + Screenshot Functionality")
    print("=" * 50)
    
    tests = [
        ("Server Health", test_server_health),
        ("Image Analysis", test_image_analysis),
        ("STT Service", test_stt_service),
        ("TTS Service", test_tts_service),
        ("Voice Recorder", test_voice_recorder),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The voice + screenshot functionality should work.")
        print("\n🎯 Next steps:")
        print("1. Start the server: cd server && python -m uvicorn src.main:app --reload")
        print("2. Start the client: cd client && python src/main.py")
        print("3. Press Ctrl+Shift+V to test the complete workflow!")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("- Make sure the server is running")
        print("- Check that all dependencies are installed")
        print("- Verify your microphone is working")

if __name__ == "__main__":
    main() 