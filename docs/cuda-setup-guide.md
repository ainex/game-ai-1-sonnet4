# CUDA Setup Guide for GPU-Accelerated TTS

This guide helps you set up CUDA acceleration for the Text-to-Speech service in the Sims 4 AI Gaming Assistant. GPU acceleration dramatically improves TTS performance, reducing generation time from 15-30 seconds to 1-3 seconds per sentence.

## Hardware Requirements

### Recommended GPUs
- **RTX 40 Series**: RTX 4070 Super (12GB), RTX 4080, RTX 4090 - Excellent performance
- **RTX 30 Series**: RTX 3070 (8GB), RTX 3080, RTX 3090 - Very good performance  
- **RTX 20 Series**: RTX 2070, RTX 2080 - Good performance
- **GTX 16 Series**: GTX 1660 Ti, GTX 1070 - Basic performance

### Memory Requirements
- **Minimum**: 6GB VRAM
- **Recommended**: 8GB+ VRAM (for comfortable multi-model usage)
- **Optimal**: 12GB+ VRAM (RTX 4070 Super or better)

## Step-by-Step Installation

### 1. Check Your GPU Driver

First, verify your NVIDIA driver version:

```powershell
nvidia-smi
```

**Required driver versions:**
- **RTX 40 Series**: Driver 537.13 or newer
- **RTX 30 Series**: Driver 472.12 or newer
- **Older GPUs**: Driver 456.71 or newer

### 2. Install Visual Studio Build Tools

Required for compiling CUDA applications:

```powershell
# Using Windows Package Manager (recommended)
winget install --id=Microsoft.VisualStudio.2022.BuildTools -e

# Or manually download from:
# https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**Restart your computer after installation.**

### 3. Install CUDA Toolkit

Download and install CUDA 11.8 (recommended for best compatibility):

1. Go to [NVIDIA CUDA Toolkit Archive](https://developer.nvidia.com/cuda-11-8-0-download-archive)
2. Select: **Windows** → **x86_64** → **Local Installer**
3. Download and run the installer
4. Choose **Custom Installation** and select:
   - CUDA Toolkit
   - CUDA Documentation (optional)
   - CUDA Samples (optional)

### 4. Install PyTorch with CUDA Support

```powershell
# For CUDA 11.8 (recommended)
pip install torch>=2.0.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1+ (newer, ensure compatibility)
pip install torch>=2.0.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 5. Verify Installation

Run our verification script:

```powershell
python scripts/verify_cuda.py
```

Expected output for successful setup:
```
🎮 Sims 4 AI Gaming Assistant - CUDA Verification
=======================================================

=== Python Version Check ===
Python Version: 3.11.x
✅ Python version is suitable (3.11+)

=== PyTorch & CUDA Check ===
PyTorch Version: 2.0.x+cu118
CUDA Available: True
CUDA Version: 11.8
GPU Count: 1
GPU 0: NVIDIA GeForce RTX 4070 SUPER (12.0 GB)
✅ CUDA setup is working!

=== TTS Library Check ===
✅ TTS library is available

=== TTS GPU Performance Test ===
Initializing TTS model (this may take a moment on first run)...
Model initialization: 12.34 seconds
Testing inference with text: 'Testing GPU acceleration...'
✅ TTS inference completed in 1.23 seconds
🚀 Excellent GPU performance!

=== GPU Memory Check ===
GPU 0 Memory:
  Total: 12.0 GB
  Allocated: 0.000 GB
  Reserved: 0.000 GB
  Available: 12.0 GB
  ✅ Sufficient VRAM for TTS workloads

🎉 Your system is ready for GPU-accelerated TTS!
```

## Performance Expectations

### RTX 4070 Super (12GB) Performance:
- **Short sentences** (10-20 words): 0.5-1 seconds
- **Medium sentences** (20-40 words): 1-2 seconds  
- **Long sentences** (40+ words): 2-3 seconds
- **Model loading**: ~10-15 seconds (first run only)
- **VRAM usage**: 2-4GB for XTTS-v2

