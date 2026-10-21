# Generated from openapi.json by scripts/generate.py. Do not edit by hand.

"""Pydantic v2 models for the CrawlForge REST API request bodies and ToolInfo."""


from typing import Any, Dict, List, Literal, Optional, Union, cast

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "ToolInfo",
    "AgentRequest",
    "AnalyzeContentRequest",
    "BatchScrapeRequestUrlsItemCustomConfig",
    "BatchScrapeRequestUrlsItem",
    "BatchScrapeRequestBatchConfig",
    "BatchScrapeRequestExtractionTemplateFieldsItem",
    "BatchScrapeRequestExtractionTemplate",
    "BatchScrapeRequestOutputConfig",
    "BatchScrapeRequestOptions",
    "BatchScrapeRequestRedactPii",
    "BatchScrapeRequest",
    "BrowserSessionRequestViewport",
    "BrowserSessionRequestActionsItem",
    "BrowserSessionRequestRedactPii",
    "BrowserSessionRequest",
    "CrawlDeepRequestRedactPii",
    "CrawlDeepRequest",
    "DeepResearchRequestResearchScope",
    "DeepResearchRequest",
    "ExtractContentRequestRedactPii",
    "ExtractContentRequest",
    "ExtractEmbeddedStateRequest",
    "ExtractLinksRequest",
    "ExtractMetadataRequest",
    "ExtractStructuredRequestSchema",
    "ExtractStructuredRequestLlmConfig",
    "ExtractStructuredRequest",
    "ExtractTextRequestRedactPii",
    "ExtractTextRequest",
    "ExtractWithLlmRequest",
    "FetchUrlRequest",
    "GenerateLlmsTxtRequestAnalysisOptions",
    "GenerateLlmsTxtRequestOutputOptions",
    "GenerateLlmsTxtRequest",
    "GetBatchResultsRequest",
    "ListOllamaModelsRequest",
    "LocalizationRequest",
    "MapSiteRequest",
    "ProcessDocumentRequestRedactPii",
    "ProcessDocumentRequest",
    "ReadResultRequest",
    "RedditSearchRequest",
    "ScrapeRequestFormatsItemHighlights",
    "ScrapeRequestFormatsItemQuestion",
    "ScrapeRequestRedactPii",
    "ScrapeRequest",
    "ScrapeStructuredRequest",
    "ScrapeTemplateRequest",
    "ScrapeWithActionsRequestActionsItemPosition",
    "ScrapeWithActionsRequestActionsItem",
    "ScrapeWithActionsRequestFormAutoFill",
    "ScrapeWithActionsRequestBrowserOptionsProxyRotation",
    "ScrapeWithActionsRequestBrowserOptions",
    "ScrapeWithActionsRequestExtractionOptions",
    "ScrapeWithActionsRequestRedactPii",
    "ScrapeWithActionsRequest",
    "SearchWebRequestRedactPii",
    "SearchWebRequest",
    "SerpRankRequest",
    "StealthModeRequestStealthConfig",
    "StealthModeRequestRedactPii",
    "StealthModeRequest",
    "SummarizeContentRequest",
    "TrackChangesRequest",
]


class _RequestModel(BaseModel):
    """A request body. Unknown keys are rejected: a misspelled argument fails locally."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class _ResponseModel(BaseModel):
    """A response body. Unknown keys are kept so a newer server still parses."""

    model_config = ConfigDict(extra="allow")


class ToolInfo(_ResponseModel):
    """A tool's self-description, as its GET returns it and as this document was generated from it."""
    tool: str = Field(description="The tool name, as in the path.")
    description: str = Field()
    credits_cost: float = Field(description="The base price in credits. A per-unit or conditional price is explained in credits_note.")
    credits_note: Optional[str] = Field(default=None)
    parameters: Dict[str, Any] = Field(description="JSON Schema (draft 2020-12) for the POST request body.")
    example: Dict[str, Any] = Field(description="A request body that runs.")
    extra: Optional[Dict[str, Any]] = Field(default=None, description="Tool-specific notes, such as a price table by operation or an execution model.")


