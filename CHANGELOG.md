# Changelog

## 0.2.0 (2026-09-12)

- New `browser_session()` method on both clients — an interactive browser
  session held across several calls, driven by an `operation` enum
  (`open | snapshot | act | read | screenshot | close | list`). `snapshot`
  returns an accessibility tree whose interactive elements carry stable refs
  (`@e1`, `@e2` …) and a later call can act on those refs, so a multi-step flow
  no longer has to guess CSS selectors up front the way `scrape_with_actions`
  does. Billed per operation: `open` 3 credits, `read` 2, and 1 each for
  `snapshot`, `act`, `screenshot`, `close` and `list`.

  Two limits to know before building on it: a session lives in one backend
  instance's memory and does not survive a redeploy or restart, and a REST API
  key may hold only **one** session at a time — a second `open` is refused by
  name rather than queued, so call `close` when done instead of waiting for the
  TTL. Persistent login profiles are not available over REST.

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
