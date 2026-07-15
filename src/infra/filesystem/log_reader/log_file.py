import asyncio
import logging
import os
from collections.abc import AsyncIterator

import aiofiles

from src.infra.filesystem.log_reader.log_finder import log_finder
from src.api.log_dispatchers.game.abcs import ILogFile


class LogFile(ILogFile):
    """
    Читает новые строки из последнего лог-файла в директории.

    Модуль чтения (reader) начинает работу с конца файла, периодически проверяет
    ротацию логов и автоматически переключается на более новый лог-файл.
    Слишком длинные строки, превышающие размер ``max_chunk_size``, пропускаются.
    """

    _SKIP_LINE_MSG = (
        "Skipped oversized line in file://{file_path}, "
        "total_skipped_size={total_skipped_size}"
    )
    _NEW_FILE_MSG = "Find new log file://{file_path}"
    _NO_NEW_FILE_MSG = "Log file not found in directory file://{log_dir}"
    _EMPTY_LINES = {"\n", "\r", "\r\n", "\n\r", ""}

    def __init__(
        self,
        log_dir: str,
        *,
        find_pattern: str = "output_log_client__*.txt",
        max_chunk_size: int = 1000,
        poll_interval: float = 0.1,
        rotation_check_interval: float = 10,
        logger: logging.Logger | None = None,
    ) -> None:
        """
        Инициализирует модуль чтения лог-файлов.

        Args:
            log_dir: Директория, в которой находятся лог-файлы.
            find_pattern: Шаблон поиска (glob pattern) для локализации лог-файлов.
            max_chunk_size: Максимальное количество символов, считываемых за один раз.
            poll_interval: Задержка между попытками чтения новых данных из файла.
            rotation_check_interval: Интервал проверки более свежего лог-файла.
            logger: Экземпляр логгера для вывода диагностических сообщений.
        """
        self._log_dir = log_dir
        self._find_pattern = find_pattern
        self._max_chunk_size = max_chunk_size
        self._poll_interval = poll_interval
        self._rotation_check_interval = rotation_check_interval
        self._logger = logger or logging.getLogger(__name__)
        self._running = True

    @property
    def log_dir(self) -> str:
        return self._log_dir

    async def close(self) -> None:
        """Останавливает цикл чтения файла."""
        self._running = False

    async def _find_latest_log_file(self) -> str | None:
        file_path = await asyncio.to_thread(
            lambda: log_finder(
                log_dir=self.log_dir,
                find_pattern=self._find_pattern,
            )
        )
        if file_path is None:
            self._logger.warning(self._NO_NEW_FILE_MSG.format(log_dir=self.log_dir))

        return file_path

    async def _skip_oversized_line(
        self,
        file,
        file_path: str,
        line: str,
    ) -> None:
        total_skipped_size = len(line)
        while not line.endswith("\n"):
            line = await file.readline(self._max_chunk_size)
            if not line:
                break

            total_skipped_size += len(line)

        self._logger.warning(
            self._SKIP_LINE_MSG.format(
                file_path=file_path,
                total_skipped_size=total_skipped_size,
            )
        )

    async def get_line(self) -> AsyncIterator[str]:
        file_path = None
        max_empty_reads = int(self._rotation_check_interval / self._poll_interval)
        while self._running:
            empty_reads = 0
            rotate_file = False
            if file_path is None:
                file_path = await self._find_latest_log_file()

                if file_path is None:
                    await asyncio.sleep(self._rotation_check_interval)
                    continue

                self._logger.info(self._NEW_FILE_MSG.format(file_path=file_path))

            try:
                async with aiofiles.open(file_path, encoding="utf-8") as file:
                    await file.seek(0, os.SEEK_END)

                    while self._running and not rotate_file:
                        line = await file.readline(self._max_chunk_size)
                        if line in self._EMPTY_LINES:
                            empty_reads += 1
                            await asyncio.sleep(self._poll_interval)
                            if empty_reads > max_empty_reads:
                                new_file_path = await self._find_latest_log_file()
                                empty_reads = 0

                                if new_file_path and new_file_path != file_path:
                                    file_path = new_file_path
                                    rotate_file = True
                                    self._logger.info(
                                        self._NEW_FILE_MSG.format(file_path=file_path)
                                    )

                            continue

                        empty_reads = 0

                        if not line.endswith("\n"):
                            await self._skip_oversized_line(
                                file=file,
                                file_path=file_path,
                                line=line,
                            )
                            continue

                        yield line
            except OSError:
                file_path = None
