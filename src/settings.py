from dataclasses import dataclass

from src.core.environ import environ, environ_get


@dataclass(frozen=True, slots=True)
class AppSettings:
    DEBUG_MODE: str | None = environ_get(str, "DEBUG_MODE")
    LOG_PATH: str = environ(str, "LOG_PATH")
    GAME_API_URL: str = environ(str, "GAME_API_URL")
    AI_API_URL: str = environ(str, "AI_API_URL")

    @property
    def debug(self) -> bool:
        if self.DEBUG_MODE is None:
            return False

        return self.DEBUG_MODE.lower() == "true"
