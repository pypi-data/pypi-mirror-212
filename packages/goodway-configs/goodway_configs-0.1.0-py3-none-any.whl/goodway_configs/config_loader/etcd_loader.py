import base64
import json

import httpx

from goodway_configs.config_loader.base import ConfigLoaderBase, ConfigsError


class EtcdConfigLoader(ConfigLoaderBase):
    def __init__(
            self,
            host: str,
            port: int,
            username: str | None,
            password: str | None,
            use_ssl: bool,
            key: str,
    ):
        self._host = host
        self._port = port
        self._key = key
        self._username = username
        self._password = password
        self._use_ssl = use_ssl

        self._schema = 'https' if use_ssl else 'http'
        self._key_b64 = base64.b64encode(self._key.encode(encoding='utf-8')).decode(encoding='utf-8')

    async def load_config(self) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f'{self._schema}://{self._host}:{self._port}/v3/kv/range',
                json={
                    'key': self._key_b64,
                },
                headers=self._get_headers(),
            )

            response.raise_for_status()

        results = response.json().get('kvs')

        if not results:
            raise ConfigsError(f'Key not found: `{self._key}`!')

        value = base64.b64decode(results[0]['value']).decode(encoding='utf-8')

        return json.loads(value)

    def _get_headers(self) -> dict | None:
        if self._username and self._password:
            return {
                'Authorization': f'Basic {self._username}:{self._password}'
            }

        return None
