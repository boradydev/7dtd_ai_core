from pathlib import Path

from src.application.game_data.schemas.localization import LocalizationGameData
from src.infrastructure.csv_parser.common.parser import UniversalCsvParser
from src.infrastructure.csv_parser.patterns.localization import PATTERN


sdtd_config_dir = Path("C:/Steam/steamapps/common/7 Days To Die/Data/Config")
file_name = "Localization.csv"


def test_localization():
    csv_parser = UniversalCsvParser(
        str(
            sdtd_config_dir / file_name,
        ),
        PATTERN,
    )
    raw_data = csv_parser.run()

    schemas = [LocalizationGameData.model_validate(row) for row in raw_data]

    assert len(schemas) == len(raw_data)
