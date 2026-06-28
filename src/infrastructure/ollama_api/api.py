import logging
from collections.abc import AsyncGenerator

from ollama import AsyncClient

from src.application.chat_messages.abcs import IAIClient
from src.application.common.ai.abcs import IModelConfig, ISystemInstructions


class OllamaApi[Behavior](IAIClient[Behavior]):
    _ATTEMPT_MSG = "attempt: {attempt}"

    def __init__(
        self,
        host: str,
        instructions: type[ISystemInstructions[Behavior]],
        options: type[IModelConfig[Behavior]],
        model_name: str = "llama3.1",
    ) -> None:
        """
        Инициализирует клиент OllamaApi.

        Args:
            host: URL-адрес хоста, на котором запущен сервис Ollama.
            instructions: Класс ``system`` промптов для настройки поведения модели.
            options: Класс конфигурации параметров генерации модели.
            model_name: Название используемой языковой модели. По умолчанию "llama3.1".
        """
        self._client = AsyncClient(host=host)
        self._instructions = instructions
        self._options = options
        self._model_name = model_name
        self._logger = logging.getLogger(__name__)

    async def chat(
        self,
        behavior: Behavior,
        message: str,
        history: list[dict[str, str]] | None = None,
    ) -> AsyncGenerator[str]:
        """
        Запрос в ИИ.

        Args:
            behavior:
                Поведение ИИ, определяет системный промпт.

                Пример:

                    {
                        "role": "system",
                        "content": "Ты чат бот в игре 7dtd"
                    }

            message:
                Сообщение клиента.

            history:
                История сообщений.

                Важно:
                    Не должна содержать роль ``system``.
                    Главный системный промпт автоматически добавляется
                    кодом в начало списка.

                Формат:

                    [
                        {"role": "user", "content": "Поза-предыдущий промпт"},

                        {"role": "assistant", "content": "Поза-предыдущий ответ"},

                        {"role": "user", "content": "Предыдущий промпт"},

                        {"role": "assistant", "content": "Предыдущий ответ"}
                    ]
        """
        messages = [{"role": "system", "content": self._instructions.get(behavior)}]
        if history:
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
