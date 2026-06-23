from abc import ABC, abstractmethod


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


class IGlobalChat(ABC):
    @abstractmethod
    async def send(self, text: str) -> None:
        raise NotImplementedError


class IAIClient[DTO](ABC):
    """Интерфейс для взаимодействия с API нейросетей."""

    @abstractmethod
    async def chat(
        self,
        prompt: str,
        sanitize: bool = True,
        normalize: bool = True,
    ) -> DTO:
        """Отправляет запрос в нейросеть и возвращает ответ."""
        raise NotImplementedError


class IChatHistoriesRepository(ABC):
    @abstractmethod
    async def save(
        self,
        player_id: str,
        history: list[dict[str, str]],
    ) -> None:
        """Создает или сохраняет историю чата."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_player_id(self, player_id: str) -> list[dict[str, str]] | None:
        """Поиск истории чата, история может еще существовать."""
        raise NotImplementedError


class IChatHistoriesUOW(ABC):
    @property
    @abstractmethod
    def histories(self) -> IChatHistoriesRepository:
        """Требует репозиторий истории чатов."""
        raise NotImplementedError
