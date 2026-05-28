import logging
from collections.abc import AsyncIterator

from ollama import AsyncClient

from src.application.common.ai.abcs import IModelConfig, ISystemInstructions


class AIService[Behavior]:
    _ATTEMPT_MSG = "attempt: {attempt}"

    def __init__(
        self,
        host: str,
        instructions: type[ISystemInstructions[Behavior]],
        options: type[IModelConfig[Behavior]],
        model_name: str = "llama3.1",
    ) -> None:
        self._client = AsyncClient(host=host)
        self._instructions = instructions
        self._options = options
        self._model_name = model_name
        self._logger = logging.getLogger(__name__)

    async def process_prompt(
        self,
        behavior: Behavior,
        message: str,
        history: list[dict[str, str]],
    ) -> AsyncIterator[str]:
        """
        Запрос в ИИ.

        Args:
            behavior: Поведение ИИ.
            message: Сообщение клиента.
            history: Изменяемый, в него добавляется история.
        """
        messages = [{"role": "system", "content": self._instructions.get(behavior)}]
        messages.extend(history)
        messages.append({"role": "user", "content": message})

        attempt = 0
        while True:
            try:
                response_stream = await self._client.chat(
                    model=self._model_name,
                    messages=messages,
                    options=self._options.get(behavior),
                    stream=True,
                )
                break
            except Exception as exc:
                attempt += 1
                self._logger.warning(self._ATTEMPT_MSG.format(attempt=attempt))
                if attempt >= 3:
                    raise exc

        async for token in response_stream:
            if token.message and token.message.content:
                yield token.message.content
