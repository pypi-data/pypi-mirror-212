# Goodway Configs

This library contains utilities to work with configs in a good way.

## Installation

`pip install goodway-configs`

## Getting Started

The following code uses `MultiConfigLoader` and `JsonConfigLoader` to combine two config files together.

```python
from pathlib import Path

from goodway_configs.config_loader.json_loader import JsonConfigLoader
from goodway_configs.config_loader.multi_loader import MultiConfigLoader

loader = MultiConfigLoader(config_loaders=[
    JsonConfigLoader(file_path=Path('./config1.json')),
    JsonConfigLoader(file_path=Path('./config2.json')),
])

config = await loader.load_config()
```

## Documentation

Documentation can be found [here](https://mahs4d.github.io/goodway-configs/).
