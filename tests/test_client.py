"""Request shape, result mapping, argument handling and the two constructors."""

import json
from typing import Any, Dict

import httpx
import pydantic
import pytest

from crawlforge import TOOLS, AsyncCrawlForge, CrawlForge, CrawlForgeError, ToolInfo, ToolResult
from crawlforge._version import __version__
from crawlforge.models import ExtractStructuredRequest, FetchUrlRequest

from .conftest import API_KEY, BASE_URL, FixtureServer, load_fixture

SUCCESS_TOOLS = [
    "fetch_url",
    "extract_text",
    "extract_links",
    "extract_metadata",
    "search_web",
    "map_site",
    "read_result",
    "scrape_structured",
]


def assert_post_shape(request: httpx.Request, tool: str, body: Dict[str, Any]) -> None:
    assert request.method == "POST"
    assert str(request.url) == f"{BASE_URL}/tools/{tool}"
    assert request.headers["X-API-Key"] == API_KEY
    assert request.headers["Content-Type"] == "application/json"
    assert request.headers["Accept"] == "application/json"
    assert request.headers["User-Agent"] == f"crawlforge-sdk-python/{__version__}"
    assert json.loads(request.content) == body


def test_sync_request_shape() -> None:
    server = FixtureServer("fetch_url")
    fixture = load_fixture("fetch_url")
    with server.sync_client() as client:
        result = client.fetch_url(**fixture["request"])
    assert_post_shape(server.last, "fetch_url", fixture["request"])
    assert isinstance(result, ToolResult)


async def test_async_request_shape() -> None:
    server = FixtureServer("fetch_url")
    fixture = load_fixture("fetch_url")
    async with server.async_client() as client:
        result = await client.fetch_url(**fixture["request"])
    assert_post_shape(server.last, "fetch_url", fixture["request"])
    assert isinstance(result, ToolResult)


@pytest.mark.parametrize("tool", SUCCESS_TOOLS)
def test_tool_result_mapping_sync(tool: str, spec: Dict[str, Any]) -> None:
    fixture = load_fixture(tool)
    body = fixture["response"]["body"]
    server = FixtureServer(tool)
    with server.sync_client() as client:
        result = getattr(client, tool)(**fixture["request"])
    assert_post_shape(server.last, tool, fixture["request"])
    assert result.data == body["data"]
    assert result.credits_used == body["credits_used"]
    assert result.credits_used == spec["paths"][f"/tools/{tool}"]["post"]["x-credits"]
    assert result.credits_remaining == body["credits_remaining"]
    assert result.processing_time == body["processing_time"]
    assert result.warnings == body.get("warnings", [])


@pytest.mark.parametrize("tool", SUCCESS_TOOLS)
async def test_tool_result_mapping_async(tool: str) -> None:
    fixture = load_fixture(tool)
    body = fixture["response"]["body"]
    server = FixtureServer(tool)
    async with server.async_client() as client:
        result = await getattr(client, tool)(**fixture["request"])
    assert_post_shape(server.last, tool, fixture["request"])
    assert result.data == body["data"]
    assert result.credits_used == body["credits_used"]


def test_warnings_are_kept() -> None:
    body = load_fixture("fetch_url")["response"]["body"]
    body = {**body, "warnings": ["robots.txt override recorded"]}
    server = FixtureServer(httpx.Response(200, json=body))
    with server.sync_client() as client:
        result = client.fetch_url(url="https://example.com", respect_robots=False)
    assert result.warnings == ["robots.txt override recorded"]


def test_positional_model_and_dict_send_the_same_body() -> None:
    server = FixtureServer("fetch_url", "fetch_url")
    with server.sync_client() as client:
        client.fetch_url(FetchUrlRequest(url="https://example.com", timeout=15000))
        client.fetch_url({"url": "https://example.com", "timeout": 15000})
    first, second = server.requests
    assert (
        json.loads(first.content)
        == json.loads(second.content)
        == {
            "url": "https://example.com",
            "timeout": 15000,
        }
    )


