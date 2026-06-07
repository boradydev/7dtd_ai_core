import re
from operator import itemgetter
from typing import Any

from src.application.chat_messages.abcs import ITextProcessor
from src.infrastructure.http.client import IHTTPClient
from src.infrastructure.text_processors.language_tool.abcs import ICustomDictionary
from src.infrastructure.text_processors.language_tool.excs import (
    TextNormalizationException,
)


class CustomDictionary(ICustomDictionary):
    def __init__(self, words: set[str]) -> None:
        self._words = {word.lower() for word in words}

    def reload(self, words: set[str]) -> None:
        self._words = {word.lower() for word in words}

    def contains(self, word: str) -> bool:
        return word.lower() in self._words


class LanguageToolProcessor(ITextProcessor):
    _HTML_TAG_PATTERN = re.compile(r"<[^>]*>")
    _MULTIPLE_SPACES_PATTERN = re.compile(r"\s+")

    def __init__(
        self,
        http_client: IHTTPClient,
        language: str = "ru-RU",
        custom_dictionary: ICustomDictionary | None = None,
    ) -> None:
        self._http_client = http_client
        self._language = language
        self._custom_dictionary = custom_dictionary or CustomDictionary(set())

    async def process(self, text: str) -> str:
        """Очищает технический мусор и исправляет текст через LanguageTool."""
        if not text:
            return ""

        result_data = await self.fetch_corrections(text)
        if result_data is None:
            raise TextNormalizationException

        return result_data

    async def fetch_corrections(self, text: str) -> str | None:
        """Выполняет сетевой запрос к LanguageTool."""
        data = {
            "text": text,
            "language": self._language,
        }
        response_json = await self._http_client.post("/v2/check", data=data)
        if not isinstance(response_json, dict):
            return None
        return self._apply_corrections(text=text, data=response_json)

    def _apply_corrections(
        self,
        text: str,
        data: dict[str, Any],
    ) -> str:
        """
        Применение корректировки.

        Применяет лучшие варианты исправлений к исходному тексту.
        Не применяет слова исключения.
        """
        matches = data.get("matches", [])
        if not matches:
            return text

        matches.sort(key=itemgetter("offset"), reverse=True)
        text_list = list(text)

        for match in matches:
            offset = match["offset"]
            length = match["length"]

            original_word = text[offset : offset + length]

            if self._custom_dictionary.contains(original_word):
                continue

            replacements = match["replacements"]

            if replacements:
                best_replacement = replacements[0].get("value", "")
                text_list[offset : offset + length] = list(best_replacement)

        return "".join(text_list)