### Comparison by GPU:
| GPU Model | VRAM | TTS Speed | Multi-Model Capable |
|-----------|------|-----------|-------------------|
| RTX 4090 | 24GB | Excellent | Yes (multiple large models) |
| RTX 4080 | 16GB | Excellent | Yes |
| RTX 4070 Super | 12GB | Excellent | Yes |
| RTX 3080 | 10GB | Very Good | Limited |
| RTX 3070 | 8GB | Good | Basic |
| GTX 1660 Ti | 6GB | Basic | CPU recommended |

## Troubleshooting

### Common Issues

#### Issue: `torch.cuda.is_available()` returns `False`

**Solutions:**
1. **Reinstall PyTorch with CUDA:**
   ```powershell
   pip uninstall torch torchvision torchaudio
   pip install torch>=2.0.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Check CUDA installation:**
   ```powershell
   nvcc --version
   ```

3. **Verify NVIDIA drivers:**
   ```powershell
   nvidia-smi
   ```

#### Issue: `RuntimeError: CUDA out of memory`

**Solutions:**
1. **Clear CUDA cache:**
   ```python
   import torch
   torch.cuda.empty_cache()
   ```

2. **Restart Python to fully clear VRAM**

3. **Close other GPU-intensive applications**

#### Issue: Slow inference despite GPU detection

**Check if model is actually using GPU:**
```python
from TTS.api import TTS
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
# Check model device
print(f"Model device: {next(tts.model.parameters()).device}")
```

Should show: `cuda:0`

#### Issue: `ModuleNotFoundError: No module named 'TTS'`

**Solution:**
```powershell
pip install TTS>=0.19.0
```

### Advanced Troubleshooting

#### Force GPU Usage
```python
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # Use first GPU
```

#### Check GPU Utilization
```powershell
# Monitor GPU usage during TTS
nvidia-smi -l 1
```

#### Verify CUDA Compute Capability
```python
import torch
if torch.cuda.is_available():
    props = torch.cuda.get_device_properties(0)
    print(f"Compute Capability: {props.major}.{props.minor}")
```

## Model Storage and Caching

### Model Download Locations
- **Windows**: `C:\Users\{username}\.local\share\tts\`
- **Models size**: XTTS-v2 ≈ 1.8GB

### First-Time Setup
- **Initial download**: ~5-10 minutes (depending on internet speed)
- **Model caching**: Subsequent runs load from disk (~10-15 seconds)

## Multiple GPU Support

If you have multiple GPUs:

```python
import torch
print(f"Available GPUs: {torch.cuda.device_count()}")
for i in range(torch.cuda.device_count()):
    print(f"GPU {i}: {torch.cuda.get_device_name(i)}")

# Use specific GPU
torch.cuda.set_device(0)  # Use first GPU
```

## Environment Variables

Useful CUDA environment variables:

```powershell
# Use specific GPU
set CUDA_VISIBLE_DEVICES=0

# Enable CUDA debugging
set CUDA_LAUNCH_BLOCKING=1

# Optimize memory allocation
set PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
```

## Additional Resources

- [NVIDIA CUDA Installation Guide](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/)
- [PyTorch CUDA Documentation](https://pytorch.org/get-started/locally/)
- [TTS Library Documentation](https://tts.readthedocs.io/)

## Next Steps

After successful CUDA setup:

1. **Test the TTS service**: `python scripts/verify_cuda.py`
2. **Start the server**: `cd server && python -m uvicorn src.main:app --reload`
3. **Test API endpoints**: Use `/api/v1/tts/speak` with GPU acceleration
4. **Monitor performance**: Watch GPU utilization with `nvidia-smi`

Your RTX 4070 Super provides excellent performance for the Sims 4 AI Gaming Assistant! 🚀 