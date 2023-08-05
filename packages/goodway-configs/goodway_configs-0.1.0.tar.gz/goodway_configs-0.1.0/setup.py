# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'lib'}

packages = \
['goodway_configs', 'goodway_configs.config_loader']

package_data = \
{'': ['*']}

extras_require = \
{'etcd-loader': ['httpx>=0.24.1,<0.25.0'], 'yaml-loader': ['pyyaml>=6.0,<7.0']}

setup_kwargs = {
    'name': 'goodway-configs',
    'version': '0.1.0',
    'description': 'configs in a good way',
    'long_description': "# Goodway Configs\n\nThis library contains utilities to work with configs in a good way.\n\n## Installation\n\n`pip install goodway-configs`\n\n## Getting Started\n\nThe following code uses `MultiConfigLoader` and `JsonConfigLoader` to combine two config files together.\n\n```python\nfrom pathlib import Path\n\nfrom goodway_configs.config_loader.json_loader import JsonConfigLoader\nfrom goodway_configs.config_loader.multi_loader import MultiConfigLoader\n\nloader = MultiConfigLoader(config_loaders=[\n    JsonConfigLoader(file_path=Path('./config1.json')),\n    JsonConfigLoader(file_path=Path('./config2.json')),\n])\n\nconfig = await loader.load_config()\n```\n\n## Documentation\n\nDocumentation can be found [here](https://mahs4d.github.io/goodway-configs/).\n",
    'author': 'Mahdi Sadeghi',
    'author_email': 'mahdi74sadeghi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mahs4d/goodway-config',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
