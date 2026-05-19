from abc import ABC, abstractmethod
from typing import Protocol


class ICase[DTO](ABC):
    @abstractmethod
    async def execute(self, dto: DTO) -> None:
        raise NotImplementedError


class ILogger(Protocol):
    def debug(self, msg, *args, **kwargs) -> None: ...

    def info(self, msg, *args, **kwargs) -> None: ...

    def error(self, msg, *args, **kwargs) -> None: ...

    def warning(self, msg, *args, **kwargs) -> None: ...

    def critical(self, msg, *args, **kwargs) -> None: ...

    def exception(self, msg, *args, **kwargs) -> None: ...


class IChatMapper(ABC):
    @classmethod
    def extract_fields(cls, line: str) -> dict[str, str] | None:
        """Извлекает данные из строки."""
        raise NotImplementedError
