"""Regenerate crawlforge/_generated/*.py and the README method table from openapi.json.

Usage: python scripts/generate.py   (or: make generate)

Deterministic: the output depends only on openapi.json, so CI regenerates and
fails on any diff.
"""

import sys
from pathlib import Path

from gen_models import generate_models, generate_readme_table, generate_tools, load_spec

ROOT = Path(__file__).resolve().parent.parent
README_START = "<!-- generated:tools:start -->"
README_END = "<!-- generated:tools:end -->"


def write(path: Path, content: str) -> None:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        print(f"unchanged {path.relative_to(ROOT)}")
        return
    path.write_text(content, encoding="utf-8")
    print(f"wrote     {path.relative_to(ROOT)}")


def update_readme(path: Path, table: str) -> None:
    text = path.read_text(encoding="utf-8")
    start = text.index(README_START) + len(README_START)
    end = text.index(README_END)
    write(path, text[:start] + "\n" + table + text[end:])


def main() -> int:
    spec = load_spec(str(ROOT / "openapi.json"))
    write(ROOT / "crawlforge" / "_generated" / "models.py", generate_models(spec))
    write(ROOT / "crawlforge" / "_generated" / "tools.py", generate_tools(spec))
    update_readme(ROOT / "README.md", generate_readme_table(spec))
    return 0


if __name__ == "__main__":
    sys.exit(main())
