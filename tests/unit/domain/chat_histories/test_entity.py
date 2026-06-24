import pytest
from src.domain.chat_histories.entity import ChatHistory
from src.domain.chat_histories.vals import AssistantMessage, UserMessage
from src.domain.players.vals import PlayerId


class TestChatHistoryEntity:
    """Группа тестов для сущности ChatHistory."""

    def test_success_create_initializes_empty_history(self) -> None:
        player_id = PlayerId("76561198001453454")
        chat_history = ChatHistory.create(player_id=player_id)

        assert chat_history.player_id == player_id
        assert chat_history.history == []
        assert len(chat_history.history) == 0

    def test_append_turn_adds_both_messages_with_correct_structure(self) -> None:
        player_id = PlayerId("76561198001453454")
        chat_history = ChatHistory.create(player_id=player_id)

        user_msg = UserMessage("How to craft a stone axe?")
        assistant_msg = AssistantMessage("You need 2 stone and 2 wood.")

        chat_history.append_turn(
            user_message=user_msg,
            assistant_message=assistant_msg,
        )

        assert len(chat_history.history) == 2
        assert chat_history.history[0] == {
            "role": "user",
            "content": "How to craft a stone axe?",
        }

        assert chat_history.history[1] == {
            "role": "assistant",
            "content": "You need 2 stone and 2 wood.",
        }

    def test_append_multiple_turns_preserves_strict_chronological_order(self) -> None:
        player_id = PlayerId("76561198001453454")
        chat_history = ChatHistory.create(player_id=player_id)

        turn_1_user = UserMessage("Hello")
        turn_1_assistant = AssistantMessage("Hi there")

        turn_2_user = UserMessage("What is your name?")
        turn_2_assistant = AssistantMessage("I am an AI assistant")

        chat_history.append_turn(turn_1_user, turn_1_assistant)
        chat_history.append_turn(turn_2_user, turn_2_assistant)

        assert len(chat_history.history) == 4

        roles = [msg["role"] for msg in chat_history.history]
        assert roles == ["user", "assistant", "user", "assistant"]

        assert chat_history.history[2]["content"] == "What is your name?"
        assert chat_history.history[3]["content"] == "I am an AI assistant"


def test_append_turn_truncates_oldest_messages_when_limit_exceeded() -> None:
    player_id = PlayerId("76561198001453454")
    chat_history = ChatHistory.create(player_id=player_id)

    max_turns = ChatHistory._MAX_HISTORY_SIZE // 2

    for i in range(max_turns):
        chat_history.append_turn(
            UserMessage(f"Вопрос {i}"),
            AssistantMessage(f"Ответ {i}")
        )

    assert len(chat_history.history) == ChatHistory._MAX_HISTORY_SIZE
    assert chat_history.history[0]["content"] == "Вопрос 0"

    chat_history.append_turn(
        UserMessage("Свежий вопрос"),
        AssistantMessage("Свежий ответ")
    )

    assert len(chat_history.history) == ChatHistory._MAX_HISTORY_SIZE

    assert chat_history.history[0]["content"] == "Вопрос 1"

    assert chat_history.history[-2]["content"] == "Свежий вопрос"
    assert chat_history.history[-1]["content"] == "Свежий ответ"
