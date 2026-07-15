from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.app.chat_messages.abcs import (
    IChatHistoriesRepository,
    IChatHistoriesUOW,
)
from src.infra.db.postgres.repos.chat_histories.repo import (
    ChatHistoriesRepository,
)
from src.infra.db.postgres.uow.common import IPostgresUOW


class ChatHistoriesUOW(IPostgresUOW, IChatHistoriesUOW):
    @property
    def histories(self) -> IChatHistoriesRepository:
        return self._histories

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        """
        Реализация Unit of Work для управления транзакциями.

        Включает:
            ``ChatHistoriesRepository``
        """
        self._session_factory = session_factory

    async def __aenter__(self) -> Self:
        """Инициализирует сессию и подготавливает репозитории к работе."""
        self._session = self._session_factory()
        self._histories = ChatHistoriesRepository(
            session=self._session,
        )
        return self
