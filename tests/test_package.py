"""The installed distribution on the running interpreter."""

import re
import sys
from importlib.metadata import metadata, requires
from pathlib import Path

import crawlforge
from crawlforge._version import FALLBACK_VERSION

ROOT = Path(__file__).parent.parent


def test_imports_on_this_interpreter() -> None:
    assert sys.version_info >= (3, 9)
    assert crawlforge.CrawlForge and crawlforge.AsyncCrawlForge
    assert re.fullmatch(r"\d+\.\d+\.\d+", crawlforge.__version__)


def test_python_requires_and_runtime_dependencies() -> None:
    meta = metadata("crawlforge")
    assert meta["Requires-Python"] == ">=3.9"
    assert meta["Name"] == "crawlforge"
    runtime = [r for r in (requires("crawlforge") or []) if "extra ==" not in r]
    names = sorted(re.split(r"[<>=!~;\[ ]", r, maxsplit=1)[0] for r in runtime)
    assert names == ["httpx", "pydantic"]


def test_fallback_version_matches_pyproject() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"$', pyproject, re.MULTILINE)
    assert match and match.group(1) == FALLBACK_VERSION == crawlforge.__version__


def test_typed_marker_ships() -> None:
    assert (Path(crawlforge.__file__).parent / "py.typed").exists()
