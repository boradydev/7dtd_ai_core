from dataclasses import dataclass

from src.core.environ import environ_get


@dataclass(frozen=True, slots=True)
class AppSettings:
    DEBUG_MODE: str | None = environ_get(str, "DEBUG_MODE")
    LOG_PATH: str | None = environ_get(str, "LOG_PATH")

    @property
    def debug(self) -> bool:
        if self.DEBUG_MODE is None:
            return False

        return self.DEBUG_MODE.lower() == "true"
