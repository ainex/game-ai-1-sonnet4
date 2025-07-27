#!/usr/bin/env python3
"""
AI Gaming Assistant - PRODUCTION Environment Setup for Windows
This script sets up the production environment with AI models (no CUDA changes)
"""

import subprocess
import sys
import warnings
warnings.filterwarnings('ignore')

def run_command(cmd):
    """Run a shell command and handle errors."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        print(f"Error: {result.stderr}")
        return False
    print(f"✅ Success: {cmd}")
    return True

def install_production_ai():
    """Install production AI dependencies (skip CUDA since it's already installed)."""
    print("🤖 Installing PRODUCTION AI dependencies...")
    
    # Install specific versions for better compatibility
    ai_packages = [
        "transformers>=4.35.0",
        "accelerate>=0.24.0", 
        "datasets>=2.14.0",
        "tokenizers>=0.15.0",
        "sentencepiece>=0.1.99",
        "safetensors>=0.4.0",
        "huggingface-hub>=0.19.0",
        "TTS>=0.19.0",
        "librosa>=0.10.0", 
        "pydub>=0.25.0",
        "scipy>=1.11.0",
        "soundfile>=0.12.0"
    ]
    
    for package in ai_packages:
        if not run_command(f"pip install --no-cache-dir {package}"):
            print(f"Failed to install {package}")
            return False
    
    return True

def download_production_models():
    """Download AI models for production."""
    print("📥 Downloading AI models for production...")
    
    try:
        print("Importing required packages...")
        from transformers import pipeline
        from TTS.api import TTS
        import torch
        
        print('Downloading image captioning model...')
        # Use pipeline to properly download the image-to-text model
        captioner = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
        print('✅ Image captioning model downloaded')
        
        print('Downloading TTS model...')
        # Use CPU to avoid GPU compatibility issues  
        tts = TTS(model_name='tts_models/en/ljspeech/tacotron2-DDC', progress_bar=True, gpu=False)
        print('✅ TTS model downloaded')
        
        print('✅ All production AI models downloaded!')
        return True
        
    except Exception as e:
        print(f'❌ Model download error: {e}')
        return False

def main():
    """Main production setup."""
    print("🚀 Starting PRODUCTION setup for Windows...")
    print("(Skipping CUDA installation - using existing CUDA)")
    
    # Install production AI packages
    if not install_production_ai():
        print("❌ Failed to install AI packages")
        sys.exit(1)
    
    # Download models
    if not download_production_models():
        print("❌ Failed to download models")
        sys.exit(1)
    
    print("\n🎉 PRODUCTION environment setup complete!")
    print("")
    print("🚀 Production AI Ready:")
    print("   - Using existing CUDA installation")
    print("   - All AI models downloaded and cached")
    print("   - Production-grade package versions")
    print("   - Ready for production deployment")
    print("")
    print("🔄 Please restart your server to use the new setup!")

if __name__ == "__main__":
    main() 