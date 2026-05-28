import logging

from src.application.common.abcs import ICase, ILogger
from src.application.common.dtos import IBaseDTO
from src.presentation.log_dispatchers.abcs import IParser, IRoute


class Route[DTO: IBaseDTO](IRoute):
    def __init__(
        self,
        parser: type[IParser],
        dto_type: type[DTO],
        logger: ILogger | None = None,
    ) -> None:
        self._parser = parser
        self._dto_type = dto_type
        self._logger = logger or logging.getLogger(__name__)
        self._cases: list[ICase[DTO]] = []

    def add_case(self, case: ICase[DTO]) -> None:
        self._cases.append(case)

    def extract(self, line: str) -> dict[str, str] | None:
        return self._parser.extract_fields(line)

    async def run(self, data: dict[str, str]) -> None:
        try:
            dto = self._dto_type(**data)
            for case in self._cases:
                await case.execute(dto)
        except Exception as exc:
            self._logger.error(exc, exc_info=True)
