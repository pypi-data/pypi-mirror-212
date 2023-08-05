from goodway_configs.config_loader.base import ConfigLoaderBase


def deep_update(first: dict, second: dict) -> dict:
    """Deep update first dictionary with data from the second."""
    first = first.copy()
    for k, v in second.items():
        if k in first and isinstance(first[k], dict) and isinstance(v, dict):
            first[k] = deep_update(first[k], v)
        else:
            first[k] = v

    return first


class MultiConfigLoader(ConfigLoaderBase):
    """ConfigLoader implementation that combines config from multiple config loaders."""

    def __init__(self, config_loaders: list[ConfigLoaderBase]):
        super().__init__()

        self.config_loaders = config_loaders

    async def load_config(self) -> dict:
        """Load config from a file."""
        config = {}

        for config_loader in self.config_loaders:
            config_update = await config_loader.load_config()
            config = deep_update(config, config_update)

        return config
