from os import PathLike
from pathlib import Path


class MarkdownLoader:
    def __init__(
        self,
        base_dir: PathLike[str] | str,
    ) -> None:
        """
        Создает экземпляр.

        Args:
            base_dir: Путь до базовой директории с MD файлами или директориями.

        Returns:
            Текст из SQL скрипта.
        """
        self._base_dir = Path(base_dir)

    def load(
        self,
        file_path: PathLike[str] | str,
    ) -> str:
        """
        Получает текст из файла MD.

        Args:
            file_path: Текущий путь до MD файла

        Returns:
            Текст из MD файла
        """
        md_path = self._base_dir / file_path
        return md_path.read_text(encoding="utf-8")
