import sys
from io import TextIOWrapper


def pytest_configure():
    """
    Принудительно настраиваем stdout на работу с UTF-8.

    Решает проблему нечитаемых символов при выводе print (Windows, Linux, macOS).

    ``errors="replace"`` Заменит символ на ? которые не может закодировать.
    """
    if isinstance(sys.stdout, TextIOWrapper):
        sys.stdout.reconfigure(
            encoding="utf-8",
            errors="replace",
        )