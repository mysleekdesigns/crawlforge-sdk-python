"""The generated code agrees with openapi.json, and the spec's own examples validate."""

import importlib.util
import inspect
import re
from pathlib import Path
from typing import Any, Dict

import pydantic
import pytest

from crawlforge import TOOLS, AsyncCrawlForge, CrawlForge
from crawlforge import models as public_models
from crawlforge._generated import models, tools

ROOT = Path(__file__).parent.parent
CROSS_FIELD_RULE_TOOLS = {
    "analyze_content",
    "extract_links",
    "extract_metadata",
    "extract_text",
    "extract_with_llm",
    "scrape_structured",
    "scrape_template",
    "search_web",
    "summarize_content",
}


def spec_tools(spec: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    found = {}
    for path, item in spec["paths"].items():
        match = re.fullmatch(r"/tools/([a-z0-9_]+)", path)
        assert match, path
        found[match.group(1)] = item["post"]
    return found


def test_tools_table_matches_the_spec_paths(spec: Dict[str, Any]) -> None:
    expected = spec_tools(spec)
    assert len(expected) == 31
    assert list(TOOLS) == list(expected)
    for name, post in expected.items():
        tool = TOOLS[name]
        assert tool.name == name == post["operationId"]
        assert tool.credits == post["x-credits"]
        assert tool.credits_note == post.get("x-credits-note")
        assert tool.docs_url == post["x-docs-url"]
        assert tool.summary == post["summary"]
        ref = post["requestBody"]["content"]["application/json"]["schema"]["$ref"]
        assert tool.request_model.__name__ == ref.rsplit("/", 1)[1]


@pytest.mark.parametrize("client_cls", [CrawlForge, AsyncCrawlForge])
def test_every_tool_is_a_method_named_after_it(client_cls: type) -> None:
    for name in TOOLS:
        method = getattr(client_cls, name)
        assert callable(method)
        assert inspect.iscoroutinefunction(method) == (client_cls is AsyncCrawlForge)
        params = inspect.signature(method).parameters
        assert list(params)[:2] == ["self", "request"]
        assert params["request"].kind is inspect.Parameter.POSITIONAL_ONLY
        for field in TOOLS[name].request_model.model_fields.values():
            wire_name = field.alias or next(
                n for n, f in TOOLS[name].request_model.model_fields.items() if f is field
            )
            assert params[wire_name].kind is inspect.Parameter.KEYWORD_ONLY


@pytest.mark.parametrize("name", list(TOOLS))
def test_spec_examples_validate_and_round_trip(name: str, spec: Dict[str, Any]) -> None:
    post = spec_tools(spec)[name]
    example = post["requestBody"]["content"]["application/json"]["example"]
    model = TOOLS[name].request_model.model_validate(example)
    assert model.model_dump(exclude_unset=True, by_alias=True, mode="json") == example


def test_cross_field_rules_do_not_reject_valid_bodies() -> None:
    assert CROSS_FIELD_RULE_TOOLS <= set(TOOLS)
    # Each rule is url-or-content style; both halves are accepted locally (the server enforces).
    TOOLS["extract_text"].request_model.model_validate({"url": "https://example.com"})
    TOOLS["extract_text"].request_model.model_validate({"html": "<p>hi</p>"})
    TOOLS["search_web"].request_model.model_validate({"query": "a"})
    TOOLS["search_web"].request_model.model_validate({"queries": ["a", "b"]})
    TOOLS["scrape_template"].request_model.model_validate({"template": "list"})
    TOOLS["scrape_template"].request_model.model_validate(
        {"template": "auto", "url": "https://x.y"}
    )


def test_request_models_forbid_unknown_keys_and_response_models_allow_them() -> None:
    with pytest.raises(pydantic.ValidationError):
        models.FetchUrlRequest.model_validate({"url": "https://example.com", "nope": 1})
    info = models.ToolInfo.model_validate(
        {
            "tool": "x",
            "description": "d",
            "credits_cost": 1,
            "parameters": {},
            "example": {},
            "availability": {"hosted_api": True},
        }
    )
    assert info.model_dump()["availability"] == {"hosted_api": True}


def test_public_models_module_re_exports_everything() -> None:
    assert set(public_models.__all__) == set(models.__all__)
    assert len(models.REQUEST_MODELS) == 31
    assert all(name in models.__all__ for name in ("ToolInfo", "ScrapeRequest"))


def test_generated_files_are_fresh() -> None:
    """Regenerating from openapi.json must reproduce the committed files byte for byte."""
    spec_path = ROOT / "scripts" / "gen_models.py"
    loader = importlib.util.spec_from_file_location("gen_models", spec_path)
    assert loader and loader.loader
    gen = importlib.util.module_from_spec(loader)
    loader.loader.exec_module(gen)
    spec = gen.load_spec(str(ROOT / "openapi.json"))
    generated_dir = ROOT / "crawlforge" / "_generated"
    assert gen.generate_models(spec) == (generated_dir / "models.py").read_text(encoding="utf-8")
    assert gen.generate_tools(spec) == (generated_dir / "tools.py").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert gen.generate_readme_table(spec) in readme
    assert tools.__file__ and tools.__file__.endswith("tools.py")


def test_generated_code_never_uses_pipe_unions_or_future_annotations() -> None:
    """Python 3.9 cannot evaluate `X | Y` inside pydantic models."""
    for name in ("models.py", "tools.py"):
        source = (ROOT / "crawlforge" / "_generated" / name).read_text(encoding="utf-8")
        assert "from __future__" not in source
        assert not re.search(r":\s*[A-Za-z\]]+ \| ", source)
