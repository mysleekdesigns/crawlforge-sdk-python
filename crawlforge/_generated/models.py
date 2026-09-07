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
    "ScrapeWithActionsRequestActionsItem",
    "ScrapeWithActionsRequestFormAutoFill",
    "ScrapeWithActionsRequestBrowserOptions",
    "ScrapeWithActionsRequestExtractionOptions",
    "ScrapeWithActionsRequest",
    "SearchWebRequestRedactPii",
    "SearchWebRequest",
    "SerpRankRequest",
    "StealthModeRequestStealthConfig",
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
    fields: Optional[List[BatchScrapeRequestExtractionTemplateFieldsItem]] = Field(default=None, description="Fields to extract from each page: { name, selector (CSS), attribute? }. Without attribute the element text is returned; xpath is not supported.")
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
    clean_html: Optional[bool] = Field(default=True, description="Return clean text instead of HTML")
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
    max_inline_chars: Optional[int] = Field(default=None, ge=1000, le=10000000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")


class ExtractLinksRequest(_RequestModel):
    html: Optional[str] = Field(default=None, min_length=1, description="HTML content to extract links from")
    url: Optional[str] = Field(default=None, description="URL to fetch and extract links from")
    base_url: Optional[str] = Field(default=None, description="Base URL for resolving relative links")
    filter_domains: Optional[List[str]] = Field(default=None, description="Only include links from specified domains")
    include_external: Optional[bool] = Field(default=True, description="Include external links")
    include_internal: Optional[bool] = Field(default=True, description="Include internal links")
    include_anchors: Optional[bool] = Field(default=False, description="Include anchor links (#fragment)")
    deduplicate: Optional[bool] = Field(default=True, description="Remove duplicate links")
    include_metadata: Optional[bool] = Field(default=True, description="Include link metadata (title, domain, etc.)")
    respect_robots: Optional[bool] = Field(default=True)


class ExtractMetadataRequest(_RequestModel):
    html: Optional[str] = Field(default=None, min_length=1, description="HTML content to extract metadata from")
    url: Optional[str] = Field(default=None, description="URL to fetch and extract metadata from")
    include_social: Optional[bool] = Field(default=True, description="Include Open Graph and Twitter Card metadata")
    include_seo: Optional[bool] = Field(default=True, description="Include SEO-related metadata")
    include_technical: Optional[bool] = Field(default=True, description="Include technical metadata (scripts, stylesheets, etc.)")
    include_structured_data: Optional[bool] = Field(default=True, description="Include structured data (JSON-LD, microdata)")
    respect_robots: Optional[bool] = Field(default=True)


class ExtractStructuredRequestSchema(_RequestModel):
    """JSON Schema defining the data structure to extract"""
    type: Optional[str] = Field(default=None)
    properties: Dict[str, Any] = Field()
    required: Optional[List[str]] = Field(default=None)


class ExtractStructuredRequestLlmConfig(_RequestModel):
    """Accepted for compatibility; this endpoint never calls an LLM provider"""
    provider: Optional[str] = Field(default=None)
    apiKey: Optional[str] = Field(default=None)


class ExtractStructuredRequest(_RequestModel):
    url: str = Field(description="The URL to extract structured data from")
    schema_: ExtractStructuredRequestSchema = Field(alias="schema", description="JSON Schema defining the data structure to extract")
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
    clean: Optional[bool] = Field(default=True, description="Remove extra whitespace and formatting")
    preserve_links: Optional[bool] = Field(default=False, description="Include links in the extracted text")
    preserve_formatting: Optional[bool] = Field(default=False, description="Preserve basic HTML formatting")
    max_length: Optional[float] = Field(default=None, ge=1, le=1000000, description="Maximum length of extracted text")
    respect_robots: Optional[bool] = Field(default=True)
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


class GetBatchResultsRequest(_RequestModel):
    batchId: str = Field(min_length=1, description="The batch_id returned by batch_scrape")
    page: Optional[int] = Field(default=1, ge=1, le=9007199254740991, description="Page number to retrieve (1-based)")
    limit: Optional[int] = Field(default=25, ge=1, le=100, description="Results per page (1-100)")


class ListOllamaModelsRequest(_RequestModel):
    pass


class LocalizationRequest(_RequestModel):
    url: str = Field(description="The URL to analyze for localization")
    target_language: Optional[str] = Field(default=None, description="Target language code (e.g., \"en\", \"fr\", \"es\")")
    target_country: Optional[str] = Field(default=None, description="Target country code (e.g., \"US\", \"FR\", \"JP\")")
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


class ProcessDocumentRequestRedactPii(_RequestModel):
    entities: Optional[List[str]] = Field(default=None, max_length=16)
    replace_style: Optional[Literal["tag", "mask", "remove"]] = Field(default=None)
    mode: Optional[Literal["fast", "model"]] = Field(default=None)


class ProcessDocumentRequest(_RequestModel):
    url: str = Field(description="URL of the document to process (max 25MB)")
    respect_robots: Optional[bool] = Field(default=True, description="Fetch the origin's robots.txt and refuse the document if it disallows CrawlForge. A missing or unreachable robots.txt is treated as no restrictions. Returns 403 ROBOTS_DISALLOWED, and no credits are charged.")
    document_type: Optional[Literal["pdf", "docx", "xlsx", "csv", "txt", "auto"]] = Field(default="auto", description="Document type; auto-detected from Content-Type, URL extension, then content sniffing")
    extract_text: Optional[bool] = Field(default=True, description="Extract text content (capped at 200000 characters; PDFs read up to 200 pages)")
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
    source: Optional[Literal["auto", "arctic_shift", "pullpush", "web_discovery"]] = Field(default="auto", description="Force a specific backend: auto, arctic_shift, web_discovery (unscoped keyword searches only \u2014 posts or comments), or pullpush (no longer serves automated clients; kept for when it returns)")


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
    formats: Optional[List[Union[Literal["markdown", "html", "rawHtml", "text", "links", "metadata", "screenshot", "json-schema"], ScrapeRequestFormatsItemHighlights, ScrapeRequestFormatsItemQuestion]]] = Field(default=cast('List[Union[Literal["markdown", "html", "rawHtml", "text", "links", "metadata", "screenshot", "json-schema"], ScrapeRequestFormatsItemHighlights, ScrapeRequestFormatsItemQuestion]]', ["markdown"]), min_length=1, description="Output formats: markdown, html, rawHtml, text, links, metadata, plus two query-scoped object formats. { type: 'highlights', query, max_highlights (1-50, default 10), mode } returns the sentences and code blocks matching the query, verbatim, each with an offset and length into the markdown format of the same call (table rows too on the MCP server; this API flattens tables to text). { type: 'question', question, mode } returns an answer assembled from the best-matching passages, with its evidence. mode defaults to 'extractive'; mode 'model' needs an LLM and is rejected here, as are the 'screenshot' and 'json-schema' formats, which require the CrawlForge MCP server (browser/LLM).")
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


class ScrapeWithActionsRequestActionsItem(_RequestModel):
    type: Optional[Literal["wait", "click", "type", "press", "scroll", "screenshot", "executeJavaScript", "select", "hover", "navigate"]] = Field(default=None, description="Action to perform")
    selector: Optional[str] = Field(default=None, description="CSS selector the action targets")
    text: Optional[str] = Field(default=None, description="type: text to enter")
    key: Optional[str] = Field(default=None, description="press: key to press")
    value: Optional[str] = Field(default=None, description="select: one option to choose in the <select> named by selector. Matches an option by its value or by its visible label.")
    values: Optional[List[Any]] = Field(default=None, description="select: several options to choose, same matching rule as value. Supply value or values, not neither.")
    url: Optional[str] = Field(default=None, description="navigate: URL to load mid-chain, in the same browser session. Passes the same robots.txt and SSRF checks as the top-level url.")
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
    position: Optional[Dict[str, Any]] = Field(default=None, description="click/hover: relative position { x, y }")
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


class ScrapeWithActionsRequestFormAutoFill(_RequestModel):
    """Form auto-fill configuration"""
    fields: Optional[List[Any]] = Field(default=None, description="Fields to fill: { selector, value, type: text|select|checkbox|radio|file, waitAfter }")
    submitSelector: Optional[str] = Field(default=None, description="Selector of the submit control")
    waitAfterSubmit: Optional[float] = Field(default=2000, description="Wait after submit in ms (0-30000)")


class ScrapeWithActionsRequestBrowserOptions(_RequestModel):
    """Browser configuration options"""
    headless: Optional[bool] = Field(default=True)
    userAgent: Optional[str] = Field(default=None)
    viewportWidth: Optional[float] = Field(default=1280, description="800-1920")
    viewportHeight: Optional[float] = Field(default=720, description="600-1080")
    timeout: Optional[float] = Field(default=30000, description="Browser timeout in ms (10000-120000)")
    stealth: Optional[bool] = Field(default=False, description="Run the action chain in the stealth Chromium engine at its medium profile instead of the standard browser pool. The boolean is the only knob \u2014 level, fingerprint randomization and engine are not settable from here. Slower to start; it renders JavaScript, it does not solve challenges.")


class ScrapeWithActionsRequestExtractionOptions(_RequestModel):
    """Content extraction options"""
    selectors: Optional[Dict[str, Any]] = Field(default=None, description="Key-value pairs of data to extract using CSS selectors")
    includeMetadata: Optional[bool] = Field(default=True)
    includeLinks: Optional[bool] = Field(default=True)
    includeImages: Optional[bool] = Field(default=True)


class ScrapeWithActionsRequest(_RequestModel):
    url: str = Field(description="The URL to scrape")
    actions: List[ScrapeWithActionsRequestActionsItem] = Field(description="Browser actions to perform before scraping (1-20)")
    formats: Optional[List[Any]] = Field(default=["json"], description="Output formats: markdown, html, json, text, screenshots")
    captureIntermediateStates: Optional[bool] = Field(default=False, description="Capture page state after each action")
    captureScreenshots: Optional[bool] = Field(default=True, description="Take screenshots during action execution")
    formAutoFill: Optional[ScrapeWithActionsRequestFormAutoFill] = Field(default=None, description="Form auto-fill configuration")
    browserOptions: Optional[ScrapeWithActionsRequestBrowserOptions] = Field(default=None, description="Browser configuration options")
    respect_robots: Optional[bool] = Field(default=True, description="Respect the target site's robots.txt. Omitted, the compliant default (true) applies: a URL disallowed for CrawlForge is refused before the browser opens and no credits are charged, and every navigate action is checked the same way. Setting this to false is honoured, returns a warning in the response, and is recorded against your API key.")
    extractionOptions: Optional[ScrapeWithActionsRequestExtractionOptions] = Field(default=None, description="Content extraction options")
    continueOnActionError: Optional[bool] = Field(default=False, description="Continue executing actions if one fails")
    maxRetries: Optional[float] = Field(default=1, description="Maximum retry attempts on failure (0-3)")
    screenshotOnError: Optional[bool] = Field(default=True, description="Capture screenshot when an error occurs")
    max_inline_chars: Optional[float] = Field(default=40000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")
    redact_pii: Optional[Union[bool, Dict[str, Any]]] = Field(default=False, description="Remove personal data from the text this call returns, before it is stored or sent back. true is shorthand for { mode: \"fast\" }: every entity, tagged. As an object: entities (any of EMAIL, PHONE, FINANCIAL, SECRET; omitted or empty means all four, and any other name is a 400 rather than a silent no-op), replace_style (\"tag\" \u2192 <EMAIL>, \"mask\" \u2192 [REDACTED], \"remove\" \u2192 nothing; default \"tag\") and mode (\"fast\", the default, is regex-only and costs no extra credits; \"model\" covers PERSON and LOCATION, needs an LLM and is rejected here \u2014 use the CrawlForge MCP server). The response carries redaction: { entities, count, mode } inside data, saying what was removed. Detection is deliberately conservative: a card number must pass Luhn and an IBAN mod-97, so a false positive cannot silently destroy real page content. URLs, queries and identifiers the response uses to name what was fetched are left intact, and counters derived from the text (content_length, word_count, character_count) describe the text as it was extracted, before redaction.")


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


class SerpRankRequest(_RequestModel):
    keyword: str = Field(min_length=1, description="The search query to check ranking for")
    target: str = Field(min_length=1, description="Domain or URL to locate in the results (e.g. 'example.com')")
    depth: Optional[float] = Field(default=100, ge=10, le=200, description="How many results to scan (10-200; 100 = 1 page of cost)")
    device: Optional[Literal["desktop", "mobile"]] = Field(default="desktop", description="Device to emulate: desktop or mobile")
    language_code: Optional[str] = Field(default="en", description="Language code (e.g. 'en')")
    location_name: Optional[str] = Field(default="United States", description="Location, e.g. 'United States' or 'London,England,United Kingdom'")
    location_code: Optional[float] = Field(default=None, description="Numeric DataForSEO location code (overrides location_name)")


class StealthModeRequestStealthConfig(_RequestModel):
    """Stealth browser configuration"""
    level: Optional[Literal["basic", "medium", "advanced"]] = Field(default="medium")
    randomizeFingerprint: Optional[bool] = Field(default=True)
    hideWebDriver: Optional[bool] = Field(default=True)
    blockWebRTC: Optional[bool] = Field(default=True)
    simulateHumanBehavior: Optional[bool] = Field(default=True)
    customUserAgent: Optional[str] = Field(default=None)
    locale: Optional[str] = Field(default="en-US")
    timezone: Optional[str] = Field(default=None)


class StealthModeRequest(_RequestModel):
    operation: Optional[Literal["scrape", "configure", "enable", "disable", "create_context", "create_page", "get_stats", "cleanup"]] = Field(default="configure", description="Stealth operation to perform. \"scrape\" creates a context, navigates to url, returns the requested formats and tears the context down, all in one billed call.")
    stealthConfig: Optional[StealthModeRequestStealthConfig] = Field(default=None, description="Stealth browser configuration")
    engine: Optional[Literal["playwright", "camoufox"]] = Field(default="playwright", description="Browser engine (camoufox only where installed on the backend)")
    contextId: Optional[str] = Field(default=None, description="Browser context ID for page operations (from a create_context call)")
    urlToTest: Optional[str] = Field(default=None, description="URL to navigate to when creating a page")
    url: Optional[str] = Field(default=None, description="URL to scrape. Required for operation \"scrape\"; the other operations use urlToTest instead.")
    formats: Optional[List[Any]] = Field(default=["markdown"], description="Formats operation \"scrape\" returns: markdown, html, text, links, metadata, screenshot. A screenshot comes back as a crawlforge://screenshot/{id} resource URI, not inline base64 \u2014 this endpoint passes that URI through without resolving it, so for now screenshot is usable only from the CrawlForge MCP server.")
    wait_for: Optional[float] = Field(default=None, description="Extra wait after page load, in ms (0-30000), for content that renders after DOMContentLoaded")
    verbose: Optional[bool] = Field(default=False, description="Return the full generated fingerprint from create_context instead of a summary")
    respect_robots: Optional[bool] = Field(default=True, description="Respect the target site's robots.txt. Omitted, the compliant default (true) applies: a URL disallowed for CrawlForge is refused before any browser is launched and no credits are charged, and every navigation is checked the same way. The rule is matched against the CrawlForge product token even though the stealth browser presents a randomized User-Agent, so a site owner's \"User-agent: CrawlForge\" directive binds stealth traffic too. Setting this to false is honoured, returns a warning in the response, and is recorded against your API key.")
    max_inline_chars: Optional[float] = Field(default=40000, description="Largest result returned inline, in characters of its JSON (1000-10000000; env CRAWLFORGE_MAX_INLINE_CHARS sets the default). Over it, the result is stored for 1 hour and the response carries a preview, a result_handle, total_chars and truncated: true; read the rest with read_result (1 credit).")
    redact_pii: Optional[Union[bool, Dict[str, Any]]] = Field(default=False, description="Remove personal data from the text this call returns, before it is stored or sent back. true is shorthand for { mode: \"fast\" }: every entity, tagged. As an object: entities (any of EMAIL, PHONE, FINANCIAL, SECRET; omitted or empty means all four, and any other name is a 400 rather than a silent no-op), replace_style (\"tag\" \u2192 <EMAIL>, \"mask\" \u2192 [REDACTED], \"remove\" \u2192 nothing; default \"tag\") and mode (\"fast\", the default, is regex-only and costs no extra credits; \"model\" covers PERSON and LOCATION, needs an LLM and is rejected here \u2014 use the CrawlForge MCP server). The response carries redaction: { entities, count, mode } inside data, saying what was removed. Detection is deliberately conservative: a card number must pass Luhn and an IBAN mod-97, so a false positive cannot silently destroy real page content. URLs, queries and identifiers the response uses to name what was fetched are left intact, and counters derived from the text (content_length, word_count, character_count) describe the text as it was extracted, before redaction.")


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
    operation: Optional[Literal["create_baseline", "compare", "monitor"]] = Field(default="compare", description="create_baseline captures and stores the current page text (kept 90 days). compare fetches the page again and diffs it against the stored baseline. monitor (scheduled checks) is not yet available on the hosted REST API and returns 501 \u2014 use the CrawlForge MCP server for scheduled monitoring.")
    selector: Optional[str] = Field(default=None, description="CSS selector to scope tracking to part of the page (e.g. \".pricing-table\"). Baselines are stored per (url, selector) pair; 422 if the selector matches nothing.")
    update_baseline: Optional[bool] = Field(default=False, description="compare only: overwrite the stored baseline with the freshly fetched content after diffing")
    respect_robots: Optional[bool] = Field(default=True, description="Fetch the origin's robots.txt and refuse the URL if it disallows CrawlForge. A missing or unreachable robots.txt is treated as no restrictions. Returns 403 ROBOTS_DISALLOWED for both create_baseline and compare, and no credits are charged.")


REQUEST_MODELS = (
    AgentRequest,
    AnalyzeContentRequest,
    BatchScrapeRequest,
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
