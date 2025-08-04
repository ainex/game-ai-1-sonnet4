"""Test script for Claude 4 models - verify the new reasoning capabilities."""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
server_src = str(project_root / "server" / "src")
sys.path.insert(0, server_src)

# Also add the server directory itself for relative imports
server_dir = str(project_root / "server")
sys.path.insert(0, server_dir)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment from {env_path}")
    else:
        print(f"Warning: No .env file found at {env_path}")
        print("Trying to load from parent directories...")
        # Try parent directory
        parent_env = project_root.parent / ".env"
        if parent_env.exists():
            load_dotenv(parent_env)
            print(f"Loaded environment from {parent_env}")
except ImportError:
    print("Warning: python-dotenv not installed. Run: pip install python-dotenv")

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_claude_models():
    """Test different Claude 4 models."""
    try:
        # Import using absolute paths to avoid relative import issues
        sys.path.insert(0, str(project_root / "server" / "src"))
        from src.services.claude_service import get_claude_service
        from src.core.config import get_server_config
        
        # Get services
        claude_service = get_claude_service()
        config = get_server_config()
        
        # Show available models
        print("\n=== Available Claude Models ===")
        for model_name, api_name in config.claude_models.items():
            print(f"- {model_name} -> {api_name}")
        
        # Test with a simple game scenario
        print("\n=== Testing Claude 4 Models ===")
        
        # Create a test scenario
        test_question = "I'm playing a strategy game and I have limited resources. Should I focus on building defenses or expanding my economy first?"
        
        # Read a sample screenshot (you can replace with actual game screenshot)
        test_image_path = project_root / "tests" / "fixtures" / "sample_screenshot.png"
        if not test_image_path.exists():
            # Create a dummy image for testing
            from PIL import Image
            import io
            img = Image.new('RGB', (800, 600), color='gray')
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            screenshot_bytes = buffer.getvalue()
            print("Using dummy screenshot for testing")
        else:
            with open(test_image_path, 'rb') as f:
                screenshot_bytes = f.read()
        
        # Test different models
        models_to_test = [
            ("claude-4-sonnet", "Standard Claude 4 Sonnet"),
            ("claude-4-opus", "Claude 4 Opus (Most Powerful)"),
            ("claude-4-sonnet-thinking", "Claude 4 Sonnet with Extended Thinking"),
        ]
        
        for model_id, description in models_to_test:
            print(f"\n--- Testing {description} ({model_id}) ---")
            
            try:
                response = claude_service.analyze_game_situation(
                    screenshot_bytes=screenshot_bytes,
                    question_text=test_question,
                    system_prompt="You are an expert game strategist. Provide concise, strategic advice.",
                    model=model_id
                )
                
                print(f"Response from {model_id}:")
                print(f"{response[:500]}..." if len(response) > 500 else response)
                print(f"\nResponse length: {len(response)} characters")
                
            except Exception as e:
                print(f"Error testing {model_id}: {e}")
                if "rate_limit" in str(e).lower():
                    print("Rate limit hit - waiting before next test...")
                    import time
                    time.sleep(5)
        
        # Show how to configure default model
        print("\n=== Configuration Tips ===")
        print("1. To use Claude 4 Opus (most powerful) as default:")
        print("   Set DEFAULT_MODEL=claude-4-opus in your .env file")
        print("\n2. To use extended thinking mode:")
        print("   Set DEFAULT_MODEL=claude-4-opus-thinking in your .env file")
        print("\n3. Current default model:", config.default_model)
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you're running from the project root directory")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Claude 4 Model Test Script")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "sk-ant-api03-your-key-here":
        print("\nERROR: ANTHROPIC_API_KEY not found in environment")
        print("\nPossible solutions:")
        print("1. Make sure python-dotenv is installed:")
        print("   pip install python-dotenv")
        print("\n2. Or set the environment variable directly:")
        print("   set ANTHROPIC_API_KEY=your-actual-key-here")
        print("\n3. Or run from the server directory where dotenv is loaded:")
        print("   cd server/src")
        print("   python ../../test_claude4_models.py")
        sys.exit(1)
    else:
        # Mask the key for security
        masked_key = f"{api_key[:15]}...{api_key[-4:]}"
        print(f"API Key found: {masked_key}")
    
    test_claude_models()