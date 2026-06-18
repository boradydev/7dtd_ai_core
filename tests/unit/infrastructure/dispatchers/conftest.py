from unittest.mock import AsyncMock, MagicMock

import pytest

from src.presentation.log_dispatchers.abcs import ILogFile, IRoute


@pytest.fixture
def mock_log_file() -> AsyncMock | ILogFile:
    return MagicMock(spec_set=ILogFile)


@pytest.fixture
def mock_first_route() -> AsyncMock | IRoute:
    return MagicMock(spec_set=IRoute)


@pytest.fixture
def mock_second_route() -> AsyncMock | IRoute:
    return MagicMock(spec_set=IRoute)
