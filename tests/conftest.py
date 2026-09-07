"""A fixture server on httpx.MockTransport: no sockets, no respx.

Replies are scripted per test: a fixture name (tests/fixtures/<name>.json), a
ready httpx.Response, or an exception to raise from the transport. Every
request is recorded for assertions.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Union

import httpx
import pytest

from crawlforge import AsyncCrawlForge, CrawlForge

FIXTURES = Path(__file__).parent / "fixtures"
SPEC_PATH = Path(__file__).parent.parent / "openapi.json"
API_KEY = "cf_test_0123456789abcdef_do_not_print"
BASE_URL = "https://www.crawlforge.dev/api/v1"

Reply = Union[str, httpx.Response, Exception]


def load_fixture(name: str) -> Dict[str, Any]:
    return json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))


def fixture_response(fixture: Dict[str, Any]) -> httpx.Response:
    reply = fixture["response"]
    headers = reply.get("headers", {})
    if "text" in reply:
        return httpx.Response(reply["status"], headers=headers, text=reply["text"])
    return httpx.Response(reply["status"], headers=headers, json=reply["body"])


class FixtureServer:
    def __init__(self, *replies: Reply) -> None:
        self.replies: List[Reply] = list(replies)
        self.requests: List[httpx.Request] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if not self.replies:
            raise AssertionError(f"unexpected request {request.method} {request.url}")
        reply = self.replies.pop(0)
        if isinstance(reply, str):
            reply = fixture_response(load_fixture(reply))
        if isinstance(reply, Exception):
            raise reply
        return reply

    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]

    def sync_client(self, **options: Any) -> CrawlForge:
        transport = httpx.MockTransport(self.handler)
        return CrawlForge(api_key=API_KEY, http_client=httpx.Client(transport=transport), **options)

    def async_client(self, **options: Any) -> AsyncCrawlForge:
        transport = httpx.MockTransport(self.handler)
        return AsyncCrawlForge(
            api_key=API_KEY, http_client=httpx.AsyncClient(transport=transport), **options
        )


@pytest.fixture
def spec() -> Dict[str, Any]:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def sleeps(monkeypatch: pytest.MonkeyPatch) -> List[float]:
    """Replace both waits with recorders so retry tests take no wall-clock time."""
    recorded: List[float] = []

    def fake_sleep(seconds: float) -> None:
        recorded.append(seconds)

    async def fake_async_sleep(seconds: float) -> None:
        recorded.append(seconds)

    monkeypatch.setattr("crawlforge._client._sleep", fake_sleep)
    monkeypatch.setattr("crawlforge._client._async_sleep", fake_async_sleep)
    return recorded
