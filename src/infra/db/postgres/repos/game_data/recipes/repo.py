import json

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.game_data.abcs import IRecipesRepository
from src.app.game_data.dtos import RecipeDTO
from src.app.game_data.schemas.recipes import RecipeGameData
from src.infra.db.postgres.repos.game_data.recipes.sql.registry import (
    SQL,
)


class RecipesRepository(IRecipesRepository):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def add_many(
        self,
        dtos: list[RecipeGameData],
    ) -> None:
        params = []
        for dto in dtos:
            params.append(
                dict(
                    key=dto.key,
                    raw_data=json.dumps(dto.raw_data),
                )
            )
        await self._session.execute(SQL.ADD_MANY, params)

    async def list_by_key(self, key: str) -> list[RecipeDTO]:
        params = dict(key=key)
        result = await self._session.execute(
            SQL.LIST_BY_KEY,
            params,
        )
        rows = result.mappings().all()

        return [RecipeDTO(**row) for row in rows]

    async def clear(self) -> None:
        await self._session.execute(SQL.CLEAR)
