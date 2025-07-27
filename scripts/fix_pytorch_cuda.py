#!/usr/bin/env python3
"""
PyTorch CUDA Version Fix Script for AI Gaming Assistant

This script helps fix PyTorch installation issues by uninstalling current
PyTorch and reinstalling with the correct CUDA version for TTS compatibility.

Usage:
    python scripts/fix_pytorch_cuda.py

This script will:
1. Uninstall current PyTorch installation
2. Reinstall PyTorch with CUDA 11.8 (recommended for TTS)
3. Verify the installation
"""

import subprocess
import sys
import time


def run_command(command, description):
    """Run a command and show progress."""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def check_current_pytorch():
    """Check current PyTorch installation."""
    print("🔍 Checking current PyTorch installation...")
    
    try:
        import torch
        print(f"Current PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"Current CUDA version: {torch.version.cuda}")
            print(f"GPU detected: {torch.cuda.get_device_name(0)}")
        else:
            print("CUDA not available in current installation")
        
        return True
    except ImportError:
        print("PyTorch not currently installed")
        return False


def uninstall_pytorch():
    """Uninstall current PyTorch installation."""
    commands = [
        "pip uninstall torch torchvision torchaudio -y",
        "pip cache purge"
    ]
    
    for cmd in commands:
        description = f"Running: {cmd}"
        if not run_command(cmd, description):
            return False
    
    return True


def install_pytorch_cuda118():
    """Install PyTorch with CUDA 11.8."""
    print("\n📦 Installing PyTorch with CUDA 11.8...")
    
    # Update pip first
    run_command("python -m pip install --upgrade pip", "Updating pip")
    
    # Install PyTorch with CUDA 11.8
    pytorch_cmd = (
        "pip install torch>=2.0.0 torchvision torchaudio "
        "--index-url https://download.pytorch.org/whl/cu118"
    )
    
    return run_command(pytorch_cmd, "Installing PyTorch with CUDA 11.8")


def verify_installation():
    """Verify the new PyTorch installation."""
    print("\n✅ Verifying new installation...")
    
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✅ CUDA version: {torch.version.cuda}")
            print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
            
            # Test GPU functionality
            x = torch.randn(1000, 1000).cuda()
            y = torch.randn(1000, 1000).cuda()
            z = torch.mm(x, y)
            print(f"✅ GPU test successful: {z.shape}")
            
            return True
        else:
            print("❌ CUDA not available after installation")
            return False
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False


def install_tts():
    """Try to install TTS after fixing PyTorch."""
    print("\n🎤 Attempting to install TTS...")
    
    return run_command("pip install TTS>=0.19.0", "Installing TTS library")


def main():
    """Main execution flow."""
    print("🔧 PyTorch CUDA Fix Script for AI Gaming Assistant")
    print("=" * 60)
    
    # Check current installation
    had_pytorch = check_current_pytorch()
    
    if had_pytorch:
        # Ask user to confirm
        response = input("\n⚠️  This will uninstall and reinstall PyTorch. Continue? (y/N): ")
        if response.lower() != 'y':
            print("Operation cancelled")
            return
    
    # Step 1: Uninstall current PyTorch
    if had_pytorch:
        if not uninstall_pytorch():
            print("❌ Failed to uninstall PyTorch. Please try manually.")
            return
    
    # Step 2: Install PyTorch with CUDA 11.8
    if not install_pytorch_cuda118():
        print("❌ Failed to install PyTorch with CUDA 11.8")
        print("\n🔧 Manual installation command:")
        print("pip install torch>=2.0.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
        return
    
    # Step 3: Verify installation
    if not verify_installation():
        print("❌ PyTorch installation verification failed")
        return
    
    # Step 4: Try to install TTS
    print("\n" + "="*60)
    tts_success = install_tts()
    
    if tts_success:
        print("\n🎉 Success! PyTorch and TTS are now properly installed!")
        print("\n📝 Next steps:")
        print("   1. Run: python scripts/verify_cuda.py")
        print("   2. Start the server: cd server && python -m uvicorn src.main:app --reload")
    else:
        print("\n⚠️  PyTorch fixed but TTS installation still failed.")
        print("\n🔧 Try these alternatives:")
        print("   1. conda install -c conda-forge coqui-tts")
        print("   2. See docs/troubleshooting-windows-installation.md")


if __name__ == "__main__":
    main() 