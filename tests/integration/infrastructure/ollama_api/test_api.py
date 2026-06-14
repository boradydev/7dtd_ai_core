from src.application.common.ai.behavior import AIBehavior


async def test_assistant_mechanics(ai_service):
    message = "Напомни какого уровня я достиг?"
    history = [
        {"role": "user", "content": "Привет Я достиг 10 левла"},
        {
            "role": "assistant",
            "content": "Поздравляю! Ты действительно достиг 10 уровня!",
        },
    ]

    print(f"\n[{AIBehavior.ASSISTANT}]: ", end="", flush=True)

    chunks = []
    async for chunk in ai_service.process_prompt(
        behavior=AIBehavior.ASSISTANT,
        message=message,
        history=history,
    ):
        chunks.append(chunk)
        print(chunk, end="", flush=True)

    response = "".join(chunks)
    print()

    assert "10" in response
    assert len(response) > 0