class AgentRequest(_RequestModel):
    prompt: str = Field(description="Natural-language task or question (1-2000 chars)")
    urls: Optional[List[Any]] = Field(default=None, description="Optional seed URLs to include (max 20)")
    schema_: Optional[Dict[str, Any]] = Field(default=None, alias="schema", description="Optional JSON schema for structured output")
    model: Optional[Literal["default", "pro"]] = Field(default="default", description="\"default\" = built-in planning loop. \"pro\" requires interactive confirmation and is rejected by the REST API \u2014 use the CrawlForge MCP server for pro runs.")
    maxSteps: Optional[float] = Field(default=5, description="Max fetch iterations (hard cap: 10)")
    maxUrls: Optional[float] = Field(default=10, description="Max URLs to fetch (hard cap: 20)")
    max_inline_chars: Optional[float] = Field(default=40000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")


class AnalyzeContentRequest(_RequestModel):
    url: Optional[str] = Field(default=None, description="URL to fetch and analyze content from")
    content: Optional[str] = Field(default=None, description="Direct content to analyze (if URL not provided)")
    analyze_sentiment: Optional[bool] = Field(default=False, description="Perform sentiment analysis")
    extract_keywords: Optional[bool] = Field(default=True, description="Extract top keywords")
    detect_language: Optional[bool] = Field(default=True, description="Detect content language. Returns an ISO 639-1 code, or \"und\" when the text is too short or the language is not recognised.")
    analyze_readability: Optional[bool] = Field(default=False, description="Calculate readability scores")
    timeout: Optional[float] = Field(default=10000, ge=1000, le=30000, description="Request timeout in milliseconds (1000-30000)")
    respect_robots: Optional[bool] = Field(default=True)


class BatchScrapeRequestUrlsItemCustomConfig(_RequestModel):
    headers: Optional[Dict[str, str]] = Field(default=None)
    timeout: Optional[float] = Field(default=None, ge=1000, le=60000)
    selectors: Optional[Dict[str, str]] = Field(default=None)


class BatchScrapeRequestUrlsItem(_RequestModel):
    url: str = Field(description="Target URL")
    id: Optional[str] = Field(default=None, description="Optional identifier (defaults to the array index)")
    priority: Optional[Literal["high", "medium", "low"]] = Field(default=None)
    custom_config: Optional[BatchScrapeRequestUrlsItemCustomConfig] = Field(default=None)


class BatchScrapeRequestBatchConfig(_RequestModel):
    """Batch processing configuration"""
    concurrency: Optional[float] = Field(default=5, ge=1, le=10, description="Max concurrent requests (capped at 8)")
    delay_between_batches: Optional[float] = Field(default=None, ge=0, le=10000)
    retry_failed: Optional[bool] = Field(default=None)
    max_retries: Optional[float] = Field(default=None, ge=0, le=5)
    fail_fast: Optional[bool] = Field(default=None)
    preserve_order: Optional[bool] = Field(default=None)


class BatchScrapeRequestExtractionTemplateFieldsItem(_RequestModel):
    name: str = Field()
    selector: Optional[str] = Field(default=None)
    xpath: Optional[str] = Field(default=None)
    attribute: Optional[str] = Field(default=None)


class BatchScrapeRequestExtractionTemplate(_RequestModel):
    """Optional per-page field extraction"""
    fields: Optional[List[BatchScrapeRequestExtractionTemplateFieldsItem]] = Field(default=None, description="Fields to extract from each page: { name, selector (CSS), attribute? }. Without attribute the element text is returned, one line per block element; xpath is not supported.")
    capture_screenshots: Optional[bool] = Field(default=None)
    extract_links: Optional[bool] = Field(default=None)
    extract_images: Optional[bool] = Field(default=None)


class BatchScrapeRequestOutputConfig(_RequestModel):
    format: Optional[Literal["json", "csv", "xml"]] = Field(default=None)
    include_metadata: Optional[bool] = Field(default=None)
    include_errors: Optional[bool] = Field(default=None)
    flatten_results: Optional[bool] = Field(default=None)


class BatchScrapeRequestOptions(_RequestModel):
    user_agent: Optional[str] = Field(default=None)
    follow_redirects: Optional[bool] = Field(default=None)
    javascript_enabled: Optional[bool] = Field(default=None)
    respect_robots_txt: Optional[bool] = Field(default=None)
    rate_limit_per_domain: Optional[float] = Field(default=None, ge=100, le=5000)


class BatchScrapeRequestRedactPii(_RequestModel):
    entities: Optional[List[str]] = Field(default=None, max_length=16)
    replace_style: Optional[Literal["tag", "mask", "remove"]] = Field(default=None)
    mode: Optional[Literal["fast", "model"]] = Field(default=None)


class BatchScrapeRequest(_RequestModel):
    urls: List[BatchScrapeRequestUrlsItem] = Field(min_length=1, max_length=50, description="Array of URLs to scrape (max 50 per synchronous batch on the hosted REST API)")
    respect_robots: Optional[bool] = Field(default=True, description="Fetch each origin's robots.txt and skip URLs it disallows for CrawlForge. A missing or unreachable robots.txt is treated as no restrictions. A disallowed URL returns status \"skipped\" and is not charged; the rest of the batch runs.")
    batch_config: Optional[BatchScrapeRequestBatchConfig] = Field(default=None, description="Batch processing configuration")
    extraction_template: Optional[BatchScrapeRequestExtractionTemplate] = Field(default=None, description="Optional per-page field extraction")
    output_config: Optional[BatchScrapeRequestOutputConfig] = Field(default=None)
    options: Optional[BatchScrapeRequestOptions] = Field(default=None)
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")
    redact_pii: Optional[Union[bool, BatchScrapeRequestRedactPii]] = Field(default=None, description="Remove personal data from the text this call returns, before it is stored or sent back. true is shorthand for { mode: \"fast\" }: every entity, tagged. As an object: entities (any of EMAIL, PHONE, FINANCIAL, SECRET; omitted or empty means all four, and any other name is a 400 rather than a silent no-op), replace_style (\"tag\" \u2192 <EMAIL>, \"mask\" \u2192 [REDACTED], \"remove\" \u2192 nothing; default \"tag\") and mode (\"fast\", the default, is regex-only and costs no extra credits; \"model\" covers PERSON and LOCATION, needs an LLM and is rejected here \u2014 use the CrawlForge MCP server). The response carries redaction: { entities, count, mode } inside data, saying what was removed. Detection is deliberately conservative: a card number must pass Luhn and an IBAN mod-97, so a false positive cannot silently destroy real page content. URLs, queries and identifiers the response uses to name what was fetched are left intact, and counters derived from the text (content_length, word_count, character_count) describe the text as it was extracted, before redaction.")


class BrowserSessionRequestViewport(_RequestModel):
    """open: viewport size"""
    width: Optional[float] = Field(default=None, description="800-1920")
    height: Optional[float] = Field(default=None, description="600-1080")


class BrowserSessionRequestActionsItem(_RequestModel):
    type: Optional[Literal["wait", "click", "type", "press", "scroll", "screenshot", "executeJavaScript", "select", "hover", "navigate", "snapshot"]] = Field(default=None, description="Action to perform. executeJavaScript is refused in a session on the hosted API \u2014 the script would run in a browser on our servers, not on your machine.")
    selector: Optional[str] = Field(default=None, description="What the action targets: a CSS selector, or a @e ref from the last snapshot")


class BrowserSessionRequestRedactPii(_RequestModel):
    entities: Optional[List[str]] = Field(default=None, max_length=16)
    replace_style: Optional[Literal["tag", "mask", "remove"]] = Field(default=None)
    mode: Optional[Literal["fast", "model"]] = Field(default=None)


class BrowserSessionRequest(_RequestModel):
    operation: Literal["open", "snapshot", "act", "read", "screenshot", "close", "list"] = Field(description="What this call does to the session. Every operation but open and list needs session_id. Priced per operation, not per call: open 3, read 2, snapshot / act / screenshot / close / list 1 each.")
    session_id: Optional[str] = Field(default=None, description="The id operation \"open\" returned. Required by snapshot, act, read, screenshot and close.")
    url: Optional[str] = Field(default=None, description="open: the URL to load the session on")
    stealth: Optional[bool] = Field(default=False, description="open: run the session in the stealth browser instead of the standard pool")
    ttl: Optional[float] = Field(default=None, description="open: seconds the session may live from the moment it opens (30-3600, default 600)")
    activity_ttl: Optional[float] = Field(default=None, description="open: seconds the session may sit idle between calls (10-3600, default 300). The session dies at whichever of the two clocks runs out first.")
    viewport: Optional[BrowserSessionRequestViewport] = Field(default=None, description="open: viewport size")
    timeout: Optional[float] = Field(default=30000, description="Per-action timeout in ms (10000-120000). The REST call itself waits up to ~50s, so a timeout above that cannot be reached here.")
    respect_robots: Optional[bool] = Field(default=True, description="Respect the target site's robots.txt. Omitted, the compliant default (true) applies: a URL disallowed for CrawlForge is refused before the browser opens and no credits are charged, and every navigate action inside the session is checked the same way. It applies to the call it is sent on and is never remembered by the session, so an override has to be repeated on each call that navigates. Setting this to false is honoured, returns a warning in the response, and is recorded against your API key.")
    interactive_only: Optional[bool] = Field(default=True, description="snapshot: give refs to interactive elements only. Set false to list headings and landmarks too; only interactive elements are ever given a ref.")
    max_nodes: Optional[float] = Field(default=200, description="snapshot: cap on how many nodes the tree lists (1-1000). The result reports truncated: true when the cap stopped the walk.")
    actions: Optional[List[BrowserSessionRequestActionsItem]] = Field(default=None, description="act: the actions to run against the open page, 1-20 of them, in the same shape scrape_with_actions takes \u2014 see that tool for every per-action field. Target an element by a @e ref from the most recent snapshot (for example \"@e2\") in selector, or by a CSS selector. Navigation invalidates refs, so snapshot again after one.")
    continue_on_error: Optional[bool] = Field(default=False, description="act: keep going past a failed action instead of stopping the call")
    formats: Optional[List[Any]] = Field(default=["markdown"], description="read: formats to return from the live DOM \u2014 markdown, html, text, json. The page is read as it stands after everything the session has done, cookies and all; nothing is re-fetched.")
    onlyMainContent: Optional[bool] = Field(default=False, description="read: false (default) returns the whole page as markdown/text (markdown leaves out nav, footer and aside elements, as scrape's does; text leaves out nothing); true keeps only the main article block via Readability, which drops navigation and footers but can also drop list items on listing and app pages. The result's extractionMethod says which ran (\"full_page\" for the whole page).")
    full_page: Optional[bool] = Field(default=False, description="screenshot: capture the full scrollable page")
    format: Optional[Literal["png", "jpeg"]] = Field(default="png", description="screenshot: image format")
    quality: Optional[float] = Field(default=80, description="screenshot: JPEG quality (0-100)")
    selector: Optional[str] = Field(default=None, description="screenshot: capture just this element (a @e ref works)")
    max_inline_chars: Optional[float] = Field(default=40000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")
    redact_pii: Optional[Union[bool, BrowserSessionRequestRedactPii]] = Field(default=False, description="Remove personal data from the text this call returns, before it is stored or sent back. true is shorthand for { mode: \"fast\" }: every entity, tagged. As an object: entities (any of EMAIL, PHONE, FINANCIAL, SECRET; omitted or empty means all four, and any other name is a 400 rather than a silent no-op), replace_style (\"tag\" \u2192 <EMAIL>, \"mask\" \u2192 [REDACTED], \"remove\" \u2192 nothing; default \"tag\") and mode (\"fast\", the default, is regex-only and costs no extra credits; \"model\" covers PERSON and LOCATION, needs an LLM and is rejected here \u2014 use the CrawlForge MCP server). The response carries redaction: { entities, count, mode } inside data, saying what was removed. Detection is deliberately conservative: a card number must pass Luhn and an IBAN mod-97, so a false positive cannot silently destroy real page content. URLs, queries and identifiers the response uses to name what was fetched are left intact, and counters derived from the text (content_length, word_count, character_count) describe the text as it was extracted, before redaction.")


class CrawlDeepRequestRedactPii(_RequestModel):
    entities: Optional[List[str]] = Field(default=None, max_length=16)
    replace_style: Optional[Literal["tag", "mask", "remove"]] = Field(default=None)
    mode: Optional[Literal["fast", "model"]] = Field(default=None)


class CrawlDeepRequest(_RequestModel):
    start_url: str = Field(description="The starting URL for the crawl")
    max_pages: Optional[float] = Field(default=10, ge=1, le=100, description="Maximum number of pages to crawl (1-100)")
    max_depth: Optional[float] = Field(default=3, ge=1, le=5, description="Maximum depth to crawl (1-5)")
    same_domain_only: Optional[bool] = Field(default=True, description="Only crawl pages on the same domain")
    respect_robots: Optional[bool] = Field(default=True, description="Fetch each origin's robots.txt and skip URLs it disallows for CrawlForge. A missing or unreachable robots.txt is treated as no restrictions. Returns 403 ROBOTS_DISALLOWED when start_url itself is disallowed, with no credits charged; URLs disallowed mid-crawl are skipped and counted in warnings. Setting this to false is recorded against your API key.")
    respect_robots_txt: Optional[bool] = Field(default=True, description="Alias of respect_robots, kept for callers that already send it. Either parameter set to false disables the gate.")
    crawl_delay: Optional[float] = Field(default=1000, ge=0, le=5000, description="Delay between requests to the same host, in milliseconds (0-5000). Resolved against the site's own robots.txt Crawl-delay as the longer of the two, so the site wins when it asks for more and the two never stack. A delay that will not fit in the crawl timeout skips the page rather than overrunning the budget.")
    timeout: Optional[float] = Field(default=30000, ge=1000, le=60000, description="Total crawl timeout in milliseconds (1000-60000)")
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")
    redact_pii: Optional[Union[bool, CrawlDeepRequestRedactPii]] = Field(default=None, description="Remove personal data from the text this call returns, before it is stored or sent back. true is shorthand for { mode: \"fast\" }: every entity, tagged. As an object: entities (any of EMAIL, PHONE, FINANCIAL, SECRET; omitted or empty means all four, and any other name is a 400 rather than a silent no-op), replace_style (\"tag\" \u2192 <EMAIL>, \"mask\" \u2192 [REDACTED], \"remove\" \u2192 nothing; default \"tag\") and mode (\"fast\", the default, is regex-only and costs no extra credits; \"model\" covers PERSON and LOCATION, needs an LLM and is rejected here \u2014 use the CrawlForge MCP server). The response carries redaction: { entities, count, mode } inside data, saying what was removed. Detection is deliberately conservative: a card number must pass Luhn and an IBAN mod-97, so a false positive cannot silently destroy real page content. URLs, queries and identifiers the response uses to name what was fetched are left intact, and counters derived from the text (content_length, word_count, character_count) describe the text as it was extracted, before redaction.")


class DeepResearchRequestResearchScope(_RequestModel):
    """Optional scoping controls"""
    depth_level: Optional[Literal["surface", "moderate", "deep", "comprehensive"]] = Field(default="moderate", description="How many sources to gather: surface (3), moderate (5), deep (8), comprehensive (10)")
    time_range: Optional[Literal["any", "day", "week", "month", "year"]] = Field(default="any", description="Restrict results by recency: any, day, week, month, year")
    language: Optional[str] = Field(default="en", min_length=2, max_length=10, description="Search language code (e.g. 'en')")
    domains: Optional[List[str]] = Field(default=None, max_length=10, description="Restrict results to these domains (e.g. ['nature.com', 'arxiv.org']; max 10)")


class DeepResearchRequest(_RequestModel):
    research_query: str = Field(min_length=10, description="The research question or topic (minimum 10 characters)")
    research_scope: Optional[DeepResearchRequestResearchScope] = Field(default=None, description="Optional scoping controls")
    max_sources: Optional[int] = Field(default=None, ge=1, le=10, description="Override the source count from depth_level (1-10)")
    respect_robots: Optional[bool] = Field(default=True, description="Fetch each origin's robots.txt and skip source pages it disallows for CrawlForge. A missing or unreachable robots.txt is treated as no restrictions. A disallowed source is reported with fetched: false and contributes only its search snippet; the reason is named in warnings. The search itself is a documented Google API call and is never gated.")
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")


class ExtractContentRequestRedactPii(_RequestModel):
    entities: Optional[List[str]] = Field(default=None, max_length=16)
    replace_style: Optional[Literal["tag", "mask", "remove"]] = Field(default=None)
    mode: Optional[Literal["fast", "model"]] = Field(default=None)


class ExtractContentRequest(_RequestModel):
    url: str = Field(description="The URL to extract content from")
    include_images: Optional[bool] = Field(default=True, description="Include images found in the content")
    include_links: Optional[bool] = Field(default=False, description="Include links found in the content")
    clean_html: Optional[bool] = Field(default=True, description="Return clean text instead of HTML: one line per block element (heading, paragraph, list item, table row)")
    extract_main_content: Optional[bool] = Field(default=True, description="Use readability algorithms to find main content")
    timeout: Optional[float] = Field(default=10000, ge=1000, le=30000, description="Request timeout in milliseconds (1000-30000)")
    respect_robots: Optional[bool] = Field(default=True)
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")
    redact_pii: Optional[Union[bool, ExtractContentRequestRedactPii]] = Field(default=None, description="Remove personal data from the text this call returns, before it is stored or sent back. true is shorthand for { mode: \"fast\" }: every entity, tagged. As an object: entities (any of EMAIL, PHONE, FINANCIAL, SECRET; omitted or empty means all four, and any other name is a 400 rather than a silent no-op), replace_style (\"tag\" \u2192 <EMAIL>, \"mask\" \u2192 [REDACTED], \"remove\" \u2192 nothing; default \"tag\") and mode (\"fast\", the default, is regex-only and costs no extra credits; \"model\" covers PERSON and LOCATION, needs an LLM and is rejected here \u2014 use the CrawlForge MCP server). The response carries redaction: { entities, count, mode } inside data, saying what was removed. Detection is deliberately conservative: a card number must pass Luhn and an IBAN mod-97, so a false positive cannot silently destroy real page content. URLs, queries and identifiers the response uses to name what was fetched are left intact, and counters derived from the text (content_length, word_count, character_count) describe the text as it was extracted, before redaction.")


class ExtractEmbeddedStateRequest(_RequestModel):
    url: str = Field(description="URL to read embedded state from")
    path: Optional[str] = Field(default=None, description="Return one subtree instead of everything, e.g. \"next_data.props.pageProps\" or \"json_scripts[0].data\". Dotted keys and array indexes only \u2014 not JSONPath: no wildcards, filters, slices or recursive descent. A path that does not resolve is a 400 naming the keys that were available at the point it stopped, and costs no credits.")
    user_agent: Optional[str] = Field(default=None, description="Override the User-Agent sent to the target")
    respect_robots: Optional[bool] = Field(default=True, description="Honour the target's robots.txt. Setting this to false is recorded against your API key.")
    timeout: Optional[int] = Field(default=20000, ge=1000, le=60000, description="Fetch timeout in ms (1000-60000)")
    keys_only: Optional[bool] = Field(default=False, description="Return keys instead of data: the selected data (after path, if given) described two levels deep, each leaf labelled \"object\", \"array(<n>)\", \"string\", \"number\", \"boolean\" or \"null\", and an array as { length, first } with the shape of its first element. found and bytes are unchanged, so one cheap call shows which path to ask for.")
    find: Optional[str] = Field(default=None, min_length=1, max_length=100, description="Return `matches` instead of `data`: every property with this key name (case-insensitive) anywhere in the selected data (after `path`), in document order, each as {path, preview} with the first 200 characters of its value - at most 50, with `matches_total` and `matches_truncated`. Each match path already starts with `path`, so it can be passed straight back as `path`. Discover where a field lives without downloading the payload. Cannot be combined with keys_only")
    raw: Optional[bool] = Field(default=False, description="Also keep the undecoded __NUXT_DATA__ devalue array under json_scripts, beside the decoded nuxt_data. Default: false")
    escalate: Optional[bool] = Field(default=False, description="Retry a blocked page in a stealth browser, in this same call. The plain fetch always runs first; only a bot wall, an empty shell with no state, or a 403, 429 or 444 escalates \u2014 never a 404 or a 5xx. The rendered HTML goes through the same parser. The response carries escalated: true|false whenever this is set, plus stealth: { engine, vendor_detected } when the render ran. It costs the escalation add-on only when it ran. The stage needs the CrawlForge execution backend: where that is not configured it returns 503 TOOL_NOT_AVAILABLE and charges nothing. robots.txt is respected on the escalated path too. Reading window globals (window_state) is MCP-server only: the render here returns HTML.")
    escalate_engine: Optional[Literal["playwright", "camoufox"]] = Field(default="playwright", description="Browser engine for the escalated render (camoufox only where installed on the backend). Ignored when no escalation runs.")
    wait_for: Optional[int] = Field(default=None, ge=0, le=30000, description="Extra wait after page load for the escalated render, in ms (0-30000), passed to stealth_mode for state that is written after DOMContentLoaded. Ignored when no escalation runs.")
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit). Here the response keeps url, path, bytes, found, data_keys (the top-level keys of data) and escalated/stealth, and preview is the head of the pretty-printed JSON cut at a line boundary, so no value is ever split and the response stays within max_inline_chars; read_result json_path reads any field of the stored result, e.g. \"data.next_data.props\".")