def test_only_set_fields_are_sent() -> None:
    server = FixtureServer("fetch_url")
    with server.sync_client() as client:
        client.fetch_url(url="https://example.com")
    assert json.loads(server.last.content) == {"url": "https://example.com"}


def test_aliased_field_keeps_its_wire_name() -> None:
    server = FixtureServer("fetch_url", "fetch_url")
    schema = {"type": "object", "properties": {"title": {"type": "string"}}}
    with server.sync_client() as client:
        client.extract_structured(url="https://example.com", schema=schema)
        client.extract_structured(
            ExtractStructuredRequest(url="https://example.com", schema=schema)
        )
    for request in server.requests:
        assert json.loads(request.content) == {"url": "https://example.com", "schema": schema}


def test_nested_objects_accept_dicts() -> None:
    server = FixtureServer("fetch_url")
    with server.sync_client() as client:
        client.scrape(
            url="https://example.com",
            formats=["markdown", {"type": "highlights", "query": "pricing"}],
            redact_pii={"mode": "fast"},
        )
    assert json.loads(server.last.content) == {
        "url": "https://example.com",
        "formats": ["markdown", {"type": "highlights", "query": "pricing"}],
        "redact_pii": {"mode": "fast"},
    }


def test_model_and_kwargs_together_is_an_error() -> None:
    server = FixtureServer()
    with server.sync_client() as client:
        with pytest.raises(TypeError):
            client.fetch_url(FetchUrlRequest(url="https://example.com"), timeout=1000)
    assert server.requests == []


def test_wrong_model_type_is_an_error() -> None:
    server = FixtureServer()
    with server.sync_client() as client:
        with pytest.raises(TypeError):
            client.scrape(FetchUrlRequest(url="https://example.com"))  # type: ignore[arg-type]
    assert server.requests == []


def test_misspelled_keyword_fails_before_any_request() -> None:
    """The explicit signature rejects an unknown keyword; a dict goes through pydantic."""
    server = FixtureServer()
    with server.sync_client() as client:
        with pytest.raises(TypeError) as info:
            client.fetch_url(urll="https://example.com")  # type: ignore[call-arg]
        assert "urll" in str(info.value)
        with pytest.raises(pydantic.ValidationError) as dict_info:
            client.fetch_url({"url": "https://example.com", "urll": "x"})
        assert "urll" in str(dict_info.value)
    assert server.requests == []


def test_wrong_type_fails_before_any_request() -> None:
    server = FixtureServer()
    with server.sync_client() as client:
        with pytest.raises(pydantic.ValidationError):
            client.fetch_url(url="https://example.com", timeout="soon")  # type: ignore[arg-type]
        with pytest.raises(pydantic.ValidationError):
            client.fetch_url(url="https://example.com", timeout=1)  # below the spec minimum
    assert server.requests == []


async def test_misspelled_keyword_fails_before_any_request_async() -> None:
    server = FixtureServer()
    async with server.async_client() as client:
        with pytest.raises(TypeError):
            await client.fetch_url(urll="https://example.com")  # type: ignore[call-arg]
        with pytest.raises(pydantic.ValidationError):
            await client.fetch_url({"url": "https://example.com", "urll": "x"})
    assert server.requests == []


def test_call_sends_the_raw_body() -> None:
    server = FixtureServer("fetch_url")
    with server.sync_client() as client:
        result = client.call("fetch_url", {"url": "https://example.com", "undocumented": 1})
    assert_post_shape(server.last, "fetch_url", {"url": "https://example.com", "undocumented": 1})
    assert result.credits_used == 1


async def test_call_async() -> None:
    server = FixtureServer("fetch_url")
    async with server.async_client() as client:
        result = await client.call("fetch_url", {"url": "https://example.com"})
    assert result.credits_used == 1


