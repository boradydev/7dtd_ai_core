from dataclasses import dataclass


@dataclass(frozen=True)
class BaseAppException(Exception):
    message: str | None = None

    def __str__(self) -> str:
        return self.message or ""
