import re

from src.app.chat_messages.abcs import ITextProcessor


class TechnicalRubbishCleaner(ITextProcessor):
    _HTML_TAG_PATTERN = re.compile(r"<[^>]*>")
    _MULTIPLE_SPACES_PATTERN = re.compile(r"\s+")

    async def process(self, text: str) -> str:
        text = self._HTML_TAG_PATTERN.sub("", text)
        text = self._MULTIPLE_SPACES_PATTERN.sub(" ", text)
        return text.strip()