class ExtractLinksRequest(_RequestModel):
    html: Optional[str] = Field(default=None, min_length=1, description="HTML content to extract links from")
    url: Optional[str] = Field(default=None, description="URL to fetch and extract links from")
    base_url: Optional[str] = Field(default=None, description="Base URL for resolving relative links")
    filter_domains: Optional[List[str]] = Field(default=None, description="Only include links from specified domains")
    include_external: Optional[bool] = Field(default=True, description="Include external links")
    include_internal: Optional[bool] = Field(default=True, description="Include internal links (same hostname as the page)")
    filter_external: Optional[bool] = Field(default=None, description="The MCP tool's name for outbound-only: true is the same as include_internal: false. An alias; when true it overrides include_internal.")
    include_anchors: Optional[bool] = Field(default=False, description="Include anchor links (#fragment)")
    deduplicate: Optional[bool] = Field(default=True, description="Remove duplicate links, compared without fragment or trailing slash; the first occurrence is kept")
    include_metadata: Optional[bool] = Field(default=True, description="Include each link's title and the domains count map. Every record always carries href, text, type, domain, rel and original_href \u2014 the shape the MCP tool returns. type is internal, external, anchor, other (mailto:, tel:, javascript: and other non-web schemes; href is null except for mailto: and tel:) or relative (html input with no base_url). A <base href> in the page is honoured unless base_url is given.")
    respect_robots: Optional[bool] = Field(default=True)
    escalate: Optional[bool] = Field(default=False, description="Retry a walled page in a stealth browser, in this same call (url input only). The plain fetch always runs first; only a named bot wall, a 403, 429 or 444, or an empty shell or error placeholder served as 2xx escalates \u2014 never a 404, a 5xx, a binary or a host whose Retry-After window is still open. The response carries escalated: true|false whenever this is set, plus stealth: { engine, vendor_detected } when the render ran. It costs the escalation add-on only when it ran. The stage needs the CrawlForge execution backend: where that is not configured it returns 503 TOOL_NOT_AVAILABLE and charges nothing. robots.txt is respected on the escalated path too.")
    escalate_engine: Optional[Literal["playwright", "camoufox"]] = Field(default="playwright", description="Browser engine for the escalated render (camoufox only where installed on the backend). Ignored when no escalation runs.")
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")


class ExtractMetadataRequest(_RequestModel):
    html: Optional[str] = Field(default=None, min_length=1, description="HTML content to extract metadata from")
    url: Optional[str] = Field(default=None, description="URL to fetch and extract metadata from. The response always carries redirected (true when the fetch ended on a different URL, compared after parsing, so https://example.com and https://example.com/ are the same page), and requested_url when it did; metadata.basic.url and extracted_from are the final URL")
    include_social: Optional[bool] = Field(default=True, description="Include Open Graph and Twitter Card metadata")
    include_seo: Optional[bool] = Field(default=True, description="Include SEO-related metadata")
    include_technical: Optional[bool] = Field(default=True, description="Include technical metadata (scripts, stylesheets, etc.)")
    include_structured_data: Optional[bool] = Field(default=True, description="Include structured data (JSON-LD, microdata)")
    respect_robots: Optional[bool] = Field(default=True)
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")


class ExtractStructuredRequestSchema(_RequestModel):
    """JSON Schema defining the data structure to extract. A number or integer property takes the first number in the text found ("4.5 out of 5" is 4.5; an integer only when whole); text with no number is returned as it is"""
    type: Optional[str] = Field(default=None)
    properties: Dict[str, Any] = Field()
    required: Optional[List[str]] = Field(default=None)


class ExtractStructuredRequestLlmConfig(_RequestModel):
    """Accepted for compatibility; this endpoint never calls an LLM provider"""
    provider: Optional[str] = Field(default=None)
    apiKey: Optional[str] = Field(default=None)


