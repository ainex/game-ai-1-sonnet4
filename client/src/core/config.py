"""Configuration and feature flags for the AI Gaming Assistant client."""

import os
import json
from pathlib import Path


class Config:
    """Configuration manager with feature flags."""
    
    def __init__(self):
        # Default feature flags
        self.features = {
            "use_tts": False,  # Text-to-speech disabled for phase 1
            "use_overlay": True,  # Use transparent overlay for responses
            "log_responses": True,  # Always log responses to console/file
            "auto_show_overlay": True,  # Automatically show overlay on response
        }
        
        # Load user config if exists
        self.config_path = Path.home() / ".ai_gaming_assistant" / "config.json"
        self.load_config()
    
    def load_config(self):
        """Load configuration from user's config file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                    # Update features with user preferences
                    if "features" in user_config:
                        self.features.update(user_config["features"])
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
    
    def save_config(self):
        """Save current configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump({"features": self.features}, f, indent=2)
    
    def get_feature(self, feature_name: str, default: bool = False) -> bool:
        """Get a feature flag value."""
        return self.features.get(feature_name, default)
    
    def set_feature(self, feature_name: str, value: bool):
        """Set a feature flag value."""
        self.features[feature_name] = value
        self.save_config()


# Global config instance
_config_instance = None


def get_config() -> Config:
    """Get or create the global config instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance