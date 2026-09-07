"""The sync and async clients: headers, validation, retries and response mapping."""

from __future__ import annotations

import asyncio
import copy
import os
import random
import re
import time
from typing import Any, Dict, Mapping, Optional, TypeVar

import httpx
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError

from crawlforge._generated.models import ToolInfo
from crawlforge._generated.tools import TOOLS, AsyncToolsMixin, SyncToolsMixin
from crawlforge._version import __version__
from crawlforge.errors import (
    CrawlForgeError,
    error_from_response,
    parse_retry_after,
    request_id_from,
)
from crawlforge.types import ToolResult

DEFAULT_BASE_URL = "https://www.crawlforge.dev/api/v1"
DEFAULT_MAX_RETRIES = 2
DEFAULT_TIMEOUT = 60.0
MAX_RETRY_WAIT = 60.0
USER_AGENT = f"crawlforge-sdk-python/{__version__}"

_TOOL_NAME = re.compile(r"[a-z0-9_]+")
_ClientT = TypeVar("_ClientT", bound="_Core")

# Module attributes so tests can replace the waits without touching the stdlib.
_sleep = time.sleep
_async_sleep = asyncio.sleep


def retry_wait(retry_after: Optional[float], attempt: int) -> float:
    """Seconds to wait before retry number ``attempt`` (0-based) of a 429.

    Retry-After wins when present; otherwise exponential backoff from 1 s with
    +/-20 % jitter. Either way the wait is capped at 60 s.
    """
    if retry_after is not None:
        return min(retry_after, MAX_RETRY_WAIT)
    return min((2.0**attempt) * random.uniform(0.8, 1.2), MAX_RETRY_WAIT)


class _Core:
    def __init__(
        self,
        api_key: Optional[str],
        base_url: Optional[str],
        max_retries: int,
        timeout: float,
    ) -> None:
        key = api_key if api_key is not None else os.environ.get("CRAWLFORGE_API_KEY")
        if not key:
            raise CrawlForgeError(
                0,
                "MISSING_API_KEY",
                "No API key: pass api_key=... or set CRAWLFORGE_API_KEY. "
                "Keys are created at https://www.crawlforge.dev/dashboard/keys",
            )
        self._api_key = key
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.max_retries = max_retries
        self.timeout = timeout
        self._owns_http = False

    def __repr__(self) -> str:
        # Never the key.
        return f"{type(self).__name__}(base_url={self.base_url!r})"

    def with_options(
        self: _ClientT, *, timeout: Optional[float] = None, max_retries: Optional[int] = None
    ) -> _ClientT:
        """A copy of this client with a different per-request timeout or retry budget.

        The copy shares the HTTP connection pool; closing it does not close the original.
        """
        clone = copy.copy(self)
        clone._owns_http = False
        if timeout is not None:
            clone.timeout = timeout
        if max_retries is not None:
            clone.max_retries = max_retries
        return clone

    def _url(self, tool: str) -> str:
        if not _TOOL_NAME.fullmatch(tool):
            raise ValueError(f"invalid tool name {tool!r}")
        return f"{self.base_url}/tools/{tool}"

    def _headers(self, *, auth: bool, body: bool) -> Dict[str, str]:
        headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
        if body:
            headers["Content-Type"] = "application/json"
        if auth:
            headers["X-API-Key"] = self._api_key
        return headers

    @staticmethod
    def _body(tool: str, request: Any, params: Mapping[str, Any]) -> Dict[str, Any]:
        """Validate a typed call locally and return the JSON body to send."""
        model_cls = TOOLS[tool].request_model
        given = {key: value for key, value in params.items() if value is not None}
        if request is not None and given:
            raise TypeError(
                f"{tool}(): pass either a request object or keyword arguments, not both"
            )
        if request is None:
            model = model_cls.model_validate(given)
        elif isinstance(request, model_cls):
            model = request
        elif isinstance(request, Mapping):
            model = model_cls.model_validate(dict(request))
        else:
            raise TypeError(
                f"{tool}(): expected {model_cls.__name__} or a dict, got {type(request).__name__}"
            )
        return model.model_dump(exclude_unset=True, by_alias=True, mode="json")

    @staticmethod
    def _json(response: httpx.Response) -> Any:
        try:
            return response.json()
        except ValueError:
            raise CrawlForgeError(
                response.status_code,
                "UNEXPECTED_RESPONSE",
                f"HTTP {response.status_code} with a non-JSON body",
                response.text,
                request_id_from(response.headers),
            ) from None

    def _result(self, response: httpx.Response) -> ToolResult:
        body = self._json(response)
        if response.status_code >= 400 or (isinstance(body, dict) and body.get("success") is False):
            raise error_from_response(response.status_code, body, response.headers)
        try:
            return ToolResult.model_validate(body)
        except PydanticValidationError:
            raise CrawlForgeError(
                response.status_code,
                "UNEXPECTED_RESPONSE",
                f"HTTP {response.status_code} without a ToolSuccess envelope",
                body,
                request_id_from(response.headers),
            ) from None

    def _info(self, response: httpx.Response) -> ToolInfo:
        body = self._json(response)
        if response.status_code >= 400:
            raise error_from_response(response.status_code, body, response.headers)
        try:
            return ToolInfo.model_validate(body)
        except PydanticValidationError:
            raise CrawlForgeError(
                response.status_code,
                "UNEXPECTED_RESPONSE",
                f"HTTP {response.status_code} without a ToolInfo body",
                body,
                request_id_from(response.headers),
            ) from None

    @staticmethod
    def _network_error(exc: httpx.TransportError) -> CrawlForgeError:
        return CrawlForgeError(0, "NETWORK_ERROR", f"{type(exc).__name__}: {exc}")


class CrawlForge(_Core, SyncToolsMixin):
    """Synchronous client for the CrawlForge REST API.

    ``api_key`` falls back to the CRAWLFORGE_API_KEY environment variable.
    ``http_client`` injects an ``httpx.Client`` (its transport is used as is;
    headers, URLs and timeouts come from this client). Only a 429 is retried:
    ``max_retries`` counts retries, so 2 means up to three requests.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        timeout: float = DEFAULT_TIMEOUT,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        super().__init__(api_key, base_url, max_retries, timeout)
        self._http = http_client if http_client is not None else httpx.Client()
        self._owns_http = http_client is None

    def close(self) -> None:
        if self._owns_http:
            self._http.close()

    def __enter__(self) -> CrawlForge:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def _send(
        self, method: str, url: str, body: Optional[Dict[str, Any]], *, auth: bool
    ) -> httpx.Response:
        attempt = 0
        while True:
            try:
                response = self._http.request(
                    method,
                    url,
                    json=body,
                    headers=self._headers(auth=auth, body=body is not None),
                    timeout=self.timeout,
                )
            except httpx.TransportError as exc:
                raise self._network_error(exc) from exc
            if response.status_code == 429 and attempt < self.max_retries:
                _sleep(retry_wait(parse_retry_after(response.headers), attempt))
                attempt += 1
                continue
            return response

    def _run_tool(self, tool: str, request: Any, params: Dict[str, Any]) -> ToolResult:
        body = self._body(tool, request, params)
        return self._result(self._send("POST", self._url(tool), body, auth=True))

    def call(self, tool: str, params: Mapping[str, Any]) -> ToolResult:
        """Run any tool by name with a raw body. Nothing is validated locally."""
        return self._result(self._send("POST", self._url(tool), dict(params), auth=True))

    def describe(self, tool: str) -> ToolInfo:
        """The tool's self-description (GET, no API key sent)."""
        return self._info(self._send("GET", self._url(tool), None, auth=False))


class AsyncCrawlForge(_Core, AsyncToolsMixin):
    """Asynchronous client for the CrawlForge REST API; same options as ``CrawlForge``."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_retries: int = DEFAULT_MAX_RETRIES,
        timeout: float = DEFAULT_TIMEOUT,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        super().__init__(api_key, base_url, max_retries, timeout)
        self._http = http_client if http_client is not None else httpx.AsyncClient()
        self._owns_http = http_client is None

    async def aclose(self) -> None:
        if self._owns_http:
            await self._http.aclose()

    async def __aenter__(self) -> AsyncCrawlForge:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()

    async def _send(
        self, method: str, url: str, body: Optional[Dict[str, Any]], *, auth: bool
    ) -> httpx.Response:
        attempt = 0
        while True:
            try:
                response = await self._http.request(
                    method,
                    url,
                    json=body,
                    headers=self._headers(auth=auth, body=body is not None),
                    timeout=self.timeout,
                )
            except httpx.TransportError as exc:
                raise self._network_error(exc) from exc
            if response.status_code == 429 and attempt < self.max_retries:
                await _async_sleep(retry_wait(parse_retry_after(response.headers), attempt))
                attempt += 1
                continue
            return response

    async def _run_tool(self, tool: str, request: Any, params: Dict[str, Any]) -> ToolResult:
        body = self._body(tool, request, params)
        return self._result(await self._send("POST", self._url(tool), body, auth=True))

    async def call(self, tool: str, params: Mapping[str, Any]) -> ToolResult:
        """Run any tool by name with a raw body. Nothing is validated locally."""
        return self._result(await self._send("POST", self._url(tool), dict(params), auth=True))

    async def describe(self, tool: str) -> ToolInfo:
        """The tool's self-description (GET, no API key sent)."""
        return self._info(await self._send("GET", self._url(tool), None, auth=False))


__all__ = ["CrawlForge", "AsyncCrawlForge", "BaseModel", "retry_wait"]
