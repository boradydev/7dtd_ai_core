from typing import Any

import aiohttp

from src.application.common.abcs import IHTTPClient


class HTTPClient(IHTTPClient):
    def __init__(
        self,
        base_url: str,
        headers: dict[str, str] | None = None,
        limit: int = 5,
    ) -> None:
        self._base_url = base_url
        self._headers = headers or {}
        self._limit = limit
        self._session: aiohttp.ClientSession | None = None

    def _get_session(self) -> aiohttp.ClientSession:
        """Ленивая инициализация сессии при первом запросе."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                base_url=self._base_url,
                headers=self._headers,
                connector=aiohttp.TCPConnector(limit=self._limit),
            )
        return self._session

    async def post_json(
        self,
        url: str,
        data: dict[str, Any],
    ) -> Any:
        session = self._get_session()
        async with session.post(url, json=data) as response:
            response.raise_for_status()
            return await response.json()

    async def post_form(
        self,
        url: str,
        data: dict[str, Any],
    ) -> Any:
        session = self._get_session()
        async with session.post(url, data=data) as response:
            response.raise_for_status()
            return await response.json()

    async def close(self) -> None:
        """Закрывает все открытые HTTP соединения."""
        if self._session and not self._session.closed:
            await self._session.close()
