# Windows Installation Troubleshooting Guide

This guide helps resolve common Windows-specific installation issues for the AI Gaming Assistant, particularly TTS library compilation problems.

## Common Error: "Microsoft Visual C++ 14.0 or greater is required"

### The Problem
When installing the TTS library with `pip install TTS`, you may encounter:
```
error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools"
ERROR: Failed building wheel for TTS
```

This happens because the TTS library contains C++ extensions that need to be compiled during installation.

### Solution 1: Install Visual Studio Build Tools (Recommended)

#### Step 1: Install Build Tools
```powershell
# Using Windows Package Manager (fastest)
winget install --id=Microsoft.VisualStudio.2022.BuildTools -e

# Alternative: Manual download
# Go to: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

#### Step 2: Restart Your Computer
**Important**: Restart your computer after installing Build Tools.

#### Step 3: Install TTS
```powershell
pip install --upgrade pip
pip install TTS>=0.19.0
```

### Solution 2: Use Pre-compiled Wheels (Faster Alternative)

If Build Tools installation fails, try using pre-compiled wheels:

```powershell
# Install dependencies first
pip install torch>=2.0.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Try installing TTS with specific flags
pip install TTS>=0.19.0 --find-links https://download.pytorch.org/whl/torch_stable.html

# Alternative: Install without building wheels
pip install TTS>=0.19.0 --no-build-isolation
```

### Solution 3: Use Conda (Alternative Package Manager)

If pip continues to fail, use Conda instead:

```powershell
# Install Miniconda first: https://docs.conda.io/en/latest/miniconda.html

# Create environment with conda
conda create -n game-ai python=3.11
conda activate game-ai

# Install TTS via conda-forge
conda install -c conda-forge coqui-tts

# Install other dependencies
pip install fastapi uvicorn sqlalchemy pytest
```

### Solution 4: Docker Development Environment

For persistent issues, use Docker:

```powershell
# Create Dockerfile
# See: Docker setup section below
docker build -t game-ai .
docker run -it --gpus all game-ai
```

## Other Common Windows Issues

### Issue: "Python was not found"

**Solution:**
1. Install Python 3.11 from [python.org](https://python.org)
2. Check "Add Python to PATH" during installation
3. Restart Command Prompt

### Issue: "pip is not recognized"

**Solution:**
```powershell
# Reinstall pip
python -m ensurepip --upgrade

# Or use py launcher
py -m pip install --upgrade pip
```

### Issue: Virtual Environment Issues

**Solution:**
```powershell
# Create virtual environment
python -m venv venv

# Activate (Command Prompt)
venv\Scripts\activate.bat

# Activate (PowerShell)
venv\Scripts\Activate.ps1
```

### Issue: PowerShell Execution Policy

If you get "execution of scripts is disabled":

```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Advanced Troubleshooting

### Check Your Python Installation

```powershell
python --version
python -m pip --version
python -c "import sys; print(sys.executable)"
```

### Clean Installation

If problems persist, clean install:

```powershell
# Remove virtual environment
rmdir /s venv

# Clear pip cache
python -m pip cache purge

# Recreate environment
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
```

### Alternative TTS Libraries

If TTS installation continues to fail, try lighter alternatives:

```powershell
# Option 1: Use edge-tts (Microsoft Edge TTS)
pip install edge-tts

# Option 2: Use pyttsx3 (System TTS)
pip install pyttsx3

# Option 3: Use gTTS (Google TTS) - requires internet
pip install gtts
```

## Docker Setup (Complete Solution)

Create a `Dockerfile` for a containerized environment:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "-m", "uvicorn", "server.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```powershell
docker build -t game-ai .
docker run -p 8000:8000 game-ai
```

## Verification Commands

After successful installation, verify your setup:

```powershell
# Check TTS installation
python -c "from TTS.api import TTS; print('TTS installed successfully')"

# Run our verification script
python scripts/verify_cuda.py

# Test basic functionality
python -c "
from TTS.api import TTS
tts = TTS(model_name='tts_models/en/ljspeech/tacotron2-DDC', gpu=False)
print('TTS basic test successful')
"
```

## Getting Help

If you continue to have issues:

1. **Check Python version**: Ensure you're using Python 3.11+
2. **Try different terminal**: Use Command Prompt instead of PowerShell
3. **Run as Administrator**: Some installations require admin privileges
4. **Check antivirus**: Temporarily disable antivirus during installation
5. **Use WSL**: Install Windows Subsystem for Linux as alternative

## Alternative Lightweight Setup

For development without full TTS:

```powershell
# Install core dependencies only
pip install fastapi uvicorn sqlalchemy pytest pillow requests

# Use mock TTS for development
# The verification script will detect missing TTS and suggest alternatives
```

This allows you to develop other parts of the application while working on TTS setup. 