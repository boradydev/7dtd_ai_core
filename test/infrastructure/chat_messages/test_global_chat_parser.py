import pytest

from src.infrastructure.chat_messages.parser import GlobalChatParser


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        (
            "2026-05-16T11:53:47 70867.715 INF Chat (from 'Steam_76561198004196286',"
            " entity id '171', to 'Global'): 'gamer': Привет как дела",
            {
                "raw_steam_id": "Steam_76561198004196286",
                "entity_id": "171",
                "channel": "Global",
                "raw_message": "'gamer': Привет как дела",
            },
        ),
        (
            "2026-05-16T11:54:44 70925.216 INF Chat (from '-non-player-', "
            "entity id '-1', to 'Global'): Молчание золото",
            {
                "raw_steam_id": "-non-player-",
                "entity_id": "-1",
                "channel": "Global",
                "raw_message": "Молчание золото",
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
