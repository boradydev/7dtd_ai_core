from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self


class InterfaceUOW(ABC):
    """Интерфейс Unit of Work для управления транзакциями."""

    @abstractmethod
    async def __aenter__(self) -> Self:
        """Открывает транзакцию и подготавливает ресурсы."""

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Закрывает контекст. Выполняет автоматический откат при ошибке."""

    @abstractmethod
    async def commit(self) -> None:
        """Фиксирует все изменения текущей транзакции в базе данных."""

    @abstractmethod
    async def rollback(self) -> None:
        """Отменяет все незафиксированные изменения."""
