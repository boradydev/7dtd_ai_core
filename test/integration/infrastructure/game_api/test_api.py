import asyncio
import time


async def test_game_api(game_api):
    await asyncio.gather(
        *[game_api.send_message(f"attempt:{attempt + 1}. Test") for attempt in range(3)]
    )

    async def send_with_time(text):
        start = time.time()
        response = await game_api.send_message(text)
        end = time.time()
        print(f"Запрос '{text}' завершен за: {end - start:.3f} сек")
        return response

    await asyncio.gather(*[send_with_time(f"Test {i}") for i in range(10)])
