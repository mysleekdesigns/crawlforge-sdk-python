# Changelog

## 0.3.0 (2026-10-20)

Request models and the tool table regenerated from the API's current OpenAPI
specification, which had moved on with crawlforge-mcp-server 6.7 through 6.22
while the SDK stayed at the 6.6 spec.

- Added to `extract_embedded_state()`: `keys_only` (the shape of the selected
  state, two levels deep, instead of the data), `find` (every path carrying one
  key name, instead of the data), `raw` (keep the undecoded `__NUXT_DATA__`
  array), and `escalate`, `escalate_engine` and `wait_for` to retry a walled
  page or an empty shell in a stealth browser within the same call (5 extra
  credits only when the stealth render actually runs). `keys_only` and `find`
  are exclusive; the API refuses both together.
- Added to `extract_links()` and `extract_text()`: `escalate` and
  `escalate_engine`, the same in-call stealth retry. `extract_links()` also
  takes `filter_external` (the MCP tool's name for outbound-only);
  `extract_text()` takes `output_format` (`text` or `markdown`).
- Added to `scrape_with_actions()`: `browserOptions.consent` (`off`, `reject`
  or `accept`, cookie-banner handling after each navigation) and
  `browserOptions.proxyRotation` (your own proxies, Chromium engine only).
- Added to `browser_session()`: `onlyMainContent` for the `read` operation.
- Added `max_inline_chars` to `agent()`, `extract_links()`,
  `extract_metadata()`, `generate_llms_txt()`, `map_site()`,
  `scrape_template()` and `search_web()`: a result larger than this is stored
  for an hour and the response carries a preview and a `result_handle` for
  `read_result()`.
- Changed: `TOOLS["agent"].credits` is 18, the ceiling reserved before a run
  (8 for the run plus 5 for each walled page the agent retries in a stealth
  browser, at most 2 a run); the charge is what ran and is reported as
  `credits_used`. `serp_rank()` default `depth` is 30 (was 100);
  `scrape_with_actions()` default `maxRetries` is 0 (was 1) and a retry
  replays the whole chain. `scrape()` accepts at most one `highlights` and one
  `question` format per call. `search_web()` is backed by Brave Search (was
  Google Custom Search). Docstrings and field descriptions updated throughout.
- Removed: `scrape_with_actions()` `captureScreenshots` (add a
  `{"type": "screenshot"}` action instead) and the `stealth_mode()` operations
  `enable` and `disable`.

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
