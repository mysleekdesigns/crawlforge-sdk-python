# Changelog

## 0.1.0 (2026-09-07)

Initial release.

- `CrawlForge` (sync) and `AsyncCrawlForge` (async) clients on `httpx`.
- One typed method per tool, 30 in all, generated from `openapi.json`; every
  keyword argument is validated locally by a pydantic v2 request model before
  a request is sent.
- `call(tool, params)` for a raw body and `describe(tool)` for a tool's
  self-description.
- Error classes by status: `ValidationError`, `AuthenticationError`,
  `InsufficientCreditsError`, `RateLimitError`, `ToolError`; `NETWORK_ERROR`
  and `UNEXPECTED_RESPONSE` on the base `CrawlForgeError`.
- Retries on 429 only, honouring `Retry-After` (seconds or HTTP date, capped
  at 60 s) with jittered exponential backoff otherwise.
- Python 3.9 to 3.13. Runtime dependencies: `httpx` and `pydantic` only.
