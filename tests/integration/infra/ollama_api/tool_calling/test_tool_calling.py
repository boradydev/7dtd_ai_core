import time

import pytest

from src.app.common.ai.behavior import AIBehavior


@pytest.mark.parametrize(
    ("message", "category"),
    [
        ("Привет, как дела?", None),
        ("Спасибо!", None),
        ("Кто ты?", None),
        ("Какая сегодня погода?", None),

        ("Чем добывать древесину?", "woodcutting"),
        ("Чем рубить деревья?", "woodcutting"),
        ("Как срубить дерево?", "woodcutting"),
        ("Какой инструмент нужен для дерева?", "woodcutting"),
        ("Чем добывать бревна?", "woodcutting"),
        ("Как быстрее добывать дерево?", "woodcutting"),

        ("Как добыть камень?", "mining"),
        ("Чем добывать руду?", "mining"),
        ("Как добывать железо?", "mining"),
        ("Как добывать уголь?", "mining"),
        ("Какая кирка лучше?", "mining"),

        ("Чем копать землю?", "digging"),
        ("Как выкопать яму?", "digging"),
        ("Чем копать песок?", "digging"),
        ("Как быстрее копать?", "digging"),
        ("Как выкопать траншею?", "digging"),
        ("Чем копать глину?", "digging"),

        ("Чем добывать древисину?", "woodcutting"),
        ("Как дабыть камень?", "mining"),
        ("Чем капать землю?", "digging"),

        ("How do I cut trees?", "woodcutting"),
        ("How do I mine stone?", "mining"),
        ("How do I dig soil?", "digging"),

        (
            "Привет! Подскажи, пожалуйста, чем лучше добывать древесину в начале игры?",
            "woodcutting",
        ),
        (
            "Я только начал играть, каким инструментом добывать камень?",
            "mining",
        ),
        (
            "Подскажи, чем лучше копать землю возле базы?",
            "digging",
        ),
    ],
)
async def test_tool_calling_registry_returns_tool_by_name(
    tool_registry,
    qwen2_api,
    message,
    category,
    benchmark,
) -> None:
    started = time.perf_counter()

    tools_call = await qwen2_api.predict_tool_calls(
        behavior=AIBehavior.TOOL_ROUTER,
        message=message,
        tools=tool_registry.get_all(),
    )

    elapsed = time.perf_counter() - started

    predicted = tools_call[0].kwargs.get("category") if tools_call else "NO_TOOL"
    expected = category or "NO_TOOL"

    print(
        f"{'✅' if predicted == expected else '❌'} "
        f"[{elapsed:.3f}s] "
        f"{expected:<12} | {predicted:<12} | {message}"
    )

    benchmark.add(
        elapsed=elapsed,
        success=(predicted == expected),
    )