import csv
from collections.abc import Sequence
from pathlib import Path


class UniversalCsvParser:
    """
    Универсальный парсер CSV-файлов с поддержкой фильтрации и переименования колонок.

    Класс позволяет читать CSV-файлы и преобразовывать их строки в словари,
    оставляя только нужные поля и переименовывая их согласно заданному шаблону.

    Каждый элемент шаблона — это кортеж из двух строк:
    1. Название колонки в исходном CSV-файле (чувствительно к регистру).
    2. Новое имя для этой колонки, которое будет использоваться в коде.
    Шаблон: pattern = [("key1_from_csv", "key1_for_dict"), ("key2_csv", "key2_dict"),]
    """

    def __init__(
        self,
        file_path: str | Path,
        pattern: Sequence[tuple[str, str]],
    ) -> None:
        self._file_path = Path(file_path)
        self._pattern = pattern

    def run(self) -> list[dict[str, str]]:
        """
        Запускает процесс чтения и трансформации CSV-файла.

        Метод открывает файл с кодировкой 'utf-8-sig' для корректной обработки
        BOM-маркеров, фильтрует данные по шаблону и выводит их в консоль.

        Returns:
            Список словарей. Каждый словарь представляет собой строку из CSV,
            где ключи — это новые имена из шаблона pattern, а значения —
            текст из соответствующих ячеек файла.

        Raises:
            FileNotFoundError: Если указанный файл не существует.
            KeyError: Если в CSV-файле отсутствует колонка, указанная в шаблоне.
        """
        with open(self._file_path, encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            result = []
            for row in reader:
                new_row = {}
                for prev_key, new_key in self._pattern:
                    new_row[new_key] = row[prev_key]

                result.append(new_row)

            return result
