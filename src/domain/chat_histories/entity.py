from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar, Final, Self

from src.domain.chat_histories.vals import AssistantMessage, UserMessage
from src.domain.common.entity import BaseEntity
from src.domain.players.vals import PlayerId


@dataclass(slots=True, kw_only=True)
class ChatHistory(BaseEntity):
    _player_id: PlayerId
    _history: list[dict[str, str]]

    _MAX_HISTORY_SIZE: ClassVar[Final[int]] = 30

    @property
    def player_id(self) -> PlayerId:
        return self._player_id

    @property
    def history(self) -> Sequence[dict[str, str]]:
        return self._history

    @classmethod
    def create(cls, player_id: PlayerId) -> Self:
        return cls(
            _player_id=player_id,
            _history=[],
        )

    def append_turn(
        self,
        user_message: UserMessage,
        assistant_message: AssistantMessage,
    ) -> None:
        """Добавляет в историю чата, запрос от user и ответ от assistant."""
        self._history.append(dict(role="user", content=user_message.value))
        self._history.append(dict(role="assistant", content=assistant_message.value))

        if len(self._history) > self._MAX_HISTORY_SIZE:
            self._history = self._history[2:]
