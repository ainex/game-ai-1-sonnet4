"""Simple Claude 4 test without server dependencies."""

import os
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == "win32":
    os.system("chcp 65001 > nul")

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"[OK] Loaded environment from {env_path}")
    else:
        print("[ERROR] No .env file found")
except ImportError:
    print("[WARNING] Install python-dotenv: pip install python-dotenv")

# Test Claude 4 models directly
def test_claude4_direct():
    """Test Claude 4 models directly with the Anthropic library."""
    
    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("[ERROR] No ANTHROPIC_API_KEY found")
        return
    
    print(f"[KEY] API Key: {api_key[:15]}...{api_key[-4:]}")
    
    try:
        import anthropic
        print("[OK] Anthropic library available")
        
        # Initialize client
        client = anthropic.Anthropic(api_key=api_key)
        
        # Test different Claude 4 models
        models_to_test = [
            "claude-sonnet-4-20250514",  # Claude 4 Sonnet
            "claude-opus-4-20250514",    # Claude 4 Opus  
            "claude-opus-4-20250514-thinking",  # Claude 4 Opus with thinking
        ]
        
        test_prompt = """You are an expert game strategist. A player asks: "I'm playing a strategy game and have limited resources. Should I focus on building defenses or expanding my economy first?" 

Please provide concise strategic advice."""
        
        for model_name in models_to_test:
            print(f"\n[TEST] Testing {model_name}...")
            
            try:
                response = client.messages.create(
                    model=model_name,
                    max_tokens=300,
                    temperature=0.7,
                    messages=[{
                        "role": "user", 
                        "content": test_prompt
                    }]
                )
                
                result = response.content[0].text
                print(f"[SUCCESS] Response length: {len(result)} chars")
                print(f"[SAMPLE] {result[:200]}...")
                
            except Exception as e:
                error_msg = str(e)
                if "model" in error_msg.lower():
                    print(f"[ERROR] Model not available: {error_msg}")
                elif "rate" in error_msg.lower():
                    print(f"[RATE LIMIT] {error_msg}")
                else:
                    print(f"[ERROR] {error_msg}")
    
    except ImportError:
        print("[ERROR] Anthropic library not installed")
        print("[TIP] Run: pip install anthropic")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

def show_model_info():
    """Show information about Claude 4 models."""
    print("\n" + "="*60)
    print("CLAUDE 4 MODELS AVAILABLE")
    print("="*60)
    
    models = {
        "claude-sonnet-4-20250514": {
            "name": "Claude 4 Sonnet",
            "description": "Balanced performance and speed",
            "best_for": "General gaming advice, quick strategic decisions"
        },
        "claude-opus-4-20250514": {
            "name": "Claude 4 Opus", 
            "description": "Most powerful reasoning capabilities",
            "best_for": "Complex strategy analysis, detailed planning"
        },
        "claude-opus-4-20250514-thinking": {
            "name": "Claude 4 Opus (Thinking Mode)",
            "description": "Extended reasoning with visible thought process",
            "best_for": "Complex problems requiring step-by-step analysis"
        }
    }
    
    for api_name, info in models.items():
        print(f"\n[MODEL] {info['name']}")
        print(f"   API: {api_name}")
        print(f"   Description: {info['description']}")
        print(f"   Best for: {info['best_for']}")

if __name__ == "__main__":
    print("Simple Claude 4 Test")
    print("="*50)
    
    show_model_info()
    
    print("\n" + "="*50)
    print("RUNNING TESTS")
    print("="*50)
    
    test_claude4_direct()
    
    print("\n" + "="*50)
    print("CONFIGURATION TIPS")
    print("="*50)
    print("To use Claude 4 Opus as default in your gaming app:")
    print("1. Edit your .env file")
    print("2. Set: DEFAULT_MODEL=claude-4-opus")
    print("3. Restart the server and client")
    print("\nFor extended reasoning mode:")
    print("   DEFAULT_MODEL=claude-4-opus-thinking")