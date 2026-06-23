history = [
    {"role": "user", "content": "Привет, как сохраняется кириллица в базу данных!"},
    {"role": "assistant", "content": "Hi! How can I help you?"},
    {"role": "user", "content": "What is your name?"},
    {"role": "assistant", "content": "My name is ."},
]


async def test_save_chat_history(
    uow,
) -> None:
    async with uow as db:
        await db.histories.save("exist_id", history)
        await db.commit()


async def test_find_chat_history(
    uow,
) -> None:
    async with uow as db:
        assert await db.histories.find_by_player_id("exist_id") == history
        assert await db.histories.find_by_player_id("not_exist_id") is None
