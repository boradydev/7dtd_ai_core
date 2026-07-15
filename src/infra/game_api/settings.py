from dataclasses import dataclass, field
from os import environ


@dataclass(frozen=True, slots=True)
class SDTDAPISettings:
    GAME_API_URL: str = field(default_factory=lambda: environ["GAME_API_URL"])
    API_TOKEN_NAME: str = field(default_factory=lambda: environ["API_TOKEN_NAME"])
    API_SECRET: str = field(default_factory=lambda: environ["API_SECRET"])
    CONNECTION_LIMIT: int = field(
        default_factory=lambda: int(environ["CONNECTION_LIMIT"])
    )
