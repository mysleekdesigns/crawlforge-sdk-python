# CrawlForge Python SDK

The official Python client for the [CrawlForge REST API](https://www.crawlforge.dev/docs/api-reference):
30 metered web tools (scrape, search, crawl, extract, research) behind one API key.

- Sync `CrawlForge` and async `AsyncCrawlForge` clients on `httpx`
- One typed method per tool, generated from the API's [OpenAPI spec](https://www.crawlforge.dev/openapi.json)
- Arguments validated locally by pydantic v2 before any request is sent
- Retries on rate limits only, honouring `Retry-After`
- Python 3.9+, fully typed (`py.typed`), runtime dependencies `httpx` and `pydantic` only

## Install

```bash
pip install crawlforge
```

Create an API key at https://www.crawlforge.dev/dashboard/keys and export it as
`CRAWLFORGE_API_KEY`, or pass `api_key=` to the client.

## Quick start

```python
from crawlforge import CrawlForge

with CrawlForge() as client:  # reads CRAWLFORGE_API_KEY
    result = client.scrape(url="https://example.com", formats=["markdown", "links"])

print(result.data["formats"]["markdown"][:200])
print(result.credits_used, result.credits_remaining)
```

Async:

```python
import asyncio
from crawlforge import AsyncCrawlForge

async def main() -> None:
    async with AsyncCrawlForge() as client:
        result = await client.search_web(query="web scraping", limit=5)
        for hit in result.data["results"]:
            print(hit["title"], hit["url"])

asyncio.run(main())
```

Every tool method returns a `ToolResult`:

| Field | Meaning |
|---|---|
| `data` | The tool's result. **Tool-specific and untyped (`dict`) in this release**; its shape is documented on the tool's docs page. |
| `credits_used` | Credits charged for this call. |
| `credits_remaining` | Your balance after the call. |
| `processing_time` | Server-side processing time in milliseconds. |
| `warnings` | Non-fatal notes, `[]` when there are none. |

## Calling a tool

Each tool is a method named exactly like the tool. Pass keyword arguments, a
dict, or the tool's request model; all three send the same body, and only the
fields you set are sent.

```python
from crawlforge.models import FetchUrlRequest

client.fetch_url(url="https://example.com", timeout=15000)
client.fetch_url({"url": "https://example.com", "timeout": 15000})
client.fetch_url(FetchUrlRequest(url="https://example.com", timeout=15000))
```

Keyword names are the API's wire names, camelCase included (`onlyMainContent`,
`maxUrls`). Nested objects can be passed as dicts. A misspelled keyword is a
`TypeError` from the method signature; a wrong type, a value outside the spec's
range, or an unknown key in a dict is a `pydantic.ValidationError`. Either way
nothing is sent and nothing is charged.

Two escape hatches:

- `client.call(tool, params)` posts a raw body to any tool without local
  validation, for a parameter the spec does not list or a tool newer than this
  SDK.
- `client.describe(tool)` fetches the tool's self-description (`ToolInfo`: price,
  JSON Schema, example) with no API key.

### Per-call timeout and retries

`with_options()` returns a copy of the client sharing the same connection pool:

```python
client.with_options(timeout=10.0, max_retries=0).fetch_url(url="https://example.com")
```

The tool parameter `timeout` (milliseconds, on `fetch_url` and ten other tools)
is unrelated to the HTTP timeout, which is why the HTTP one is not a keyword on
the tool methods.

## Tools and credits

Prices are the `x-credits` of each operation in the spec. An error response,
whatever its status, charges nothing: credits are deducted only after a tool
succeeded.

