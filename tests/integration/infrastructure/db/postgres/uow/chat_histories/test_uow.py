from src.domain.chat_histories.entity import ChatHistory
from src.domain.chat_histories.vals import AssistantMessage, UserMessage
from src.domain.players.vals import PlayerId


history = [
    {"role": "user", "content": "Привет, как сохраняется кириллица в базу данных!"},
    {"role": "assistant", "content": "Hi! How can I help you?"},
    {"role": "user", "content": "What is your name?"},
    {"role": "assistant", "content": "My name is ."},
]

player_id = PlayerId("76561198001453454")

dto = ChatHistory.create(player_id=player_id)
dto.append_turn(
    user_message=UserMessage("Привет, как сохраняется кириллица в базу данных!"),
    assistant_message=AssistantMessage("Hi! How can I help you?"),
)
dto.append_turn(
    user_message=UserMessage("What is your name?"),
    assistant_message=AssistantMessage("My name is ."),
)


async def test_save_chat_history(
    uow,
) -> None:
    async with uow as db:
        await db.histories.save(dto)
        await db.commit()


async def test_find_chat_history(
    uow,
) -> None:
    async with uow as db:
        chat_history = await db.histories.find_by_player_id(player_id)
        assert chat_history is not None
        assert chat_history.history == history

        not_exists_player_id = PlayerId("76561198001000000")
        not_exists = await db.histories.find_by_player_id(not_exists_player_id)
        assert not_exists is None
