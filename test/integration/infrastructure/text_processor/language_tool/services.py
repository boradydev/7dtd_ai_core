import sys
from io import TextIOWrapper

import pytest


if isinstance(sys.stdout, TextIOWrapper):
    sys.stdout.reconfigure(
        encoding="utf-8",
        errors="replace",
    )


@pytest.mark.parametrize(
    ("input_text", "exclude_word"),
    [
        ("на меня бежит замбятник помогите", "замбятник"),
        ("где найти инструменты для верстака??", None),
        ("нужен цымент и бетономишалка срочно", None),
        ("опять скримерша пришла паламала стену", "скримерша"),
        ("киньте канатную лестнецу на крышу базы", None),
        ("<p>  зомби   в   доме! </p>", None),
    ],
)
async def test_language_tool_processing_examples(
    processor,
    custom_dictionary,
    input_text,
    exclude_word,
) -> None:
    exclude_words = {"замбятник", "скримерша"}
    custom_dictionary.reload(exclude_words)

    result = await processor.process(input_text)
    if exclude_word is not None:
        assert exclude_word in result

    print(f"\n{result}", end="", flush=True)


@pytest.mark.parametrize(
    "input_text",
    [
        "привет игрок. я не могу выдать тебе предмет",
        "извините команда временно не работает",
        "телепортация невозможна потому что точка назначения недоступна",
        "сервер будет перезапущен через 5 минут пожалуйста завершите свои дела",
        "ваша база находится слишком далеко от точки телепортации",
    ],
)
async def test_language_tool_formal_response_examples(
    processor,
    input_text,
) -> None:
    result = await processor.process(input_text)
    assert result

    print(f"\n{result}", end="", flush=True)
