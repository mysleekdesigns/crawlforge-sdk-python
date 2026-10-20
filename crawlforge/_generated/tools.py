# Generated from openapi.json by scripts/generate.py. Do not edit by hand.

"""One typed method per tool, generated from openapi.json, as client mixins."""


from typing import Any, Dict, List, Literal, Optional, Union

from crawlforge._generated.models import (
    AgentRequest,
    AnalyzeContentRequest,
    BatchScrapeRequest,
    BatchScrapeRequestBatchConfig,
    BatchScrapeRequestExtractionTemplate,
    BatchScrapeRequestOptions,
    BatchScrapeRequestOutputConfig,
    BatchScrapeRequestRedactPii,
    BatchScrapeRequestUrlsItem,
    BrowserSessionRequest,
    BrowserSessionRequestActionsItem,
    BrowserSessionRequestRedactPii,
    BrowserSessionRequestViewport,
    CrawlDeepRequest,
    CrawlDeepRequestRedactPii,
    DeepResearchRequest,
    DeepResearchRequestResearchScope,
    ExtractContentRequest,
    ExtractContentRequestRedactPii,
    ExtractEmbeddedStateRequest,
    ExtractLinksRequest,
    ExtractMetadataRequest,
    ExtractStructuredRequest,
    ExtractStructuredRequestLlmConfig,
    ExtractStructuredRequestSchema,
    ExtractTextRequest,
    ExtractTextRequestRedactPii,
    ExtractWithLlmRequest,
    FetchUrlRequest,
    GenerateLlmsTxtRequest,
    GenerateLlmsTxtRequestAnalysisOptions,
    GenerateLlmsTxtRequestOutputOptions,
    GetBatchResultsRequest,
    ListOllamaModelsRequest,
    LocalizationRequest,
    MapSiteRequest,
    ProcessDocumentRequest,
    ProcessDocumentRequestRedactPii,
    ReadResultRequest,
    RedditSearchRequest,
    ScrapeRequest,
    ScrapeRequestFormatsItemHighlights,
    ScrapeRequestFormatsItemQuestion,
    ScrapeRequestRedactPii,
    ScrapeStructuredRequest,
    ScrapeTemplateRequest,
    ScrapeWithActionsRequest,
    ScrapeWithActionsRequestActionsItem,
    ScrapeWithActionsRequestBrowserOptions,
    ScrapeWithActionsRequestExtractionOptions,
    ScrapeWithActionsRequestFormAutoFill,
    ScrapeWithActionsRequestRedactPii,
    SearchWebRequest,
    SearchWebRequestRedactPii,
    SerpRankRequest,
    StealthModeRequest,
    StealthModeRequestRedactPii,
    StealthModeRequestStealthConfig,
    SummarizeContentRequest,
    TrackChangesRequest,
)
from crawlforge.types import ToolResult, ToolSpec

TOOLS: Dict[str, ToolSpec] = {
    "agent": ToolSpec(
        name="agent",
        credits=18,
        credits_note="8 per run, plus 5 for each walled page (challenge, 403/429, empty shell, timeout) the agent gets by retrying it in a stealth browser, at most 2 a run; a retry blocked again is free. The published 18 is the ceiling reserved before the run; the charge is what ran, and the response reports it as credits_used.",
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/agent",
        summary="Autonomous research/extraction from a natural-language prompt \u2014 no URLs required. Plans search queries, fetches and filters relevant pages, and returns a prose or structured answer under hard safety caps. Agent runs can exceed the REST API's ~50s window (the MCP tool allows 120s) \u2014 keep maxSteps/maxUrls small, or use the CrawlForge MCP server for long runs.",
        request_model=AgentRequest,
    ),
    "analyze_content": ToolSpec(
        name="analyze_content",
        credits=3,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/analyze-content",
        summary="Analyze web content for language, keywords, sentiment, and readability",
        request_model=AnalyzeContentRequest,
    ),
    "batch_scrape": ToolSpec(
        name="batch_scrape",
        credits=5,
        credits_note="5 per URL attempted (skipped URLs are not charged)",
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/batch-scrape",
        summary="Fetch up to 50 URLs concurrently in one synchronous call, returning title, text, and optional CSS-extracted fields per URL",
        request_model=BatchScrapeRequest,
    ),
    "browser_session": ToolSpec(
        name="browser_session",
        credits=3,
        credits_note="Priced per operation, not per call: open 3, read 2, and snapshot, act, screenshot, close and list 1 each. The published 3 is the ceiling \u2014 it is what an unrecognised operation costs and what is reserved before the body is read, and the charge drops to the operation's own price. A login-then-read flow (open, snapshot, act, act, read, close) costs 9.",
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/browser-session",
        summary="Drive a browser across several calls, keeping the page, its cookies and its login in between. The loop is: open a session on a URL, snapshot it to list the interactive elements as refs (@e1, @e2 ...), act on those refs, read the content (the whole page by default, onlyMainContent: true for the main article block alone), close. Because the page stays open you can look before each step instead of committing to a whole chain up front, so a wrong selector costs one call rather than all of them. Not for a page that renders without interaction (scrape), and not for an interaction you can write out in advance \u2014 that is one scrape_with_actions call.",
        request_model=BrowserSessionRequest,
    ),
    "crawl_deep": ToolSpec(
        name="crawl_deep",
        credits=4,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/crawl-deep",
        summary="Crawl websites deeply using breadth-first search to discover and extract content",
        request_model=CrawlDeepRequest,
    ),
    "deep_research": ToolSpec(
        name="deep_research",
        credits=10,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/deep-research",
        summary="Multi-query web research: runs web searches, fetches the top sources, and returns the most relevant passages verbatim with citations. Synthesis is extractive (no LLM on the hosted API) \u2014 for LLM-synthesized research use the CrawlForge MCP server.",
        request_model=DeepResearchRequest,
    ),
    "extract_content": ToolSpec(
        name="extract_content",
        credits=2,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/extract-content",
        summary="Extract main article content from web pages using readability detection",
        request_model=ExtractContentRequest,
    ),
    "extract_embedded_state": ToolSpec(
        name="extract_embedded_state",
        credits=2,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/extract-embedded-state",
        summary="Return the JSON state a page already ships in its own HTML: __NEXT_DATA__, React Server Component flight chunks (self.__next_f, \"$<id>\" references between rows resolved, plus a data_rows index of the rows carrying data), __NUXT__ and Nuxt 3's __NUXT_DATA__ (decoded), SvelteKit kit.start data, __APOLLO_STATE__, __INITIAL_STATE__, __PRELOADED_STATE__, ytInitialData, ytInitialPlayerResponse, __remixContext and other window globals (JSON, or a JavaScript literal evaluated statically \u2014 no page code runs), Inertia data-page, Shopify meta and product JSON, JSON data-* attributes and <script type=\"application/json\"> blocks. One fetch, exact values, and no LLM in the extraction path \u2014 the numbers come from the site's own serialized state, so they cannot be fabricated. Sources are reported in \"found\" with their sizes; use \"path\" to return one subtree instead of a multi-megabyte blob, keys_only to see its shape first, or find to list the paths of one key. A bot-defence wall or an empty shell carrying no state returns success: false, unbilled; with escalate: true the same call renders the page once in a stealth browser and reads the state from that instead.",
        request_model=ExtractEmbeddedStateRequest,
    ),
    "extract_links": ToolSpec(
        name="extract_links",
        credits=1,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/extract-links",
        summary="Extract and analyze all links from HTML content. A url is fetched once (15 s timeout; a 429 or 503 whose Retry-After is 10 s or less is retried once after that wait). A PDF or other binary returns 415 UNSUPPORTED_CONTENT_TYPE with next_step process_document; a JSON body returns no links and a warning. A bot wall is a BLOCKED error, unbilled; with escalate: true the same call renders the page once in a stealth browser and reads the links from that instead. An empty client-side shell succeeds with rendered: false and the warning \"page renders client-side; use scrape\".",
        request_model=ExtractLinksRequest,
    ),
    "extract_metadata": ToolSpec(
        name="extract_metadata",
        credits=1,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/extract-metadata",
        summary="Extract comprehensive metadata from HTML including SEO, social, and technical information",
        request_model=ExtractMetadataRequest,
    ),
    "extract_structured": ToolSpec(
        name="extract_structured",
        credits=3,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/extract-structured",
        summary="Extract structured data matching a JSON Schema from CSS selector hints, JSON-LD structured data, and OpenGraph/meta tags. LLM-guided extraction is available via the CrawlForge MCP server, not this endpoint.",
        request_model=ExtractStructuredRequest,
    ),
    "extract_text": ToolSpec(
        name="extract_text",
        credits=1,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/extract-text",
        summary="Extract clean text content from HTML with various formatting options. A url is fetched once (15 s timeout; a 429 or 503 whose Retry-After is 10 s or less is retried once after that wait). A PDF or other binary returns 415 UNSUPPORTED_CONTENT_TYPE with next_step process_document; a JSON body is returned as text with a warning. A bot wall is a BLOCKED error, unbilled; with escalate: true the same call renders the page once in a stealth browser and extracts the text from that instead. An empty client-side shell succeeds with rendered: false and the warning \"page renders client-side; use scrape\".",
        request_model=ExtractTextRequest,
    ),
    "extract_with_llm": ToolSpec(
        name="extract_with_llm",
        credits=3,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/extract-with-llm",
        summary="Extract structured data from a URL or text using a natural-language prompt. On a locally-run MCP server this defaults to local Ollama; provider \"openai\" or \"anthropic\" use cloud models.",
        request_model=ExtractWithLlmRequest,
    ),
    "fetch_url": ToolSpec(
        name="fetch_url",
        credits=1,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/fetch-url",
        summary="Fetch content from a URL with optional headers and configuration",
        request_model=FetchUrlRequest,
    ),
    "generate_llms_txt": ToolSpec(
        name="generate_llms_txt",
        credits=5,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/generate-llms-txt",
        summary="Generate llms.txt (and optionally llms-full.txt) from a real analysis of the site: fetches the target page, robots.txt, and sitemap.xml, then reads up to 8 key same-domain pages (about/docs/pricing/blog/api/contact/faq and similar) for their titles, descriptions, and main text.",
        request_model=GenerateLlmsTxtRequest,
    ),
    "get_batch_results": ToolSpec(
        name="get_batch_results",
        credits=1,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/get-batch-results",
        summary="Retrieve paginated results for a batch_scrape job by batchId. Results are stored for 24h after the batch completes and are only readable by the account that submitted the batch. batch_scrape runs synchronously, so a stored result set is always complete and the response reports status \"completed\".",
        request_model=GetBatchResultsRequest,
    ),
    "list_ollama_models": ToolSpec(
        name="list_ollama_models",
        credits=1,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/list-ollama-models",
        summary="Lists the Ollama models installed on the machine running the MCP server. Use this to discover which model values you can pass to extract_with_llm.",
        request_model=ListOllamaModelsRequest,
    ),
    "localization": ToolSpec(
        name="localization",
        credits=2,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/localization",
        summary="Audit the language and region signals of one page: html lang, the Content-Language header, hreflang alternates, the language detected in the visible text, and geo meta tags. It reads that page and applies nothing to any other call: target_language and target_country shape this one request only. No proxy is used, so the request leaves from the same address as every other tool and a geo-block is not lifted (a regional block follows the exit IP). To request a page in a language elsewhere, pass it on that call: fetch_url headers {\"Accept-Language\": ...} or stealth_mode stealthConfig {locale, timezone}; scrape has no locale parameter. The CrawlForge MCP server's localization tool is a different surface (configure_country and other operations) that returns a country's locale values and likewise applies none.",
        request_model=LocalizationRequest,
    ),
    "map_site": ToolSpec(
        name="map_site",
        credits=2,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/map-site",
        summary="Enumerate a site's pages: reads {origin}/sitemap.xml when available (up to 500 URLs, following up to 3 child sitemaps), otherwise falls back to a bounded breadth-first crawl (up to 30 pages, ~18s budget)",
        request_model=MapSiteRequest,
    ),
    "process_document": ToolSpec(
        name="process_document",
        credits=2,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/process-document",
        summary="Fetch a document by URL and extract its real text, metadata, and tables. Supported on this endpoint: PDF (text, metadata, tables via pdf-parse), CSV (text + parsed rows), TXT, and HTML (text + metadata). DOCX/XLSX return 501 and are supported by the CrawlForge MCP server.",
        request_model=ProcessDocumentRequest,
    ),
    "read_result": ToolSpec(
        name="read_result",
        credits=1,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/read-result",
        summary="Read part of a stored result. A tool whose result exceeded max_inline_chars returned a preview and a result_handle; this reads the stored copy by character range (slice), by case-insensitive literal search with context and offsets (search), by line (lines), or by dotted JSON path (json_path). Results are kept for 1 hour and are readable only by the account that produced them. Nothing is fetched.",
        request_model=ReadResultRequest,
    ),
    "reddit_search": ToolSpec(
        name="reddit_search",
        credits=5,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/reddit-search",
        summary="Search Reddit posts/comments or read a full comment thread \u2014 reads the Arctic Shift community archive (reddit.com blocks direct scraping). A scoped search (subreddit or author) queries the archive directly. A Reddit-wide keyword search finds posts with a site-restricted web search and then reads those posts from the archive \u2014 or, in comments mode, searches each of the first five posts' comments for the keywords \u2014 because Arctic Shift cannot keyword-search across all of Reddit. A scoped comment search Arctic Shift times out on is retried over the last 7d and 3d and reports window_applied. Arctic Shift is tried first and PullPush (api.pullpush.io) second: when Arctic Shift or the web-discovery path fails a posts or comments search, PullPush is queried and the response reports fallback_used. PullPush has refused automated clients since August 2026, so that fallback usually reports its refusal too.",
        request_model=RedditSearchRequest,
    ),
    "scrape": ToolSpec(
        name="scrape",
        credits=2,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/scrape",
        summary="Unified single-fetch, multi-format extraction. One fetch serves every requested format: markdown, html, rawHtml, text, links, metadata. A bot-defence challenge page returns success: false with blocked.vendor whatever its HTTP status; an empty shell or an error placeholder served as HTTP 200 is a failure too. Neither is charged. A PDF or other binary returns 415 UNSUPPORTED_CONTENT_TYPE, unbilled; use process_document. A success whose markdown is empty carries a warning saying so. With escalate: true that same call renders the page once in a stealth browser and returns the formats from it, instead of returning the block.",
        request_model=ScrapeRequest,
    ),
    "scrape_structured": ToolSpec(
        name="scrape_structured",
        credits=2,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/scrape-structured",
        summary="Extract structured data from HTML using CSS selectors",
        request_model=ScrapeStructuredRequest,
    ),
    "scrape_template": ToolSpec(
        name="scrape_template",
        credits=1,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/scrape-template",
        summary="Pre-built scrapers for popular sites and public APIs \u2014 no schema or selectors required. Three modes: name a template and pass a URL; pass template \"auto\" with a URL to have the matching template picked (the response reports which one it chose); or pass template \"list\" to enumerate them. Templates come in two kinds, reported as \"mode\" by the list. An entity template returns one record from one page. A list connector returns N records from one call, as data.items with a data.count \u2014 that covers the job-board group (Greenhouse, Lever, Ashby, Workable, Recruitee, Teamtailor), which reads a company's whole board from its ATS API, the government group (NHTSA vPIC VIN decoding, NPPES NPI provider registry), which reads free keyless federal registries, and shopify-collection, which lists a whole storefront collection. A list connector is driven either by a URL or by \"params\" \u2014 e.g. { \"template\": \"greenhouse-jobs\", \"params\": { \"company\": \"stripe\" } }. Sites that block plain HTTP fetches (e.g. Amazon) may return sparse data here; the CrawlForge MCP server version uses stealth browsing for those. reddit-thread reads the post from the Arctic Shift archive, because reddit.com blocks direct scraping; the reddit_search tool reads the comment tree. linkedin-profile and tweet are retired \u2014 those sites' robots.txt disallow every keyless path \u2014 and naming one, or passing one of their URLs to \"auto\", returns 400 TEMPLATE_UNAVAILABLE with the reason and no charge. Several templates read a machine-readable endpoint rather than the rendered page \u2014 shopify-product reads the store's own /products/<handle>.json, npm-package reads the npm registry API, and every list connector reads its platform's API \u2014 and report the URL they actually read as \"fetched_url\". When a Shopify store refuses its JSON endpoint (401, 403, 404 or 410), shopify-product reads the product page's own schema.org JSON-LD instead: the record carries \"source\": \"json-ld\" and a warning says so, with per-variant stock, compare-at prices and option names null because JSON-LD does not carry them.",
        request_model=ScrapeTemplateRequest,
    ),
    "scrape_with_actions": ToolSpec(
        name="scrape_with_actions",
        credits=5,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/scrape-with-actions",
        summary="Interact with a page before scraping \u2014 click, type, press keys, hover, choose a select option, scroll, navigate on, run JavaScript, or wait for dynamic content. Use for SPAs, login-gated content, or multi-step flows. Set browserOptions.stealth to run the chain in a stealth browser context. A click or form submit that loads another page is a navigation too: it gets its own navigations entry (trigger names the action type), and finalUrl is where the chain ended. Screenshots are taken by {type:\"screenshot\"} actions (and on error) and stored as crawlforge://screenshot/{actionId} resources.",
        request_model=ScrapeWithActionsRequest,
    ),
    "search_web": ToolSpec(
        name="search_web",
        credits=5,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/search-web",
        summary="Search the live web (Brave Search API) and get ranked results as JSON. One query per call, or up to 10 in a single call with queries.",
        request_model=SearchWebRequest,
    ),
    "serp_rank": ToolSpec(
        name="serp_rank",
        credits=5,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/serp-rank",
        summary="Check a domain's organic position in Google search results for a keyword (powered by DataForSEO). One lookup is one sample: Google can return a different result set for the same query minutes apart, so compare several lookups before reading a change in rank. A result set that barely mentions the keyword, a likely decoy page, comes back with suspect: true and a warning",
        request_model=SerpRankRequest,
    ),
    "stealth_mode": ToolSpec(
        name="stealth_mode",
        credits=5,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/stealth-mode",
        summary="Stealth browser scraping for sites that block normal scrapers (Cloudflare, DataDome, bot detection). Use operation \"scrape\" for a one-call render of a single URL. create_context then create_page is a navigation and challenge check: create_page loads urlToTest, reports its status, title and any challenge page, and closes the page before the call returns, so nothing on it carries over to a later call. For work over several calls on one page (log in, then read; click, then read), use browser_session with stealth: true. Operation \"configure\" only validates a stealthConfig and returns it with the defaults filled in \u2014 it stores nothing, so pass stealthConfig on each scrape or create_context call that should use it.",
        request_model=StealthModeRequest,
    ),
    "summarize_content": ToolSpec(
        name="summarize_content",
        credits=4,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/summarize-content",
        summary="Generate intelligent summaries of web content using extractive summarization",
        request_model=SummarizeContentRequest,
    ),
    "track_changes": ToolSpec(
        name="track_changes",
        credits=3,
        credits_note=None,
        docs_url="https://www.crawlforge.dev/docs/api-reference/tools/track-changes",
        summary="Detect content changes on a page by comparing it against a stored baseline (create_baseline, then compare), or create a hosted monitor that checks it on a schedule (monitor)",
        request_model=TrackChangesRequest,
    ),
}
"""Every tool in the spec, keyed by name; credits are the operation's x-credits."""


