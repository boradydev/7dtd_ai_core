from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable

from src.application.common.ai.types import ToolsType


class IAIService[Behavior](ABC):
    """Интерфейс для взаимодействия с сервисом искусственного интеллекта."""

    @abstractmethod
    async def process_prompt_with_tools(
        self,
        behavior: Behavior,
        message: str,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        """
        Обрабатывает промпт пользователя с поддержкой инструментов и истории.

        Returns:
            Текстовый ответ от модели ИИ.
        """
        raise NotImplementedError


class ISystemInstructions[Behavior](ABC):
    """Пресеты системных инструкций для разных ролей ИИ-админа в 7 Days to Die."""

    @classmethod
    @abstractmethod
    def get(cls, behavior: Behavior) -> str:
        """
        Возвращает системный промт для указанного поведения.

        Raises:
            KeyError: Если режим отсутствует в словаре пресетов.
        """
        raise NotImplementedError


class ITools[Behavior](ABC):
    """Пресеты инструментов для разных ролей ИИ-админа в 7 Days to Die."""

    @classmethod
    @abstractmethod
    def get_tools(cls, behavior: Behavior) -> list[Callable[..., Awaitable[ToolsType]]]:
        """
        Возвращает список инструментов для указанного поведения.

        Инструмент это функция, которую использует AI для получения данных.

        Raises:
            KeyError: Если режим отсутствует в словаре пресетов.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_tools_map(
        cls,
        behavior: Behavior,
    ) -> dict[str, Callable[..., Awaitable[ToolsType]]]:
        """
        Возвращает предрассчитанную мапу инструментов для быстрого поиска по имени.

        Raises:
            KeyError: Если режим отсутствует в словаре пресетов.
        """
        raise NotImplementedError


class IModelConfig[Behavior](ABC):
    """Конфигурация параметров генерации текста для локальной нейросети Ollama."""

    @classmethod
    @abstractmethod
    def get(cls, behavior: Behavior) -> dict[str, dict[str, int | float]]:
        """
        Возвращает конфиг для указанного поведения.

        Raises:
            KeyError: Если режим отсутствует в словаре пресетов.
        """
        raise NotImplementedError
