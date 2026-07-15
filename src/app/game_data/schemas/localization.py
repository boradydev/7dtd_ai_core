from typing import Any

from pydantic import BaseModel, field_validator


class LocalizationGameData(BaseModel):
    key: str

    file: str | None
    type: str | None

    used_in_main_menu: bool
    no_translate: bool
    keep_loaded: bool

    english: str
    context: str | None

    german: str | None
    spanish: str | None
    french: str | None
    italian: str | None
    japanese: str | None
    koreana: str | None
    polish: str | None
    brazilian: str | None
    russian: str | None
    turkish: str | None
    schinese: str | None
    tchinese: str | None

    @field_validator(
        "file",
        "type",
        "context",
        "german",
        "spanish",
        "french",
        "italian",
        "japanese",
        "koreana",
        "polish",
        "brazilian",
        "russian",
        "turkish",
        "schinese",
        "tchinese",
        mode="before",
    )
    @classmethod
    def empty_string_to_none(cls, value: Any) -> str | None:
        if value == "":
            return None
        return value

    @field_validator(
        "used_in_main_menu",
        "no_translate",
        "keep_loaded",
        mode="before",
    )
    @classmethod
    def parse_checkbox(cls, value: Any) -> bool:
        if isinstance(value, str):
            return value.strip().lower() == "x"
        return bool(value)
