import pytest

from src.app.game_data.schemas.localization import LocalizationGameData
from src.infra.csv_parser.common.parser import UniversalCsvParser
from src.infra.csv_parser.patterns.localization import PATTERN


@pytest.mark.timeout(5)
async def test_game_data_localization_repo(
    game_data_uow,
    config_dir,
) -> None:
    file_path = config_dir / "localization.csv"

    parser = UniversalCsvParser(
        file_path=file_path,
        pattern=PATTERN,
    )

    game_data = [LocalizationGameData.model_validate(row) for row in parser.run()]

    async with game_data_uow as uow:
        await uow.localization.clear()
        await uow.localization.add_many(game_data)
        await uow.commit()
