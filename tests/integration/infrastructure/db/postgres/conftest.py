from collections.abc import AsyncGenerator
from typing import Any

import pytest

from src.infrastructure.db.postgres.database import Postgres
from src.infrastructure.db.postgres.settings import PostgresSettings


@pytest.fixture
def postgres_settings() -> PostgresSettings:
    return PostgresSettings(
        POSTGRES_HOST="localhost",
        POSTGRES_PORT="5432",
        POSTGRES_USER="postgres",
        POSTGRES_PASSWORD="postgres",
        POSTGRES_DB="test_7dtd",
    )


@pytest.fixture
async def postgres(postgres_settings) -> AsyncGenerator[Postgres, Any]:
    postgres = Postgres(postgres_settings.DB_URL_ASYNC)
    yield postgres
    await postgres.dispose()
