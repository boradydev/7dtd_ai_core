import re
from dataclasses import dataclass
from typing import ClassVar, Final

from src.domain.chat_histories import excs


@dataclass(frozen=True, slots=True)
class UserMessage:
    """
    Валидированное и нормализованное сообщение от игрока.

    Очищает текст от лишних пробелов и невидимых управляющих символов,
    контролирует максимальную длину контента.
    """

    value: str

    _MAX_LENGTH: ClassVar[Final[int]] = 8192
    _CLEAN_PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(
        r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]"
    )

    def __post_init__(self) -> None:
        cleaned_content = self._CLEAN_PATTERN.sub("", self.value).strip()

        if not cleaned_content:
            raise excs.EmptyMessageException

        if len(cleaned_content) > self._MAX_LENGTH:
            raise excs.MessageTooLongException

        object.__setattr__(
            self,
            "value",
            cleaned_content,
        )


@dataclass(frozen=True, slots=True)
class AssistantMessage:
    """
    Валидированное сообщение от ассистента (Ollama).

    Очищает текст от лишних пробелов и невидимых управляющих символов,
    контролирует максимальную длину контента.
    """

    value: str

    _MAX_LENGTH: ClassVar[Final[int]] = 16384
    _CLEAN_PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(
        r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]"
    )

    def __post_init__(self) -> None:
        self.check_message_length(len(self.value))
        cleaned_content = self._CLEAN_PATTERN.sub("", self.value).strip()

        if not cleaned_content:
            raise excs.EmptyMessageException

        object.__setattr__(
            self,
            "value",
            cleaned_content,
        )

    @classmethod
    def check_message_length(cls, message_len: int) -> None:
        if message_len > cls._MAX_LENGTH:
            raise excs.MessageTooLongException
