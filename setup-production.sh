#!/bin/bash

# AI Gaming Assistant - PRODUCTION Environment Setup Script
# This script sets up the FULL production environment with heavy AI models
# Use this for actual deployment on Windows or production Linux servers

set -e  # Exit on any error

echo "🚀 Setting up AI Gaming Assistant PRODUCTION environment..."

# Install heavy AI dependencies
install_production_ai() {
    echo "🤖 Installing PRODUCTION AI dependencies..."

    # Install CUDA toolkit for GPU acceleration
    echo "Installing CUDA support for GPU acceleration..."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update
        sudo apt-get install -y nvidia-cuda-toolkit
    fi

    # Install heavy AI packages
    echo "Installing FULL AI/ML packages..."
    pip install --no-cache-dir torch>=2.0.0 torchvision>=0.15.0 torchaudio>=2.0.0 --index-url https://download.pytorch.org/whl/cu118

    pip install --no-cache-dir \
        transformers>=4.35.0 \
        accelerate>=0.24.0 \
        datasets>=2.14.0 \
        tokenizers>=0.15.0 \
        sentencepiece>=0.1.99 \
        safetensors>=0.4.0 \
        huggingface-hub>=0.19.0

    # Install full TTS and audio processing
    pip install --no-cache-dir \
        TTS>=0.19.0 \
        librosa>=0.10.0 \
        pydub>=0.25.0 \
        scipy>=1.11.0 \
        soundfile>=0.12.0
}

# Download AI models for production
download_production_models() {
    echo "📥 Downloading AI models for production..."

    python3 -c "
import warnings
warnings.filterwarnings('ignore')

try:
    from transformers import AutoProcessor, AutoModelForCausalLM
    from TTS.api import TTS
    import torch

    print('Downloading image captioning model...')
    model_name = 'nlpconnect/vit-gpt2-image-captioning'
    processor = AutoProcessor.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print('✅ Image captioning model downloaded')

    print('Downloading TTS model...')
    gpu_available = torch.cuda.is_available()
    print(f'GPU available: {gpu_available}')

    tts = TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2', progress_bar=True, gpu=gpu_available)
    print('✅ TTS model downloaded')

    print('✅ All production AI models downloaded!')

except Exception as e:
    print(f'❌ Model download error: {e}')
    exit(1)
"
}

# Main production setup
main() {
    echo "🚀 Starting PRODUCTION setup..."

    # Run basic setup first (reuse from main setup.sh)
    if [ -f "./setup.sh" ]; then
        # Run the basic setup but skip AI parts
        echo "Running basic environment setup..."
        # You would modify this to skip AI parts or create a base setup function
    fi

    # Install production AI
    install_production_ai

    # Download models
    download_production_models

    echo "🎉 PRODUCTION environment setup complete!"
    echo ""
    echo "🚀 Production AI Ready:"
    echo "   - Full CUDA GPU support"
    echo "   - All AI models downloaded"
    echo "   - Heavy TTS/Audio processing libraries"
    echo "   - Ready for production deployment"
    echo ""
}

# Run main function
main "$@"
