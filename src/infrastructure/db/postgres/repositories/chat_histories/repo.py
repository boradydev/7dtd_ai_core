import json

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.chat_messages.abcs import IChatHistoriesRepository
from src.infrastructure.db.postgres.repositories.chat_histories.sql.registry import SQL
from src.infrastructure.db.postgres.repositories.common.excs import (
    InvalidResultTypeException,
)


class ChatHistoriesRepository(IChatHistoriesRepository):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def save(
        self,
        player_id: str,
        history: list[dict[str, str]],
    ) -> None:
        params = dict(
            player_id=player_id,
            history=json.dumps(history),
        )
        await self._session.execute(SQL.SAVE, params)

    async def find_by_player_id(self, player_id: str) -> list[dict[str, str]] | None:
        params = dict(player_id=player_id)
        raw = await self._session.execute(SQL.FIND_BY_PLAYER_ID, params)
        result = raw.scalar_one_or_none()
        if result is None:
            return None

        if not isinstance(result, list):
            raise InvalidResultTypeException(
                f"Expected {type(list)}, got: {type(result)}"
            )

        return result
