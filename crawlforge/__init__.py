"""CrawlForge Python SDK: 30 metered web tools behind one API key.

from crawlforge import CrawlForge

client = CrawlForge()  # reads CRAWLFORGE_API_KEY
result = client.scrape(url="https://example.com", formats=["markdown"])
print(result.data["formats"]["markdown"], result.credits_remaining)
"""

from crawlforge._client import AsyncCrawlForge, CrawlForge
from crawlforge._generated.models import ToolInfo
from crawlforge._generated.tools import TOOLS
from crawlforge._version import __version__
from crawlforge.errors import (
    AuthenticationError,
    CrawlForgeError,
    InsufficientCreditsError,
    RateLimitError,
    ToolError,
    ValidationError,
)
from crawlforge.types import ToolResult, ToolSpec

__all__ = [
    "AsyncCrawlForge",
    "AuthenticationError",
    "CrawlForge",
    "CrawlForgeError",
    "InsufficientCreditsError",
    "RateLimitError",
    "TOOLS",
    "ToolError",
    "ToolInfo",
    "ToolResult",
    "ToolSpec",
    "ValidationError",
    "__version__",
]
