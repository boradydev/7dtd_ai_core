from src.application.common.abcs import IGameAPI
from src.infrastructure.http.client import HTTPClient


class GameAPI(IGameAPI):
    """
    Игра обрабатывает команды по очереди, без параллельного выполнения.

    Рекомендуется одно http подключение, тогда команды выполнятся по порядку.
    """

    _HTTP_MSG = "status: {file_path}, msg: {msg}"

    def __init__(
        self,
        http_client: HTTPClient,
    ) -> None:
        self._http_client = http_client
        self._command_url = "/api/command"

    async def send_message(self, text: str) -> None:
        """Отправляет сообщение от имени сервера в глобальный чат."""
        await self._http_client.post_json(
            url=self._command_url,
            data={
                "command": f'say "{text}"',
                "format": "Full",
            },
        )

    async def buff_player(
        self,
        player_id: str,
        buff_name: str,
    ) -> None:
        """Накладывает баф на игрока."""
        raise NotImplementedError

    async def debuff_player(
        self,
        player_id: str,
        debuff_name: str,
    ) -> None:
        """Накладывает дебаф на игрока."""
        raise NotImplementedError

    async def get_player_name(self, entity_id: str) -> str:
        raise NotImplementedError
