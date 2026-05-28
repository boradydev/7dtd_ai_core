from abc import ABC, abstractmethod
from typing import Protocol


class ITextProcessor(Protocol):
    @abstractmethod
    async def process(self, text: str) -> str:
        raise NotImplementedError


class IGlobalChat(ABC):
    @abstractmethod
    async def send(self, text: str) -> None:
        raise NotImplementedError


class IAIClient[DTO](ABC):
    """Интерфейс для взаимодействия с API нейросетей."""

    @abstractmethod
    async def send_prompt(
        self,
        prompt: str,
        sanitize: bool = True,
        normalize: bool = True,
    ) -> DTO:
        """Отправляет запрос в нейросеть и возвращает ответ."""
        raise NotImplementedError
