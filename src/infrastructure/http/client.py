from types import TracebackType

import aiohttp


class HTTPClient:
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str],
        limit: int = 5,
    ) -> None:
        self._base_url = base_url
        self._headers = headers
        self._limit = limit
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                base_url=self._base_url,
                headers=self._headers,
                connector=aiohttp.TCPConnector(limit=self._limit),
            )
        return self._session

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        pass

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