class ExtractStructuredRequest(_RequestModel):
    url: str = Field(description="The URL to extract structured data from")
    schema_: ExtractStructuredRequestSchema = Field(alias="schema", description="JSON Schema defining the data structure to extract. A number or integer property takes the first number in the text found (\"4.5 out of 5\" is 4.5; an integer only when whole); text with no number is returned as it is")
    prompt: Optional[str] = Field(default=None, description="Accepted for compatibility; only used by the MCP server LLM extraction")
    llmConfig: Optional[ExtractStructuredRequestLlmConfig] = Field(default=None, description="Accepted for compatibility; this endpoint never calls an LLM provider")
    selectorHints: Optional[Dict[str, str]] = Field(default=None, description="CSS selectors per schema property, checked before structured data")
    fallbackToSelectors: Optional[bool] = Field(default=True, description="When false and required fields are set, extracting nothing returns EXTRACTION_FAILED instead of nulls")
    respect_robots: Optional[bool] = Field(default=True)


class ExtractTextRequestRedactPii(_RequestModel):
    entities: Optional[List[str]] = Field(default=None, max_length=16)
    replace_style: Optional[Literal["tag", "mask", "remove"]] = Field(default=None)
    mode: Optional[Literal["fast", "model"]] = Field(default=None)


class ExtractTextRequest(_RequestModel):
    html: Optional[str] = Field(default=None, min_length=1, description="HTML content to extract text from")
    url: Optional[str] = Field(default=None, description="URL to fetch and extract text from")
    selector: Optional[str] = Field(default=None, description="CSS selector to target specific elements")
    clean: Optional[bool] = Field(default=True, description="Collapse runs of spaces within a line and drop blank lines; line breaks between blocks are kept. Text mode only.")
    preserve_links: Optional[bool] = Field(default=False, description="Append the links as \"text (href)\" lines after the text. REST only (the MCP tool has no such option); text mode only.")
    preserve_formatting: Optional[bool] = Field(default=False, description="Keep paragraph and heading breaks from the HTML source. REST only (the MCP tool has no such option); text mode only.")
    max_length: Optional[float] = Field(default=None, ge=1, le=1000000, description="Maximum length of the returned text or markdown; a cut text ends in \"...\" and data.truncated is true (data.truncated is always present, false when nothing was cut)")
    output_format: Optional[Literal["text", "markdown"]] = Field(default="text", description="text (default): data.text, one line per block element. markdown: data.markdown, the selected elements (or the body) converted with Turndown, data tables as GFM pipe tables and image and link URLs absolute. Either way data carries output_format, word_count and char_count, named as the MCP tool names them; markdown is counted without its # * ` _ [ ] syntax.")
    respect_robots: Optional[bool] = Field(default=True)
    escalate: Optional[bool] = Field(default=False, description="Retry a walled page in a stealth browser, in this same call (url input only). The plain fetch always runs first; only a named bot wall, a 403, 429 or 444, or an empty shell or error placeholder served as 2xx escalates \u2014 never a 404, a 5xx, a binary or a host whose Retry-After window is still open. The response carries escalated: true|false whenever this is set, plus stealth: { engine, vendor_detected } when the render ran. It costs the escalation add-on only when it ran. The stage needs the CrawlForge execution backend: where that is not configured it returns 503 TOOL_NOT_AVAILABLE and charges nothing. robots.txt is respected on the escalated path too.")
    escalate_engine: Optional[Literal["playwright", "camoufox"]] = Field(default="playwright", description="Browser engine for the escalated render (camoufox only where installed on the backend). Ignored when no escalation runs.")
    redact_pii: Optional[Union[bool, ExtractTextRequestRedactPii]] = Field(default=None, description="Remove personal data from the text this call returns, before it is stored or sent back. true is shorthand for { mode: \"fast\" }: every entity, tagged. As an object: entities (any of EMAIL, PHONE, FINANCIAL, SECRET; omitted or empty means all four, and any other name is a 400 rather than a silent no-op), replace_style (\"tag\" \u2192 <EMAIL>, \"mask\" \u2192 [REDACTED], \"remove\" \u2192 nothing; default \"tag\") and mode (\"fast\", the default, is regex-only and costs no extra credits; \"model\" covers PERSON and LOCATION, needs an LLM and is rejected here \u2014 use the CrawlForge MCP server). The response carries redaction: { entities, count, mode } inside data, saying what was removed. Detection is deliberately conservative: a card number must pass Luhn and an IBAN mod-97, so a false positive cannot silently destroy real page content. URLs, queries and identifiers the response uses to name what was fetched are left intact, and counters derived from the text (content_length, word_count, character_count) describe the text as it was extracted, before redaction.")


class ExtractWithLlmRequest(_RequestModel):
    url: Optional[str] = Field(default=None, description="URL to fetch and extract from (one of url/content required)")
    content: Optional[str] = Field(default=None, description="Pre-fetched text to extract from (one of url/content required)")
    prompt: str = Field(description="Natural-language extraction instruction")
    schema_: Optional[Dict[str, Any]] = Field(default=None, alias="schema", description="Optional JSON-schema for output shape (used as Ollama structured-outputs format when provider is \"ollama\")")
    provider: Optional[Literal["openai", "anthropic", "ollama", "auto"]] = Field(default="auto", description="LLM provider. \"auto\" prefers a local Ollama instance where one exists; \"openai\"/\"anthropic\" use cloud models (require the matching API key on the execution side)")
    model: Optional[str] = Field(default=None, description="Override the model. For ollama, pass a name returned by list_ollama_models. Defaults: openai=\"gpt-4o-mini\", anthropic=\"claude-haiku-4-5-20251001\", ollama=\"llama3.2\"")
    maxTokens: Optional[float] = Field(default=4096, description="Maximum output tokens")


class FetchUrlRequest(_RequestModel):
    url: str = Field(description="The URL to fetch")
    headers: Optional[Dict[str, str]] = Field(default=None, description="Optional HTTP headers to include")
    timeout: Optional[float] = Field(default=10000, ge=1000, le=30000, description="Request timeout in milliseconds (1000-30000)")
    follow_redirects: Optional[bool] = Field(default=True, description="Whether to follow HTTP redirects")
    user_agent: Optional[str] = Field(default=None, description="Custom User-Agent header")
    respect_robots: Optional[bool] = Field(default=True)
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")


class GenerateLlmsTxtRequestAnalysisOptions(_RequestModel):
    """Analysis options. maxPages is clamped to 30 and maxDepth to 2 on the hosted REST API (clamps are reported in clamps_applied). respectRobots skips pages disallowed by robots.txt; detectAPIs flags /api, /docs/api, openapi, and swagger links found in fetched HTML."""
    maxDepth: Optional[float] = Field(default=3, ge=1, le=5)
    maxPages: Optional[float] = Field(default=100, ge=10, le=500)
    respectRobots: Optional[bool] = Field(default=True)
    detectAPIs: Optional[bool] = Field(default=True)
    analyzeContent: Optional[bool] = Field(default=True)
    checkSecurity: Optional[bool] = Field(default=True)


class GenerateLlmsTxtRequestOutputOptions(_RequestModel):
    """Output customization: organizationName (overrides the site title), contactEmail, customGuidelines, customRestrictions"""
    organizationName: Optional[str] = Field(default=None)
    contactEmail: Optional[str] = Field(default=None)
    customGuidelines: Optional[List[str]] = Field(default=None)
    customRestrictions: Optional[List[str]] = Field(default=None)
    includeDetailed: Optional[bool] = Field(default=True)
    includeAnalysis: Optional[bool] = Field(default=False)


class GenerateLlmsTxtRequest(_RequestModel):
    url: str = Field(description="The website URL to generate llms.txt for")
    respect_robots: Optional[bool] = Field(default=True, description="Fetch each origin's robots.txt and skip URLs it disallows for CrawlForge. A missing or unreachable robots.txt is treated as no restrictions. Returns 403 ROBOTS_DISALLOWED when the target URL itself is disallowed, with no credits charged; disallowed pages are left out of the analysis and counted in warnings. analysisOptions.respectRobots is an alias \u2014 either one set to false disables the gate.")
    format: Optional[Literal["both", "llms-txt", "llms-full-txt"]] = Field(default="both", description="Output format; llms-full.txt inlines up to 2000 characters of text per analyzed page")
    complianceLevel: Optional[Literal["basic", "standard", "strict"]] = Field(default="standard", description="Accepted for compatibility; content is derived from real site data, not canned policy text")
    analysisOptions: Optional[GenerateLlmsTxtRequestAnalysisOptions] = Field(default=None, description="Analysis options. maxPages is clamped to 30 and maxDepth to 2 on the hosted REST API (clamps are reported in clamps_applied). respectRobots skips pages disallowed by robots.txt; detectAPIs flags /api, /docs/api, openapi, and swagger links found in fetched HTML.")
    outputOptions: Optional[GenerateLlmsTxtRequestOutputOptions] = Field(default=None, description="Output customization: organizationName (overrides the site title), contactEmail, customGuidelines, customRestrictions")
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")


class GetBatchResultsRequest(_RequestModel):
    batchId: str = Field(min_length=1, description="The batch_id returned by batch_scrape")
    page: Optional[int] = Field(default=1, ge=1, le=9007199254740991, description="Page number to retrieve (1-based)")
    limit: Optional[int] = Field(default=25, ge=1, le=100, description="Results per page (1-100)")


class ListOllamaModelsRequest(_RequestModel):
    pass


