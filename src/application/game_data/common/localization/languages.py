from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True, slots=True)
class LocalizationConfig:
    column: str
    lang: str


class LocalizationLanguage(StrEnum):
    RUSSIAN = "russian"
    ENGLISH = "english"

    @property
    def config(self) -> LocalizationConfig:
        return _LANGUAGE_CONFIGS[self]


_LANGUAGE_CONFIGS = {
    LocalizationLanguage.RUSSIAN: LocalizationConfig(
        column="russian",
        lang="russian",
    ),
    LocalizationLanguage.ENGLISH: LocalizationConfig(
        column="english",
        lang="english",
    ),
}
