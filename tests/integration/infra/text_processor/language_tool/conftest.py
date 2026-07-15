from collections.abc import AsyncGenerator

import pytest

from src.infra.http.client import HTTPClient
from src.infra.text_processors.language_tool.services import (
    CustomDictionary,
    LanguageToolProcessor,
)


@pytest.fixture
def custom_dictionary() -> CustomDictionary:
    return CustomDictionary(set())


@pytest.fixture
async def processor(custom_dictionary) -> AsyncGenerator[LanguageToolProcessor]:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    http_client = HTTPClient(
        base_url="http://192.168.1.108:8010",
        headers=headers,
    )
    processor = LanguageToolProcessor(
        http_client=http_client,
        custom_dictionary=custom_dictionary,
    )

    yield processor
    await http_client.close()
