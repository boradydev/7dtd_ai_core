from src.application.chat_messages.abcs import IAIClient, IMessageBuilder
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
        message_builder: IMessageBuilder,
    ) -> None:
        self._uow = uow
        self._game_api = game_api
        self._ai_client = ai_client
        self._message_builder = message_builder

    async def execute(self, dto: GlobalChatDTO) -> None:
        player_id = PlayerId(dto.steam_id)
        async with self._uow as uow:
            chat_history = await uow.histories.find_by_player_id(player_id)

        if chat_history is None:
            chat_history = ChatHistory.create(
                player_id=player_id,
            )

        player_name = await self._game_api.get_player_name(
            steam_id=dto.steam_id,
        )
        user_message = UserMessage(dto.strip_player_prefix(player_name=player_name))

        tokens: list[str] = []
        async for token in self._ai_client.chat(
            history=chat_history.history,
            message=user_message.value,
            behavior=AIBehavior.ASSISTANT,
        ):
            tokens.append(token)
            if current_message := self._message_builder.push(token=token):
                await self._game_api.send_message(
                    text=current_message.value,
                )

        if current_message := self._message_builder.flush():
            await self._game_api.send_message(
                text=current_message.value,
            )

        chat_history.append_turn(
            user_message=user_message,
            assistant_message=AssistantMessage("".join(tokens)),
        )

        async with self._uow as uow:
            await uow.histories.save(chat_history)
            await uow.commit()
