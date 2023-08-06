import os
from typing import Any, Dict, List, Optional, TypeVar

import httpx

from .__version__ import __version__


T = TypeVar("T", bound="BaseAsyncClient")
USER_AGENT = f"python-lamadava/{__version__}"


class BaseClient:
    def __init__(self, token: Optional[str] = None, timeout: Optional[float] = 10):
        if token is None:
            token = os.getenv("LAMADAVA_TOKEN")
        assert (
            token is not None
        ), "Token not found. Use Client(token='<token>') or set env LAMADAVA_TOKEN=<token>"
        self._url = "https://api.lamadava.com{}"
        self._token = token
        self._timeout = timeout
        self._headers = {
            "accept": "application/json",
            "user-agent": USER_AGENT,
            "x-access-key": token,
        }


class BaseSyncClient(BaseClient):
    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
    ) -> Dict:
        url = self._url.format(path)
        if params:
            params = {k: v for k, v in params.items() if v}
        resp = httpx.request(
            method,
            url,
            headers=self._headers,
            params=params,
            data=data,
            timeout=self._timeout,
        )
        return resp.json()

    def _paging_request(
        self,
        path: str,
        params: Optional[Dict[str, Any]],
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        page_key: str = "page_id",
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        if params is None:
            params = {}
        if container is None:
            container = []
        work_count = 0
        request_count = 0
        while True:
            res = self._request("GET", path, params=params)
            request_count += 1
            if isinstance(res, list) and len(res) == 2:
                items, npid = res
            else:
                items = res["response"].get("items", res["response"].get("users"))
                npid = res.get("next_page_id")
            if count is not None:
                rest = count - work_count
                items = items[:rest]
            container.extend(items)
            work_count += len(items)
            if not npid:
                break
            if count is not None and work_count == count:
                break
            if max_requests is not None and max_requests >= request_count:
                break
            params[page_key] = npid
        return container


class BaseAsyncClient(BaseClient):
    def __init__(self, token: Optional[str] = None, timeout: Optional[float] = 10):
        super().__init__(token=token, timeout=timeout)
        self._client = httpx.AsyncClient()

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
    ) -> Dict:
        url = self._url.format(path)
        if params:
            params = {k: v for k, v in params.items() if v}
        resp = await self._client.request(
            method,
            url,
            headers=self._headers,
            params=params,
            data=data,
            timeout=self._timeout,
        )
        return resp.json()

    async def _paging_request(
        self,
        path: str,
        params: Optional[Dict[str, Any]],
        count: Optional[int] = None,
        container: Optional[List[Dict]] = None,
        page_key: str = "page_id",
        max_requests: Optional[int] = None,
    ) -> List[Dict]:
        if params is None:
            params = {}
        if container is None:
            container = []
        work_count = 0
        request_count = 0
        while True:
            res = await self._request("GET", path, params=params)
            request_count += 1
            if isinstance(res, list) and len(res) == 2:
                items, npid = res
            else:
                items = res["response"].get("items", res["response"].get("users"))
                npid = res.get("next_page_id")
            if count is not None:
                rest = count - work_count
                items = items[:rest]
            container.extend(items)
            work_count += len(items)
            if not npid:
                break
            if count is not None and work_count == count:
                break
            if max_requests is not None and max_requests >= request_count:
                break
            params[page_key] = npid
        return container

    async def aclose(self) -> None:
        """
        Close client.
        """
        await self._client.aclose()

    async def __aenter__(self: T) -> T:
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args) -> None:
        await self._client.__aexit__(*args)
