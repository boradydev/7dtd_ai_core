from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class GlobalMassageDTO:
    raw_steam_id: str
    entity_id: str
    channel: str
    raw_message: str
    timestamp: datetime = field(default_factory=datetime.now, init=False)