<!-- generated:tools:start -->
| Method | Credits | Note | Docs |
|---|---|---|---|
| `agent` | 8 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/agent) |
| `analyze_content` | 3 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/analyze-content) |
| `batch_scrape` | 5 | 5 per URL attempted (skipped URLs are not charged) | [docs](https://www.crawlforge.dev/docs/api-reference/tools/batch-scrape) |
| `crawl_deep` | 4 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/crawl-deep) |
| `deep_research` | 10 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/deep-research) |
| `extract_content` | 2 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/extract-content) |
| `extract_embedded_state` | 2 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/extract-embedded-state) |
| `extract_links` | 1 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/extract-links) |
| `extract_metadata` | 1 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/extract-metadata) |
| `extract_structured` | 3 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/extract-structured) |
| `extract_text` | 1 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/extract-text) |
| `extract_with_llm` | 3 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/extract-with-llm) |
| `fetch_url` | 1 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/fetch-url) |
| `generate_llms_txt` | 5 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/generate-llms-txt) |
| `get_batch_results` | 1 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/get-batch-results) |
| `list_ollama_models` | 1 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/list-ollama-models) |
| `localization` | 2 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/localization) |
| `map_site` | 2 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/map-site) |
| `process_document` | 2 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/process-document) |
| `read_result` | 1 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/read-result) |
| `reddit_search` | 5 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/reddit-search) |
| `scrape` | 2 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/scrape) |
| `scrape_structured` | 2 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/scrape-structured) |
| `scrape_template` | 1 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/scrape-template) |
| `scrape_with_actions` | 5 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/scrape-with-actions) |
| `search_web` | 5 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/search-web) |
| `serp_rank` | 5 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/serp-rank) |
| `stealth_mode` | 5 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/stealth-mode) |
| `summarize_content` | 4 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/summarize-content) |
| `track_changes` | 3 |  | [docs](https://www.crawlforge.dev/docs/api-reference/tools/track-changes) |
<!-- generated:tools:end -->

## Errors

All errors derive from `crawlforge.CrawlForgeError`, with `status`, `code`,
`message`, `details` and `request_id`. The class follows the HTTP status:

| Status | Class | Extra attributes |
|---|---|---|
| 400 | `ValidationError` | `details` is the list of validation issues |
| 401 | `AuthenticationError` | |
| 402 | `InsufficientCreditsError` | `auto_recharge_triggered` (from the `X-Auto-Recharge-Triggered` header) |
| 429 | `RateLimitError` | `retry_after` in seconds, `None` when absent; `code` is `RATE_LIMIT_EXCEEDED` or `HOST_BACKOFF` |
| other | `ToolError` | `blocked` (vendor and evidence when a bot wall was met) and `escalated` |

A response that is not JSON is a `CrawlForgeError` with code
`UNEXPECTED_RESPONSE` and the raw text in `details`; a connection or timeout
failure is code `NETWORK_ERROR` with `status` 0. No error message ever contains
your API key.

```python
from crawlforge import CrawlForge, InsufficientCreditsError, RateLimitError, ToolError

try:
    result = client.scrape(url="https://example.com", escalate=True)
except RateLimitError as e:
    print("slow down", e.retry_after)
except InsufficientCreditsError as e:
    print("top up", e.auto_recharge_triggered)
except ToolError as e:
    print(e.code, e.blocked)
```

## Retries

Only a 429 is retried, and only `max_retries` times (default 2, so up to three
requests). The wait is the `Retry-After` header when present (seconds or an HTTP
date, capped at 60 s), otherwise exponential backoff from 1 s with ±20 % jitter.
A 5xx is never retried, because a failed call is not charged but a repeated
one might be. After the last retry the `RateLimitError` is raised.

## Configuration

```python
CrawlForge(
    api_key=None,          # default: CRAWLFORGE_API_KEY
    base_url=None,         # default: https://www.crawlforge.dev/api/v1
    max_retries=2,
    timeout=60.0,          # seconds, per request
    http_client=None,      # your own httpx.Client (AsyncClient for AsyncCrawlForge)
)
```

Passing `http_client` is also the test seam: an `httpx.Client` on an
`httpx.MockTransport` gives a fixture server with no sockets. The SDK stores
nothing: results live only in the `ToolResult` you hold.

## Python 3.9+

The generated models use `Optional[...]`, `List[...]` and `Dict[...]` rather
than `X | Y`, which pydantic cannot evaluate on 3.9. Tested on 3.9 through 3.13.

## Development

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
python scripts/generate.py   # or: make generate
ruff check . && mypy crawlforge scripts && pytest
python -m build
```

`crawlforge/_generated/models.py`, `crawlforge/_generated/tools.py` and the
table above are generated from `openapi.json` by `scripts/generate.py`
(`scripts/gen_models.py` is the generator) and committed; CI regenerates and
fails on any diff. `openapi.json` is copied verbatim from
https://www.crawlforge.dev/openapi.json and never edited by hand.

The generator is in-repo and standard-library only. It replaced
`datamodel-code-generator` 0.76.2, which on this spec has no Python 3.9 target
(it emits `X | None`), splits the nine request schemas with a top-level
`anyOf`/`oneOf`/`allOf` cross-field rule into `RootModel` unions, maps
`format: uri` to `AnyUrl` (which rewrites URLs before they are sent) and
`format: email` to `EmailStr` (an extra dependency). The in-repo generator keeps
wire names, ignores the cross-field rules locally (the server enforces them),
skips `pattern` (the spec's lookaheads are not supported by pydantic's default
regex engine) and forbids unknown keys on request models.

## Links

- API reference: https://www.crawlforge.dev/docs/api-reference
- OpenAPI spec: https://www.crawlforge.dev/openapi.json
- API keys: https://www.crawlforge.dev/dashboard/keys
- Changelog: [CHANGELOG.md](CHANGELOG.md)

MIT licensed.
