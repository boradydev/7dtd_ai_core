import pytest

from src.app.chat_messages.dtos import GlobalChatDTO
from src.infra.chat_messages.parser import GlobalChatParser


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        (
            "2026-05-16T11:53:47 70867.715 INF Chat (from 'Steam_76561198004196286',"
            " entity id '171', to 'Global'): 'gamer': Привет как дела",
            {
                "steam_id": "76561198004196286",
                "entity_id": "171",
                "channel": "Global",
                "raw_message": "'gamer': Привет как дела",
            },
        ),
    ],
)
def test_global_chat_parser_success(
    line,
    expected,
) -> None:
    data = GlobalChatParser.extract_fields(line)
    assert data is not None
    assert data == expected
    assert GlobalChatDTO(**data)
