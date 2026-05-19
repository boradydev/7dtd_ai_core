from dataclasses import dataclass, field
from datetime import datetime

from src.application.common.dtos import IBaseDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class GlobalChatDTO(IBaseDTO):
    raw_steam_id: str
    entity_id: str
    channel: str
    raw_message: str
    timestamp: datetime = field(default_factory=datetime.now, init=False)
