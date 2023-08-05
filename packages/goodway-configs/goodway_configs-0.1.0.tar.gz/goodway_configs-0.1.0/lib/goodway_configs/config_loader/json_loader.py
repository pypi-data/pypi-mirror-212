import json
from pathlib import Path

from goodway_configs.config_loader.base import ConfigLoaderBase, ConfigsError


class JsonConfigLoader(ConfigLoaderBase):
    """ConfigLoader implementation that loads config from json files."""

    def __init__(self, file_path: Path):
        super().__init__()

        self.file_path = file_path

    async def load_config(self) -> dict:
        """Load config from a file."""
        if not self.file_path.exists():
            raise ConfigsError(f'File not found: `{self.file_path}`!')

        return json.loads(self.file_path.read_text())
