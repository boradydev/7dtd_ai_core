import asyncio
import logging

import dotenv

from src.api.log_dispatchers.game.bootstrap import run_game_dispatcher
from src.settings import AppSettings


async def main() -> None:
    dotenv.load_dotenv(encoding="utf-8")
    app_settings = AppSettings()
    logging.basicConfig(
        level=logging.DEBUG if app_settings.DEBUG_MODE else logging.INFO,
    )
    await run_game_dispatcher(app_settings)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