def test_describe_sends_no_key() -> None:
    server = FixtureServer("describe_fetch_url")
    with server.sync_client() as client:
        info = client.describe("fetch_url")
    request = server.last
    assert request.method == "GET"
    assert str(request.url) == f"{BASE_URL}/tools/fetch_url"
    assert "X-API-Key" not in request.headers
    assert "x-api-key" not in {k.lower() for k in request.headers}
    assert request.headers["Accept"] == "application/json"
    assert isinstance(info, ToolInfo)
    assert info.tool == "fetch_url"
    assert info.credits_cost == TOOLS["fetch_url"].credits
    assert info.parameters["required"] == ["url"]


async def test_describe_async_sends_no_key() -> None:
    server = FixtureServer("describe_fetch_url")
    async with server.async_client() as client:
        info = await client.describe("fetch_url")
    assert "X-API-Key" not in server.last.headers
    assert info.example == {
        "url": "https://example.com",
        "headers": {"Accept": "text/html"},
        "timeout": 15000,
        "follow_redirects": True,
    }


def test_invalid_tool_name_is_rejected_locally() -> None:
    server = FixtureServer()
    with server.sync_client() as client:
        with pytest.raises(ValueError):
            client.call("../admin", {})
        with pytest.raises(ValueError):
            client.describe("Fetch URL")
    assert server.requests == []


def test_missing_key_raises_at_construction(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CRAWLFORGE_API_KEY", raising=False)
    with pytest.raises(CrawlForgeError) as info:
        CrawlForge()
    assert info.value.code == "MISSING_API_KEY"
    assert info.value.status == 0
    with pytest.raises(CrawlForgeError):
        AsyncCrawlForge()
    with pytest.raises(CrawlForgeError):
        CrawlForge(api_key="")


def test_key_falls_back_to_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CRAWLFORGE_API_KEY", API_KEY)
    server = FixtureServer("fetch_url")
    client = CrawlForge(http_client=httpx.Client(transport=httpx.MockTransport(server.handler)))
    client.fetch_url(url="https://example.com")
    assert server.last.headers["X-API-Key"] == API_KEY


def test_client_repr_never_shows_the_key() -> None:
    client = CrawlForge(api_key=API_KEY)
    try:
        assert API_KEY not in repr(client)
        assert API_KEY not in str(client)
        assert API_KEY not in repr(vars(client).keys())
    finally:
        client.close()


def test_defaults_and_base_url() -> None:
    client = CrawlForge(api_key=API_KEY)
    try:
        assert client.base_url == BASE_URL
        assert client.max_retries == 2
        assert client.timeout == 60.0
    finally:
        client.close()
    server = FixtureServer("fetch_url")
    with server.sync_client(base_url="http://localhost:3000/api/v1/") as client:
        client.fetch_url(url="https://example.com")
    assert str(server.last.url) == "http://localhost:3000/api/v1/tools/fetch_url"


def test_with_options_overrides_per_call_and_shares_the_pool() -> None:
    server = FixtureServer("fetch_url", "fetch_url")
    with server.sync_client() as client:
        fast = client.with_options(timeout=5.0, max_retries=0)
        assert fast.timeout == 5.0 and fast.max_retries == 0
        assert client.timeout == 60.0 and client.max_retries == 2
        fast.fetch_url(url="https://example.com")
        fast.close()  # does not close the shared pool
        client.fetch_url(url="https://example.com")
    assert len(server.requests) == 2
    assert server.requests[0].extensions["timeout"]["read"] == 5.0
    assert server.requests[1].extensions["timeout"]["read"] == 60.0


def test_injected_http_client_is_not_closed_by_the_sdk() -> None:
    http = httpx.Client(transport=httpx.MockTransport(FixtureServer("fetch_url").handler))
    with CrawlForge(api_key=API_KEY, http_client=http) as client:
        client.fetch_url(url="https://example.com")
    assert not http.is_closed
    http.close()


def test_owned_http_client_is_closed() -> None:
    client = CrawlForge(api_key=API_KEY)
    client.close()
    assert client._http.is_closed


async def test_owned_async_http_client_is_closed() -> None:
    client = AsyncCrawlForge(api_key=API_KEY)
    await client.aclose()
    assert client._http.is_closed
