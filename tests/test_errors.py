"""Every error class, the two non-API failure modes, and G4 (the key never appears)."""

import httpx
import pytest

from crawlforge import (
    AuthenticationError,
    CrawlForgeError,
    InsufficientCreditsError,
    RateLimitError,
    ToolError,
    ValidationError,
)

from .conftest import API_KEY, FixtureServer, load_fixture

ERROR_CASES = [
    ("error_400", ValidationError, 400, "VALIDATION_ERROR"),
    ("error_401", AuthenticationError, 401, "INVALID_API_KEY"),
    ("error_402", InsufficientCreditsError, 402, "INSUFFICIENT_CREDITS"),
    ("error_402_no_recharge", InsufficientCreditsError, 402, "SPEND_CAP_REACHED"),
    ("error_429", RateLimitError, 429, "RATE_LIMIT_EXCEEDED"),
    ("error_429_host_backoff", RateLimitError, 429, "HOST_BACKOFF"),
    ("error_502_blocked", ToolError, 502, "BLOCKED"),
    ("error_500", ToolError, 500, "INTERNAL_ERROR"),
]


@pytest.mark.parametrize("fixture,cls,status,code", ERROR_CASES)
def test_error_class_by_status_sync(fixture: str, cls: type, status: int, code: str) -> None:
    server = FixtureServer(fixture)
    with server.sync_client(max_retries=0) as client:
        with pytest.raises(cls) as info:
            client.fetch_url(url="https://example.com")
    error = info.value
    assert type(error) is cls
    assert error.status == status
    assert error.code == code
    assert error.message == load_fixture(fixture)["response"]["body"]["error"]["message"]
    assert str(error).startswith(f"[{status}] {code}: ")
    assert API_KEY not in str(error) and API_KEY not in repr(error)


@pytest.mark.parametrize("fixture,cls,status,code", ERROR_CASES)
async def test_error_class_by_status_async(fixture: str, cls: type, status: int, code: str) -> None:
    server = FixtureServer(fixture)
    async with server.async_client(max_retries=0) as client:
        with pytest.raises(cls) as info:
            await client.fetch_url(url="https://example.com")
    assert type(info.value) is cls
    assert info.value.status == status
    assert info.value.code == code


def test_validation_error_carries_the_issue_list() -> None:
    server = FixtureServer("error_400")
    with server.sync_client() as client:
        with pytest.raises(ValidationError) as info:
            client.fetch_url(url="https://example.com")
    assert info.value.details == [{"field": "url", "message": "Required", "code": "invalid_type"}]


def test_insufficient_credits_reads_the_recharge_header() -> None:
    with FixtureServer("error_402").sync_client() as client:
        with pytest.raises(InsufficientCreditsError) as triggered:
            client.scrape(url="https://example.com")
    assert triggered.value.auto_recharge_triggered is True
    assert triggered.value.details["required"] == 2

    with FixtureServer("error_402_no_recharge").sync_client() as client:
        with pytest.raises(InsufficientCreditsError) as not_triggered:
            client.scrape(url="https://example.com")
    assert not_triggered.value.auto_recharge_triggered is False

    body = load_fixture("error_402")["response"]["body"]
    with FixtureServer(httpx.Response(402, json=body)).sync_client() as client:
        with pytest.raises(InsufficientCreditsError) as no_header:
            client.scrape(url="https://example.com")
    assert no_header.value.auto_recharge_triggered is False


def test_rate_limit_error_parses_retry_after() -> None:
    with FixtureServer("error_429").sync_client(max_retries=0) as client:
        with pytest.raises(RateLimitError) as info:
            client.fetch_url(url="https://example.com")
    assert info.value.retry_after == 2.0
    assert info.value.details == {"plan": "free", "limit": 1}

    with FixtureServer("error_429_no_header").sync_client(max_retries=0) as client:
        with pytest.raises(RateLimitError) as absent:
            client.fetch_url(url="https://example.com")
    assert absent.value.retry_after is None


