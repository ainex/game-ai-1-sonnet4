## General Solution Description (sd)

This implementation adds **local AI capabilities** to the AI Gaming Assistant:

1. **Local Image Recognition**: Use `nlpconnect/vit-gpt2-image-captioning` to analyze screenshots and generate descriptive text about the game state
2. **Local Text-to-Speech**: Use `XTTS-v2` (Coqui TTS) to read image analysis results aloud to the user
3. **Server-side Processing**: Both models run on the FastAPI server to utilize the 4070S GPU (12GB VRAM)
4. **Client Trigger**: Simple client-side buttons to capture screenshots and request TTS playback

### Key Benefits:

- **Fully Offline**: No internet required for core AI functionality
- **GPU Optimized**: Leverages 4070S with 12GB VRAM efficiently
- **Multilingual TTS**: Support for English, Russian, German via XTTS-v2
- **Game-Aware**: Image captioning specifically for game UI and gameplay elements

## Dependencies and Dependants Investigation

### Current Dependencies (Already in [setup.sh](http://setup.sh/)):

- ✅ **FastAPI/Uvicorn**: Server framework
- ✅ **Pillow**: Image processing
- ✅ **SQLAlchemy**: Database for storing analysis history
- ✅ **PyAudio/sounddevice**: Audio output capabilities
- ✅ **pytest**: Testing framework

### New Dependencies Required:

### For Image Recognition:

- **transformers**: Hugging Face transformers library
- **torch**: PyTorch for model execution
- **accelerate**: GPU acceleration for transformers
- **torchvision**: Vision model support

### For TTS:

- **TTS**: Coqui TTS library with XTTS-v2
- **torch**: Already covered above
- **torchaudio**: Audio processing for TTS
- **librosa**: Audio manipulation
- **pydub**: Audio format conversion

### System Dependencies:

- **CUDA support**: For GPU acceleration
- **espeak-ng**: Fallback TTS support
- **libsndfile**: Audio file handling

### Dependants:

- **Screenshot API endpoint**: Will use image recognition
- **Voice response system**: Will use TTS capabilities
- **Game analysis service**: Will combine both features

## Detailed Step-by-Step Action Plan

### Phase 1: Setup Script Enhancement (Priority: CRITICAL for Codex)

### Step 1.1: Update [setup.sh](http://setup.sh/) with AI Model Dependencies

```bash
# Add to install_system_packages() function:
echo "Installing AI model system dependencies..."
$SUDO apt-get install -y \\
    espeak-ng espeak-data \\
    libsndfile1-dev \\
    libasound2-plugins \\
    nvidia-cuda-toolkit \\
    libcudnn8 \\
    libcudnn8-dev

```

### Step 1.2: Update Python Dependencies in [setup.sh](http://setup.sh/)

```bash
# Add to install_python_packages() function:
echo "Installing AI/ML packages..."
pip install --no-cache-dir \\
    torch>=2.0.0 torchvision torchaudio --index-url <https://download.pytorch.org/whl/cu118> \\
    transformers>=4.35.0 \\
    accelerate>=0.24.0 \\
    TTS>=0.19.0 \\
    librosa>=0.10.0 \\
    pydub>=0.25.0 \\
    scipy>=1.11.0

```

### Step 1.3: Add Model Download Verification

```bash
# Add to verify_installation() function:
echo "Verifying AI models..."
python3 -c "
from transformers import pipeline
from TTS.api import TTS

# Test image captioning model
try:
    captioner = pipeline('image-to-text', model='nlpconnect/vit-gpt2-image-captioning')
    print('✅ Image captioning model loaded')
except Exception as e:
    print(f'❌ Image captioning error: {e}')

# Test TTS model
try:
    tts = TTS(model_name='tts_models/multilingual/multi-dataset/xtts_v2', gpu=True)
    print('✅ TTS model loaded')
except Exception as e:
    print(f'❌ TTS error: {e}')
"

```

### Phase 2: Server-Side Image Recognition Service

### Step 2.1: Create Image Analysis Service

**File**: `server/src/services/image_analysis.py`

- Initialize `nlpconnect/vit-gpt2-image-captioning` model
- GPU memory management for 4070S
- Screenshot processing pipeline
- Caching for repeated analysis

### Step 2.2: Create Image Analysis API Endpoint

**File**: `server/src/api/endpoints/image_analysis.py`

- `POST /api/image/analyze` - Accept screenshot, return description
- `GET /api/image/history` - Retrieve analysis history
- Error handling and validation

### Step 2.3: Database Models for Image Analysis

**File**: `server/src/models/image_analysis.py`

- `ImageAnalysis` table with timestamp, image_hash, description
- SQLAlchemy model definitions
- Migration scripts

### Phase 3: Server-Side TTS Service

### Step 3.1: Create TTS Service

**File**: `server/src/services/tts.py`

- Initialize XTTS-v2 model with GPU support
- Language detection and selection
- Audio generation and caching
- Memory management for 12GB VRAM limit

### Step 3.2: Create TTS API Endpoint

**File**: `server/src/api/endpoints/tts.py`

- `POST /api/tts/speak` - Convert text to audio file
- `GET /api/tts/languages` - Available languages
- Audio streaming support

### Step 3.3: Audio Output Management

**File**: `server/src/services/audio_output.py`

- Audio file serving
- Format conversion (wav, mp3)
- Cleanup of temporary audio files

### Phase 4: Integration and Workflow

### Step 4.1: Combined Analysis Endpoint

**File**: `server/src/api/endpoints/game_analysis.py`

- `POST /api/game/analyze-and-speak` - Screenshot → Description → TTS
- Workflow orchestration
- Error handling for model failures

### Step 4.2: Client Integration Points

**File**: `client/src/core/ai_client.py`

- HTTP client for image analysis
- Audio playback integration
- Simple UI buttons for triggering analysis

### Step 4.3: Configuration Management

**File**: `server/src/core/ai_config.py`

- Model paths and parameters
- GPU memory allocation settings
- Language preferences

### Phase 5: Testing and Mocking

### Step 5.1: Mock Implementations

**File**: `tests/mocks/ai_models.py`

- Mock image captioning responses
- Mock TTS audio generation
- Offline testing support

### Step 5.2: Unit Tests

**Files**: `tests/unit/test_image_analysis.py`, `tests/unit/test_tts.py`

- Model loading tests
- API endpoint tests
- Error handling validation

### Step 5.3: Integration Tests

**File**: `tests/integration/test_ai_workflow.py`

- Full workflow testing
- Performance benchmarks
- Memory usage validation

### Phase 6: Performance Optimization

### Step 6.1: Model Optimization

- FP16 precision for 4070S
- Model quantization options
- Batch processing for multiple requests

### Step 6.2: Caching Strategy

- LRU cache for frequent descriptions
- Audio file caching
- Model weight sharing