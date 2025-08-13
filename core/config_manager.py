"""
Configuration manager for DevTerm
"""

import json
import os
from pathlib import Path

class ConfigManager:
    """Manages application configuration and settings"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.devterm'
        self.config_file = self.config_dir / 'config.json'
        self.default_config = {
            'git': {
                'last_repo_path': '',
                'last_clone_destination': str(Path.home()),
                'default_commit_message': ''
            },
            'docker': {
                'last_image_name': '',
                'last_dockerfile_path': '',
                'default_host_port': 8080,
                'default_container_port': 80
            },
            'ui': {
                'window_geometry': None,
                'last_tab': 0
            }
        }
        
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    
                # Merge with defaults to ensure all keys exist
                config = self.default_config.copy()
                self._deep_update(config, loaded_config)
                return config
            else:
                return self.default_config.copy()
                
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config.copy()
            
    def save_config(self):
        """Save configuration to file"""
        try:
            # Create config directory if it doesn't exist
            self.config_dir.mkdir(exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
                
        except Exception as e:
            print(f"Error saving config: {e}")
            
    def get(self, section, key, default=None):
        """Get configuration value"""
        return self.config.get(section, {}).get(key, default)
        
    def set(self, section, key, value):
        """Set configuration value"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        
    def _deep_update(self, base_dict, update_dict):
        """Recursively update nested dictionary"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value