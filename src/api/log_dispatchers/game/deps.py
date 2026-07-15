from src.app.chat_messages.cases import ChatMessageCase
from src.app.common.abcs import IGameAPI
from src.infra.db.postgres.database import Postgres
from src.infra.db.postgres.uow.chat_histories import ChatHistoriesUOW
from src.infra.ollama_api.api import OllamaApi
from src.infra.ollama_api.config import AIModelConfig
from src.infra.ollama_api.instructions import SystemInstruction
from src.settings import AppSettings


def create_chat_message_case(
    app_settings: AppSettings,
    postgres: Postgres,
    game_api: IGameAPI,
) -> ChatMessageCase:
    uow = ChatHistoriesUOW(
        session_factory=postgres.session_factory,
    )

    ollama_api = OllamaApi(
        host=app_settings.AI_API_URL,
        instructions=SystemInstruction,
        options=AIModelConfig,
        model_name="llama3.1",
    )

    return ChatMessageCase(
        uow=uow,
        game_api=game_api,
        ai_client=ollama_api,
    )
