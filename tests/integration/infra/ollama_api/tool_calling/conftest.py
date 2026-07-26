import json
from collections.abc import Callable, Generator
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

import pytest

from src.infra.ollama_api.api import OllamaApi
from src.infra.ollama_api.config import AIModelConfig
from src.infra.ollama_api.instructions.registry import SystemInstruction
from src.infra.ollama_api.tool_calling.registry import ToolRegistry


MODEL_NAME = "qwen2.5:3b"


@pytest.fixture
def enum_func() -> Callable[..., Any]:
    class GameToolCategory(StrEnum):
        WOODCUTTING = "woodcutting"
        DIGGING = "digging"
        MINING = "mining"

    def get_tools_json(category: GameToolCategory) -> str:
        tools = []
        match category:
            case GameToolCategory.WOODCUTTING:
                tools = [
                    "Axe",
                    "Felling axe",
                    "Hand saw",
                    "Chainsaw",
                    "Two-man saw",
                ]
            case GameToolCategory.DIGGING:
                tools = [
                    "Shovel",
                    "Spade",
                    "Entrenching tool",
                    "Trowel",
                    "Mattock",
                ]
            case GameToolCategory.MINING:
                tools = [
                    "Pickaxe",
                    "Jackhammer",
                    "Drill",
                    "Sledgehammer",
                    "Chisel",
                ]
            case _:
                raise ValueError(f"Unknown category: {category}")

        return json.dumps({"tools": tools}, ensure_ascii=False)

    return get_tools_json


@pytest.fixture
def tool_registry(enum_func) -> ToolRegistry:
    registry = ToolRegistry(base_dir=Path(__file__).parent)
    registry.register(file_path="prompt_description/enum.md", func=enum_func)
    return registry


@pytest.fixture
def qwen2_api():
    return OllamaApi(
        host="http://192.168.1.108:11434",
        instructions=SystemInstruction,
        options=AIModelConfig,
        model_name=MODEL_NAME,
    )


@dataclass(slots=True)
class ModelBenchmark:
    model: str
    total: int = 0
    correct: int = 0
    total_time: float = 0.0

    def add(self, elapsed: float, success: bool) -> None:
        self.total += 1
        self.total_time += elapsed
        if success:
            self.correct += 1

    @property
    def accuracy(self) -> float:
        return self.correct / self.total * 100

    @property
    def average_time(self) -> float:
        return self.total_time / self.total


@pytest.fixture(scope="module")
def benchmark() -> Generator[ModelBenchmark]:
    benchmark = ModelBenchmark(model=MODEL_NAME)

    yield benchmark

    print()
    print("=" * 42)
    print(f"Model    : {benchmark.model}")
    print(
        f"Accuracy : {benchmark.correct}/{benchmark.total} ({benchmark.accuracy:.1f}%)"
    )
    print(f"Average  : {benchmark.average_time:.3f}s")
    print("=" * 42)

    assert benchmark.accuracy >= 90