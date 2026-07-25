from sqlalchemy.ext.asyncio import AsyncSession

from src.app.game_data.abcs import IItemsRepository
from src.app.game_data.common.localization.languages import LocalizationLanguage
from src.app.game_data.dtos import MatchedItemDTO
from src.infra.db.postgres.repos.game_data.items.sql.registry import (
    SQL,
)


class ItemsRepository(IItemsRepository):
    _THRESHOLD = 0.2

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def search_by_fuzzy(
        self,
        text: str,
        lang: LocalizationLanguage = LocalizationLanguage.ENGLISH,
    ) -> list[MatchedItemDTO]:
        params = dict(
            text=text,
            file="items",
            limit=10,
            threshold=self._THRESHOLD,
        )
        result = await self._session.execute(
            SQL.GET_SEARCH_BY_FUZZY(lang.config),
            params,
        )
        rows = result.mappings().all()

        return [MatchedItemDTO(**row) for row in rows]
