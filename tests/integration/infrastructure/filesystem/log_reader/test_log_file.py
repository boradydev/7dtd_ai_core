import asyncio

import aiofiles
import pytest

from src.infrastructure.filesystem.log_reader.log_file import LogFile


async def test_log_file_reads_dynamic_lines(
    writer,
    tmp_path,
) -> None:
    """Проверяет чтение новых строк, которые динамически дописываются в лог-файл."""
    log_reader = LogFile(
        str(tmp_path),
        find_pattern="test_*",
        poll_interval=0.01,
        rotation_check_interval=1,
    )

    expected_lines = [f"line_{i}\n" for i in range(100)]
    received_lines: list[str] = []

    async def reader() -> None:
        async for line in log_reader.get_line():
            received_lines.append(line)

            if len(received_lines) == len(expected_lines):
                await log_reader.close()
                break

    reader_task = asyncio.create_task(reader())

    await asyncio.sleep(0.2)

    try:
        await asyncio.wait_for(
            asyncio.gather(
                writer(expected_lines),
                reader_task,
            ),
            timeout=5.0,
        )
    except TimeoutError:
        pytest.fail(
            f"Timeout. Received {len(received_lines)} "
            f"of {len(expected_lines)} lines. "
            f"Last lines: {received_lines[-5:] if received_lines else []}"
        )

    assert received_lines == expected_lines


async def test_log_file_skips_oversized_line(
    file_path,
    writer,
    mock_logger,
) -> None:
    """Проверяет пропуск строк, превышающих max_chunk_size."""
    oversized_line = "line_over_max_chunk_size\n"

    input_lines = [
        "line_1\n",
        oversized_line,
        "line_3\n",
        "\n",
        "",
        "line_5\n",
    ]

    expected_lines = [
        "line_1\n",
        "line_3\n",
        "line_5\n",
    ]

    log_file = LogFile(
        str(file_path.parent),
        find_pattern="test_*",
        max_chunk_size=10,
        poll_interval=0.01,
        rotation_check_interval=1,
        logger=mock_logger,
    )

    received_lines: list[str] = []

    async def reader() -> None:
        async for line in log_file.get_line():
            received_lines.append(line)

            if len(received_lines) == len(expected_lines):
                await log_file.close()
                break

    reader_task = asyncio.create_task(reader())

    await asyncio.sleep(0.2)

    try:
        await asyncio.wait_for(
            asyncio.gather(
                writer(input_lines),
                reader_task,
            ),
            timeout=5.0,
        )
    except TimeoutError:
        pytest.fail(f"Timeout. Received lines: {received_lines}")

    assert received_lines == expected_lines

    mock_logger.warning.assert_called_once_with(
        log_file._SKIP_LINE_MSG.format(
            file_path=str(file_path),
            total_skipped_size=len(oversized_line),
        )
    )


async def test_log_file_switches_to_rotated_file(
    tmp_path,
) -> None:
    """Проверяет автоматическое переключение на новый лог-файл после ротации."""
    first_file = tmp_path / "test_1.log"
    second_file = tmp_path / "test_2.log"

    first_file.touch()

    log_file = LogFile(
        str(tmp_path),
        find_pattern="test_*",
        poll_interval=0.01,
        rotation_check_interval=0.1,
    )

    received_lines: list[str] = []

    async def reader() -> None:
        async for line in log_file.get_line():
            received_lines.append(line)

            if len(received_lines) == 2:
                await log_file.close()
                break

    reader_task = asyncio.create_task(reader())

    await asyncio.sleep(0.2)

    async with aiofiles.open(first_file, mode="a") as file:
        await file.write("line_1\n")
        await file.flush()

    await asyncio.sleep(0.2)

    second_file.touch()

    await asyncio.sleep(0.2)

    async with aiofiles.open(second_file, mode="a") as file:
        await file.write("line_2\n")
        await file.flush()

    await asyncio.wait_for(reader_task, timeout=5)

    assert received_lines == [
        "line_1\n",
        "line_2\n",
    ]


async def test_find_latest_log_file(
    tmp_path,
) -> None:
    """Проверяет поиск самого нового лог-файла по шаблону."""
    first_file = tmp_path / "test_1.log"
    second_file = tmp_path / "test_2.log"

    first_file.touch()

    await asyncio.sleep(0.01)

    second_file.touch()

    log_file = LogFile(
        str(tmp_path),
        find_pattern="test_*",
    )

    result = await log_file._find_latest_log_file()

    assert result == str(second_file)


async def test_log_file_waits_until_file_appears(
    tmp_path,
) -> None:
    """Проверяет ожидание появления лог-файла и последующее чтение новых строк."""
    file_path = tmp_path / "test_1.log"

    log_file = LogFile(
        str(tmp_path),
        find_pattern="test_*",
        poll_interval=0.01,
        rotation_check_interval=0.1,
    )

    received_lines: list[str] = []

    async def reader() -> None:
        async for line in log_file.get_line():
            received_lines.append(line)
            await log_file.close()
            break

    reader_task = asyncio.create_task(reader())

    await asyncio.sleep(0.5)

    file_path.touch()

    await asyncio.sleep(0.5)

    async with aiofiles.open(file_path, mode="a") as file:
        await file.write("hello\n")
        await file.flush()

    await asyncio.wait_for(reader_task, timeout=5)

    assert received_lines == ["hello\n"]
