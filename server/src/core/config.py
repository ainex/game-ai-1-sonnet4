"""Server configuration for AI models and settings."""

import os
import logging
from pathlib import Path
from typing import Dict, Optional

# Set up logging
logger = logging.getLogger(__name__)

# Secure environment loading
try:
    from dotenv import load_dotenv
    # Load .env from project root (3 levels up from this file)
    project_root = Path(__file__).parent.parent.parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=False)  # Don't override existing env vars
        logger.info(f"✅ Loaded environment from {env_path}")
    else:
        logger.info("ℹ️ No .env file found, using system environment variables")
except ImportError:
    logger.warning("⚠️ python-dotenv not available, using system environment variables only")


class ServerConfig:
    """Server configuration for AI models and services."""
    
    def __init__(self):
        # Default model configuration
        self.default_model = os.getenv("DEFAULT_MODEL", "claude-4-sonnet")
        
        # Model mappings to actual API model names
        self.claude_models: Dict[str, str] = {
            "claude-3.5-sonnet": "claude-3-5-sonnet-20241022",
            "claude-4-sonnet": "claude-sonnet-4-20250514",  # Claude 4 Sonnet
            "claude-4-opus": "claude-opus-4-20250514",  # Claude 4 Opus (most powerful)
            "claude-4-sonnet-thinking": "claude-sonnet-4-20250514-thinking",  # Extended thinking mode
            "claude-4-opus-thinking": "claude-opus-4-20250514-thinking",  # Extended thinking mode
        }
        
        self.openai_models: Dict[str, str] = {
            "gpt-4o-mini": "gpt-4o-mini",
            "gpt-4o": "gpt-4o",
            "o3": "gpt-4o",  # Using gpt-4o until o3 is available
            # When o3 is released, update to:
            # "o3": "o3",
        }
        
        # System prompts
        self.claude_system_prompt = os.getenv(
            "CLAUDE_SYSTEM_PROMPT",
            "You are the greatest gamer and assistant. Here is my game situation screenshot and my question. Provide specific, actionable advice for the player."
        )
        
        self.openai_system_prompt = os.getenv(
            "OPENAI_SYSTEM_PROMPT",
            "You are a helpful game assistant. Analyze the screenshot and answer the user's question about the game situation."
        )
    
    def get_claude_model(self, requested_model: Optional[str] = None) -> str:
        """Get the actual Claude model name for API calls."""
        if requested_model is None:
            requested_model = self._get_default_claude_model()
        
        model_name = self.claude_models.get(requested_model)
        if model_name is None:
            logger.warning(f"⚠️ Unknown Claude model: {requested_model}, using default")
            model_name = self.claude_models.get(self._get_default_claude_model(), "claude-3-5-sonnet-20241022")
        
        logger.info(f"🤖 Using Claude model: {requested_model} -> {model_name}")
        return model_name
    
    def get_openai_model(self, requested_model: Optional[str] = None) -> str:
        """Get the actual OpenAI model name for API calls."""
        if requested_model is None:
            requested_model = self._get_default_openai_model()
        
        model_name = self.openai_models.get(requested_model)
        if model_name is None:
            logger.warning(f"⚠️ Unknown OpenAI model: {requested_model}, using default")
            model_name = self.openai_models.get(self._get_default_openai_model(), "gpt-4o-mini")
        
        logger.info(f"🤖 Using OpenAI model: {requested_model} -> {model_name}")
        return model_name
    
    def _get_default_claude_model(self) -> str:
        """Get the default model for Claude based on configuration."""
        if self.default_model.startswith("claude"):
            return self.default_model
        return "claude-4-sonnet"  # Default Claude model
    
    def _get_default_openai_model(self) -> str:
        """Get the default model for OpenAI based on configuration."""
        if self.default_model in ["gpt-4o-mini", "gpt-4o", "o3"]:
            return self.default_model
        return "gpt-4o-mini"  # Default OpenAI model
    
    def get_available_models(self) -> Dict[str, list]:
        """Get all available models."""
        return {
            "claude": list(self.claude_models.keys()),
            "openai": list(self.openai_models.keys()),
            "default": self.default_model
        }


# Global config instance
_config_instance: Optional[ServerConfig] = None


def get_server_config() -> ServerConfig:
    """Get or create the global server config instance."""
    global _config_instance
    if _config_instance is None:
        logger.info("🏭 Creating server config instance")
        _config_instance = ServerConfig()
    return _config_instance