class LocalizationRequest(_RequestModel):
    url: str = Field(description="The URL to analyze for localization")
    target_language: Optional[str] = Field(default=None, description="Language you expect (e.g., \"en\", \"fr\", \"es\"). Sent as this request's Accept-Language and compared with the detected language and html lang")
    target_country: Optional[str] = Field(default=None, description="Country you expect (e.g., \"US\", \"FR\", \"JP\"). Echoed back and sent as an X-Country-Code header on this request; it does not change where the request comes from")
    detect_language: Optional[bool] = Field(default=True, description="Detect the page language from its visible text. Returns an ISO 639-1 code, or \"und\" when the language cannot be determined.")
    extract_hreflang: Optional[bool] = Field(default=True, description="Extract hreflang alternate language tags")
    check_geo_targeting: Optional[bool] = Field(default=False, description="Check for geo-targeting metadata")
    timeout: Optional[float] = Field(default=10000, ge=1000, le=30000, description="Request timeout in milliseconds (1000-30000)")
    respect_robots: Optional[bool] = Field(default=True)


class MapSiteRequest(_RequestModel):
    url: str = Field(description="The starting URL to map")
    respect_robots: Optional[bool] = Field(default=True, description="Fetch each origin's robots.txt and skip URLs it disallows for CrawlForge. A missing or unreachable robots.txt is treated as no restrictions. Returns 403 ROBOTS_DISALLOWED when the start URL itself is disallowed, with no credits charged; a disallowed sitemap.xml falls back to the crawl, and pages disallowed mid-crawl are skipped and counted in warnings.")
    max_depth: Optional[float] = Field(default=2, ge=1, le=5, description="Maximum crawl depth for the fallback crawl (1-5); unused when a sitemap is found")
    include_external: Optional[bool] = Field(default=False, description="Include external links in per-page link lists (crawl mode only; external pages are never crawled)")
    timeout: Optional[float] = Field(default=15000, ge=1000, le=30000, description="Overall crawl budget in milliseconds (1000-30000; capped at ~18000 to fit the serverless limit)")
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")


class ProcessDocumentRequestRedactPii(_RequestModel):
    entities: Optional[List[str]] = Field(default=None, max_length=16)
    replace_style: Optional[Literal["tag", "mask", "remove"]] = Field(default=None)
    mode: Optional[Literal["fast", "model"]] = Field(default=None)


class ProcessDocumentRequest(_RequestModel):
    url: str = Field(description="URL of the document to process (max 25MB)")
    respect_robots: Optional[bool] = Field(default=True, description="Fetch the origin's robots.txt and refuse the document if it disallows CrawlForge. A missing or unreachable robots.txt is treated as no restrictions. Returns 403 ROBOTS_DISALLOWED, and no credits are charged.")
    document_type: Optional[Literal["pdf", "docx", "xlsx", "csv", "txt", "auto"]] = Field(default="auto", description="Document type; auto-detected from Content-Type, URL extension, then content sniffing")
    extract_text: Optional[bool] = Field(default=True, description="Extract text content (capped at 200000 characters; PDFs read up to 200 pages, and pages_read { start, end, count, total_pages } says which; HTML is read one line per block element)")
    extract_metadata: Optional[bool] = Field(default=True, description="Extract document metadata (PDF info dictionary; HTML title/description/author)")
    extract_tables: Optional[bool] = Field(default=False, description="Extract tables (PDF via ruled-grid detection, CSV via parsing; not available for HTML). Up to 20 tables of 1000 rows; a table ruled only horizontally keeps its rows but reports one column")
    extract_images: Optional[bool] = Field(default=False, description="Not available on the hosted REST API \u2014 returns images: null with a note; use the CrawlForge MCP server for image extraction")
    timeout: Optional[float] = Field(default=30000, ge=1000, le=60000, description="Fetch timeout in milliseconds (1000-60000; capped at 20000 to fit the serverless limit)")
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")
    redact_pii: Optional[Union[bool, ProcessDocumentRequestRedactPii]] = Field(default=None, description="Remove personal data from the text this call returns, before it is stored or sent back. true is shorthand for { mode: \"fast\" }: every entity, tagged. As an object: entities (any of EMAIL, PHONE, FINANCIAL, SECRET; omitted or empty means all four, and any other name is a 400 rather than a silent no-op), replace_style (\"tag\" \u2192 <EMAIL>, \"mask\" \u2192 [REDACTED], \"remove\" \u2192 nothing; default \"tag\") and mode (\"fast\", the default, is regex-only and costs no extra credits; \"model\" covers PERSON and LOCATION, needs an LLM and is rejected here \u2014 use the CrawlForge MCP server). The response carries redaction: { entities, count, mode } inside data, saying what was removed. Detection is deliberately conservative: a card number must pass Luhn and an IBAN mod-97, so a false positive cannot silently destroy real page content. URLs, queries and identifiers the response uses to name what was fetched are left intact, and counters derived from the text (content_length, word_count, character_count) describe the text as it was extracted, before redaction.")


class ReadResultRequest(_RequestModel):
    handle: str = Field(min_length=1, description="The result_handle returned by a tool (res_ followed by a UUID)")
    operation: Literal["slice", "search", "lines", "json_path"] = Field(description="slice: a character range. search: every case-insensitive literal occurrence of query, each with its offset and 200 chars of context on each side. lines: a page of lines. json_path: one field of the stored JSON.")
    offset: Optional[int] = Field(default=None, ge=0, le=9007199254740991, description="slice: first character index. lines: first line index.")
    length: Optional[int] = Field(default=None, ge=1, le=200000, description="slice: characters to return (default 10000, max 200000). lines: lines to return (default 200, max 5000). Both are also capped at max_inline_chars.")
    query: Optional[str] = Field(default=None, min_length=1, max_length=500, description="search: the literal text to find (1-500 chars); never interpreted as a pattern")
    max_matches: Optional[int] = Field(default=20, ge=1, le=100, description="search: matches to return (1-100); total_matches still counts every occurrence")
    path: Optional[str] = Field(default=None, min_length=1, max_length=500, description="json_path: dotted path into the stored result, e.g. \"formats.links[0].href\" or \"formats.links.0.href\". Keys and indexes only \u2014 no wildcards. The subject is the stored payload, or the parsed body when the stored text is itself JSON. A path that does not resolve is a 400 naming the keys available where it stopped.")
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Cap on the characters this call returns (1000-10000000)")


class RedditSearchRequest(_RequestModel):
    query: Optional[str] = Field(default=None, min_length=1, description="Keyword search. Posts: matches title+selftext; comments: matches body. Supports \"quoted phrases\", OR, -exclusion")
    subreddit: Optional[str] = Field(default=None, min_length=1, description="Limit to one subreddit (with or without the r/ prefix)")
    author: Optional[str] = Field(default=None, min_length=1, description="Limit to one author (with or without the u/ prefix)")
    mode: Optional[Literal["posts", "comments", "thread"]] = Field(default="posts", description="What to search: posts (default), comments, or thread (full comment tree \u2014 requires link_id)")
    link_id: Optional[str] = Field(default=None, min_length=1, description="Post ID (e.g. '1twm1zh' or 't3_1twm1zh') \u2014 required for thread mode, optional filter for comments mode")
    after: Optional[str] = Field(default=None, min_length=1, description="Only content posted after this date \u2014 ISO 8601, epoch seconds, or an offset like '7d'")
    before: Optional[str] = Field(default=None, min_length=1, description="Only content posted before this date \u2014 same formats as after")
    limit: Optional[int] = Field(default=25, ge=1, le=100, description="Max results (1-100; thread mode: max comments returned)")
    sort: Optional[Literal["asc", "desc"]] = Field(default="desc", description="Sort by post date (desc = newest first)")
    source: Optional[Literal["auto", "arctic_shift", "pullpush", "web_discovery"]] = Field(default="auto", description="Force a specific backend: auto (Arctic Shift first, PullPush second), arctic_shift, web_discovery (unscoped keyword searches only \u2014 posts or comments), or pullpush (the automatic second source; has refused automated clients since August 2026)")


class ScrapeRequestFormatsItemHighlights(_RequestModel):
    type: Literal["highlights"] = Field()
    query: str = Field(min_length=1, max_length=500)
    max_highlights: Optional[int] = Field(default=10, ge=1, le=50)
    mode: Optional[Literal["extractive", "model"]] = Field(default="extractive")


class ScrapeRequestFormatsItemQuestion(_RequestModel):
    type: Literal["question"] = Field()
    question: str = Field(min_length=1, max_length=500)
    mode: Optional[Literal["extractive", "model"]] = Field(default="extractive")


class ScrapeRequestRedactPii(_RequestModel):
    entities: Optional[List[str]] = Field(default=None, max_length=16)
    replace_style: Optional[Literal["tag", "mask", "remove"]] = Field(default=None)
    mode: Optional[Literal["fast", "model"]] = Field(default=None)


