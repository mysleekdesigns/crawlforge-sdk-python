"""Live smoke test: one fetch_url call against production. Bills 1 credit.

Usage: CRAWLFORGE_API_KEY=... python scripts/smoke.py
Prints credits_used and credits_remaining; exits 1 on any error. Never prints the key.
"""

import os
import sys

from crawlforge import CrawlForge, CrawlForgeError


def main() -> int:
    if not os.environ.get("CRAWLFORGE_API_KEY"):
        print("CRAWLFORGE_API_KEY is not set", file=sys.stderr)
        return 1
    try:
        with CrawlForge() as client:
            result = client.fetch_url(url="https://example.com")
    except CrawlForgeError as exc:
        print(f"smoke failed: {exc}", file=sys.stderr)
        return 1
    print(f"credits_used={result.credits_used} credits_remaining={result.credits_remaining}")
    print(f"status={result.data.get('status')} final_url={result.data.get('final_url')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
