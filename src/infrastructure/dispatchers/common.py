import asyncio
import logging
from logging import Logger

from src.presentation.log_dispatchers.abcs import IDispatcher, ILogFile, IRoute


class Dispatcher(IDispatcher):
    _NO_ROUTE_MSG = "No route found for line {line!r} in file://{log_dir}"
    _START_MSG = "The dispatcher is started. file://{log_dir}"

    def __init__(
        self,
        log_file: ILogFile,
        logger: Logger | None = None,
        log_unhandled: bool = False,
    ) -> None:
        self._log_file = log_file
        self._create_task = asyncio.create_task
        self._logger = logger or logging.getLogger(__name__)
        self._routes: list[IRoute] = []
        self._log_unhandled = log_unhandled

    def add_route(self, route: IRoute):
        self._routes.append(route)

    async def run(self) -> None:
        self._logger.info(self._START_MSG.format(log_dir=self._log_file.log_dir))
        async for raw_line in self._log_file.get_line():
            line = raw_line.strip()
            if not line:
                continue

            is_handled = False
            for route in self._routes:
                data = route.extract(line)
                if data is not None:
                    self._create_task(route.run(data))
                    is_handled = True

            if self._log_unhandled and not is_handled:
                self._logger.warning(
                    self._NO_ROUTE_MSG.format(
                        line=line,
                        log_dir=self._log_file.log_dir,
                    )
                )
