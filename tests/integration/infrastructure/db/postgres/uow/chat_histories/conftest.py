import pytest

from src.infrastructure.db.postgres.uow.uow import ChatHistoriesUOW


@pytest.fixture
def uow(postgres) -> ChatHistoriesUOW:
    return ChatHistoriesUOW(
        session_factory=postgres.session_factory,
    )
