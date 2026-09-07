# Changelog

## 0.1.1 (2026-09-07)

- Models regenerated from the corrected OpenAPI specification. The object form
  of `redact_pii` on `stealth_mode` and `scrape_with_actions` is now a typed
  model (`entities`, `replace_style`, `mode`) instead of a free dict, an
  action's `position` is `{x, y}`, and `extractionOptions.selectors` is
  `Dict[str, str]`. A dict is still accepted wherever a model is; an unknown
  key inside one of these objects is now rejected locally, before any request,
  as it already was for every other request model.

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
