from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.game_data.abcs import IGameDataUOW
from src.infrastructure.db.postgres.repositories.game_data.localization.repo import (
    LocalizationRepository,
)
from src.infrastructure.db.postgres.repositories.game_data.recipes.repo import (
    RecipesRepository,
)
from src.infrastructure.db.postgres.uow.common import IPostgresUOW


class GameDataUOW(IPostgresUOW, IGameDataUOW):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        """
        Реализация Unit of Work для управления транзакциями Game Data.

        Включает:
            ``RecipesRepository``,
            ``LocalizationRepository``
        """
        self._session_factory = session_factory

    async def __aenter__(self) -> Self:
        """Инициализирует сессию и подготавливает репозитории к работе."""
        self._session = self._session_factory()
        self._recipes = RecipesRepository(
            session=self._session,
        )
        self._localization = LocalizationRepository(
            session=self._session,
        )
        return self

    @property
    def recipes(self) -> RecipesRepository:
        return self._recipes

    @property
    def localization(self) -> LocalizationRepository:
        return self._localization
