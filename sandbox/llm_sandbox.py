"""
Development sandbox.

Используется для ручного тестирования LLM без запуска сервера 7DTD.
"""

import asyncio
import logging
import sys
from io import TextIOWrapper

from src.app.chat_messages.abcs import IMessageBuilder
from src.app.chat_messages.cases import ChatMessageCase
from src.app.chat_messages.dtos import GlobalChatDTO
from src.app.chat_messages.services import MessageBuilder
from src.app.common.abcs import IGameAPI
from src.app.common.ai.behavior import AIBehavior
from src.infra.db.postgres.database import Postgres
from src.infra.db.postgres.settings import PostgresSettings
from src.infra.db.postgres.uow.chat_histories import ChatHistoriesUOW
from src.infra.ollama_api.api import OllamaApi
from src.infra.ollama_api.config import AIModelConfig
from src.infra.ollama_api.instructions import SystemInstruction


postgres_settings = PostgresSettings(
    POSTGRES_HOST="localhost",
    POSTGRES_PORT="5432",
    POSTGRES_USER="postgres",
    POSTGRES_PASSWORD="postgres",
    POSTGRES_DB="test_7dtd",
)

postgres = Postgres(
    db_url=postgres_settings.DB_URL_ASYNC,
)

uow = ChatHistoriesUOW(
    session_factory=postgres.session_factory,
)


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

ai_client = OllamaApi[AIBehavior](
    host="http://192.168.1.108:11434",
    instructions=SystemInstruction,
    options=AIModelConfig,
)


class FakeMessageBuilder(IMessageBuilder):
    _first_prefix = "\nassistant: "

    def flush(self) -> str | None:
        print("\n", flush=True)
        self._first_prefix = "\nassistant: "

    def push(self, token: str) -> None:
        if self._first_prefix:
            print(self._first_prefix, flush=True, end="")
            self._first_prefix = None

        print(token, flush=True, end="")


fake_message_builder = FakeMessageBuilder()

message_builder = MessageBuilder()


def get_case() -> ChatMessageCase:
    return ChatMessageCase(
        uow=uow,
        game_api=fake_game_api,
        ai_client=ai_client,
    )


async def main() -> None:
    if isinstance(sys.stdout, TextIOWrapper):
        sys.stdout.reconfigure(
            encoding="utf-8",
            errors="replace",
        )
    print(
        "Интерактивный режим запросов к нейросети (для выхода введите 'exit')",
        flush=True,
        end="\n",
    )

    while True:
        logging.basicConfig(level=logging.INFO)
        user_query = input("\nuser: ")

        if user_query.strip().lower() == "exit":
            print("Завершение работы.")
            break

        if not user_query.strip():
            continue

        dto = GlobalChatDTO(
            steam_id="76561198001453454",
            entity_id="entity_id",
            channel="global",
            raw_message=f"Player: {user_query}",
        )
        use_case = get_case()
        print()
        await use_case.execute(dto)


if __name__ == "__main__":
    asyncio.run(main())
