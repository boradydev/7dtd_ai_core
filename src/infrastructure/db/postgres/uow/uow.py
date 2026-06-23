from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.chat_messages.abcs import (
    IChatHistoriesRepository,
    IChatHistoriesUOW,
)
from src.infrastructure.db.postgres.repositories.chat_histories.repo import (
    ChatHistoriesRepository,
)
from src.infrastructure.db.postgres.uow.common import IPostgresUOW


class ChatHistoriesUOW(IPostgresUOW, IChatHistoriesUOW):
    """Реализация Unit of Work для управления транзакциями сущностей игроки."""

    @property
    def histories(self) -> IChatHistoriesRepository:
        return self._histories

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        chat_histories_class: type[ChatHistoriesRepository],
    ) -> None:
        """
        Инициализирует Unit of Work.

        Этот класс является точкой сопряжения абстрактного интерфейса IPlayerUOW
            и конкретной реализации БД через SQLAlchemy.
        """
        self._session_factory = session_factory
        self._chat_histories_class = chat_histories_class

    async def __aenter__(self) -> Self:
        """Инициализирует сессию и подготавливает репозитории к работе."""
        self._session = self._session_factory()
        self._histories = ChatHistoriesRepository(
            session=self._session,
        )
        return self
