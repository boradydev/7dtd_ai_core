import re

from src.presentation.log_dispatchers.game.abcs import IParser


class GlobalChatParser(IParser):
    """
    Извлекает только сообщения игроков в глобальном чате.
    """
    CHAT_RE = re.compile(
        r"Chat \(from 'Steam_(?P<steam_id>.*?)', "
        r"entity id '(?P<entity_id>-?\d+)', "
        r"to '(?P<channel>.*?)'\): "
        r"(?P<raw_message>.*)"
    )

    @classmethod
    def extract_fields(cls, line: str) -> dict[str, str] | None:
        tokens = line.split(maxsplit=3)
        if len(tokens) < 4:
            return None

        payload = tokens[3]
        if not payload.startswith("Chat"):
            return None

        match = cls.CHAT_RE.match(payload)
        if match:
            return match.groupdict()

        return None
