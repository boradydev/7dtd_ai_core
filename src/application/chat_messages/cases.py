import logging

from src.application.chat_messages.dtos import GlobalChatDTO
from src.application.common.abcs import ICase


class ChatMassageCase(ICase[GlobalChatDTO]):
    def __init__(
        self,
        logger: logging.Logger | None = None,
    ) -> None:
        self._logger = logger or logging.getLogger(__name__)

    async def execute(self, dto: GlobalChatDTO) -> None:
        pass
