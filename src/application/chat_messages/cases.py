import logging

from src.application.chat_messages.abcs import IAIClient, IGlobalChat
from src.application.chat_messages.dtos import GlobalChatDTO
from src.application.common.abcs import ICase, IGameAPI
from src.application.common.ai.behavior import AIBehavior
from src.domain.chat_histories.entity import ChatHistory
from src.domain.chat_histories.vals import AssistantMessage, UserMessage
from src.domain.players.vals import PlayerId
from src.infrastructure.db.postgres.uow.uow import ChatHistoriesUOW


class ChatMessageCase(ICase[GlobalChatDTO]):
    def __init__(
        self,
        uow: ChatHistoriesUOW,
        game_api: IGameAPI,
        ai_client: IAIClient[AIBehavior],
        global_chat: IGlobalChat,
        logger: logging.Logger | None = None,
    ) -> None:
        self._uow = uow
        self._game_api = game_api
        self._ai_client = ai_client
        self._global_chat = global_chat
        self._logger = logger or logging.getLogger(__name__)

    async def execute(self, dto: GlobalChatDTO) -> None:
        player_id = PlayerId(dto.steam_id)
        async with self._uow as uow:
            chat_history = await uow.histories.find_by_player_id(player_id)

        if chat_history is None:
            chat_history = ChatHistory.create(player_id=player_id)

        player_name = await self._game_api.get_player_name(entity_id=dto.entity_id)
        user_message = UserMessage(dto.strip_player_prefix(player_name=player_name))

        tokens: list[str] = []
        async for token in self._ai_client.chat(
            history=chat_history.history,
            message=user_message.value,
            behavior=AIBehavior.ASSISTANT,
        ):
            tokens.append(token)

        assistant_message = AssistantMessage("".join(tokens))
        await self._global_chat.send(assistant_message.value)

        chat_history.append_turn(
            user_message=user_message,
            assistant_message=assistant_message,
        )

        async with self._uow as uow:
            await uow.histories.save(chat_history)
