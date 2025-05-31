#!/usr/bin/env python3
"""
CUDA Setup Verification Script for Sims 4 AI Gaming Assistant

This script verifies that CUDA, PyTorch, and the TTS service are properly
configured for GPU acceleration on your system.

Usage:
    python scripts/verify_cuda.py

Requirements:
    - NVIDIA GPU with CUDA support
    - CUDA Toolkit installed
    - PyTorch with CUDA support
    - TTS library installed
"""

import sys
import time
from typing import Optional
import os


def check_python_version() -> bool:
    """Check if Python version is suitable."""
    print("=== Python Version Check ===")
    version = sys.version_info
    print(f"Python Version: {sys.version}")
    
    if version >= (3, 11):
        print("✅ Python version is suitable (3.11+)")
        return True
    else:
        print("❌ Python version should be 3.11 or higher")
        return False


def check_torch_installation() -> bool:
    """Check PyTorch installation and CUDA availability."""
    print("\n=== PyTorch & CUDA Check ===")
    
    try:
        import torch
        print(f"PyTorch Version: {torch.__version__}")
        
        cuda_available = torch.cuda.is_available()
        print(f"CUDA Available: {cuda_available}")
        
        if cuda_available:
            print(f"CUDA Version: {torch.version.cuda}")
            device_count = torch.cuda.device_count()
            print(f"GPU Count: {device_count}")
            
            for i in range(device_count):
                gpu_name = torch.cuda.get_device_name(i)
                gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1e9
                print(f"GPU {i}: {gpu_name} ({gpu_memory:.1f} GB)")
            
            print("✅ CUDA setup is working!")
            return True
        else:
            print("❌ CUDA not available - TTS will use CPU (slow)")
            return False
            
    except ImportError as e:
        print(f"❌ PyTorch not installed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking PyTorch: {e}")
        return False


def check_tts_installation() -> bool:
    """Check TTS library installation."""
    print("\n=== TTS Library Check ===")
    
    try:
        from TTS.api import TTS
        print("✅ TTS library is available")
        return True
    except ImportError as e:
        print(f"❌ TTS library not installed: {e}")
        print("Install with: pip install TTS>=0.19.0")
        return False
    except Exception as e:
        print(f"❌ Error checking TTS: {e}")
        return False


def test_tts_gpu_performance() -> Optional[float]:
    """Test TTS GPU performance with a sample inference."""
    print("\n=== TTS GPU Performance Test ===")
    
    try:
        # Set environment variable BEFORE importing TTS or torch related to model loading
        os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"
        print("ℹ️  Applied TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1 to allow older model format.")

        from TTS.api import TTS
        import torch
        
        if not torch.cuda.is_available():
            print("⚠️  Skipping GPU test - CUDA not available")
            return None
        
        print("Initializing TTS model (this may take a moment on first run)...")
        start_init = time.time()
        tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            gpu=True,
            progress_bar=False
        )
        init_time = time.time() - start_init
        print(f"Model initialization: {init_time:.2f} seconds")
        
        # Test inference
        test_text = "Testing GPU acceleration with RTX graphics card for optimal TTS performance!"
        print(f"Testing inference with text: '{test_text}'")
        
        start_inference = time.time()

        # --- MODIFICATION FOR XTTS SPEAKER --- 
        speaker_wav_path = "scripts/text_to_speech_audio.mp3"
        print(f"ℹ️  Using speaker_wav: {speaker_wav_path}")

        audio = tts.tts(text=test_text, language="en", speaker_wav=speaker_wav_path)
        # --- END MODIFICATION ---

        inference_time = time.time() - start_inference
        
        print(f"✅ TTS inference completed in {inference_time:.2f} seconds")
        
        # Save the generated audio so user can hear it
        output_path = "scripts/verification_test_output.wav"
        tts.tts_to_file(
            text=test_text, 
            language="en", 
            speaker_wav=speaker_wav_path,
            file_path=output_path
        )
        print(f"💾 Audio saved to: {output_path}")
        print("🔊 You can now play this file to hear the generated voice!")
        
        # Performance evaluation
        if inference_time < 3.0:
            print("🚀 Excellent GPU performance!")
        elif inference_time < 6.0:
            print("✅ Good GPU performance")
        elif inference_time < 10.0:
            print("⚠️  Moderate performance - check GPU utilization")
        else:
            print("❌ Poor performance - may be using CPU instead of GPU")
        
        return inference_time
        
    except Exception as e:
        print(f"❌ TTS GPU test failed: {e}")
        return None


