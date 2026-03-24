"""GPTMaker async HTTP client with auth, retry, and rate limiting."""

import asyncio
import os
from typing import Any, Optional

import httpx

BASE_URL = "https://api.gptmaker.ai"


class ApiError(Exception):
    def __init__(self, message: str, status_code: int = 0):
        self.status_code = status_code
        super().__init__(message)


class RateLimitError(ApiError):
    pass


class GptMakerClient:
    """Async HTTP client for GPTMaker API."""

    def __init__(self):
        self._token = os.environ.get("GPTMAKER_API_TOKEN", "")
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=BASE_URL,
                timeout=httpx.Timeout(30.0, read=60.0),
                limits=httpx.Limits(max_connections=20),
            )
        return self._client

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token}"}

    async def request(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> Any:
        client = await self._get_client()
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        clean_json = {k: v for k, v in (json or {}).items() if v is not None} if json is not None else None

        for attempt in range(3):
            response = await client.request(
                method,
                path,
                params=clean_params or None,
                json=clean_json,
                headers=self._headers(),
            )

            if response.status_code in (200, 201):
                try:
                    return response.json()
                except Exception:
                    return response.text

            if response.status_code == 429:
                if attempt < 2:
                    await asyncio.sleep(2 ** (attempt + 1))
                    continue
                raise RateLimitError(response.text, status_code=429)

            raise ApiError(
                f"HTTP {response.status_code}: {response.text}",
                status_code=response.status_code,
            )

        raise ApiError("Max retries exceeded")

    async def get(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        return await self.request("GET", path, params=params)

    async def post(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        return await self.request("POST", path, json=json)

    async def put(self, path: str, json: Optional[dict[str, Any]] = None) -> Any:
        return await self.request("PUT", path, json=json)

    async def delete(self, path: str) -> Any:
        return await self.request("DELETE", path)

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()
