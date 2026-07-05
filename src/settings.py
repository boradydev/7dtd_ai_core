from dataclasses import dataclass, field
from os import environ


@dataclass(frozen=True, slots=True, kw_only=True)
class AppSettings:
    DEBUG_MODE: bool = field(
        default_factory=lambda: environ.get("DEBUG_MODE", "").lower() == "true"
    )
    LOG_FOLDER_DIR: str = field(default_factory=lambda: environ["LOG_FOLDER_DIR"])
    CONFIG_DIR: str = field(default_factory=lambda: environ["CONFIG_DIR"])
    GAME_API_URL: str = field(default_factory=lambda: environ["GAME_API_URL"])
    AI_API_URL: str = field(default_factory=lambda: environ["AI_API_URL"])
