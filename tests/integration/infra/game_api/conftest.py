from typing import Any, Generator, AsyncGenerator

import pytest

from src.infra.http.client import HTTPClient
from src.infra.game_api.api import GameAPI
from src.infra.game_api.settings import SDTDAPISettings


@pytest.fixture
async def game_api() -> AsyncGenerator[GameAPI, Any]:
    settings = SDTDAPISettings(
        GAME_API_URL="http://192.168.1.108:8080/",
        API_TOKEN_NAME="adminuser1",
        API_SECRET="supersecrettoken",
        CONNECTION_LIMIT=1,
    )
    http_client = HTTPClient(
            base_url=settings.GAME_API_URL,
            headers={
                "X-SDTD-API-TOKENNAME": settings.API_TOKEN_NAME,
                "X-SDTD-API-SECRET": settings.API_SECRET,
                "Accept": "application/json",
            },
            limit=settings.CONNECTION_LIMIT,
        )

    yield GameAPI(http_client=http_client)
    await http_client.close()