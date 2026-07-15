from pathlib import Path

import pytest

from src.infra.csv_parser.common.parser import UniversalCsvParser


current_dir = Path(__file__).resolve().parent


def test_universal_csv_parser_success():
    test_pattern = (
        ("Key", "name"),
        ("russian", "ru"),
    )

    file_path = "data.csv"

    parser = UniversalCsvParser(str(current_dir / file_path), test_pattern)
    result = parser.run()

    assert len(result) == 2

    assert result[0] == {"name": "menu_start", "ru": "Старт"}

    assert "unused_column" not in result[0]
    assert "english" not in result[0]


def test_universal_csv_parser_missing_key():
    bad_pattern = (("russian", "ru"),)
    file_path = "miss_key.csv"

    parser = UniversalCsvParser(str(current_dir / file_path), bad_pattern)

    with pytest.raises(KeyError):
        parser.run()
