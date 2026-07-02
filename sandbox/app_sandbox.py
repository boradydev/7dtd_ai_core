"""
Development sandbox.

Используется для ручного тестирования LLM без запуска сервера 7DTD.
"""

import asyncio
import logging
import sys
from io import TextIOWrapper

import dotenv

from src.application.common.abcs import IGameAPI
from src.core.paths import PROJECT_DIR
from src.infrastructure.filesystem.log_reader.log_file import LogFile
from src.presentation.log_dispatchers.game.app import app
from src.settings import AppSettings


async def aio_input(prompt: str) -> str:
    """Читает ввод пользователя, не блокируя event loop."""
    return await asyncio.to_thread(input, prompt)


async def main() -> None:
    if isinstance(sys.stdout, TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    logging.basicConfig(
        level=logging.INFO,
    )

    dotenv.load_dotenv(encoding="utf-8")

    class FakeGameAPI(IGameAPI):
        async def send_message(self, text: str) -> None:
            print("assistant: ", flush=True, end="")
            print(text, flush=True, end="\n")

        async def buff_player(self, player_id: str, buff_name: str) -> None:
            pass

        async def debuff_player(self, player_id: str, debuff_name: str) -> None:
            pass

        async def get_player_name(self, steam_id: str) -> str:
            return "Player"

    fake_game_api = FakeGameAPI()
    app_settings = AppSettings()
    log_dir = PROJECT_DIR / "7dtd_data/log/console"
    log_file = LogFile(
        log_dir=str(log_dir),
        find_pattern="sdtdserver-console*.log",
    )

    app_task = asyncio.create_task(
        app(
            app_settings=app_settings,
            game_api=fake_game_api,
            log_file=log_file,
        )
    )

    await asyncio.sleep(0.1)

    print(
        "Режим симуляции логов игрового сервера 7DTD.\n"
        "Введенный текст будет записан в консольный лог как глобальный чат игрока.\n"
        "Для выхода введите 'exit'\n"
        "Нужно просто ввести текст в консоль",
        flush=True,
        end="\n",
    )
    while True:
        user_query = await aio_input("")

        if user_query.lower() == "exit":
            print("Завершение работы...")
            app_task.cancel()
            try:
                await app_task
            except asyncio.CancelledError:
                pass
            await log_file.close()
            break

        file_path = (
            PROJECT_DIR / app_settings.LOG_FOLDER_PATH / "sdtdserver-console.log"
        )
        line = (
            f"2026-05-16T11:53:47 70867.715 INF Chat (from 'Steam_76561198001453454', "
            f"entity id '171', to 'Global'): "
            f"'Player': {user_query}\n"
        )

        with file_path.open(mode="a", encoding="utf-8") as file:
            file.write(line)

        await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())
