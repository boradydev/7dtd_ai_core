import pytest

from src.domain.chat_histories import excs
from src.domain.chat_histories.vals import AssistantMessage, UserMessage


@pytest.mark.parametrize(
    "message_class",
    [
        UserMessage,
        AssistantMessage,
    ],
)
class TestChatMessagesBaseValidation:
    """Группа тестов для базовой валидации обоих типов сообщений."""

    def test_success_creation_with_valid_text(self, message_class) -> None:
        text = "Hello, world!"
        msg = message_class(text)
        assert msg.value == "Hello, world!"

    def test_strip_whitespace_on_creation(self, message_class) -> None:
        text = "   \n  Some text with spaces  \t  "
        msg = message_class(text)
        assert msg.value == "Some text with spaces"

    def test_remove_invisible_control_characters(self, message_class) -> None:
        text = "Line1\n\x00Line2\t\x07Line3\x1f"
        msg = message_class(text)
        assert msg.value == "Line1\nLine2\tLine3"

    @pytest.mark.parametrize(
        "empty_value",
        [
            "",
            "   ",
            "\n\n",
            "\x00\x07",
        ],
    )
    def test_raise_exception_when_content_is_empty(
        self, message_class, empty_value
    ) -> None:
        with pytest.raises(excs.EmptyMessageException):
            message_class(empty_value)


class TestUserMessageSpecifics:
    """Тесты, специфичные только для UserMessage (например, лимиты длины)."""

    def test_raise_exception_when_user_message_too_long(self) -> None:
        too_long_text = "a" * (UserMessage._MAX_LENGTH + 1)
        with pytest.raises(excs.MessageTooLongException):
            UserMessage(too_long_text)

    def test_success_when_user_message_exactly_at_max_length(self) -> None:
        max_length_text = "a" * UserMessage._MAX_LENGTH
        msg = UserMessage(max_length_text)
        assert len(msg.value) == UserMessage._MAX_LENGTH


class TestAssistantMessageSpecifics:
    """Тесты, специфичные только для AssistantMessage."""

    def test_raise_exception_when_assistant_message_too_long(self) -> None:
        too_long_text = "a" * (AssistantMessage._MAX_LENGTH + 1)
        with pytest.raises(excs.MessageTooLongException):
            AssistantMessage(too_long_text)

    def test_success_when_assistant_message_exactly_at_max_length(self) -> None:
        max_length_text = "a" * AssistantMessage._MAX_LENGTH
        msg = AssistantMessage(max_length_text)
        assert len(msg.value) == AssistantMessage._MAX_LENGTH


@pytest.mark.parametrize(
    "message_class",
    [
        UserMessage,
        AssistantMessage,
    ],
)
def test_value_objects_are_frozen(message_class) -> None:
    """Проверяет, что dataclass действительно frozen и защищен от мутации извне."""
    msg = message_class("Original")
    with pytest.raises(AttributeError):
        msg.value = "Mutated"
