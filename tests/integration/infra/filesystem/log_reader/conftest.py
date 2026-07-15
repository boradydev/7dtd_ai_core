import asyncio
from collections.abc import Callable, Coroutine
from pathlib import Path
from typing import Any

import aiofiles
import pytest


@pytest.fixture
def file_path(tmp_path) -> Path:
    file_path = tmp_path / "test_1.log"
    file_path.touch()
    return file_path


@pytest.fixture
def writer(file_path) -> Callable[[list[str]], Coroutine[Any, Any, None]]:
    async def _writer(expected_lines: list[str]) -> None:
        async with aiofiles.open(file_path, mode="a") as file:
            for line in expected_lines:
                await file.write(line)
                await file.flush()
                await asyncio.sleep(0.001)

    return _writer
