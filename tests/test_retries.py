"""The retry policy: 429 only, Retry-After honoured and capped, jittered backoff, give up."""

from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from typing import List

import httpx
import pytest

from crawlforge import RateLimitError, ToolError
from crawlforge._client import retry_wait

from .conftest import FixtureServer, load_fixture

RATE_LIMITED = load_fixture("error_429")["response"]["body"]


def limited(**headers: str) -> httpx.Response:
    return httpx.Response(429, json=RATE_LIMITED, headers=headers)


def test_retry_after_seconds_then_success(sleeps: List[float]) -> None:
    server = FixtureServer("error_429", "fetch_url")
    with server.sync_client() as client:
        result = client.fetch_url(url="https://example.com")
    assert result.credits_used == 1
    assert len(server.requests) == 2
    assert sleeps == [2.0]


async def test_retry_after_seconds_then_success_async(sleeps: List[float]) -> None:
    server = FixtureServer("error_429", "fetch_url")
    async with server.async_client() as client:
        result = await client.fetch_url(url="https://example.com")
    assert result.credits_used == 1
    assert len(server.requests) == 2
    assert sleeps == [2.0]


def test_retry_after_http_date(sleeps: List[float]) -> None:
    when = datetime.now(timezone.utc) + timedelta(seconds=30)
    server = FixtureServer(
        limited(**{"Retry-After": format_datetime(when, usegmt=True)}), "fetch_url"
    )
    with server.sync_client() as client:
        client.fetch_url(url="https://example.com")
    assert len(sleeps) == 1
    assert 25.0 <= sleeps[0] <= 30.0


def test_retry_after_is_capped_at_60_seconds(sleeps: List[float]) -> None:
    far = datetime.now(timezone.utc) + timedelta(seconds=600)
    server = FixtureServer(
        limited(**{"Retry-After": "3600"}),
        limited(**{"Retry-After": format_datetime(far, usegmt=True)}),
        "fetch_url",
    )
    with server.sync_client() as client:
        client.fetch_url(url="https://example.com")
    assert sleeps == [60.0, 60.0]


def test_past_http_date_waits_zero(sleeps: List[float]) -> None:
    past = datetime.now(timezone.utc) - timedelta(seconds=30)
    server = FixtureServer(
        limited(**{"Retry-After": format_datetime(past, usegmt=True)}), "fetch_url"
    )
    with server.sync_client() as client:
        client.fetch_url(url="https://example.com")
    assert sleeps == [0.0]


def test_missing_or_bad_retry_after_uses_jittered_backoff(sleeps: List[float]) -> None:
    server = FixtureServer("error_429_no_header", limited(**{"Retry-After": "soon"}), "fetch_url")
    with server.sync_client() as client:
        client.fetch_url(url="https://example.com")
    assert len(sleeps) == 2
    assert 0.8 <= sleeps[0] <= 1.2
    assert 1.6 <= sleeps[1] <= 2.4


def test_gives_up_after_max_retries(sleeps: List[float]) -> None:
    server = FixtureServer("error_429", "error_429", "error_429", "error_429")
    with server.sync_client(max_retries=2) as client:
        with pytest.raises(RateLimitError) as info:
            client.fetch_url(url="https://example.com")
    assert len(server.requests) == 3  # 1 attempt + 2 retries
    assert sleeps == [2.0, 2.0]
    assert info.value.retry_after == 2.0
    assert len(server.replies) == 1  # the fourth reply was never requested


async def test_gives_up_after_max_retries_async(sleeps: List[float]) -> None:
    server = FixtureServer("error_429", "error_429", "error_429")
    async with server.async_client(max_retries=2) as client:
        with pytest.raises(RateLimitError):
            await client.fetch_url(url="https://example.com")
    assert len(server.requests) == 3


def test_zero_retries_means_one_request(sleeps: List[float]) -> None:
    server = FixtureServer("error_429", "fetch_url")
    with server.sync_client(max_retries=0) as client:
        with pytest.raises(RateLimitError):
            client.fetch_url(url="https://example.com")
    assert len(server.requests) == 1
    assert sleeps == []


def test_with_options_max_retries_applies_per_call(sleeps: List[float]) -> None:
    server = FixtureServer("error_429", "error_429", "error_429", "error_429", "error_429")
    with server.sync_client(max_retries=0) as client:
        with pytest.raises(RateLimitError):
            client.with_options(max_retries=4).fetch_url(url="https://example.com")
    assert len(server.requests) == 5


@pytest.mark.parametrize("fixture", ["error_500", "error_502_blocked", "error_502_html"])
def test_never_retries_a_5xx(fixture: str, sleeps: List[float]) -> None:
    server = FixtureServer(fixture, "fetch_url")
    with server.sync_client() as client:
        with pytest.raises(Exception) as info:
            client.fetch_url(url="https://example.com")
    assert not isinstance(info.value, RateLimitError)
    assert len(server.requests) == 1
    assert sleeps == []


def test_describe_is_retried_on_429_too(sleeps: List[float]) -> None:
    server = FixtureServer("error_429", "describe_fetch_url")
    with server.sync_client() as client:
        info = server and client.describe("fetch_url")
    assert info.tool == "fetch_url"
    assert sleeps == [2.0]


def test_retry_wait_policy() -> None:
    assert retry_wait(2.0, 0) == 2.0
    assert retry_wait(3600.0, 0) == 60.0
    for attempt, (low, high) in enumerate([(0.8, 1.2), (1.6, 2.4), (3.2, 4.8), (6.4, 9.6)]):
        for _ in range(50):
            assert low <= retry_wait(None, attempt) <= high
    assert retry_wait(None, 10) == 60.0


def test_a_5xx_error_class_is_tool_error() -> None:
    with FixtureServer("error_500").sync_client() as client:
        with pytest.raises(ToolError):
            client.fetch_url(url="https://example.com")
