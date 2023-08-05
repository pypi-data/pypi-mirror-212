import functools
from abc import ABC, abstractmethod


class ConfigsError(Exception):
    pass


class ConfigLoaderBase(ABC):
    """Base class for all config loaders."""

    @abstractmethod
    async def load_config(self) -> dict:
        """Load config as dictionary."""
