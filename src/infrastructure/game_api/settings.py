from dataclasses import dataclass

from src.core.environ import environ


@dataclass(frozen=True, slots=True)
class SDTDAPISettings:
    GAME_API_URL: str = environ(str, "GAME_API_URL")
    API_TOKEN_NAME: str = environ(str, "API_TOKEN_NAME ")
    API_SECRET: str = environ(str, "API_SECRET ")
    CONNECTION_LIMIT: int = environ(int, "API_SECRET ")
