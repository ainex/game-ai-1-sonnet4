#!/usr/bin/env python3
"""Debug script to test the services directly."""

import requests
import io
from PIL import Image, ImageDraw

def test_dependencies():
    """Test if required dependencies are available."""
    print("🔍 Testing dependencies...")
    
    # Test transformers
    try:
        from transformers import pipeline
        print("✅ transformers available")
        try:
            captioner = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
            print("✅ Image captioning model loaded successfully")
        except Exception as e:
            print(f"❌ Image captioning model failed to load: {e}")
    except ImportError as e:
        print(f"❌ transformers not available: {e}")
    
    # Test TTS
    try:
        from TTS.api import TTS
        print("✅ TTS available")
        try:
            tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=False)
            print("✅ TTS model loaded successfully")
        except Exception as e:
            print(f"❌ TTS model failed to load: {e}")
    except ImportError as e:
        print(f"❌ TTS not available: {e}")

def create_test_image():
    """Create a simple test image."""
    img = Image.new('RGB', (300, 200), color='white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([50, 50, 250, 150], fill='blue', outline='black')
    draw.text((100, 100), "TEST IMAGE", fill='white')
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

def test_image_analysis():
    """Test the image analysis endpoint."""
    print("\n🔍 Testing image analysis endpoint...")
    
    test_image = create_test_image()
    files = {"image": ("test.png", test_image, "image/png")}
    
    try:
        response = requests.post("http://localhost:8000/api/v1/image/analyze", files=files, timeout=30)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

def test_tts():
    """Test the TTS endpoint."""
    print("\n🔊 Testing TTS endpoint...")
    
    test_data = {"text": "Hello, this is a test", "language": "en"}
    
    try:
        response = requests.post("http://localhost:8000/api/v1/tts/speak", json=test_data, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Content-Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            if len(response.content) > 0:
                # Save to file for inspection
                with open("test_tts_output.wav", "wb") as f:
                    f.write(response.content)
                print("✅ TTS response saved to test_tts_output.wav")
                
                # Check WAV header
                if response.content.startswith(b'RIFF'):
                    print("✅ Response appears to be a valid WAV file")
                else:
                    print("❌ Response does not appear to be a valid WAV file")
                    print(f"First 20 bytes: {response.content[:20]}")
            else:
                print("❌ Empty response")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

def test_combined_endpoint():
    """Test the combined game analysis endpoint."""
    print("\n🎮 Testing combined game analysis endpoint...")
    
    test_image = create_test_image()
    files = {"image": ("test.png", test_image, "image/png")}
    
    try:
        response = requests.post("http://localhost:8000/api/v1/game/analyze-and-speak", files=files, timeout=60)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        print(f"Content-Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            if len(response.content) > 0:
                with open("test_combined_output.wav", "wb") as f:
                    f.write(response.content)
                print("✅ Combined response saved to test_combined_output.wav")
                
                if response.content.startswith(b'RIFF'):
                    print("✅ Response appears to be a valid WAV file")
                else:
                    print("❌ Response does not appear to be a valid WAV file")
                    print(f"First 20 bytes: {response.content[:20]}")
            else:
                print("❌ Empty response")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    print("🐛 Starting service diagnostics...\n")
    test_dependencies()
    test_image_analysis()
    test_tts()
    test_combined_endpoint()
    print("\n✅ Diagnostics complete!") 