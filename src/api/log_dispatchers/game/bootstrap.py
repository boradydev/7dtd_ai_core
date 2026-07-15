import logging

from src.app.chat_messages.dtos import GlobalChatDTO
from src.app.common.abcs import IGameAPI
from src.infra.chat_messages.parser import GlobalChatParser
from src.infra.db.postgres.database import Postgres
from src.infra.db.postgres.settings import PostgresSettings
from src.infra.dispatchers.common import Dispatcher
from src.infra.filesystem.log_reader.log_file import LogFile
from src.infra.game_api.api import GameAPI
from src.infra.game_api.settings import SDTDAPISettings
from src.infra.http.client import HTTPClient
from src.infra.routes.common import Route
from src.api.log_dispatchers.game.abcs import ILogFile
from src.api.log_dispatchers.game.deps import create_chat_message_case
from src.settings import AppSettings


async def run_game_dispatcher(
    app_settings: AppSettings,
    game_api: IGameAPI | None = None,
    log_file: ILogFile | None = None,
) -> None:
    """
    Запуск приложения.

    Можно запустить в песочнице подменив:
        ``game_api``, ``log_file``.
    """
    logger = logging.getLogger(__name__)

    logger.info("Starting application...")

    _log_file = log_file or LogFile(
        log_dir=app_settings.LOG_FOLDER_DIR,
        find_pattern="sdtdserver-console*.log",
    )

    global_chat_route = Route(parser=GlobalChatParser, dto_type=GlobalChatDTO)

    game_api_settings = SDTDAPISettings()

    http_client = HTTPClient(
        base_url=app_settings.GAME_API_URL,
        headers={
            "X-SDTD-API-TOKENNAME": game_api_settings.API_TOKEN_NAME,
            "X-SDTD-API-SECRET": game_api_settings.API_SECRET,
            "Accept": "application/json",
        },
        limit=game_api_settings.CONNECTION_LIMIT,
    )

    _game_api = game_api or GameAPI(http_client=http_client)

    postgres_settings = PostgresSettings()
    postgres = Postgres(postgres_settings.DB_URL_ASYNC)

    def chat_case_factory():
        return create_chat_message_case(
            postgres=postgres,
            game_api=_game_api,
            app_settings=app_settings,
        )

    global_chat_route.add_case_factory(chat_case_factory)

    dispatcher = Dispatcher(
        log_file=_log_file,
        log_unhandled=app_settings.DEBUG_MODE,
    )

    dispatcher.add_route(global_chat_route)

    await dispatcher.run()

    logger.info("Application is stopped.")
    await _log_file.close()
    await postgres.dispose()
    await http_client.close()
