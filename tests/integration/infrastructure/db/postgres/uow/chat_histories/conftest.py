import pytest

from src.infrastructure.db.postgres.uow.chat_histories import ChatHistoriesUOW


@pytest.fixture
def chat_history_uow(postgres) -> ChatHistoriesUOW:
    return ChatHistoriesUOW(
        session_factory=postgres.session_factory,
    )
