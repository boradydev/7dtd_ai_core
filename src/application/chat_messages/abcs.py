from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from src.domain.chat_histories.entity import ChatHistory
from src.domain.chat_histories.vals import AssistantMessage
from src.domain.common.abcs import InterfaceUOW
from src.domain.players.vals import PlayerId


class ITextProcessor(ABC):
    """
    Отчистка и нормализации текста.

    [Входной текст]
              │
              ▼
    1. Техническая очистка (убрать HTML-теги, лишние пробелы)
              │
              ▼
    2. Фильтр мата (замена на ***)
              │
              ▼
    3. LanguageTool (исправление опечаток и пунктуации уже в "приличном" тексте)
              │
              ▼
    [Промт для ИИ]
    """

    @abstractmethod
    async def process(self, text: str) -> str:
        """Нормализует и отчищает строку."""
        raise NotImplementedError


class IMessageBuilder(ABC):
    @abstractmethod
    def push(self, token: str) -> AssistantMessage | None:
        """
        Принимает очередной токен модели.

        Возвращает все сообщения, которые можно отправить
        прямо сейчас.
        """

    @abstractmethod
    def flush(self) -> AssistantMessage | None:
        """Возвращает остаток после окончания генерации."""


class IMessageFormatter(ABC):
    """Форматирует текст под платформу, цвета и прочее."""

    @abstractmethod
    def format(self, message: str) -> str:
        raise NotImplementedError


class IAIClient[Behavior](ABC):
    """Интерфейс для взаимодействия с API нейросетей."""

    @abstractmethod
    def chat(
        self,
        behavior: Behavior,
        message: str,
        history: list[dict[str, str]] | None = None,
    ) -> AsyncGenerator[str]:
        """Отправляет запрос в нейросеть и возвращает ответ."""
        raise NotImplementedError


class IChatHistoriesRepository(ABC):
    @abstractmethod
    async def save(
        self,
        dto: ChatHistory,
    ) -> None:
        """Создает или сохраняет историю чата."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_player_id(
        self,
        player_id: PlayerId,
    ) -> ChatHistory | None:
        """Поиск истории чата, история может еще не существовать."""
        raise NotImplementedError


class IChatHistoriesUOW(InterfaceUOW, ABC):
    @property
    @abstractmethod
    def histories(self) -> IChatHistoriesRepository:
        """Требует репозиторий истории чатов."""
        raise NotImplementedError
