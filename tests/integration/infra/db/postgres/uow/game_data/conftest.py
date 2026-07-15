import pytest

from src.infra.db.postgres.uow.game_data import GameDataUOW


@pytest.fixture
def game_data_uow(postgres) -> GameDataUOW:
    return GameDataUOW(
        session_factory=postgres.session_factory,
    )