class ScrapeRequest(_RequestModel):
    url: str = Field(description="The URL to scrape")
    formats: Optional[List[Union[Literal["markdown", "html", "rawHtml", "text", "links", "metadata", "screenshot", "json-schema"], ScrapeRequestFormatsItemHighlights, ScrapeRequestFormatsItemQuestion]]] = Field(default=cast('List[Union[Literal["markdown", "html", "rawHtml", "text", "links", "metadata", "screenshot", "json-schema"], ScrapeRequestFormatsItemHighlights, ScrapeRequestFormatsItemQuestion]]', ["markdown"]), min_length=1, description="Output formats: markdown, html, rawHtml, text, links, metadata, plus two query-scoped object formats. { type: 'highlights', query, max_highlights (1-50, default 10), mode } returns the sentences and code blocks matching the query, verbatim, each with an offset and length into the markdown format of the same call (table rows too: markdown keeps data tables as GFM pipe tables). { type: 'question', question, mode } returns an answer assembled from the best-matching passages, with its evidence. At most one of each per request. mode defaults to 'extractive'; mode 'model' needs an LLM and is rejected here, as are the 'screenshot' and 'json-schema' formats, which require the CrawlForge MCP server (browser/LLM).")
    onlyMainContent: Optional[bool] = Field(default=True, description="Strip navigation, headers, and footers, returning only the main content")
    respect_robots: Optional[bool] = Field(default=True)
    escalate: Optional[bool] = Field(default=False, description="Retry a blocked page in a stealth browser, in this same call. The plain fetch always runs first; only if it meets a bot wall, an empty shell or an error placeholder does the stealth render run, and the requested formats are then derived from the rendered HTML. The response carries escalated: true|false whenever this is set, plus stealth: { engine, vendor_detected } when the render ran. It costs the escalation add-on only when it ran. The stage needs the CrawlForge execution backend: where that is not configured it returns 503 TOOL_NOT_AVAILABLE and charges nothing. robots.txt is respected on the escalated path too, matched against the same CrawlForge product token.")
    escalate_engine: Optional[Literal["playwright", "camoufox"]] = Field(default="playwright", description="Browser engine for the escalated render (camoufox only where installed on the backend). Ignored when no escalation runs.")
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")
    redact_pii: Optional[Union[bool, ScrapeRequestRedactPii]] = Field(default=None, description="Remove personal data from the text this call returns, before it is stored or sent back. true is shorthand for { mode: \"fast\" }: every entity, tagged. As an object: entities (any of EMAIL, PHONE, FINANCIAL, SECRET; omitted or empty means all four, and any other name is a 400 rather than a silent no-op), replace_style (\"tag\" \u2192 <EMAIL>, \"mask\" \u2192 [REDACTED], \"remove\" \u2192 nothing; default \"tag\") and mode (\"fast\", the default, is regex-only and costs no extra credits; \"model\" covers PERSON and LOCATION, needs an LLM and is rejected here \u2014 use the CrawlForge MCP server). The response carries redaction: { entities, count, mode } inside data, saying what was removed. Detection is deliberately conservative: a card number must pass Luhn and an IBAN mod-97, so a false positive cannot silently destroy real page content. URLs, queries and identifiers the response uses to name what was fetched are left intact, and counters derived from the text (content_length, word_count, character_count) describe the text as it was extracted, before redaction.")


class ScrapeStructuredRequest(_RequestModel):
    html: Optional[str] = Field(default=None, min_length=1, description="HTML content to extract data from")
    url: Optional[str] = Field(default=None, description="URL to fetch and extract data from")
    selectors: Dict[str, str] = Field(description="Key-value pairs of field names and CSS selectors")
    base_url: Optional[str] = Field(default=None, description="Base URL for resolving relative URLs")
    multiple: Optional[bool] = Field(default=False, description="Extract multiple items vs single item")
    clean_text: Optional[bool] = Field(default=True, description="Clean extracted text by trimming whitespace")
    include_attributes: Optional[List[str]] = Field(default=None, description="HTML attributes to extract (e.g., href, src, alt)")
    max_items: Optional[float] = Field(default=100, ge=1, le=1000, description="Maximum number of items to extract (for multiple mode)")
    respect_robots: Optional[bool] = Field(default=True)


class ScrapeTemplateRequest(_RequestModel):
    template: str = Field(description="A supported template id, \"auto\" to pick one from the url, or \"list\" to discover them.")
    url: Optional[str] = Field(default=None, description="URL to scrape. Required unless template === \"list\", or params drive a list connector. Always required for template \"auto\".")
    params: Optional[Dict[str, Any]] = Field(default=None, description="Drives a list connector in place of a url \u2014 { \"company\": \"stripe\" } for the job boards, { \"store\": \"www.allbirds.com\", \"collection\": \"mens\" } for shopify-collection, { \"vin\": \"5UXWX7C5*BA\" } for nhtsa-vin. Each connector names its own parameters in the description that template \"list\" returns. A missing or invalid parameter is a 400 naming it, and no credits are charged.")
    respect_robots: Optional[bool] = Field(default=True, description="Fetch the origin's robots.txt and refuse the URL if it disallows CrawlForge. Checked against the URL actually fetched, which is the API endpoint rather than the URL or params you pass wherever a template resolves one. A missing or unreachable robots.txt is treated as no restrictions. Returns 403 ROBOTS_DISALLOWED, and no credits are charged.")
    timeout: Optional[int] = Field(default=15000, ge=5000, le=60000, description="Request timeout in milliseconds (5000\u201360000).")
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")


class ScrapeWithActionsRequestActionsItemPosition(_RequestModel):
    """click/hover: relative position { x, y }"""
    x: Optional[float] = Field(default=None)
    y: Optional[float] = Field(default=None)


class ScrapeWithActionsRequestActionsItem(_RequestModel):
    type: Optional[Literal["wait", "click", "type", "press", "scroll", "screenshot", "executeJavaScript", "select", "hover", "navigate", "snapshot"]] = Field(default=None, description="Action to perform. executeJavaScript is disabled unless the server runs with ALLOW_JAVASCRIPT_EXECUTION=true; it is refused on the hosted API.")
    selector: Optional[str] = Field(default=None, description="What the action targets: either a CSS selector or an @e ref (for example @e1) taken from the most recent snapshot action in the same chain. Refs are invalidated by navigation \u2014 snapshot again after the page changes.")
    text: Optional[str] = Field(default=None, description="type: text to enter")
    key: Optional[str] = Field(default=None, description="press: key to press")
    value: Optional[str] = Field(default=None, description="select: one option to choose in the <select> named by selector. Matches an option by its value or by its visible label.")
    values: Optional[List[Any]] = Field(default=None, description="select: several options to choose, same matching rule as value. Supply value or values, not neither.")
    url: Optional[str] = Field(default=None, description="navigate: URL to load mid-chain, in the same browser session. Passes the same robots.txt and SSRF checks as the top-level url. Every navigation is checked for a bot wall, HTTP error page or challenge interstitial (an HTTP 202 interstitial included): this action's result carries httpStatus and, when a wall was named, blocked: { vendor, evidence } \u2014 reported, not failed. The result lists every navigation in order in navigations[] (index 0 the initial load), each { url, finalUrl, httpStatus, blocked? }, httpStatus null when unknown. A click or form submit that loads another page is a navigation too: it gets its own navigations entry with trigger naming the action type, and the top-level finalUrl is where the chain ended (url stays the one requested). A chain that ends on a wall is never reported as success: it fails (over REST, a 502 TOOL_ERROR with nothing charged).")
    waitUntil: Optional[Literal["load", "domcontentloaded", "networkidle", "commit"]] = Field(default="domcontentloaded", description="navigate: how long to wait for the new page before continuing")
    script: Optional[str] = Field(default=None, description="executeJavaScript: script to run")
    timeout: Optional[float] = Field(default=10000, description="Per-action timeout in ms, distinct from browserOptions.timeout which budgets the whole chain")
    description: Optional[str] = Field(default=None, description="Human-readable label for this action")
    continueOnError: Optional[bool] = Field(default=None, description="Keep going if this action fails")
    retries: Optional[float] = Field(default=None, description="Retry attempts for this action (0-5)")
    captureAfter: Optional[bool] = Field(default=None, description="Capture page content after this action")
    duration: Optional[float] = Field(default=None, description="wait: milliseconds to wait (0-30000)")
    condition: Optional[Literal["visible", "hidden", "enabled", "disabled", "stable"]] = Field(default=None, description="wait: condition on selector")
    button: Optional[Literal["left", "right", "middle"]] = Field(default=None, description="click: mouse button")
    clickCount: Optional[float] = Field(default=None, description="click: number of clicks (1-3)")
    delay: Optional[float] = Field(default=None, description="click/type: delay in ms (0-1000)")
    force: Optional[bool] = Field(default=None, description="click/hover: bypass actionability checks")
    position: Optional[ScrapeWithActionsRequestActionsItemPosition] = Field(default=None, description="click/hover: relative position { x, y }")
    clear: Optional[bool] = Field(default=None, description="type: clear field before typing")
    modifiers: Optional[List[Any]] = Field(default=None, description="press: modifier keys (Alt, Control, Meta, Shift)")
    direction: Optional[Literal["up", "down", "left", "right"]] = Field(default=None, description="scroll: direction")
    distance: Optional[float] = Field(default=None, description="scroll: pixels to scroll")
    smooth: Optional[bool] = Field(default=None, description="scroll: smooth scrolling")
    toElement: Optional[str] = Field(default=None, description="scroll: selector to scroll to")
    x: Optional[float] = Field(default=None, description="scroll: absolute X coordinate (window.scrollTo; with y, takes precedence over direction/distance)")
    y: Optional[float] = Field(default=None, description="scroll: absolute Y coordinate (window.scrollTo; with x, takes precedence over direction/distance)")
    fullPage: Optional[bool] = Field(default=None, description="screenshot: capture full page")
    quality: Optional[float] = Field(default=None, description="screenshot: jpeg quality (0-100)")
    format: Optional[Literal["png", "jpeg"]] = Field(default=None, description="screenshot: image format")
    args: Optional[List[Any]] = Field(default=None, description="executeJavaScript: arguments passed to the script")
    returnResult: Optional[bool] = Field(default=None, description="executeJavaScript: return the script result")
    interactiveOnly: Optional[bool] = Field(default=True, description="snapshot: list only interactive elements. Set false to include headings and landmarks too; only interactive elements are ever given a ref.")
    maxNodes: Optional[float] = Field(default=200, description="snapshot: cap on how many nodes the tree lists (1-1000); under the default interactiveOnly every one of them carries a ref. The result reports truncated: true when the cap stopped the walk.")


class ScrapeWithActionsRequestFormAutoFill(_RequestModel):
    """Form auto-fill configuration"""
    fields: Optional[List[Any]] = Field(default=None, description="Fields to fill: { selector, value, type: text|select|checkbox|radio|file, waitAfter }. type picks how the field is filled: text (default) types the value, select picks the option by value or label, checkbox/radio check the input (a selector matching a group checks the member whose value attribute equals value; a checkbox with value \"false\" is unchecked). file is not supported and fails that action")
    submitSelector: Optional[str] = Field(default=None, description="Selector of the submit control")
    waitAfterSubmit: Optional[float] = Field(default=2000, description="Wait after submit in ms (0-30000)")


