import pytest

from src.infrastructure.db.postgres.repositories.chat_histories.repo import \
    ChatHistoriesRepository
from src.infrastructure.db.postgres.uow.uow import ChatHistoriesUOW


@pytest.fixture
def uow(postgres) -> ChatHistoriesUOW:
    return ChatHistoriesUOW(
        session_factory=postgres.session_factory,
        chat_histories_class=ChatHistoriesRepository,
    )
