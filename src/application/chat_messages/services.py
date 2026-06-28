from src.application.chat_messages.abcs import IMessageBuilder
from src.domain.chat_histories.vals import AssistantMessage


class MessageBuilder(IMessageBuilder):
    """
    Сборщик сообщений ассистента из отдельных токенов.

    Буферизирует входящие токены и собирает их в готовые сообщения
    при обнаружении конца предложения или при принудительном сбросе.
    """

    def __init__(self) -> None:
        self._current_buffer: list[str] = []
        self._sentence_enders = {".", "!", "?"}
        self._full_message_len = 0

    def _build_message(self) -> AssistantMessage:
        message = AssistantMessage("".join(self._current_buffer))
        self._current_buffer.clear()
        return message

    def push(self, token: str) -> AssistantMessage | None:
        self._current_buffer.append(token)
        self._full_message_len += len(token)
        AssistantMessage.check_message_length(self._full_message_len)

        if token in self._sentence_enders:
            return self._build_message()

        return None

    def flush(self) -> AssistantMessage | None:
        if self._current_buffer:
            return self._build_message()

        return None