class ScrapeWithActionsRequestBrowserOptionsProxyRotation(_RequestModel):
    """Route the stealth browser through proxies you supply. Requires stealth: true (refused otherwise). Chromium engine only: refused on Camoufox, which applies its proxy at browser launch and shares that browser across calls. CrawlForge supplies no proxies; a residential proxy is what gets past an IP-reputation block that no fingerprint fixes. Proxies on loopback, private, link-local or metadata addresses are refused. Credentials are never echoed back: metadata.browserOptions shows them redacted."""
    enabled: Optional[bool] = Field(default=False, description="Route the chain through proxies")
    proxies: Optional[List[str]] = Field(default=None, description="Proxy URLs: \"http://user:pass@host:port\" (percent-encode a password containing @ : or /), or bare \"host:port\" for an unauthenticated HTTP proxy. http, https, socks4 and socks5 are accepted.")
    rotationInterval: Optional[float] = Field(default=300000, description="Minimum ms on one proxy before the list advances")


class ScrapeWithActionsRequestBrowserOptions(_RequestModel):
    """Browser configuration options"""
    headless: Optional[bool] = Field(default=True)
    userAgent: Optional[str] = Field(default=None)
    viewportWidth: Optional[float] = Field(default=1280, description="800-1920")
    viewportHeight: Optional[float] = Field(default=720, description="600-1080")
    timeout: Optional[float] = Field(default=30000, description="Browser timeout in ms (10000-120000)")
    stealth: Optional[bool] = Field(default=False, description="Run the action chain in the stealth Chromium engine at its medium profile instead of the standard browser pool. The boolean is the only knob \u2014 level, fingerprint randomization and engine are not settable from here. Slower to start; it renders JavaScript, it does not solve challenges.")
    consent: Optional[Literal["off", "reject", "accept"]] = Field(default="off", description="Cookie/consent banner handling. \"reject\" runs an opt-out on a recognised consent banner (DuckDuckGo autoconsent rules) once after the initial navigation and after each navigate action, capped at 2 s; \"accept\" opts in instead. When not \"off\" the result carries consent: { cmp, action, ms } for the initial navigation, and each navigate action's result carries its own result.consent. cmp is the consent platform matched, or null when none was; action is optOut, optIn, hide (a cosmetic rule hid the banner), timeout (a banner was detected but not answered within 2 s), error, or none (nothing matched). No match never fails the chain. Default \"off\", so a chain that clicks the banner itself keeps working.")
    proxyRotation: Optional[ScrapeWithActionsRequestBrowserOptionsProxyRotation] = Field(default=None, description="Route the stealth browser through proxies you supply. Requires stealth: true (refused otherwise). Chromium engine only: refused on Camoufox, which applies its proxy at browser launch and shares that browser across calls. CrawlForge supplies no proxies; a residential proxy is what gets past an IP-reputation block that no fingerprint fixes. Proxies on loopback, private, link-local or metadata addresses are refused. Credentials are never echoed back: metadata.browserOptions shows them redacted.")


class ScrapeWithActionsRequestExtractionOptions(_RequestModel):
    """Content extraction options"""
    selectors: Optional[Dict[str, str]] = Field(default=None, description="Key-value pairs of data to extract using CSS selectors. Append @attr to a selector to read an attribute instead of the text (\"a.next@href\"); @value on an input, textarea or select reads what it holds after the actions (typed or selected), and any other @attr reads the attribute as written in the page's HTML.")
    includeMetadata: Optional[bool] = Field(default=True)
    includeLinks: Optional[bool] = Field(default=True)
    includeImages: Optional[bool] = Field(default=True)


class ScrapeWithActionsRequestRedactPii(_RequestModel):
    entities: Optional[List[str]] = Field(default=None, max_length=16)
    replace_style: Optional[Literal["tag", "mask", "remove"]] = Field(default=None)
    mode: Optional[Literal["fast", "model"]] = Field(default=None)


