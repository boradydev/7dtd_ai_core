from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class ILogFile(ABC):
    @abstractmethod
    def get_line(self) -> AsyncIterator[str]:
        """Читает файл лога построчно."""
        raise NotImplementedError

    @property
    @abstractmethod
    def log_dir(self) -> str:
        raise NotImplementedError


class IRoute(ABC):
    @abstractmethod
    async def run(self, data: dict[str, str]) -> None:
        """Запускает маршрут."""
        raise NotImplementedError

    @abstractmethod
    def extract(self, line: str) -> dict[str, str] | None:
        """Попытка извлечь токены из строки."""
        raise NotImplementedError


class IDispatcher(ABC):
    @abstractmethod
    def add_route(self, route: IRoute):
        """Добавляет маршрут для строки лога."""
        raise NotImplementedError

    @abstractmethod
    async def run(self) -> None:
        """Запуск диспетчера."""
        raise NotImplementedError


class IParser(ABC):
    @classmethod
    @abstractmethod
    def extract_fields(cls, line: str) -> dict[str, str] | None:
        raise NotImplementedError
