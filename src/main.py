import asyncio
import logging

import dotenv

from src.presentation.log_dispatchers.app import app
from src.settings import AppSettings


async def main() -> None:
    dotenv.load_dotenv()
    app_settings = AppSettings()
    logging.basicConfig(
        level=logging.DEBUG if app_settings.debug else logging.INFO,
    )
    await app(app_settings)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