def test_tool_error_carries_blocked_and_escalated() -> None:
    with FixtureServer("error_502_blocked").sync_client() as client:
        with pytest.raises(ToolError) as info:
            client.scrape(url="https://example.com", escalate=True)
    assert info.value.blocked == {"vendor": "cloudflare", "evidence": "cf-mitigated: challenge"}
    assert info.value.escalated is True

    with FixtureServer("error_500").sync_client() as client:
        with pytest.raises(ToolError) as plain:
            client.fetch_url(url="https://example.com")
    assert plain.value.blocked is None
    assert plain.value.escalated is False


def test_success_false_is_an_error_whatever_the_status() -> None:
    body = load_fixture("error_502_blocked")["response"]["body"]
    with FixtureServer(httpx.Response(200, json=body)).sync_client() as client:
        with pytest.raises(ToolError) as info:
            client.scrape(url="https://example.com")
    assert info.value.code == "BLOCKED"
    assert info.value.status == 200


def test_non_json_body_is_unexpected_response() -> None:
    with FixtureServer("error_502_html").sync_client() as client:
        with pytest.raises(CrawlForgeError) as info:
            client.fetch_url(url="https://example.com")
    error = info.value
    assert type(error) is CrawlForgeError
    assert error.status == 502
    assert error.code == "UNEXPECTED_RESPONSE"
    assert "502 Bad Gateway" in str(error.details)


def test_json_without_envelope_is_unexpected_response() -> None:
    with FixtureServer(httpx.Response(200, json={"hello": "world"})).sync_client() as client:
        with pytest.raises(CrawlForgeError) as info:
            client.fetch_url(url="https://example.com")
    assert info.value.code == "UNEXPECTED_RESPONSE"
    assert info.value.status == 200
    assert info.value.details == {"hello": "world"}

    with FixtureServer(httpx.Response(500, json={"oops": True})).sync_client() as client:
        with pytest.raises(CrawlForgeError) as no_error_key:
            client.fetch_url(url="https://example.com")
    assert type(no_error_key.value) is CrawlForgeError
    assert no_error_key.value.code == "UNEXPECTED_RESPONSE"
    assert no_error_key.value.status == 500


def test_transport_error_is_network_error() -> None:
    server = FixtureServer(httpx.ConnectError("connection refused"))
    with server.sync_client() as client:
        with pytest.raises(CrawlForgeError) as info:
            client.fetch_url(url="https://example.com")
    error = info.value
    assert type(error) is CrawlForgeError
    assert error.status == 0
    assert error.code == "NETWORK_ERROR"
    assert "ConnectError" in error.message
    assert isinstance(error.__cause__, httpx.TransportError)
    assert API_KEY not in str(error) and API_KEY not in repr(error)


async def test_transport_error_is_network_error_async() -> None:
    server = FixtureServer(httpx.ReadTimeout("timed out"))
    async with server.async_client() as client:
        with pytest.raises(CrawlForgeError) as info:
            await client.fetch_url(url="https://example.com")
    assert info.value.code == "NETWORK_ERROR"
    assert info.value.status == 0


def test_request_id_comes_from_vercel_or_request_id_header() -> None:
    body = load_fixture("error_500")["response"]["body"]
    server = FixtureServer(
        httpx.Response(500, json=body, headers={"x-vercel-id": "iad1::abc"}),
        httpx.Response(500, json=body, headers={"x-request-id": "req_1"}),
        httpx.Response(500, json=body),
    )
    seen = []
    with server.sync_client() as client:
        for _ in range(3):
            with pytest.raises(ToolError) as info:
                client.fetch_url(url="https://example.com")
            seen.append(info.value.request_id)
    assert seen == ["iad1::abc", "req_1", None]


def test_error_repr_and_str_are_key_free_and_informative() -> None:
    error = RateLimitError(
        429, "RATE_LIMIT_EXCEEDED", "slow down", {"plan": "free"}, "req_1", retry_after=2.0
    )
    assert str(error) == "[429] RATE_LIMIT_EXCEEDED: slow down"
    assert repr(error) == (
        "RateLimitError(status=429, code='RATE_LIMIT_EXCEEDED', message='slow down', "
        "request_id='req_1')"
    )
    assert isinstance(error, CrawlForgeError)
    assert str(CrawlForgeError(0, "NETWORK_ERROR", "boom")) == "NETWORK_ERROR: boom"
