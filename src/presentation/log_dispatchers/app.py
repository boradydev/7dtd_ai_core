import asyncio
import logging

from src.application.chat_messages.cases import ChatMessageCase
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
    chat_case = ChatMessageCase()
    global_chat_route.add_case(chat_case)

    dispatcher = Dispatcher(log_file)
    dispatcher.add_route(global_chat_route)
    await dispatcher.run()
    await log_file.close()
