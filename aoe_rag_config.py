import yaml
from typing import Dict, Any, Optional


class AoeRagConfig:
    """Configuration manager for AoeRag application."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize configuration with optional custom settings.

        Args:
            config: Custom configuration dictionary to override defaults
        """
        # Start with default config
        self._config = {
            "llm": {"model": "gpt-4.1-nano-2025-04-14", "temperature": 0.1},
            "embedding": {"model": "text-embedding-3-small", "batch_size": 100},
            "indexing": {
                "chunk_size": 1024,
                "text_splitter": "sentence",
                "similarity_top_k": 12,
                "response_mode": "tree_summarize",
            },
            "storage": {"persist_dir": "storage"},
            "data": {"source_dir": "data"},
        }

        # Override with custom config if provided
        if config:
            self._update_recursive(self._config, config)

    def _update_recursive(self, target: Dict, source: Dict) -> None:
        """Recursively update a nested dictionary.

        Args:
            target: Target dictionary to update
            source: Source dictionary with new values
        """
        for key, value in source.items():
            if isinstance(value, dict) and key in target:
                self._update_recursive(target[key], value)
            else:
                target[key] = value

    @classmethod
    def from_yaml(cls, config_path: str = "config.yaml") -> "AoeRagConfig":
        """Create configuration from a YAML file.

        Args:
            config_path: Path to the YAML configuration file

        Returns:
            An initialized configuration object
        """
        try:
            with open(config_path, "r") as file:
                config = yaml.safe_load(file)
            return cls(config)
        except FileNotFoundError:
            print(f"Warning: Config file {config_path} not found. Using defaults.")
            return cls()

    def get(self, *keys):
        """Get a configuration value using dot notation.

        Example: config.get("llm", "model") is equivalent to config["llm"]["model"]

        Args:
            *keys: Sequence of keys to access nested config values

        Returns:
            The configuration value
        """
        result = self._config
        for key in keys:
            result = result[key]
        return result

    def as_dict(self) -> Dict[str, Any]:
        """Return the complete configuration dictionary.

        Returns:
            Dictionary containing all configuration values
        """
        return self._config.copy()