class ScrapeWithActionsRequest(_RequestModel):
    url: str = Field(description="The URL to scrape")
    actions: List[ScrapeWithActionsRequestActionsItem] = Field(description="Browser actions to perform before scraping (1-20). A snapshot action first lists the interactive elements on the page, including those inside open shadow roots and iframes, as @e refs (@e1, @e2, \u2026 in document order), which later actions can target in place of CSS selectors.")
    formats: Optional[List[Any]] = Field(default=["json"], description="Output formats for scraped content: markdown, html, json, text. For an image, add a {type:\"screenshot\"} action where you want it taken.")
    captureIntermediateStates: Optional[bool] = Field(default=False, description="Capture page state after each action: intermediateStates[] gets one entry per action (capturePoint is the action's 1-based position) with the url, title and the requested formats at that point")
    formAutoFill: Optional[ScrapeWithActionsRequestFormAutoFill] = Field(default=None, description="Form auto-fill configuration")
    browserOptions: Optional[ScrapeWithActionsRequestBrowserOptions] = Field(default=None, description="Browser configuration options")
    respect_robots: Optional[bool] = Field(default=True, description="Respect the target site's robots.txt. Omitted, the compliant default (true) applies: a URL disallowed for CrawlForge is refused before the browser opens and no credits are charged, and every navigate action is checked the same way. Setting this to false is honoured, returns a warning in the response, and is recorded against your API key.")
    extractionOptions: Optional[ScrapeWithActionsRequestExtractionOptions] = Field(default=None, description="Content extraction options")
    continueOnActionError: Optional[bool] = Field(default=False, description="Continue executing actions if one fails")
    maxRetries: Optional[float] = Field(default=0, description="Whole-chain retries on failure (0-3). A retry re-navigates to the starting URL and replays every action; each attempt is reported under attempts[]")
    screenshotOnError: Optional[bool] = Field(default=True, description="Capture screenshot when an error occurs")
    max_inline_chars: Optional[float] = Field(default=40000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")
    redact_pii: Optional[Union[bool, ScrapeWithActionsRequestRedactPii]] = Field(default=False, description="Remove personal data from the text this call returns, before it is stored or sent back. true is shorthand for { mode: \"fast\" }: every entity, tagged. As an object: entities (any of EMAIL, PHONE, FINANCIAL, SECRET; omitted or empty means all four, and any other name is a 400 rather than a silent no-op), replace_style (\"tag\" \u2192 <EMAIL>, \"mask\" \u2192 [REDACTED], \"remove\" \u2192 nothing; default \"tag\") and mode (\"fast\", the default, is regex-only and costs no extra credits; \"model\" covers PERSON and LOCATION, needs an LLM and is rejected here \u2014 use the CrawlForge MCP server). The response carries redaction: { entities, count, mode } inside data, saying what was removed. Detection is deliberately conservative: a card number must pass Luhn and an IBAN mod-97, so a false positive cannot silently destroy real page content. URLs, queries and identifiers the response uses to name what was fetched are left intact, and counters derived from the text (content_length, word_count, character_count) describe the text as it was extracted, before redaction.")


class SearchWebRequestRedactPii(_RequestModel):
    entities: Optional[List[str]] = Field(default=None, max_length=16)
    replace_style: Optional[Literal["tag", "mask", "remove"]] = Field(default=None)
    mode: Optional[Literal["fast", "model"]] = Field(default=None)


class SearchWebRequest(_RequestModel):
    query: Optional[str] = Field(default=None, min_length=1, description="Search query. Provide exactly one of query or queries.")
    queries: Optional[List[str]] = Field(default=None, min_length=1, max_length=10, description="Between 1 and 10 search queries to run in one call, as an alternative to query. Each runs the same search query does, and the payloads come back as results_by_query: a list in the order the queries were sent, each entry carrying its own query plus that search \u2014 or query and error when that one search failed. queries echoes the input and count is its length. Charged per query that returned results: the projection is the published price times every query sent, and the actual charge falls below it by every query that failed. A batch in which none succeeded still returns 200, with an error entry for each, and costs nothing. Provide exactly one of query or queries.")
    limit: Optional[float] = Field(default=10, ge=1, le=100, description="Number of results (1-100)")
    offset: Optional[float] = Field(default=0, ge=0, description="Results offset for pagination")
    lang: Optional[str] = Field(default=None, description="Language code (e.g., \"en\")")
    site: Optional[str] = Field(default=None, description="Limit search to specific site")
    safe_search: Optional[bool] = Field(default=None, description="Enable safe search")
    time_range: Optional[Literal["day", "week", "month", "year", "all"]] = Field(default=None, description="Time range: day, week, month, year, all")
    file_type: Optional[str] = Field(default=None, description="Filter by file type (e.g., \"pdf\")")
    redact_pii: Optional[Union[bool, SearchWebRequestRedactPii]] = Field(default=None, description="Remove personal data from the text this call returns, before it is stored or sent back. true is shorthand for { mode: \"fast\" }: every entity, tagged. As an object: entities (any of EMAIL, PHONE, FINANCIAL, SECRET; omitted or empty means all four, and any other name is a 400 rather than a silent no-op), replace_style (\"tag\" \u2192 <EMAIL>, \"mask\" \u2192 [REDACTED], \"remove\" \u2192 nothing; default \"tag\") and mode (\"fast\", the default, is regex-only and costs no extra credits; \"model\" covers PERSON and LOCATION, needs an LLM and is rejected here \u2014 use the CrawlForge MCP server). The response carries redaction: { entities, count, mode } inside data, saying what was removed. Detection is deliberately conservative: a card number must pass Luhn and an IBAN mod-97, so a false positive cannot silently destroy real page content. URLs, queries and identifiers the response uses to name what was fetched are left intact, and counters derived from the text (content_length, word_count, character_count) describe the text as it was extracted, before redaction.")
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")


class SerpRankRequest(_RequestModel):
    keyword: str = Field(min_length=1, description="The search query to check ranking for")
    target: str = Field(min_length=1, description="Domain or URL to locate in the results (e.g. 'example.com'). Matched by host, not exact URL: a URL is reduced to its host, and any page on that host or its subdomains counts")
    depth: Optional[float] = Field(default=30, ge=10, le=200, description="How many results to scan (10-200, default 30); deeper scans take longer. Credits stay at 5 at any depth")
    device: Optional[Literal["desktop", "mobile"]] = Field(default="desktop", description="Device to emulate: desktop or mobile")
    language_code: Optional[str] = Field(default="en", description="Language code (e.g. 'en')")
    location_name: Optional[str] = Field(default="United States", description="Location, e.g. 'United States' or 'London,England,United Kingdom'")
    location_code: Optional[float] = Field(default=None, description="Numeric DataForSEO location code (overrides location_name)")


class StealthModeRequestStealthConfig(_RequestModel):
    """Stealth browser configuration. Applies to the call it is passed on and is not remembered. Chromium applies customUserAgent, customViewport, locale and timezone per call. On camoufox customUserAgent and customViewport are not applied, locale is fixed when the browser launches, and behind a proxy locale and timezone come from the exit IP; each of these is reported in `warnings`."""
    level: Optional[Literal["basic", "medium", "advanced"]] = Field(default="medium")
    randomizeFingerprint: Optional[bool] = Field(default=True)
    hideWebDriver: Optional[bool] = Field(default=True)
    blockWebRTC: Optional[bool] = Field(default=True)
    simulateHumanBehavior: Optional[bool] = Field(default=True)
    customUserAgent: Optional[str] = Field(default=None)
    locale: Optional[str] = Field(default="en-US")
    timezone: Optional[str] = Field(default=None)


class StealthModeRequestRedactPii(_RequestModel):
    entities: Optional[List[str]] = Field(default=None, max_length=16)
    replace_style: Optional[Literal["tag", "mask", "remove"]] = Field(default=None)
    mode: Optional[Literal["fast", "model"]] = Field(default=None)


class StealthModeRequest(_RequestModel):
    operation: Optional[Literal["scrape", "configure", "create_context", "create_page", "get_stats", "cleanup"]] = Field(default="configure", description="Stealth operation to perform. \"scrape\" creates a context, navigates to url, returns the requested formats and tears the context down, all in one billed call. \"configure\" validates stealthConfig and returns it with defaults filled in; nothing is stored. \"create_context\": a stealth context to run create_page in. \"create_page\": navigate urlToTest in that context and report status, title and any challenge page; the page is closed before the call returns. \"get_stats\": the backend's open contexts, browser and proxy state. \"cleanup\": close the browser and every context.")
    stealthConfig: Optional[StealthModeRequestStealthConfig] = Field(default=None, description="Stealth browser configuration. Applies to the call it is passed on and is not remembered. Chromium applies customUserAgent, customViewport, locale and timezone per call. On camoufox customUserAgent and customViewport are not applied, locale is fixed when the browser launches, and behind a proxy locale and timezone come from the exit IP; each of these is reported in `warnings`.")
    engine: Optional[Literal["playwright", "camoufox"]] = Field(default="playwright", description="Browser engine (camoufox only where installed on the backend)")
    contextId: Optional[str] = Field(default=None, description="Browser context ID for page operations (from a create_context call)")
    urlToTest: Optional[str] = Field(default=None, description="create_page: the URL to navigate to and check")
    url: Optional[str] = Field(default=None, description="URL to scrape. Required for operation \"scrape\"; the other operations use urlToTest instead.")
    formats: Optional[List[Any]] = Field(default=["markdown"], description="Formats operation \"scrape\" returns: markdown, html, text, links, metadata, screenshot. A screenshot comes back as a crawlforge://screenshot/{id} resource URI, not inline base64 \u2014 this endpoint passes that URI through without resolving it, so for now screenshot is usable only from the CrawlForge MCP server.")
    wait_for: Optional[float] = Field(default=None, description="Extra wait after page load, in ms (0-30000), for content that renders after DOMContentLoaded")
    verbose: Optional[bool] = Field(default=False, description="Return the full generated fingerprint from create_context instead of a summary")
    respect_robots: Optional[bool] = Field(default=True, description="Respect the target site's robots.txt. Omitted, the compliant default (true) applies: a URL disallowed for CrawlForge is refused before any browser is launched and no credits are charged, and every navigation is checked the same way. The rule is matched against the CrawlForge product token even though the stealth browser presents a randomized User-Agent, so a site owner's \"User-agent: CrawlForge\" directive binds stealth traffic too. Setting this to false is honoured, returns a warning in the response, and is recorded against your API key.")
    max_inline_chars: Optional[float] = Field(default=40000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")
    redact_pii: Optional[Union[bool, StealthModeRequestRedactPii]] = Field(default=False, description="Remove personal data from the text this call returns, before it is stored or sent back. true is shorthand for { mode: \"fast\" }: every entity, tagged. As an object: entities (any of EMAIL, PHONE, FINANCIAL, SECRET; omitted or empty means all four, and any other name is a 400 rather than a silent no-op), replace_style (\"tag\" \u2192 <EMAIL>, \"mask\" \u2192 [REDACTED], \"remove\" \u2192 nothing; default \"tag\") and mode (\"fast\", the default, is regex-only and costs no extra credits; \"model\" covers PERSON and LOCATION, needs an LLM and is rejected here \u2014 use the CrawlForge MCP server). The response carries redaction: { entities, count, mode } inside data, saying what was removed. Detection is deliberately conservative: a card number must pass Luhn and an IBAN mod-97, so a false positive cannot silently destroy real page content. URLs, queries and identifiers the response uses to name what was fetched are left intact, and counters derived from the text (content_length, word_count, character_count) describe the text as it was extracted, before redaction.")


class SummarizeContentRequest(_RequestModel):
    url: Optional[str] = Field(default=None, description="URL to fetch and summarize content from")
    content: Optional[str] = Field(default=None, description="Direct content to summarize (if URL not provided)")
    respect_robots: Optional[bool] = Field(default=True, description="Fetch the origin's robots.txt and refuse a url it disallows for CrawlForge. A missing or unreachable robots.txt is treated as no restrictions. Returns 403 ROBOTS_DISALLOWED, and no credits are charged. Ignored when summarizing supplied content.")
    max_sentences: Optional[float] = Field(default=5, ge=1, le=20, description="Maximum sentences in summary (1-20)")
    summary_type: Optional[Literal["extractive", "key_points", "brief"]] = Field(default="extractive", description="Type of summary to generate")
    include_metadata: Optional[bool] = Field(default=False, description="Include page metadata in response")
    timeout: Optional[float] = Field(default=10000, ge=1000, le=30000, description="Request timeout in milliseconds (1000-30000)")


class TrackChangesRequest(_RequestModel):
    url: str = Field(description="URL of the webpage to track")
    operation: Optional[Literal["create_baseline", "compare", "monitor"]] = Field(default="compare", description="create_baseline captures and stores the current page text (kept 90 days). compare fetches the page again and diffs it against the stored baseline. monitor creates a hosted monitor that fetches and compares the page on a schedule; creating it costs nothing, and each scheduled check bills 3 credits per target that was fetched and compared. Manage monitors at /api/v1/monitors or in the dashboard.")
    selector: Optional[str] = Field(default=None, description="CSS selector to scope tracking to part of the page (e.g. \".pricing-table\"). Baselines are stored per (url, selector) pair; 422 if the selector matches nothing.")
    update_baseline: Optional[bool] = Field(default=False, description="compare only: overwrite the stored baseline with the freshly fetched content after diffing")
    respect_robots: Optional[bool] = Field(default=True, description="create_baseline and compare: fetch the origin's robots.txt and refuse the URL if it disallows CrawlForge. A missing or unreachable robots.txt is treated as no restrictions. Returns 403 ROBOTS_DISALLOWED, and no credits are charged. Hosted monitors always respect robots.txt; a disallowed target is reported as a page error.")
    schedule: Optional[str] = Field(default=None, description="monitor only: five-field cron expression, evaluated in UTC, for how often the monitor checks the page (default \"0 * * * *\", hourly). Consecutive runs must be at least 5 minutes apart; 400 VALIDATION_ERROR otherwise.")
    notify_emails: Optional[List[str]] = Field(default=None, max_length=5, description="monitor only: up to 5 addresses that receive a summary email when a check finds new, changed, blocked or errored pages")
    webhook_url: Optional[str] = Field(default=None, description="monitor only: an https endpoint that receives a signed POST (monitor.page per changed page, then monitor.check.completed) after every check. The signing secret is returned once, as webhook_secret on the created monitor.")


REQUEST_MODELS = (
    AgentRequest,
    AnalyzeContentRequest,
    BatchScrapeRequest,
    BrowserSessionRequest,
    CrawlDeepRequest,
    DeepResearchRequest,
    ExtractContentRequest,
    ExtractEmbeddedStateRequest,
    ExtractLinksRequest,
    ExtractMetadataRequest,
    ExtractStructuredRequest,
    ExtractTextRequest,
    ExtractWithLlmRequest,
    FetchUrlRequest,
    GenerateLlmsTxtRequest,
    GetBatchResultsRequest,
    ListOllamaModelsRequest,
    LocalizationRequest,
    MapSiteRequest,
    ProcessDocumentRequest,
    ReadResultRequest,
    RedditSearchRequest,
    ScrapeRequest,
    ScrapeStructuredRequest,
    ScrapeTemplateRequest,
    ScrapeWithActionsRequest,
    SearchWebRequest,
    SerpRankRequest,
    StealthModeRequest,
    SummarizeContentRequest,
    TrackChangesRequest,
)
