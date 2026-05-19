import asyncio
import logging

from src.application.chat_messages.cases import ChatMassageCase
from src.application.chat_messages.dtos import GlobalChatDTO
from src.infrastructure.chat_messages.parser import GlobalChatParser
from src.infrastructure.dispatchers.common import Dispatcher
from src.infrastructure.filesystem import LogFile
from src.infrastructure.routes.common import Route
from src.settings import AppSettings


async def app(app_settings: AppSettings) -> None:
    logger = logging.getLogger(__name__)

    logger.info("Starting application...")

    log_file = LogFile(file_path=app_settings.LOG_PATH)

    global_chat_route = Route(parser=GlobalChatParser, dto_type=GlobalChatDTO)
    chat_case = ChatMassageCase()
    global_chat_route.add_case(chat_case)

    dispatcher = Dispatcher(log_file)
    dispatcher.add_route(global_chat_route)
    await dispatcher.run()

    retry_delay = 5
    while True:
        try:
            break
        except Exception as exc:
            logger.error(f"Run error: {exc}. Restarting in {retry_delay}s...")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 120)
        finally:
            logger.info("Polling iteration finished")

    logger.info("Shutting down...")
    await log_file.close()
