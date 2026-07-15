import asyncio
from pathlib import Path

from src.infra.filesystem.log_reader.log_finder import log_finder


async def test_find_latest_log_file(tmp_path: Path) -> None:
    first_file = tmp_path / "output_log_client__1.txt"
    first_file.write_text("some text")
    print(f"Create first file: {first_file.name}", end=" -> ", flush=True)
    first_result = log_finder(str(tmp_path), "output_log_client__*.txt")
    assert first_result is not None
    print(f"received last file path: {Path(first_result).name}", flush=True)
    assert first_result == str(first_file)

    await asyncio.sleep(0.1)

    second_file = tmp_path / "output_log_client__2.txt"
    second_file.write_text("some text")
    print(f"Create second file: {second_file.name}", end=" -> ", flush=True)
    second_result = log_finder(str(tmp_path), "output_log_client__*.txt")
    assert second_result is not None
    print(f"received last file path: {Path(second_result).name}", flush=True)
    assert second_result == str(second_file)

    await asyncio.sleep(0.1)

    third_file = tmp_path / "output_log_client__3.txt"
    third_file.write_text("some text")
    print(f"Create third file: {third_file.name}", end=" -> ", flush=True)
    third_result = log_finder(str(tmp_path), "output_log_client__*.txt")
    assert third_result is not None
    print(f"received last file path: {Path(third_result).name}", flush=True)
    assert third_result == str(third_file)