def check_memory_usage() -> None:
    """Check GPU memory usage."""
    print("\n=== GPU Memory Check ===")
    
    try:
        import torch
        
        if not torch.cuda.is_available():
            print("⚠️  CUDA not available - skipping memory check")
            return
        
        for i in range(torch.cuda.device_count()):
            torch.cuda.set_device(i)
            total_memory = torch.cuda.get_device_properties(i).total_memory / 1e9
            allocated_memory = torch.cuda.memory_allocated(i) / 1e9
            reserved_memory = torch.cuda.memory_reserved(i) / 1e9
            
            print(f"GPU {i} Memory:")
            print(f"  Total: {total_memory:.1f} GB")
            print(f"  Allocated: {allocated_memory:.3f} GB")
            print(f"  Reserved: {reserved_memory:.3f} GB")
            print(f"  Available: {total_memory - reserved_memory:.1f} GB")
            
            if total_memory >= 8.0:
                print("  ✅ Sufficient VRAM for TTS workloads")
            elif total_memory >= 4.0:
                print("  ⚠️  Limited VRAM - may affect performance with large batches")
            else:
                print("  ❌ Low VRAM - consider using CPU or smaller models")
                
    except Exception as e:
        print(f"❌ Error checking GPU memory: {e}")


def provide_recommendations() -> None:
    """Provide setup recommendations based on test results."""
    print("\n=== Setup Recommendations ===")
    
    try:
        import torch
        
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            
            if "RTX" in gpu_name:
                print("🎯 RTX GPU detected - you have excellent hardware for AI workloads!")
                print("   Recommendations:")
                print("   • Use GPU acceleration for all AI services")
                print("   • Consider running multiple AI models simultaneously")
                print("   • Enable mixed precision for better performance")
            elif "GTX" in gpu_name:
                print("👍 GTX GPU detected - good for AI workloads")
                print("   Recommendations:")
                print("   • Use GPU acceleration for TTS")
                print("   • Monitor VRAM usage with larger models")
            else:
                print("ℹ️  GPU detected - test performance with your specific model")
        else:
            print("💡 CPU-only setup detected")
            print("   Recommendations:")
            print("   • Consider upgrading to a CUDA-capable GPU for better performance")
            print("   • Use lighter models when possible")
            print("   • Expect longer processing times")
            
    except Exception as e:
        print(f"Error generating recommendations: {e}")


def main() -> None:
    """Run complete CUDA verification."""
    print("🎮 Sims 4 AI Gaming Assistant - CUDA Verification")
    print("=" * 55)
    
    results = []
    
    # Run all checks
    results.append(("Python Version", check_python_version()))
    results.append(("PyTorch & CUDA", check_torch_installation()))
    results.append(("TTS Library", check_tts_installation()))
    
    # Only run performance test if basic checks pass
    if all(result[1] for result in results):
        inference_time = test_tts_gpu_performance()
        results.append(("TTS Performance", inference_time is not None))
    
    check_memory_usage()
    provide_recommendations()
    
    # Summary
    print("\n=== Verification Summary ===")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, passed_check in results:
        status = "✅ PASS" if passed_check else "❌ FAIL"
        print(f"{check_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Your system is ready for GPU-accelerated TTS!")
    else:
        print("⚠️  Some issues detected. Please address the failed checks above.")
        print("💡 See the setup documentation for troubleshooting guidance.")


if __name__ == "__main__":
    main() 