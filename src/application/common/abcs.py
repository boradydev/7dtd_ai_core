from abc import ABC, abstractmethod
from typing import Any, Protocol


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


class IHTTPClient(ABC):
    """Использует пул соединений (Keep-Alive)."""

    @abstractmethod
    async def post_json(
        self,
        url: str,
        data: dict[str, Any],
    ) -> Any:
        """Выполняет асинхронный POST-запрос в формате ``JSON``."""
        raise NotImplementedError

    @abstractmethod
    async def post_form(
        self,
        url: str,
        data: dict[str, Any],
    ) -> Any:
        """Выполняет асинхронный POST-запрос в формате ``x-www-form-urlencoded``."""
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """
        Корректно завершает работу клиента.

        Закрывает долгоживущую сессию и полностью освобождает все активные
        TCP-соединения, удерживаемые в пуле. Должен вызываться один раз
        при остановке приложения (on shutdown).
        """
        raise NotImplementedError


class IGameAPI(ABC):
    @abstractmethod
    async def get_player_name(self, entity_id: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def send_message(self, text: str) -> None:
        """Отправляет сообщение от имени сервера в глобальный чат."""
        raise NotImplementedError

    @abstractmethod
    async def buff_player(
        self,
        player_id: str,
        buff_name: str,
    ) -> None:
        """Накладывает баф на игрока."""
        raise NotImplementedError

    @abstractmethod
    async def debuff_player(
        self,
        player_id: str,
        debuff_name: str,
    ) -> None:
        """Накладывает дебаф на игрока."""
        raise NotImplementedError