class SyncToolsMixin:
    """Typed tool methods for CrawlForge. The client supplies _run_tool."""

    def _run_tool(self, tool: str, request: Any, params: Dict[str, Any]) -> ToolResult:
        raise NotImplementedError

    def agent(
        self,
        request: Optional[Union[AgentRequest, Dict[str, Any]]] = None,
        /,
        *,
        prompt: Optional[str] = None,
        urls: Optional[List[Any]] = None,
        schema: Optional[Dict[str, Any]] = None,
        model: Optional[Literal["default", "pro"]] = None,
        maxSteps: Optional[float] = None,
        maxUrls: Optional[float] = None,
        max_inline_chars: Optional[float] = None,
    ) -> ToolResult:
        """Autonomous research/extraction from a natural-language prompt — no URLs required. Plans search queries, fetches and filters relevant pages, and returns a prose or structured answer under hard safety caps. Agent runs can exceed the REST API's ~50s window (the MCP tool allows 120s) — keep maxSteps/maxUrls small, or use the CrawlForge MCP server for long runs.

        Costs 18 credits plus 8 per run, plus 5 for each walled page (challenge, 403/429, empty shell, timeout) the agent gets by retrying it in a stealth browser, at most 2 a run; a retry blocked again is free. The published 18 is the ceiling reserved before the run; the charge is what ran, and the response reports it as credits_used.. Docs: https://www.crawlforge.dev/docs/api-reference/tools/agent
        """
        return self._run_tool(
            "agent",
            request,
            {
                "prompt": prompt,
                "urls": urls,
                "schema": schema,
                "model": model,
                "maxSteps": maxSteps,
                "maxUrls": maxUrls,
                "max_inline_chars": max_inline_chars,
            },
        )

    def analyze_content(
        self,
        request: Optional[Union[AnalyzeContentRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        content: Optional[str] = None,
        analyze_sentiment: Optional[bool] = None,
        extract_keywords: Optional[bool] = None,
        detect_language: Optional[bool] = None,
        analyze_readability: Optional[bool] = None,
        timeout: Optional[float] = None,
        respect_robots: Optional[bool] = None,
    ) -> ToolResult:
        """Analyze web content for language, keywords, sentiment, and readability

        Costs 3 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/analyze-content
        """
        return self._run_tool(
            "analyze_content",
            request,
            {
                "url": url,
                "content": content,
                "analyze_sentiment": analyze_sentiment,
                "extract_keywords": extract_keywords,
                "detect_language": detect_language,
                "analyze_readability": analyze_readability,
                "timeout": timeout,
                "respect_robots": respect_robots,
            },
        )

    def batch_scrape(
        self,
        request: Optional[Union[BatchScrapeRequest, Dict[str, Any]]] = None,
        /,
        *,
        urls: Optional[List[Union[BatchScrapeRequestUrlsItem, Dict[str, Any]]]] = None,
        respect_robots: Optional[bool] = None,
        batch_config: Optional[Union[BatchScrapeRequestBatchConfig, Dict[str, Any]]] = None,
        extraction_template: Optional[Union[BatchScrapeRequestExtractionTemplate, Dict[str, Any]]] = None,
        output_config: Optional[Union[BatchScrapeRequestOutputConfig, Dict[str, Any]]] = None,
        options: Optional[Union[BatchScrapeRequestOptions, Dict[str, Any]]] = None,
        max_inline_chars: Optional[int] = None,
        redact_pii: Optional[Union[bool, BatchScrapeRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Fetch up to 50 URLs concurrently in one synchronous call, returning title, text, and optional CSS-extracted fields per URL

        Costs 5 credits plus 5 per URL attempted (skipped URLs are not charged). Docs: https://www.crawlforge.dev/docs/api-reference/tools/batch-scrape
        """
        return self._run_tool(
            "batch_scrape",
            request,
            {
                "urls": urls,
                "respect_robots": respect_robots,
                "batch_config": batch_config,
                "extraction_template": extraction_template,
                "output_config": output_config,
                "options": options,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    def browser_session(
        self,
        request: Optional[Union[BrowserSessionRequest, Dict[str, Any]]] = None,
        /,
        *,
        operation: Optional[Literal["open", "snapshot", "act", "read", "screenshot", "close", "list"]] = None,
        session_id: Optional[str] = None,
        url: Optional[str] = None,
        stealth: Optional[bool] = None,
        ttl: Optional[float] = None,
        activity_ttl: Optional[float] = None,
        viewport: Optional[Union[BrowserSessionRequestViewport, Dict[str, Any]]] = None,
        timeout: Optional[float] = None,
        respect_robots: Optional[bool] = None,
        interactive_only: Optional[bool] = None,
        max_nodes: Optional[float] = None,
        actions: Optional[List[Union[BrowserSessionRequestActionsItem, Dict[str, Any]]]] = None,
        continue_on_error: Optional[bool] = None,
        formats: Optional[List[Any]] = None,
        onlyMainContent: Optional[bool] = None,
        full_page: Optional[bool] = None,
        format: Optional[Literal["png", "jpeg"]] = None,
        quality: Optional[float] = None,
        selector: Optional[str] = None,
        max_inline_chars: Optional[float] = None,
        redact_pii: Optional[Union[bool, BrowserSessionRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Drive a browser across several calls, keeping the page, its cookies and its login in between. The loop is: open a session on a URL, snapshot it to list the interactive elements as refs (@e1, @e2 ...), act on those refs, read the content (the whole page by default, onlyMainContent: true for the main article block alone), close. Because the page stays open you can look before each step instead of committing to a whole chain up front, so a wrong selector costs one call rather than all of them. Not for a page that renders without interaction (scrape), and not for an interaction you can write out in advance — that is one scrape_with_actions call.

        Costs 3 credits plus Priced per operation, not per call: open 3, read 2, and snapshot, act, screenshot, close and list 1 each. The published 3 is the ceiling — it is what an unrecognised operation costs and what is reserved before the body is read, and the charge drops to the operation's own price. A login-then-read flow (open, snapshot, act, act, read, close) costs 9.. Docs: https://www.crawlforge.dev/docs/api-reference/tools/browser-session
        """
        return self._run_tool(
            "browser_session",
            request,
            {
                "operation": operation,
                "session_id": session_id,
                "url": url,
                "stealth": stealth,
                "ttl": ttl,
                "activity_ttl": activity_ttl,
                "viewport": viewport,
                "timeout": timeout,
                "respect_robots": respect_robots,
                "interactive_only": interactive_only,
                "max_nodes": max_nodes,
                "actions": actions,
                "continue_on_error": continue_on_error,
                "formats": formats,
                "onlyMainContent": onlyMainContent,
                "full_page": full_page,
                "format": format,
                "quality": quality,
                "selector": selector,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    def crawl_deep(
        self,
        request: Optional[Union[CrawlDeepRequest, Dict[str, Any]]] = None,
        /,
        *,
        start_url: Optional[str] = None,
        max_pages: Optional[float] = None,
        max_depth: Optional[float] = None,
        same_domain_only: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
        respect_robots_txt: Optional[bool] = None,
        crawl_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        max_inline_chars: Optional[int] = None,
        redact_pii: Optional[Union[bool, CrawlDeepRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Crawl websites deeply using breadth-first search to discover and extract content

        Costs 4 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/crawl-deep
        """
        return self._run_tool(
            "crawl_deep",
            request,
            {
                "start_url": start_url,
                "max_pages": max_pages,
                "max_depth": max_depth,
                "same_domain_only": same_domain_only,
                "respect_robots": respect_robots,
                "respect_robots_txt": respect_robots_txt,
                "crawl_delay": crawl_delay,
                "timeout": timeout,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    def deep_research(
        self,
        request: Optional[Union[DeepResearchRequest, Dict[str, Any]]] = None,
        /,
        *,
        research_query: Optional[str] = None,
        research_scope: Optional[Union[DeepResearchRequestResearchScope, Dict[str, Any]]] = None,
        max_sources: Optional[int] = None,
        respect_robots: Optional[bool] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Multi-query web research: runs web searches, fetches the top sources, and returns the most relevant passages verbatim with citations. Synthesis is extractive (no LLM on the hosted API) — for LLM-synthesized research use the CrawlForge MCP server.

        Costs 10 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/deep-research
        """
        return self._run_tool(
            "deep_research",
            request,
            {
                "research_query": research_query,
                "research_scope": research_scope,
                "max_sources": max_sources,
                "respect_robots": respect_robots,
                "max_inline_chars": max_inline_chars,
            },
        )

    def extract_content(
        self,
        request: Optional[Union[ExtractContentRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        include_images: Optional[bool] = None,
        include_links: Optional[bool] = None,
        clean_html: Optional[bool] = None,
        extract_main_content: Optional[bool] = None,
        timeout: Optional[float] = None,
        respect_robots: Optional[bool] = None,
        max_inline_chars: Optional[int] = None,
        redact_pii: Optional[Union[bool, ExtractContentRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Extract main article content from web pages using readability detection

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-content
        """
        return self._run_tool(
            "extract_content",
            request,
            {
                "url": url,
                "include_images": include_images,
                "include_links": include_links,
                "clean_html": clean_html,
                "extract_main_content": extract_main_content,
                "timeout": timeout,
                "respect_robots": respect_robots,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    def extract_embedded_state(
        self,
        request: Optional[Union[ExtractEmbeddedStateRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        path: Optional[str] = None,
        user_agent: Optional[str] = None,
        respect_robots: Optional[bool] = None,
        timeout: Optional[int] = None,
        keys_only: Optional[bool] = None,
        find: Optional[str] = None,
        raw: Optional[bool] = None,
        escalate: Optional[bool] = None,
        escalate_engine: Optional[Literal["playwright", "camoufox"]] = None,
        wait_for: Optional[int] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Return the JSON state a page already ships in its own HTML: __NEXT_DATA__, React Server Component flight chunks (self.__next_f, "$<id>" references between rows resolved, plus a data_rows index of the rows carrying data), __NUXT__ and Nuxt 3's __NUXT_DATA__ (decoded), SvelteKit kit.start data, __APOLLO_STATE__, __INITIAL_STATE__, __PRELOADED_STATE__, ytInitialData, ytInitialPlayerResponse, __remixContext and other window globals (JSON, or a JavaScript literal evaluated statically — no page code runs), Inertia data-page, Shopify meta and product JSON, JSON data-* attributes and <script type="application/json"> blocks. One fetch, exact values, and no LLM in the extraction path — the numbers come from the site's own serialized state, so they cannot be fabricated. Sources are reported in "found" with their sizes; use "path" to return one subtree instead of a multi-megabyte blob, keys_only to see its shape first, or find to list the paths of one key. A bot-defence wall or an empty shell carrying no state returns success: false, unbilled; with escalate: true the same call renders the page once in a stealth browser and reads the state from that instead.

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-embedded-state
        """
        return self._run_tool(
            "extract_embedded_state",
            request,
            {
                "url": url,
                "path": path,
                "user_agent": user_agent,
                "respect_robots": respect_robots,
                "timeout": timeout,
                "keys_only": keys_only,
                "find": find,
                "raw": raw,
                "escalate": escalate,
                "escalate_engine": escalate_engine,
                "wait_for": wait_for,
                "max_inline_chars": max_inline_chars,
            },
        )

    def extract_links(
        self,
        request: Optional[Union[ExtractLinksRequest, Dict[str, Any]]] = None,
        /,
        *,
        html: Optional[str] = None,
        url: Optional[str] = None,
        base_url: Optional[str] = None,
        filter_domains: Optional[List[str]] = None,
        include_external: Optional[bool] = None,
        include_internal: Optional[bool] = None,
        filter_external: Optional[bool] = None,
        include_anchors: Optional[bool] = None,
        deduplicate: Optional[bool] = None,
        include_metadata: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
        escalate: Optional[bool] = None,
        escalate_engine: Optional[Literal["playwright", "camoufox"]] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Extract and analyze all links from HTML content. A url is fetched once (15 s timeout; a 429 or 503 whose Retry-After is 10 s or less is retried once after that wait). A PDF or other binary returns 415 UNSUPPORTED_CONTENT_TYPE with next_step process_document; a JSON body returns no links and a warning. A bot wall is a BLOCKED error, unbilled; with escalate: true the same call renders the page once in a stealth browser and reads the links from that instead. An empty client-side shell succeeds with rendered: false and the warning "page renders client-side; use scrape".

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-links
        """
        return self._run_tool(
            "extract_links",
            request,
            {
                "html": html,
                "url": url,
                "base_url": base_url,
                "filter_domains": filter_domains,
                "include_external": include_external,
                "include_internal": include_internal,
                "filter_external": filter_external,
                "include_anchors": include_anchors,
                "deduplicate": deduplicate,
                "include_metadata": include_metadata,
                "respect_robots": respect_robots,
                "escalate": escalate,
                "escalate_engine": escalate_engine,
                "max_inline_chars": max_inline_chars,
            },
        )

    def extract_metadata(
        self,
        request: Optional[Union[ExtractMetadataRequest, Dict[str, Any]]] = None,
        /,
        *,
        html: Optional[str] = None,
        url: Optional[str] = None,
        include_social: Optional[bool] = None,
        include_seo: Optional[bool] = None,
        include_technical: Optional[bool] = None,
        include_structured_data: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Extract comprehensive metadata from HTML including SEO, social, and technical information

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-metadata
        """
        return self._run_tool(
            "extract_metadata",
            request,
            {
                "html": html,
                "url": url,
                "include_social": include_social,
                "include_seo": include_seo,
                "include_technical": include_technical,
                "include_structured_data": include_structured_data,
                "respect_robots": respect_robots,
                "max_inline_chars": max_inline_chars,
            },
        )

    def extract_structured(
        self,
        request: Optional[Union[ExtractStructuredRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        schema: Optional[Union[ExtractStructuredRequestSchema, Dict[str, Any]]] = None,
        prompt: Optional[str] = None,
        llmConfig: Optional[Union[ExtractStructuredRequestLlmConfig, Dict[str, Any]]] = None,
        selectorHints: Optional[Dict[str, str]] = None,
        fallbackToSelectors: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
    ) -> ToolResult:
        """Extract structured data matching a JSON Schema from CSS selector hints, JSON-LD structured data, and OpenGraph/meta tags. LLM-guided extraction is available via the CrawlForge MCP server, not this endpoint.

        Costs 3 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-structured
        """
        return self._run_tool(
            "extract_structured",
            request,
            {
                "url": url,
                "schema": schema,
                "prompt": prompt,
                "llmConfig": llmConfig,
                "selectorHints": selectorHints,
                "fallbackToSelectors": fallbackToSelectors,
                "respect_robots": respect_robots,
            },
        )

    def extract_text(
        self,
        request: Optional[Union[ExtractTextRequest, Dict[str, Any]]] = None,
        /,
        *,
        html: Optional[str] = None,
        url: Optional[str] = None,
        selector: Optional[str] = None,
        clean: Optional[bool] = None,
        preserve_links: Optional[bool] = None,
        preserve_formatting: Optional[bool] = None,
        max_length: Optional[float] = None,
        output_format: Optional[Literal["text", "markdown"]] = None,
        respect_robots: Optional[bool] = None,
        escalate: Optional[bool] = None,
        escalate_engine: Optional[Literal["playwright", "camoufox"]] = None,
        redact_pii: Optional[Union[bool, ExtractTextRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Extract clean text content from HTML with various formatting options. A url is fetched once (15 s timeout; a 429 or 503 whose Retry-After is 10 s or less is retried once after that wait). A PDF or other binary returns 415 UNSUPPORTED_CONTENT_TYPE with next_step process_document; a JSON body is returned as text with a warning. A bot wall is a BLOCKED error, unbilled; with escalate: true the same call renders the page once in a stealth browser and extracts the text from that instead. An empty client-side shell succeeds with rendered: false and the warning "page renders client-side; use scrape".

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-text
        """
        return self._run_tool(
            "extract_text",
            request,
            {
                "html": html,
                "url": url,
                "selector": selector,
                "clean": clean,
                "preserve_links": preserve_links,
                "preserve_formatting": preserve_formatting,
                "max_length": max_length,
                "output_format": output_format,
                "respect_robots": respect_robots,
                "escalate": escalate,
                "escalate_engine": escalate_engine,
                "redact_pii": redact_pii,
            },
        )

    def extract_with_llm(
        self,
        request: Optional[Union[ExtractWithLlmRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        content: Optional[str] = None,
        prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        provider: Optional[Literal["openai", "anthropic", "ollama", "auto"]] = None,
        model: Optional[str] = None,
        maxTokens: Optional[float] = None,
    ) -> ToolResult:
        """Extract structured data from a URL or text using a natural-language prompt. On a locally-run MCP server this defaults to local Ollama; provider "openai" or "anthropic" use cloud models.

        Costs 3 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-with-llm
        """
        return self._run_tool(
            "extract_with_llm",
            request,
            {
                "url": url,
                "content": content,
                "prompt": prompt,
                "schema": schema,
                "provider": provider,
                "model": model,
                "maxTokens": maxTokens,
            },
        )

    def fetch_url(
        self,
        request: Optional[Union[FetchUrlRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        follow_redirects: Optional[bool] = None,
        user_agent: Optional[str] = None,
        respect_robots: Optional[bool] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Fetch content from a URL with optional headers and configuration

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/fetch-url
        """
        return self._run_tool(
            "fetch_url",
            request,
            {
                "url": url,
                "headers": headers,
                "timeout": timeout,
                "follow_redirects": follow_redirects,
                "user_agent": user_agent,
                "respect_robots": respect_robots,
                "max_inline_chars": max_inline_chars,
            },
        )

    def generate_llms_txt(
        self,
        request: Optional[Union[GenerateLlmsTxtRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        respect_robots: Optional[bool] = None,
        format: Optional[Literal["both", "llms-txt", "llms-full-txt"]] = None,
        complianceLevel: Optional[Literal["basic", "standard", "strict"]] = None,
        analysisOptions: Optional[Union[GenerateLlmsTxtRequestAnalysisOptions, Dict[str, Any]]] = None,
        outputOptions: Optional[Union[GenerateLlmsTxtRequestOutputOptions, Dict[str, Any]]] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Generate llms.txt (and optionally llms-full.txt) from a real analysis of the site: fetches the target page, robots.txt, and sitemap.xml, then reads up to 8 key same-domain pages (about/docs/pricing/blog/api/contact/faq and similar) for their titles, descriptions, and main text.

        Costs 5 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/generate-llms-txt
        """
        return self._run_tool(
            "generate_llms_txt",
            request,
            {
                "url": url,
                "respect_robots": respect_robots,
                "format": format,
                "complianceLevel": complianceLevel,
                "analysisOptions": analysisOptions,
                "outputOptions": outputOptions,
                "max_inline_chars": max_inline_chars,
            },
        )

    def get_batch_results(
        self,
        request: Optional[Union[GetBatchResultsRequest, Dict[str, Any]]] = None,
        /,
        *,
        batchId: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> ToolResult:
        """Retrieve paginated results for a batch_scrape job by batchId. Results are stored for 24h after the batch completes and are only readable by the account that submitted the batch. batch_scrape runs synchronously, so a stored result set is always complete and the response reports status "completed".

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/get-batch-results
        """
        return self._run_tool(
            "get_batch_results",
            request,
            {
                "batchId": batchId,
                "page": page,
                "limit": limit,
            },
        )

    def list_ollama_models(
        self,
        request: Optional[Union[ListOllamaModelsRequest, Dict[str, Any]]] = None,
        /,
    ) -> ToolResult:
        """Lists the Ollama models installed on the machine running the MCP server. Use this to discover which model values you can pass to extract_with_llm.

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/list-ollama-models
        """
        return self._run_tool(
            "list_ollama_models",
            request,
            {
            },
        )

    def localization(
        self,
        request: Optional[Union[LocalizationRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        target_language: Optional[str] = None,
        target_country: Optional[str] = None,
        detect_language: Optional[bool] = None,
        extract_hreflang: Optional[bool] = None,
        check_geo_targeting: Optional[bool] = None,
        timeout: Optional[float] = None,
        respect_robots: Optional[bool] = None,
    ) -> ToolResult:
        """Audit the language and region signals of one page: html lang, the Content-Language header, hreflang alternates, the language detected in the visible text, and geo meta tags. It reads that page and applies nothing to any other call: target_language and target_country shape this one request only. No proxy is used, so the request leaves from the same address as every other tool and a geo-block is not lifted (a regional block follows the exit IP). To request a page in a language elsewhere, pass it on that call: fetch_url headers {"Accept-Language": ...} or stealth_mode stealthConfig {locale, timezone}; scrape has no locale parameter. The CrawlForge MCP server's localization tool is a different surface (configure_country and other operations) that returns a country's locale values and likewise applies none.

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/localization
        """
        return self._run_tool(
            "localization",
            request,
            {
                "url": url,
                "target_language": target_language,
                "target_country": target_country,
                "detect_language": detect_language,
                "extract_hreflang": extract_hreflang,
                "check_geo_targeting": check_geo_targeting,
                "timeout": timeout,
                "respect_robots": respect_robots,
            },
        )

    def map_site(
        self,
        request: Optional[Union[MapSiteRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        respect_robots: Optional[bool] = None,
        max_depth: Optional[float] = None,
        include_external: Optional[bool] = None,
        timeout: Optional[float] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Enumerate a site's pages: reads {origin}/sitemap.xml when available (up to 500 URLs, following up to 3 child sitemaps), otherwise falls back to a bounded breadth-first crawl (up to 30 pages, ~18s budget)

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/map-site
        """
        return self._run_tool(
            "map_site",
            request,
            {
                "url": url,
                "respect_robots": respect_robots,
                "max_depth": max_depth,
                "include_external": include_external,
                "timeout": timeout,
                "max_inline_chars": max_inline_chars,
            },
        )

    def process_document(
        self,
        request: Optional[Union[ProcessDocumentRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        respect_robots: Optional[bool] = None,
        document_type: Optional[Literal["pdf", "docx", "xlsx", "csv", "txt", "auto"]] = None,
        extract_text: Optional[bool] = None,
        extract_metadata: Optional[bool] = None,
        extract_tables: Optional[bool] = None,
        extract_images: Optional[bool] = None,
        timeout: Optional[float] = None,
        max_inline_chars: Optional[int] = None,
        redact_pii: Optional[Union[bool, ProcessDocumentRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Fetch a document by URL and extract its real text, metadata, and tables. Supported on this endpoint: PDF (text, metadata, tables via pdf-parse), CSV (text + parsed rows), TXT, and HTML (text + metadata). DOCX/XLSX return 501 and are supported by the CrawlForge MCP server.

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/process-document
        """
        return self._run_tool(
            "process_document",
            request,
            {
                "url": url,
                "respect_robots": respect_robots,
                "document_type": document_type,
                "extract_text": extract_text,
                "extract_metadata": extract_metadata,
                "extract_tables": extract_tables,
                "extract_images": extract_images,
                "timeout": timeout,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    def read_result(
        self,
        request: Optional[Union[ReadResultRequest, Dict[str, Any]]] = None,
        /,
        *,
        handle: Optional[str] = None,
        operation: Optional[Literal["slice", "search", "lines", "json_path"]] = None,
        offset: Optional[int] = None,
        length: Optional[int] = None,
        query: Optional[str] = None,
        max_matches: Optional[int] = None,
        path: Optional[str] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Read part of a stored result. A tool whose result exceeded max_inline_chars returned a preview and a result_handle; this reads the stored copy by character range (slice), by case-insensitive literal search with context and offsets (search), by line (lines), or by dotted JSON path (json_path). Results are kept for 1 hour and are readable only by the account that produced them. Nothing is fetched.

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/read-result
        """
        return self._run_tool(
            "read_result",
            request,
            {
                "handle": handle,
                "operation": operation,
                "offset": offset,
                "length": length,
                "query": query,
                "max_matches": max_matches,
                "path": path,
                "max_inline_chars": max_inline_chars,
            },
        )

    def reddit_search(
        self,
        request: Optional[Union[RedditSearchRequest, Dict[str, Any]]] = None,
        /,
        *,
        query: Optional[str] = None,
        subreddit: Optional[str] = None,
        author: Optional[str] = None,
        mode: Optional[Literal["posts", "comments", "thread"]] = None,
        link_id: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Literal["asc", "desc"]] = None,
        source: Optional[Literal["auto", "arctic_shift", "pullpush", "web_discovery"]] = None,
    ) -> ToolResult:
        """Search Reddit posts/comments or read a full comment thread — reads the Arctic Shift community archive (reddit.com blocks direct scraping). A scoped search (subreddit or author) queries the archive directly. A Reddit-wide keyword search finds posts with a site-restricted web search and then reads those posts from the archive — or, in comments mode, searches each of the first five posts' comments for the keywords — because Arctic Shift cannot keyword-search across all of Reddit. A scoped comment search Arctic Shift times out on is retried over the last 7d and 3d and reports window_applied. Arctic Shift is tried first and PullPush (api.pullpush.io) second: when Arctic Shift or the web-discovery path fails a posts or comments search, PullPush is queried and the response reports fallback_used. PullPush has refused automated clients since August 2026, so that fallback usually reports its refusal too.

        Costs 5 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/reddit-search
        """
        return self._run_tool(
            "reddit_search",
            request,
            {
                "query": query,
                "subreddit": subreddit,
                "author": author,
                "mode": mode,
                "link_id": link_id,
                "after": after,
                "before": before,
                "limit": limit,
                "sort": sort,
                "source": source,
            },
        )

    def scrape(
        self,
        request: Optional[Union[ScrapeRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        formats: Optional[List[Union[Literal["markdown", "html", "rawHtml", "text", "links", "metadata", "screenshot", "json-schema"], ScrapeRequestFormatsItemHighlights, Dict[str, Any], ScrapeRequestFormatsItemQuestion]]] = None,
        onlyMainContent: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
        escalate: Optional[bool] = None,
        escalate_engine: Optional[Literal["playwright", "camoufox"]] = None,
        max_inline_chars: Optional[int] = None,
        redact_pii: Optional[Union[bool, ScrapeRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Unified single-fetch, multi-format extraction. One fetch serves every requested format: markdown, html, rawHtml, text, links, metadata. A bot-defence challenge page returns success: false with blocked.vendor whatever its HTTP status; an empty shell or an error placeholder served as HTTP 200 is a failure too. Neither is charged. A PDF or other binary returns 415 UNSUPPORTED_CONTENT_TYPE, unbilled; use process_document. A success whose markdown is empty carries a warning saying so. With escalate: true that same call renders the page once in a stealth browser and returns the formats from it, instead of returning the block.

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/scrape
        """
        return self._run_tool(
            "scrape",
            request,
            {
                "url": url,
                "formats": formats,
                "onlyMainContent": onlyMainContent,
                "respect_robots": respect_robots,
                "escalate": escalate,
                "escalate_engine": escalate_engine,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    def scrape_structured(
        self,
        request: Optional[Union[ScrapeStructuredRequest, Dict[str, Any]]] = None,
        /,
        *,
        html: Optional[str] = None,
        url: Optional[str] = None,
        selectors: Optional[Dict[str, str]] = None,
        base_url: Optional[str] = None,
        multiple: Optional[bool] = None,
        clean_text: Optional[bool] = None,
        include_attributes: Optional[List[str]] = None,
        max_items: Optional[float] = None,
        respect_robots: Optional[bool] = None,
    ) -> ToolResult:
        """Extract structured data from HTML using CSS selectors

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/scrape-structured
        """
        return self._run_tool(
            "scrape_structured",
            request,
            {
                "html": html,
                "url": url,
                "selectors": selectors,
                "base_url": base_url,
                "multiple": multiple,
                "clean_text": clean_text,
                "include_attributes": include_attributes,
                "max_items": max_items,
                "respect_robots": respect_robots,
            },
        )

    def scrape_template(
        self,
        request: Optional[Union[ScrapeTemplateRequest, Dict[str, Any]]] = None,
        /,
        *,
        template: Optional[str] = None,
        url: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        respect_robots: Optional[bool] = None,
        timeout: Optional[int] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Pre-built scrapers for popular sites and public APIs — no schema or selectors required. Three modes: name a template and pass a URL; pass template "auto" with a URL to have the matching template picked (the response reports which one it chose); or pass template "list" to enumerate them. Templates come in two kinds, reported as "mode" by the list. An entity template returns one record from one page. A list connector returns N records from one call, as data.items with a data.count — that covers the job-board group (Greenhouse, Lever, Ashby, Workable, Recruitee, Teamtailor), which reads a company's whole board from its ATS API, the government group (NHTSA vPIC VIN decoding, NPPES NPI provider registry), which reads free keyless federal registries, and shopify-collection, which lists a whole storefront collection. A list connector is driven either by a URL or by "params" — e.g. { "template": "greenhouse-jobs", "params": { "company": "stripe" } }. Sites that block plain HTTP fetches (e.g. Amazon) may return sparse data here; the CrawlForge MCP server version uses stealth browsing for those. reddit-thread reads the post from the Arctic Shift archive, because reddit.com blocks direct scraping; the reddit_search tool reads the comment tree. linkedin-profile and tweet are retired — those sites' robots.txt disallow every keyless path — and naming one, or passing one of their URLs to "auto", returns 400 TEMPLATE_UNAVAILABLE with the reason and no charge. Several templates read a machine-readable endpoint rather than the rendered page — shopify-product reads the store's own /products/<handle>.json, npm-package reads the npm registry API, and every list connector reads its platform's API — and report the URL they actually read as "fetched_url". When a Shopify store refuses its JSON endpoint (401, 403, 404 or 410), shopify-product reads the product page's own schema.org JSON-LD instead: the record carries "source": "json-ld" and a warning says so, with per-variant stock, compare-at prices and option names null because JSON-LD does not carry them.

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/scrape-template
        """
        return self._run_tool(
            "scrape_template",
            request,
            {
                "template": template,
                "url": url,
                "params": params,
                "respect_robots": respect_robots,
                "timeout": timeout,
                "max_inline_chars": max_inline_chars,
            },
        )

    def scrape_with_actions(
        self,
        request: Optional[Union[ScrapeWithActionsRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        actions: Optional[List[Union[ScrapeWithActionsRequestActionsItem, Dict[str, Any]]]] = None,
        formats: Optional[List[Any]] = None,
        captureIntermediateStates: Optional[bool] = None,
        formAutoFill: Optional[Union[ScrapeWithActionsRequestFormAutoFill, Dict[str, Any]]] = None,
        browserOptions: Optional[Union[ScrapeWithActionsRequestBrowserOptions, Dict[str, Any]]] = None,
        respect_robots: Optional[bool] = None,
        extractionOptions: Optional[Union[ScrapeWithActionsRequestExtractionOptions, Dict[str, Any]]] = None,
        continueOnActionError: Optional[bool] = None,
        maxRetries: Optional[float] = None,
        screenshotOnError: Optional[bool] = None,
        max_inline_chars: Optional[float] = None,
        redact_pii: Optional[Union[bool, ScrapeWithActionsRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Interact with a page before scraping — click, type, press keys, hover, choose a select option, scroll, navigate on, run JavaScript, or wait for dynamic content. Use for SPAs, login-gated content, or multi-step flows. Set browserOptions.stealth to run the chain in a stealth browser context. A click or form submit that loads another page is a navigation too: it gets its own navigations entry (trigger names the action type), and finalUrl is where the chain ended. Screenshots are taken by {type:"screenshot"} actions (and on error) and stored as crawlforge://screenshot/{actionId} resources.

        Costs 5 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/scrape-with-actions
        """
        return self._run_tool(
            "scrape_with_actions",
            request,
            {
                "url": url,
                "actions": actions,
                "formats": formats,
                "captureIntermediateStates": captureIntermediateStates,
                "formAutoFill": formAutoFill,
                "browserOptions": browserOptions,
                "respect_robots": respect_robots,
                "extractionOptions": extractionOptions,
                "continueOnActionError": continueOnActionError,
                "maxRetries": maxRetries,
                "screenshotOnError": screenshotOnError,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    def search_web(
        self,
        request: Optional[Union[SearchWebRequest, Dict[str, Any]]] = None,
        /,
        *,
        query: Optional[str] = None,
        queries: Optional[List[str]] = None,
        limit: Optional[float] = None,
        offset: Optional[float] = None,
        lang: Optional[str] = None,
        site: Optional[str] = None,
        safe_search: Optional[bool] = None,
        time_range: Optional[Literal["day", "week", "month", "year", "all"]] = None,
        file_type: Optional[str] = None,
        redact_pii: Optional[Union[bool, SearchWebRequestRedactPii, Dict[str, Any]]] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Search the live web (Brave Search API) and get ranked results as JSON. One query per call, or up to 10 in a single call with queries.

        Costs 5 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/search-web
        """
        return self._run_tool(
            "search_web",
            request,
            {
                "query": query,
                "queries": queries,
                "limit": limit,
                "offset": offset,
                "lang": lang,
                "site": site,
                "safe_search": safe_search,
                "time_range": time_range,
                "file_type": file_type,
                "redact_pii": redact_pii,
                "max_inline_chars": max_inline_chars,
            },
        )

    def serp_rank(
        self,
        request: Optional[Union[SerpRankRequest, Dict[str, Any]]] = None,
        /,
        *,
        keyword: Optional[str] = None,
        target: Optional[str] = None,
        depth: Optional[float] = None,
        device: Optional[Literal["desktop", "mobile"]] = None,
        language_code: Optional[str] = None,
        location_name: Optional[str] = None,
        location_code: Optional[float] = None,
    ) -> ToolResult:
        """Check a domain's organic position in Google search results for a keyword (powered by DataForSEO). One lookup is one sample: Google can return a different result set for the same query minutes apart, so compare several lookups before reading a change in rank. A result set that barely mentions the keyword, a likely decoy page, comes back with suspect: true and a warning

        Costs 5 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/serp-rank
        """
        return self._run_tool(
            "serp_rank",
            request,
            {
                "keyword": keyword,
                "target": target,
                "depth": depth,
                "device": device,
                "language_code": language_code,
                "location_name": location_name,
                "location_code": location_code,
            },
        )

    def stealth_mode(
        self,
        request: Optional[Union[StealthModeRequest, Dict[str, Any]]] = None,
        /,
        *,
        operation: Optional[Literal["scrape", "configure", "create_context", "create_page", "get_stats", "cleanup"]] = None,
        stealthConfig: Optional[Union[StealthModeRequestStealthConfig, Dict[str, Any]]] = None,
        engine: Optional[Literal["playwright", "camoufox"]] = None,
        contextId: Optional[str] = None,
        urlToTest: Optional[str] = None,
        url: Optional[str] = None,
        formats: Optional[List[Any]] = None,
        wait_for: Optional[float] = None,
        verbose: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
        max_inline_chars: Optional[float] = None,
        redact_pii: Optional[Union[bool, StealthModeRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Stealth browser scraping for sites that block normal scrapers (Cloudflare, DataDome, bot detection). Use operation "scrape" for a one-call render of a single URL. create_context then create_page is a navigation and challenge check: create_page loads urlToTest, reports its status, title and any challenge page, and closes the page before the call returns, so nothing on it carries over to a later call. For work over several calls on one page (log in, then read; click, then read), use browser_session with stealth: true. Operation "configure" only validates a stealthConfig and returns it with the defaults filled in — it stores nothing, so pass stealthConfig on each scrape or create_context call that should use it.

        Costs 5 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/stealth-mode
        """
        return self._run_tool(
            "stealth_mode",
            request,
            {
                "operation": operation,
                "stealthConfig": stealthConfig,
                "engine": engine,
                "contextId": contextId,
                "urlToTest": urlToTest,
                "url": url,
                "formats": formats,
                "wait_for": wait_for,
                "verbose": verbose,
                "respect_robots": respect_robots,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    def summarize_content(
        self,
        request: Optional[Union[SummarizeContentRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        content: Optional[str] = None,
        respect_robots: Optional[bool] = None,
        max_sentences: Optional[float] = None,
        summary_type: Optional[Literal["extractive", "key_points", "brief"]] = None,
        include_metadata: Optional[bool] = None,
        timeout: Optional[float] = None,
    ) -> ToolResult:
        """Generate intelligent summaries of web content using extractive summarization

        Costs 4 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/summarize-content
        """
        return self._run_tool(
            "summarize_content",
            request,
            {
                "url": url,
                "content": content,
                "respect_robots": respect_robots,
                "max_sentences": max_sentences,
                "summary_type": summary_type,
                "include_metadata": include_metadata,
                "timeout": timeout,
            },
        )

    def track_changes(
        self,
        request: Optional[Union[TrackChangesRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        operation: Optional[Literal["create_baseline", "compare", "monitor"]] = None,
        selector: Optional[str] = None,
        update_baseline: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
        schedule: Optional[str] = None,
        notify_emails: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
    ) -> ToolResult:
        """Detect content changes on a page by comparing it against a stored baseline (create_baseline, then compare), or create a hosted monitor that checks it on a schedule (monitor)

        Costs 3 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/track-changes
        """
        return self._run_tool(
            "track_changes",
            request,
            {
                "url": url,
                "operation": operation,
                "selector": selector,
                "update_baseline": update_baseline,
                "respect_robots": respect_robots,
                "schedule": schedule,
                "notify_emails": notify_emails,
                "webhook_url": webhook_url,
            },
        )


class AsyncToolsMixin:
    """Typed tool methods for AsyncCrawlForge. The client supplies _run_tool."""

    async def _run_tool(
        self, tool: str, request: Any, params: Dict[str, Any]
    ) -> ToolResult:
        raise NotImplementedError

    async def agent(
        self,
        request: Optional[Union[AgentRequest, Dict[str, Any]]] = None,
        /,
        *,
        prompt: Optional[str] = None,
        urls: Optional[List[Any]] = None,
        schema: Optional[Dict[str, Any]] = None,
        model: Optional[Literal["default", "pro"]] = None,
        maxSteps: Optional[float] = None,
        maxUrls: Optional[float] = None,
        max_inline_chars: Optional[float] = None,
    ) -> ToolResult:
        """Autonomous research/extraction from a natural-language prompt — no URLs required. Plans search queries, fetches and filters relevant pages, and returns a prose or structured answer under hard safety caps. Agent runs can exceed the REST API's ~50s window (the MCP tool allows 120s) — keep maxSteps/maxUrls small, or use the CrawlForge MCP server for long runs.

        Costs 18 credits plus 8 per run, plus 5 for each walled page (challenge, 403/429, empty shell, timeout) the agent gets by retrying it in a stealth browser, at most 2 a run; a retry blocked again is free. The published 18 is the ceiling reserved before the run; the charge is what ran, and the response reports it as credits_used.. Docs: https://www.crawlforge.dev/docs/api-reference/tools/agent
        """
        return await self._run_tool(
            "agent",
            request,
            {
                "prompt": prompt,
                "urls": urls,
                "schema": schema,
                "model": model,
                "maxSteps": maxSteps,
                "maxUrls": maxUrls,
                "max_inline_chars": max_inline_chars,
            },
        )

    async def analyze_content(
        self,
        request: Optional[Union[AnalyzeContentRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        content: Optional[str] = None,
        analyze_sentiment: Optional[bool] = None,
        extract_keywords: Optional[bool] = None,
        detect_language: Optional[bool] = None,
        analyze_readability: Optional[bool] = None,
        timeout: Optional[float] = None,
        respect_robots: Optional[bool] = None,
    ) -> ToolResult:
        """Analyze web content for language, keywords, sentiment, and readability

        Costs 3 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/analyze-content
        """
        return await self._run_tool(
            "analyze_content",
            request,
            {
                "url": url,
                "content": content,
                "analyze_sentiment": analyze_sentiment,
                "extract_keywords": extract_keywords,
                "detect_language": detect_language,
                "analyze_readability": analyze_readability,
                "timeout": timeout,
                "respect_robots": respect_robots,
            },
        )

    async def batch_scrape(
        self,
        request: Optional[Union[BatchScrapeRequest, Dict[str, Any]]] = None,
        /,
        *,
        urls: Optional[List[Union[BatchScrapeRequestUrlsItem, Dict[str, Any]]]] = None,
        respect_robots: Optional[bool] = None,
        batch_config: Optional[Union[BatchScrapeRequestBatchConfig, Dict[str, Any]]] = None,
        extraction_template: Optional[Union[BatchScrapeRequestExtractionTemplate, Dict[str, Any]]] = None,
        output_config: Optional[Union[BatchScrapeRequestOutputConfig, Dict[str, Any]]] = None,
        options: Optional[Union[BatchScrapeRequestOptions, Dict[str, Any]]] = None,
        max_inline_chars: Optional[int] = None,
        redact_pii: Optional[Union[bool, BatchScrapeRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Fetch up to 50 URLs concurrently in one synchronous call, returning title, text, and optional CSS-extracted fields per URL

        Costs 5 credits plus 5 per URL attempted (skipped URLs are not charged). Docs: https://www.crawlforge.dev/docs/api-reference/tools/batch-scrape
        """
        return await self._run_tool(
            "batch_scrape",
            request,
            {
                "urls": urls,
                "respect_robots": respect_robots,
                "batch_config": batch_config,
                "extraction_template": extraction_template,
                "output_config": output_config,
                "options": options,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    async def browser_session(
        self,
        request: Optional[Union[BrowserSessionRequest, Dict[str, Any]]] = None,
        /,
        *,
        operation: Optional[Literal["open", "snapshot", "act", "read", "screenshot", "close", "list"]] = None,
        session_id: Optional[str] = None,
        url: Optional[str] = None,
        stealth: Optional[bool] = None,
        ttl: Optional[float] = None,
        activity_ttl: Optional[float] = None,
        viewport: Optional[Union[BrowserSessionRequestViewport, Dict[str, Any]]] = None,
        timeout: Optional[float] = None,
        respect_robots: Optional[bool] = None,
        interactive_only: Optional[bool] = None,
        max_nodes: Optional[float] = None,
        actions: Optional[List[Union[BrowserSessionRequestActionsItem, Dict[str, Any]]]] = None,
        continue_on_error: Optional[bool] = None,
        formats: Optional[List[Any]] = None,
        onlyMainContent: Optional[bool] = None,
        full_page: Optional[bool] = None,
        format: Optional[Literal["png", "jpeg"]] = None,
        quality: Optional[float] = None,
        selector: Optional[str] = None,
        max_inline_chars: Optional[float] = None,
        redact_pii: Optional[Union[bool, BrowserSessionRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Drive a browser across several calls, keeping the page, its cookies and its login in between. The loop is: open a session on a URL, snapshot it to list the interactive elements as refs (@e1, @e2 ...), act on those refs, read the content (the whole page by default, onlyMainContent: true for the main article block alone), close. Because the page stays open you can look before each step instead of committing to a whole chain up front, so a wrong selector costs one call rather than all of them. Not for a page that renders without interaction (scrape), and not for an interaction you can write out in advance — that is one scrape_with_actions call.

        Costs 3 credits plus Priced per operation, not per call: open 3, read 2, and snapshot, act, screenshot, close and list 1 each. The published 3 is the ceiling — it is what an unrecognised operation costs and what is reserved before the body is read, and the charge drops to the operation's own price. A login-then-read flow (open, snapshot, act, act, read, close) costs 9.. Docs: https://www.crawlforge.dev/docs/api-reference/tools/browser-session
        """
        return await self._run_tool(
            "browser_session",
            request,
            {
                "operation": operation,
                "session_id": session_id,
                "url": url,
                "stealth": stealth,
                "ttl": ttl,
                "activity_ttl": activity_ttl,
                "viewport": viewport,
                "timeout": timeout,
                "respect_robots": respect_robots,
                "interactive_only": interactive_only,
                "max_nodes": max_nodes,
                "actions": actions,
                "continue_on_error": continue_on_error,
                "formats": formats,
                "onlyMainContent": onlyMainContent,
                "full_page": full_page,
                "format": format,
                "quality": quality,
                "selector": selector,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    async def crawl_deep(
        self,
        request: Optional[Union[CrawlDeepRequest, Dict[str, Any]]] = None,
        /,
        *,
        start_url: Optional[str] = None,
        max_pages: Optional[float] = None,
        max_depth: Optional[float] = None,
        same_domain_only: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
        respect_robots_txt: Optional[bool] = None,
        crawl_delay: Optional[float] = None,
        timeout: Optional[float] = None,
        max_inline_chars: Optional[int] = None,
        redact_pii: Optional[Union[bool, CrawlDeepRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Crawl websites deeply using breadth-first search to discover and extract content

        Costs 4 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/crawl-deep
        """
        return await self._run_tool(
            "crawl_deep",
            request,
            {
                "start_url": start_url,
                "max_pages": max_pages,
                "max_depth": max_depth,
                "same_domain_only": same_domain_only,
                "respect_robots": respect_robots,
                "respect_robots_txt": respect_robots_txt,
                "crawl_delay": crawl_delay,
                "timeout": timeout,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    async def deep_research(
        self,
        request: Optional[Union[DeepResearchRequest, Dict[str, Any]]] = None,
        /,
        *,
        research_query: Optional[str] = None,
        research_scope: Optional[Union[DeepResearchRequestResearchScope, Dict[str, Any]]] = None,
        max_sources: Optional[int] = None,
        respect_robots: Optional[bool] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Multi-query web research: runs web searches, fetches the top sources, and returns the most relevant passages verbatim with citations. Synthesis is extractive (no LLM on the hosted API) — for LLM-synthesized research use the CrawlForge MCP server.

        Costs 10 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/deep-research
        """
        return await self._run_tool(
            "deep_research",
            request,
            {
                "research_query": research_query,
                "research_scope": research_scope,
                "max_sources": max_sources,
                "respect_robots": respect_robots,
                "max_inline_chars": max_inline_chars,
            },
        )

    async def extract_content(
        self,
        request: Optional[Union[ExtractContentRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        include_images: Optional[bool] = None,
        include_links: Optional[bool] = None,
        clean_html: Optional[bool] = None,
        extract_main_content: Optional[bool] = None,
        timeout: Optional[float] = None,
        respect_robots: Optional[bool] = None,
        max_inline_chars: Optional[int] = None,
        redact_pii: Optional[Union[bool, ExtractContentRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Extract main article content from web pages using readability detection

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-content
        """
        return await self._run_tool(
            "extract_content",
            request,
            {
                "url": url,
                "include_images": include_images,
                "include_links": include_links,
                "clean_html": clean_html,
                "extract_main_content": extract_main_content,
                "timeout": timeout,
                "respect_robots": respect_robots,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    async def extract_embedded_state(
        self,
        request: Optional[Union[ExtractEmbeddedStateRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        path: Optional[str] = None,
        user_agent: Optional[str] = None,
        respect_robots: Optional[bool] = None,
        timeout: Optional[int] = None,
        keys_only: Optional[bool] = None,
        find: Optional[str] = None,
        raw: Optional[bool] = None,
        escalate: Optional[bool] = None,
        escalate_engine: Optional[Literal["playwright", "camoufox"]] = None,
        wait_for: Optional[int] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Return the JSON state a page already ships in its own HTML: __NEXT_DATA__, React Server Component flight chunks (self.__next_f, "$<id>" references between rows resolved, plus a data_rows index of the rows carrying data), __NUXT__ and Nuxt 3's __NUXT_DATA__ (decoded), SvelteKit kit.start data, __APOLLO_STATE__, __INITIAL_STATE__, __PRELOADED_STATE__, ytInitialData, ytInitialPlayerResponse, __remixContext and other window globals (JSON, or a JavaScript literal evaluated statically — no page code runs), Inertia data-page, Shopify meta and product JSON, JSON data-* attributes and <script type="application/json"> blocks. One fetch, exact values, and no LLM in the extraction path — the numbers come from the site's own serialized state, so they cannot be fabricated. Sources are reported in "found" with their sizes; use "path" to return one subtree instead of a multi-megabyte blob, keys_only to see its shape first, or find to list the paths of one key. A bot-defence wall or an empty shell carrying no state returns success: false, unbilled; with escalate: true the same call renders the page once in a stealth browser and reads the state from that instead.

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-embedded-state
        """
        return await self._run_tool(
            "extract_embedded_state",
            request,
            {
                "url": url,
                "path": path,
                "user_agent": user_agent,
                "respect_robots": respect_robots,
                "timeout": timeout,
                "keys_only": keys_only,
                "find": find,
                "raw": raw,
                "escalate": escalate,
                "escalate_engine": escalate_engine,
                "wait_for": wait_for,
                "max_inline_chars": max_inline_chars,
            },
        )

    async def extract_links(
        self,
        request: Optional[Union[ExtractLinksRequest, Dict[str, Any]]] = None,
        /,
        *,
        html: Optional[str] = None,
        url: Optional[str] = None,
        base_url: Optional[str] = None,
        filter_domains: Optional[List[str]] = None,
        include_external: Optional[bool] = None,
        include_internal: Optional[bool] = None,
        filter_external: Optional[bool] = None,
        include_anchors: Optional[bool] = None,
        deduplicate: Optional[bool] = None,
        include_metadata: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
        escalate: Optional[bool] = None,
        escalate_engine: Optional[Literal["playwright", "camoufox"]] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Extract and analyze all links from HTML content. A url is fetched once (15 s timeout; a 429 or 503 whose Retry-After is 10 s or less is retried once after that wait). A PDF or other binary returns 415 UNSUPPORTED_CONTENT_TYPE with next_step process_document; a JSON body returns no links and a warning. A bot wall is a BLOCKED error, unbilled; with escalate: true the same call renders the page once in a stealth browser and reads the links from that instead. An empty client-side shell succeeds with rendered: false and the warning "page renders client-side; use scrape".

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-links
        """
        return await self._run_tool(
            "extract_links",
            request,
            {
                "html": html,
                "url": url,
                "base_url": base_url,
                "filter_domains": filter_domains,
                "include_external": include_external,
                "include_internal": include_internal,
                "filter_external": filter_external,
                "include_anchors": include_anchors,
                "deduplicate": deduplicate,
                "include_metadata": include_metadata,
                "respect_robots": respect_robots,
                "escalate": escalate,
                "escalate_engine": escalate_engine,
                "max_inline_chars": max_inline_chars,
            },
        )

    async def extract_metadata(
        self,
        request: Optional[Union[ExtractMetadataRequest, Dict[str, Any]]] = None,
        /,
        *,
        html: Optional[str] = None,
        url: Optional[str] = None,
        include_social: Optional[bool] = None,
        include_seo: Optional[bool] = None,
        include_technical: Optional[bool] = None,
        include_structured_data: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Extract comprehensive metadata from HTML including SEO, social, and technical information

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-metadata
        """
        return await self._run_tool(
            "extract_metadata",
            request,
            {
                "html": html,
                "url": url,
                "include_social": include_social,
                "include_seo": include_seo,
                "include_technical": include_technical,
                "include_structured_data": include_structured_data,
                "respect_robots": respect_robots,
                "max_inline_chars": max_inline_chars,
            },
        )

    async def extract_structured(
        self,
        request: Optional[Union[ExtractStructuredRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        schema: Optional[Union[ExtractStructuredRequestSchema, Dict[str, Any]]] = None,
        prompt: Optional[str] = None,
        llmConfig: Optional[Union[ExtractStructuredRequestLlmConfig, Dict[str, Any]]] = None,
        selectorHints: Optional[Dict[str, str]] = None,
        fallbackToSelectors: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
    ) -> ToolResult:
        """Extract structured data matching a JSON Schema from CSS selector hints, JSON-LD structured data, and OpenGraph/meta tags. LLM-guided extraction is available via the CrawlForge MCP server, not this endpoint.

        Costs 3 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-structured
        """
        return await self._run_tool(
            "extract_structured",
            request,
            {
                "url": url,
                "schema": schema,
                "prompt": prompt,
                "llmConfig": llmConfig,
                "selectorHints": selectorHints,
                "fallbackToSelectors": fallbackToSelectors,
                "respect_robots": respect_robots,
            },
        )

    async def extract_text(
        self,
        request: Optional[Union[ExtractTextRequest, Dict[str, Any]]] = None,
        /,
        *,
        html: Optional[str] = None,
        url: Optional[str] = None,
        selector: Optional[str] = None,
        clean: Optional[bool] = None,
        preserve_links: Optional[bool] = None,
        preserve_formatting: Optional[bool] = None,
        max_length: Optional[float] = None,
        output_format: Optional[Literal["text", "markdown"]] = None,
        respect_robots: Optional[bool] = None,
        escalate: Optional[bool] = None,
        escalate_engine: Optional[Literal["playwright", "camoufox"]] = None,
        redact_pii: Optional[Union[bool, ExtractTextRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Extract clean text content from HTML with various formatting options. A url is fetched once (15 s timeout; a 429 or 503 whose Retry-After is 10 s or less is retried once after that wait). A PDF or other binary returns 415 UNSUPPORTED_CONTENT_TYPE with next_step process_document; a JSON body is returned as text with a warning. A bot wall is a BLOCKED error, unbilled; with escalate: true the same call renders the page once in a stealth browser and extracts the text from that instead. An empty client-side shell succeeds with rendered: false and the warning "page renders client-side; use scrape".

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-text
        """
        return await self._run_tool(
            "extract_text",
            request,
            {
                "html": html,
                "url": url,
                "selector": selector,
                "clean": clean,
                "preserve_links": preserve_links,
                "preserve_formatting": preserve_formatting,
                "max_length": max_length,
                "output_format": output_format,
                "respect_robots": respect_robots,
                "escalate": escalate,
                "escalate_engine": escalate_engine,
                "redact_pii": redact_pii,
            },
        )

    async def extract_with_llm(
        self,
        request: Optional[Union[ExtractWithLlmRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        content: Optional[str] = None,
        prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        provider: Optional[Literal["openai", "anthropic", "ollama", "auto"]] = None,
        model: Optional[str] = None,
        maxTokens: Optional[float] = None,
    ) -> ToolResult:
        """Extract structured data from a URL or text using a natural-language prompt. On a locally-run MCP server this defaults to local Ollama; provider "openai" or "anthropic" use cloud models.

        Costs 3 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/extract-with-llm
        """
        return await self._run_tool(
            "extract_with_llm",
            request,
            {
                "url": url,
                "content": content,
                "prompt": prompt,
                "schema": schema,
                "provider": provider,
                "model": model,
                "maxTokens": maxTokens,
            },
        )

    async def fetch_url(
        self,
        request: Optional[Union[FetchUrlRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        follow_redirects: Optional[bool] = None,
        user_agent: Optional[str] = None,
        respect_robots: Optional[bool] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Fetch content from a URL with optional headers and configuration

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/fetch-url
        """
        return await self._run_tool(
            "fetch_url",
            request,
            {
                "url": url,
                "headers": headers,
                "timeout": timeout,
                "follow_redirects": follow_redirects,
                "user_agent": user_agent,
                "respect_robots": respect_robots,
                "max_inline_chars": max_inline_chars,
            },
        )

    async def generate_llms_txt(
        self,
        request: Optional[Union[GenerateLlmsTxtRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        respect_robots: Optional[bool] = None,
        format: Optional[Literal["both", "llms-txt", "llms-full-txt"]] = None,
        complianceLevel: Optional[Literal["basic", "standard", "strict"]] = None,
        analysisOptions: Optional[Union[GenerateLlmsTxtRequestAnalysisOptions, Dict[str, Any]]] = None,
        outputOptions: Optional[Union[GenerateLlmsTxtRequestOutputOptions, Dict[str, Any]]] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Generate llms.txt (and optionally llms-full.txt) from a real analysis of the site: fetches the target page, robots.txt, and sitemap.xml, then reads up to 8 key same-domain pages (about/docs/pricing/blog/api/contact/faq and similar) for their titles, descriptions, and main text.

        Costs 5 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/generate-llms-txt
        """
        return await self._run_tool(
            "generate_llms_txt",
            request,
            {
                "url": url,
                "respect_robots": respect_robots,
                "format": format,
                "complianceLevel": complianceLevel,
                "analysisOptions": analysisOptions,
                "outputOptions": outputOptions,
                "max_inline_chars": max_inline_chars,
            },
        )

    async def get_batch_results(
        self,
        request: Optional[Union[GetBatchResultsRequest, Dict[str, Any]]] = None,
        /,
        *,
        batchId: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> ToolResult:
        """Retrieve paginated results for a batch_scrape job by batchId. Results are stored for 24h after the batch completes and are only readable by the account that submitted the batch. batch_scrape runs synchronously, so a stored result set is always complete and the response reports status "completed".

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/get-batch-results
        """
        return await self._run_tool(
            "get_batch_results",
            request,
            {
                "batchId": batchId,
                "page": page,
                "limit": limit,
            },
        )

    async def list_ollama_models(
        self,
        request: Optional[Union[ListOllamaModelsRequest, Dict[str, Any]]] = None,
        /,
    ) -> ToolResult:
        """Lists the Ollama models installed on the machine running the MCP server. Use this to discover which model values you can pass to extract_with_llm.

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/list-ollama-models
        """
        return await self._run_tool(
            "list_ollama_models",
            request,
            {
            },
        )

    async def localization(
        self,
        request: Optional[Union[LocalizationRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        target_language: Optional[str] = None,
        target_country: Optional[str] = None,
        detect_language: Optional[bool] = None,
        extract_hreflang: Optional[bool] = None,
        check_geo_targeting: Optional[bool] = None,
        timeout: Optional[float] = None,
        respect_robots: Optional[bool] = None,
    ) -> ToolResult:
        """Audit the language and region signals of one page: html lang, the Content-Language header, hreflang alternates, the language detected in the visible text, and geo meta tags. It reads that page and applies nothing to any other call: target_language and target_country shape this one request only. No proxy is used, so the request leaves from the same address as every other tool and a geo-block is not lifted (a regional block follows the exit IP). To request a page in a language elsewhere, pass it on that call: fetch_url headers {"Accept-Language": ...} or stealth_mode stealthConfig {locale, timezone}; scrape has no locale parameter. The CrawlForge MCP server's localization tool is a different surface (configure_country and other operations) that returns a country's locale values and likewise applies none.

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/localization
        """
        return await self._run_tool(
            "localization",
            request,
            {
                "url": url,
                "target_language": target_language,
                "target_country": target_country,
                "detect_language": detect_language,
                "extract_hreflang": extract_hreflang,
                "check_geo_targeting": check_geo_targeting,
                "timeout": timeout,
                "respect_robots": respect_robots,
            },
        )

    async def map_site(
        self,
        request: Optional[Union[MapSiteRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        respect_robots: Optional[bool] = None,
        max_depth: Optional[float] = None,
        include_external: Optional[bool] = None,
        timeout: Optional[float] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Enumerate a site's pages: reads {origin}/sitemap.xml when available (up to 500 URLs, following up to 3 child sitemaps), otherwise falls back to a bounded breadth-first crawl (up to 30 pages, ~18s budget)

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/map-site
        """
        return await self._run_tool(
            "map_site",
            request,
            {
                "url": url,
                "respect_robots": respect_robots,
                "max_depth": max_depth,
                "include_external": include_external,
                "timeout": timeout,
                "max_inline_chars": max_inline_chars,
            },
        )

    async def process_document(
        self,
        request: Optional[Union[ProcessDocumentRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        respect_robots: Optional[bool] = None,
        document_type: Optional[Literal["pdf", "docx", "xlsx", "csv", "txt", "auto"]] = None,
        extract_text: Optional[bool] = None,
        extract_metadata: Optional[bool] = None,
        extract_tables: Optional[bool] = None,
        extract_images: Optional[bool] = None,
        timeout: Optional[float] = None,
        max_inline_chars: Optional[int] = None,
        redact_pii: Optional[Union[bool, ProcessDocumentRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Fetch a document by URL and extract its real text, metadata, and tables. Supported on this endpoint: PDF (text, metadata, tables via pdf-parse), CSV (text + parsed rows), TXT, and HTML (text + metadata). DOCX/XLSX return 501 and are supported by the CrawlForge MCP server.

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/process-document
        """
        return await self._run_tool(
            "process_document",
            request,
            {
                "url": url,
                "respect_robots": respect_robots,
                "document_type": document_type,
                "extract_text": extract_text,
                "extract_metadata": extract_metadata,
                "extract_tables": extract_tables,
                "extract_images": extract_images,
                "timeout": timeout,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    async def read_result(
        self,
        request: Optional[Union[ReadResultRequest, Dict[str, Any]]] = None,
        /,
        *,
        handle: Optional[str] = None,
        operation: Optional[Literal["slice", "search", "lines", "json_path"]] = None,
        offset: Optional[int] = None,
        length: Optional[int] = None,
        query: Optional[str] = None,
        max_matches: Optional[int] = None,
        path: Optional[str] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Read part of a stored result. A tool whose result exceeded max_inline_chars returned a preview and a result_handle; this reads the stored copy by character range (slice), by case-insensitive literal search with context and offsets (search), by line (lines), or by dotted JSON path (json_path). Results are kept for 1 hour and are readable only by the account that produced them. Nothing is fetched.

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/read-result
        """
        return await self._run_tool(
            "read_result",
            request,
            {
                "handle": handle,
                "operation": operation,
                "offset": offset,
                "length": length,
                "query": query,
                "max_matches": max_matches,
                "path": path,
                "max_inline_chars": max_inline_chars,
            },
        )

    async def reddit_search(
        self,
        request: Optional[Union[RedditSearchRequest, Dict[str, Any]]] = None,
        /,
        *,
        query: Optional[str] = None,
        subreddit: Optional[str] = None,
        author: Optional[str] = None,
        mode: Optional[Literal["posts", "comments", "thread"]] = None,
        link_id: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Literal["asc", "desc"]] = None,
        source: Optional[Literal["auto", "arctic_shift", "pullpush", "web_discovery"]] = None,
    ) -> ToolResult:
        """Search Reddit posts/comments or read a full comment thread — reads the Arctic Shift community archive (reddit.com blocks direct scraping). A scoped search (subreddit or author) queries the archive directly. A Reddit-wide keyword search finds posts with a site-restricted web search and then reads those posts from the archive — or, in comments mode, searches each of the first five posts' comments for the keywords — because Arctic Shift cannot keyword-search across all of Reddit. A scoped comment search Arctic Shift times out on is retried over the last 7d and 3d and reports window_applied. Arctic Shift is tried first and PullPush (api.pullpush.io) second: when Arctic Shift or the web-discovery path fails a posts or comments search, PullPush is queried and the response reports fallback_used. PullPush has refused automated clients since August 2026, so that fallback usually reports its refusal too.

        Costs 5 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/reddit-search
        """
        return await self._run_tool(
            "reddit_search",
            request,
            {
                "query": query,
                "subreddit": subreddit,
                "author": author,
                "mode": mode,
                "link_id": link_id,
                "after": after,
                "before": before,
                "limit": limit,
                "sort": sort,
                "source": source,
            },
        )

    async def scrape(
        self,
        request: Optional[Union[ScrapeRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        formats: Optional[List[Union[Literal["markdown", "html", "rawHtml", "text", "links", "metadata", "screenshot", "json-schema"], ScrapeRequestFormatsItemHighlights, Dict[str, Any], ScrapeRequestFormatsItemQuestion]]] = None,
        onlyMainContent: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
        escalate: Optional[bool] = None,
        escalate_engine: Optional[Literal["playwright", "camoufox"]] = None,
        max_inline_chars: Optional[int] = None,
        redact_pii: Optional[Union[bool, ScrapeRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Unified single-fetch, multi-format extraction. One fetch serves every requested format: markdown, html, rawHtml, text, links, metadata. A bot-defence challenge page returns success: false with blocked.vendor whatever its HTTP status; an empty shell or an error placeholder served as HTTP 200 is a failure too. Neither is charged. A PDF or other binary returns 415 UNSUPPORTED_CONTENT_TYPE, unbilled; use process_document. A success whose markdown is empty carries a warning saying so. With escalate: true that same call renders the page once in a stealth browser and returns the formats from it, instead of returning the block.

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/scrape
        """
        return await self._run_tool(
            "scrape",
            request,
            {
                "url": url,
                "formats": formats,
                "onlyMainContent": onlyMainContent,
                "respect_robots": respect_robots,
                "escalate": escalate,
                "escalate_engine": escalate_engine,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    async def scrape_structured(
        self,
        request: Optional[Union[ScrapeStructuredRequest, Dict[str, Any]]] = None,
        /,
        *,
        html: Optional[str] = None,
        url: Optional[str] = None,
        selectors: Optional[Dict[str, str]] = None,
        base_url: Optional[str] = None,
        multiple: Optional[bool] = None,
        clean_text: Optional[bool] = None,
        include_attributes: Optional[List[str]] = None,
        max_items: Optional[float] = None,
        respect_robots: Optional[bool] = None,
    ) -> ToolResult:
        """Extract structured data from HTML using CSS selectors

        Costs 2 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/scrape-structured
        """
        return await self._run_tool(
            "scrape_structured",
            request,
            {
                "html": html,
                "url": url,
                "selectors": selectors,
                "base_url": base_url,
                "multiple": multiple,
                "clean_text": clean_text,
                "include_attributes": include_attributes,
                "max_items": max_items,
                "respect_robots": respect_robots,
            },
        )

    async def scrape_template(
        self,
        request: Optional[Union[ScrapeTemplateRequest, Dict[str, Any]]] = None,
        /,
        *,
        template: Optional[str] = None,
        url: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        respect_robots: Optional[bool] = None,
        timeout: Optional[int] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Pre-built scrapers for popular sites and public APIs — no schema or selectors required. Three modes: name a template and pass a URL; pass template "auto" with a URL to have the matching template picked (the response reports which one it chose); or pass template "list" to enumerate them. Templates come in two kinds, reported as "mode" by the list. An entity template returns one record from one page. A list connector returns N records from one call, as data.items with a data.count — that covers the job-board group (Greenhouse, Lever, Ashby, Workable, Recruitee, Teamtailor), which reads a company's whole board from its ATS API, the government group (NHTSA vPIC VIN decoding, NPPES NPI provider registry), which reads free keyless federal registries, and shopify-collection, which lists a whole storefront collection. A list connector is driven either by a URL or by "params" — e.g. { "template": "greenhouse-jobs", "params": { "company": "stripe" } }. Sites that block plain HTTP fetches (e.g. Amazon) may return sparse data here; the CrawlForge MCP server version uses stealth browsing for those. reddit-thread reads the post from the Arctic Shift archive, because reddit.com blocks direct scraping; the reddit_search tool reads the comment tree. linkedin-profile and tweet are retired — those sites' robots.txt disallow every keyless path — and naming one, or passing one of their URLs to "auto", returns 400 TEMPLATE_UNAVAILABLE with the reason and no charge. Several templates read a machine-readable endpoint rather than the rendered page — shopify-product reads the store's own /products/<handle>.json, npm-package reads the npm registry API, and every list connector reads its platform's API — and report the URL they actually read as "fetched_url". When a Shopify store refuses its JSON endpoint (401, 403, 404 or 410), shopify-product reads the product page's own schema.org JSON-LD instead: the record carries "source": "json-ld" and a warning says so, with per-variant stock, compare-at prices and option names null because JSON-LD does not carry them.

        Costs 1 credit. Docs: https://www.crawlforge.dev/docs/api-reference/tools/scrape-template
        """
        return await self._run_tool(
            "scrape_template",
            request,
            {
                "template": template,
                "url": url,
                "params": params,
                "respect_robots": respect_robots,
                "timeout": timeout,
                "max_inline_chars": max_inline_chars,
            },
        )

    async def scrape_with_actions(
        self,
        request: Optional[Union[ScrapeWithActionsRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        actions: Optional[List[Union[ScrapeWithActionsRequestActionsItem, Dict[str, Any]]]] = None,
        formats: Optional[List[Any]] = None,
        captureIntermediateStates: Optional[bool] = None,
        formAutoFill: Optional[Union[ScrapeWithActionsRequestFormAutoFill, Dict[str, Any]]] = None,
        browserOptions: Optional[Union[ScrapeWithActionsRequestBrowserOptions, Dict[str, Any]]] = None,
        respect_robots: Optional[bool] = None,
        extractionOptions: Optional[Union[ScrapeWithActionsRequestExtractionOptions, Dict[str, Any]]] = None,
        continueOnActionError: Optional[bool] = None,
        maxRetries: Optional[float] = None,
        screenshotOnError: Optional[bool] = None,
        max_inline_chars: Optional[float] = None,
        redact_pii: Optional[Union[bool, ScrapeWithActionsRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Interact with a page before scraping — click, type, press keys, hover, choose a select option, scroll, navigate on, run JavaScript, or wait for dynamic content. Use for SPAs, login-gated content, or multi-step flows. Set browserOptions.stealth to run the chain in a stealth browser context. A click or form submit that loads another page is a navigation too: it gets its own navigations entry (trigger names the action type), and finalUrl is where the chain ended. Screenshots are taken by {type:"screenshot"} actions (and on error) and stored as crawlforge://screenshot/{actionId} resources.

        Costs 5 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/scrape-with-actions
        """
        return await self._run_tool(
            "scrape_with_actions",
            request,
            {
                "url": url,
                "actions": actions,
                "formats": formats,
                "captureIntermediateStates": captureIntermediateStates,
                "formAutoFill": formAutoFill,
                "browserOptions": browserOptions,
                "respect_robots": respect_robots,
                "extractionOptions": extractionOptions,
                "continueOnActionError": continueOnActionError,
                "maxRetries": maxRetries,
                "screenshotOnError": screenshotOnError,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    async def search_web(
        self,
        request: Optional[Union[SearchWebRequest, Dict[str, Any]]] = None,
        /,
        *,
        query: Optional[str] = None,
        queries: Optional[List[str]] = None,
        limit: Optional[float] = None,
        offset: Optional[float] = None,
        lang: Optional[str] = None,
        site: Optional[str] = None,
        safe_search: Optional[bool] = None,
        time_range: Optional[Literal["day", "week", "month", "year", "all"]] = None,
        file_type: Optional[str] = None,
        redact_pii: Optional[Union[bool, SearchWebRequestRedactPii, Dict[str, Any]]] = None,
        max_inline_chars: Optional[int] = None,
    ) -> ToolResult:
        """Search the live web (Brave Search API) and get ranked results as JSON. One query per call, or up to 10 in a single call with queries.

        Costs 5 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/search-web
        """
        return await self._run_tool(
            "search_web",
            request,
            {
                "query": query,
                "queries": queries,
                "limit": limit,
                "offset": offset,
                "lang": lang,
                "site": site,
                "safe_search": safe_search,
                "time_range": time_range,
                "file_type": file_type,
                "redact_pii": redact_pii,
                "max_inline_chars": max_inline_chars,
            },
        )

    async def serp_rank(
        self,
        request: Optional[Union[SerpRankRequest, Dict[str, Any]]] = None,
        /,
        *,
        keyword: Optional[str] = None,
        target: Optional[str] = None,
        depth: Optional[float] = None,
        device: Optional[Literal["desktop", "mobile"]] = None,
        language_code: Optional[str] = None,
        location_name: Optional[str] = None,
        location_code: Optional[float] = None,
    ) -> ToolResult:
        """Check a domain's organic position in Google search results for a keyword (powered by DataForSEO). One lookup is one sample: Google can return a different result set for the same query minutes apart, so compare several lookups before reading a change in rank. A result set that barely mentions the keyword, a likely decoy page, comes back with suspect: true and a warning

        Costs 5 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/serp-rank
        """
        return await self._run_tool(
            "serp_rank",
            request,
            {
                "keyword": keyword,
                "target": target,
                "depth": depth,
                "device": device,
                "language_code": language_code,
                "location_name": location_name,
                "location_code": location_code,
            },
        )

    async def stealth_mode(
        self,
        request: Optional[Union[StealthModeRequest, Dict[str, Any]]] = None,
        /,
        *,
        operation: Optional[Literal["scrape", "configure", "create_context", "create_page", "get_stats", "cleanup"]] = None,
        stealthConfig: Optional[Union[StealthModeRequestStealthConfig, Dict[str, Any]]] = None,
        engine: Optional[Literal["playwright", "camoufox"]] = None,
        contextId: Optional[str] = None,
        urlToTest: Optional[str] = None,
        url: Optional[str] = None,
        formats: Optional[List[Any]] = None,
        wait_for: Optional[float] = None,
        verbose: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
        max_inline_chars: Optional[float] = None,
        redact_pii: Optional[Union[bool, StealthModeRequestRedactPii, Dict[str, Any]]] = None,
    ) -> ToolResult:
        """Stealth browser scraping for sites that block normal scrapers (Cloudflare, DataDome, bot detection). Use operation "scrape" for a one-call render of a single URL. create_context then create_page is a navigation and challenge check: create_page loads urlToTest, reports its status, title and any challenge page, and closes the page before the call returns, so nothing on it carries over to a later call. For work over several calls on one page (log in, then read; click, then read), use browser_session with stealth: true. Operation "configure" only validates a stealthConfig and returns it with the defaults filled in — it stores nothing, so pass stealthConfig on each scrape or create_context call that should use it.

        Costs 5 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/stealth-mode
        """
        return await self._run_tool(
            "stealth_mode",
            request,
            {
                "operation": operation,
                "stealthConfig": stealthConfig,
                "engine": engine,
                "contextId": contextId,
                "urlToTest": urlToTest,
                "url": url,
                "formats": formats,
                "wait_for": wait_for,
                "verbose": verbose,
                "respect_robots": respect_robots,
                "max_inline_chars": max_inline_chars,
                "redact_pii": redact_pii,
            },
        )

    async def summarize_content(
        self,
        request: Optional[Union[SummarizeContentRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        content: Optional[str] = None,
        respect_robots: Optional[bool] = None,
        max_sentences: Optional[float] = None,
        summary_type: Optional[Literal["extractive", "key_points", "brief"]] = None,
        include_metadata: Optional[bool] = None,
        timeout: Optional[float] = None,
    ) -> ToolResult:
        """Generate intelligent summaries of web content using extractive summarization

        Costs 4 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/summarize-content
        """
        return await self._run_tool(
            "summarize_content",
            request,
            {
                "url": url,
                "content": content,
                "respect_robots": respect_robots,
                "max_sentences": max_sentences,
                "summary_type": summary_type,
                "include_metadata": include_metadata,
                "timeout": timeout,
            },
        )

    async def track_changes(
        self,
        request: Optional[Union[TrackChangesRequest, Dict[str, Any]]] = None,
        /,
        *,
        url: Optional[str] = None,
        operation: Optional[Literal["create_baseline", "compare", "monitor"]] = None,
        selector: Optional[str] = None,
        update_baseline: Optional[bool] = None,
        respect_robots: Optional[bool] = None,
        schedule: Optional[str] = None,
        notify_emails: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
    ) -> ToolResult:
        """Detect content changes on a page by comparing it against a stored baseline (create_baseline, then compare), or create a hosted monitor that checks it on a schedule (monitor)

        Costs 3 credits. Docs: https://www.crawlforge.dev/docs/api-reference/tools/track-changes
        """
        return await self._run_tool(
            "track_changes",
            request,
            {
                "url": url,
                "operation": operation,
                "selector": selector,
                "update_baseline": update_baseline,
                "respect_robots": respect_robots,
                "schedule": schedule,
                "notify_emails": notify_emails,
                "webhook_url": webhook_url,
            },
        )
