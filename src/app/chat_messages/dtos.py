from dataclasses import dataclass, field
from datetime import datetime

from src.app.common.dtos import IBaseDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class GlobalChatDTO(IBaseDTO):
    steam_id: str
    entity_id: str
    channel: str
    raw_message: str
    timestamp: datetime = field(default_factory=datetime.now, init=False)

    def strip_player_prefix(self, player_name: str | None = None) -> str:
        """Удаляет префикс перед сообщением"""
        if player_name:
            return self.raw_message.removeprefix(f"{player_name}: ")
        return self.raw_message


@dataclass(frozen=True, slots=True, kw_only=True)
class AIResponseDTO(IBaseDTO):
    text: str
