import json

from sqlalchemy.ext.asyncio import AsyncSession

from src.app.chat_messages.abcs import IChatHistoriesRepository
from src.domain.chat_histories.entity import ChatHistory
from src.domain.players.vals import PlayerId
from src.infra.db.postgres.repos.chat_histories.sql.registry import SQL


class ChatHistoriesRepository(IChatHistoriesRepository):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def save(
        self,
        dto: ChatHistory,
    ) -> None:
        params = dict(
            player_id=dto.player_id.value,
            history=json.dumps(dto.history),
        )
        await self._session.execute(SQL.SAVE, params)

    async def find_by_player_id(
        self,
        player_id: PlayerId,
    ) -> ChatHistory | None:
        params = dict(player_id=player_id.value)
        raw = await self._session.execute(SQL.FIND_BY_PLAYER_ID, params)
        result = raw.scalar_one_or_none()
        if result is None:
            return None

        return ChatHistory(
            _player_id=player_id,
            _history=result,
        )
