"""
Advanced Configuration System
Author: morningstarxcdcode
Description: Centralized configuration management for the cybersecurity suite
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

CONFIG_DIR = Path.home() / ".advanced_port_scanner"
CONFIG_FILE = CONFIG_DIR / "config.json"
PROFILES_DIR = CONFIG_DIR / "profiles"

DEFAULT_CONFIG = {
    "scanning": {
        "default_timeout": 3,
        "max_threads": 100,
        "stealth_mode": False,
        "aggressive_scan": False,
        "scan_delay": 0,
        "retries": 1,
        "user_agent": "Mozilla/5.0 (compatible; Advanced-Port-Scanner/1.0)",
    },
    "output": {
        "verbose": True,
        "colored_output": True,
        "save_logs": True,
        "log_level": "INFO",
        "report_format": "json",
        "export_formats": ["json", "csv", "pdf", "xml"],
    },
    "security": {
        "proxy_enabled": False,
        "proxy_url": "",
        "tor_enabled": False,
        "user_agent_rotation": True,
        "rate_limiting": True,
        "max_requests_per_second": 10,
    },
    "api_keys": {
        "shodan_api_key": "",
        "virustotal_api_key": "",
        "censys_api_key": "",
        "have_i_been_pwned_key": "",
    },
    "advanced": {
        "enable_osint": True,
        "enable_crypto_analysis": True,
        "enable_steganography": True,
        "enable_social_engineering": False,
        "vulnerability_scanning": True,
        "automated_exploitation": False,
    },
    "wireless": {
        "interface": "wlan0",
        "monitor_mode": False,
        "channel_hopping": True,
        "capture_handshakes": True,
        "wordlist_path": "/usr/share/wordlists/rockyou.txt",
    },
}


class ConfigManager:
    def __init__(self):
        self.config_dir = CONFIG_DIR
        self.config_file = CONFIG_FILE
        self.profiles_dir = PROFILES_DIR
        self.config = {}
        self._ensure_config_dir()
        self.load_config()

    def _ensure_config_dir(self):
        """Create configuration directories if they don't exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    self.config = json.load(f)
                # Merge with defaults to ensure all keys exist
                self.config = self._merge_configs(DEFAULT_CONFIG, self.config)
            except (json.JSONDecodeError, FileNotFoundError):
                self.config = DEFAULT_CONFIG.copy()
                self.save_config()
        else:
            self.config = DEFAULT_CONFIG.copy()
            self.save_config()
        return self.config

    def save_config(self):
        """Save current configuration to file."""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Recursively merge user config with defaults."""
        result = default.copy()
        for key, value in user.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'scanning.timeout')."""
        keys = key_path.split(".")
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def set(self, key_path: str, value: Any) -> None:
        """Set configuration value using dot notation."""
        keys = key_path.split(".")
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
        self.save_config()

    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a service."""
        key = self.get(f"api_keys.{service}_api_key")
        if not key:
            # Try environment variable
            env_key = f"{service.upper()}_API_KEY"
            key = os.environ.get(env_key)
        return key

    def create_profile(self, name: str, config: Dict[str, Any]) -> None:
        """Create a configuration profile."""
        profile_file = self.profiles_dir / f"{name}.json"
        with open(profile_file, "w") as f:
            json.dump(config, f, indent=4)

    def load_profile(self, name: str) -> bool:
        """Load a configuration profile."""
        profile_file = self.profiles_dir / f"{name}.json"
        if profile_file.exists():
            try:
                with open(profile_file, "r") as f:
                    profile_config = json.load(f)
                self.config = self._merge_configs(DEFAULT_CONFIG, profile_config)
                self.save_config()
                return True
            except json.JSONDecodeError:
                return False
        return False

    def list_profiles(self) -> list:
        """List available configuration profiles."""
        profiles = []
        for profile_file in self.profiles_dir.glob("*.json"):
            profiles.append(profile_file.stem)
        return profiles

    def delete_profile(self, name: str) -> bool:
        """Delete a configuration profile."""
        profile_file = self.profiles_dir / f"{name}.json"
        if profile_file.exists():
            profile_file.unlink()
            return True
        return False


# Global configuration instance
config = ConfigManager()
