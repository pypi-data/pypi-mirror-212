from pathlib import Path

import yaml

from goodway_configs.config_loader.base import ConfigLoaderBase, ConfigsError


class YamlConfigLoader(ConfigLoaderBase):
    """ConfigLoader implementation that loads config from yaml files."""

    def __init__(self, file_path: Path):
        super().__init__()

        self.file_path = file_path

    async def load_config(self) -> dict:
        """Load config from a file."""
        if not self.file_path.exists():
            raise ConfigsError(f'File not found: `{self.file_path}`!')

        return yaml.safe_load(self.file_path.read_text())
