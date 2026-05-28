import logging

from src.application.chat_messages.abcs import IAIClient, IGlobalChat
from src.application.chat_messages.dtos import AIResponseDTO, GlobalChatDTO
from src.application.common.abcs import ICase, IGameAPI


class ChatMessageCase(ICase[GlobalChatDTO]):
    def __init__(
        self,
        game_api: IGameAPI,
        ai_client: IAIClient[AIResponseDTO],
        global_chat: IGlobalChat,
        logger: logging.Logger | None = None,
    ) -> None:
        self._game_api = game_api
        self._ai_client = ai_client
        self._global_chat = global_chat
        self._logger = logger or logging.getLogger(__name__)

    async def execute(self, dto: GlobalChatDTO) -> None:
        player_name = await self._game_api.get_player_name(entity_id=dto.entity_id)
        message = dto.get_clean_message(player_name=player_name)
        ai_response = await self._ai_client.send_prompt(prompt=message)
        await self._global_chat.send(ai_response.text)
