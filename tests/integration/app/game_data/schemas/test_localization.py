from src.app.game_data.schemas.localization import LocalizationGameData
from src.infra.csv_parser.common.parser import UniversalCsvParser
from src.infra.csv_parser.patterns.localization import PATTERN


def test_localization(config_dir):
    csv_parser = UniversalCsvParser(
        config_dir / "Localization.csv",
        PATTERN,
    )
    raw_data = csv_parser.run()

    schemas = [LocalizationGameData.model_validate(row) for row in raw_data]

    assert len(schemas) == len(raw_data)
