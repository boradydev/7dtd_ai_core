import logging

from src.application.chat_messages.dtos import GlobalMassageDTO
from src.application.common.abcs import ICase


class ChatMassageCase(ICase[GlobalMassageDTO]):
    def __init__(
        self,
        logger: logging.Logger | None = None,
    ) -> None:
        self._logger = logger or logging.getLogger(__name__)

    async def execute(self, dto: GlobalMassageDTO) -> None:
        pass
