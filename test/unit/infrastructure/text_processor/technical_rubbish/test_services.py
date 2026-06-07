import pytest

from src.infrastructure.text_processors.technical_rubbish.services import (
    TechnicalRubbishCleaner,
)


@pytest.mark.parametrize(
    ("input_text", "expected_output"),
    [
        (
            "<p>Привет мир</p>",
            "Привет мир",
        ),
        (
            "  много     пробелов   ",
            "много пробелов",
        ),
        (
            "<div>  текст   внутри  </div>",
            "текст внутри",
        ),
        (
            "<p><strong>Зомби</strong> в доме!</p>",
            "Зомби в доме!",
        ),
        (
            "\n\tтекст\t\n",
            "текст",
        ),
        (
            "",
            "",
        ),
        (
            "обычный текст",
            "обычный текст",
        ),
    ],
    ids=[
        "remove_html",
        "collapse_spaces",
        "html_and_spaces",
        "nested_html",
        "tabs_and_newlines",
        "empty_string",
        "plain_text",
    ],
)
async def test_technical_rubbish_cleaner(
    input_text: str,
    expected_output: str,
) -> None:
    cleaner = TechnicalRubbishCleaner()

    result = await cleaner.process(input_text)

    assert result == expected_output
