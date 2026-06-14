from pathlib import Path


def log_finder(log_dir: str, find_pattern: str) -> str | None:
    """
    Находит самый свежий файл в указанной директории по заданному шаблону.

    Функция сканирует директорию в один проход без выделения лишней памяти
    и возвращает путь к файлу с максимальной датой изменения (mtime).

    Args:
        log_dir: Путь к директории, в которой необходимо выполнить поиск.
        find_pattern: Шаблон подстановки (glob pattern) для фильтрации файлов.
            Поддерживает стандартные спецсимволы:
            - `*` matches everything (например, `*.txt` найдет все текстовые файлы)
            - `?` matches any single character (например, `log_?.txt`)
            - `[seq]` matches any character in seq (например, `log_[0-9].txt`)
            - `**` для рекурсивного поиска в подпапках (например, `**/*.log`)

    Returns:
        Абсолютный или относительный путь к последнему измененному файлу
        в виде строки, либо None, если файлы по шаблону не найдены.

    Examples:
        >>> log_finder("C:/games/logs", "output_log_client__*.txt")
        'C:/games/logs/output_log_client__2026-05-16__11-45-50.txt'

        >>> log_finder("/var/log", "nginx/access.log.*")
        '/var/log/nginx/access.log.1'
    """
    _log_dir = Path(log_dir)
    file_path = max(
        _log_dir.glob(find_pattern),
        key=lambda file: file.stat().st_mtime,
        default=None,
    )
    return str(file_path) if file_path else None
