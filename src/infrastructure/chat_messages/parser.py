import re

from src.application.common.abcs import IChatMapper


class GlobalChatParser(IChatMapper):
    CHAT_RE = re.compile(
        r"Chat \(from '(?P<raw_steam_id>.*?)', "
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
