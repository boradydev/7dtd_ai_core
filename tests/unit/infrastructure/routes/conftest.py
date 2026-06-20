from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, create_autospec

import pytest

from src.application.common.abcs import ICase
from src.application.common.dtos import IBaseDTO
from src.presentation.log_dispatchers.abcs import IParser


@dataclass(frozen=True, slots=True, kw_only=True)
class FakeDTO(IBaseDTO):
    value1: str
    value2: str
    value3: str
    value4: str
    value5: str


@pytest.fixture
def mock_parser_type() -> MagicMock | type[IParser]:
    """
    Возвращает замоканный КЛАСС (тип), а не его экземпляр.

    Использует create_autospec для точного копирования сигнатуры @classmethod методов.
    """
    return create_autospec(IParser, spec_set=True)


@pytest.fixture
def mock_first_case() -> AsyncMock | ICase[FakeDTO]:
    return AsyncMock(spec_set=ICase)


@pytest.fixture
def mock_second_case() -> AsyncMock | ICase[FakeDTO]:
    return AsyncMock(spec_set=ICase)
