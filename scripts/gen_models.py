"""Turn openapi.json into Python source: pydantic v2 request models and typed tool methods.

Standard library only. This module replaced datamodel-code-generator 0.76.2 for
this SDK, because on this spec that tool

* has no Python 3.9 target (its choices start at 3.10) and emits ``X | None``
  unions, which pydantic cannot evaluate on 3.9;
* splits the nine request schemas that carry a top-level ``anyOf``/``oneOf``/
  ``allOf`` cross-field rule into ``RootModel`` unions of near-identical
  classes, which cannot back one typed method per tool;
* maps ``format: uri`` to ``AnyUrl`` (which normalises the URL before it is
  sent) and ``format: email`` to ``EmailStr`` (which needs the extra
  ``email-validator`` package).

Rules this generator applies:

* Wire names are kept exactly. A property that shadows a pydantic
  ``BaseModel`` attribute or is a Python keyword becomes ``<name>_`` with
  ``Field(alias="<name>")``; the SDK dumps with ``by_alias=True``.
* Top-level ``anyOf``/``oneOf``/``allOf`` cross-field rules are not
  enforced locally (the server enforces them); a body that satisfies the
  ``properties`` is accepted.
* ``propertyNames`` is ignored: Python dict keys are already strings.
* ``pattern`` is not emitted (pydantic's default regex engine rejects the
  lookaheads the spec uses); ``minimum``/``maximum``/``minLength``/
  ``maxLength``/``minItems``/``maxItems`` are.
* Request models forbid unknown keys, so a misspelled argument fails before
  any request is sent.
* Output depends only on the spec, so regeneration is idempotent.
"""

import json
import keyword
import re
from typing import Any, Dict, List, Tuple

# Attributes pydantic's BaseModel exposes; a field with one of these names
# would shadow it (pydantic warns and the attribute becomes ambiguous).
RESERVED_FIELD_NAMES = frozenset(
    {
        "construct",
        "copy",
        "dict",
        "from_orm",
        "json",
        "parse_file",
        "parse_obj",
        "parse_raw",
        "schema",
        "schema_json",
        "update_forward_refs",
        "validate",
    }
)

PRIMITIVES = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "null": "None",
}

# A type is a small tuple tree rendered by render_type():
#   ("name", "str")                 a primitive / Any
#   ("model", "ClassName")          a generated nested model
#   ("list", inner)
#   ("dict", inner)                 Dict[str, inner]
#   ("union", [inner, ...])
#   ("literal", [value, ...])
TypeNode = Tuple[Any, ...]


def pascal(name: str) -> str:
    return "".join(part[:1].upper() + part[1:] for part in re.split(r"[^0-9a-zA-Z]+", name) if part)


def py_literal(value: Any) -> str:
    """A JSON value as Python source (double-quoted strings, ASCII-escaped)."""
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, list):
        return "[" + ", ".join(py_literal(v) for v in value) + "]"
    if isinstance(value, dict):
        return "{" + ", ".join(f"{py_literal(k)}: {py_literal(v)}" for k, v in value.items()) + "}"
    raise TypeError(f"unsupported JSON value: {value!r}")


def python_field_name(wire_name: str) -> str:
    if (
        keyword.iskeyword(wire_name)
        or wire_name in RESERVED_FIELD_NAMES
        or wire_name.startswith("model_")
    ):
        return wire_name + "_"
    if not wire_name.isidentifier():
        raise ValueError(
            f"property {wire_name!r} is not a Python identifier; extend python_field_name()"
        )
    return wire_name


class FieldDef:
    def __init__(
        self, wire_name: str, schema: Dict[str, Any], required: bool, type_node: TypeNode
    ) -> None:
        self.wire_name = wire_name
        self.name = python_field_name(wire_name)
        self.schema = schema
        self.required = required
        self.type_node = type_node

    def default_source(self) -> str:
        """The spec default as source. A container default is cast to the declared type so a
        type checker does not narrow it to list[str] and reject a Literal element type."""
        default = self.schema.get("default")
        literal = py_literal(default)
        if isinstance(default, (list, dict)):
            annotation = Generator.render_type(self.type_node, widen_models=False)
            if "Literal[" in annotation:
                assert "'" not in annotation, annotation
                return f"cast('{annotation}', {literal})"
        return literal

    def field_kwargs(self) -> List[str]:
        s = self.schema
        kwargs: List[str] = []
        if not self.required:
            kwargs.append(f"default={self.default_source()}")
        if self.name != self.wire_name:
            kwargs.append(f"alias={json.dumps(self.wire_name)}")
        if "minimum" in s:
            kwargs.append(f"ge={py_literal(s['minimum'])}")
        if "maximum" in s:
            kwargs.append(f"le={py_literal(s['maximum'])}")
        if "exclusiveMinimum" in s and not isinstance(s["exclusiveMinimum"], bool):
            kwargs.append(f"gt={py_literal(s['exclusiveMinimum'])}")
        if "exclusiveMaximum" in s and not isinstance(s["exclusiveMaximum"], bool):
            kwargs.append(f"lt={py_literal(s['exclusiveMaximum'])}")
        for key in ("minLength", "minItems"):
            if key in s:
                kwargs.append(f"min_length={py_literal(s[key])}")
        for key in ("maxLength", "maxItems"):
            if key in s:
                kwargs.append(f"max_length={py_literal(s[key])}")
        if s.get("description"):
            kwargs.append(f"description={json.dumps(s['description'])}")
        return kwargs


class ModelDef:
    def __init__(self, name: str, doc: str, fields: List[FieldDef], base: str) -> None:
        self.name = name
        self.doc = doc
        self.fields = fields
        self.base = base


class Generator:
    def __init__(self, spec: Dict[str, Any]) -> None:
        self.spec = spec
        self.models: List[ModelDef] = []  # nested models precede the model that uses them

    # ---- schema -> type tree --------------------------------------------------

    def type_of(self, schema: Dict[str, Any], class_hint: str, base: str) -> TypeNode:
        # An object with properties is a model even when the schema also carries
        # a cross-field anyOf/oneOf/allOf (those rules are enforced server-side).
        if isinstance(schema.get("properties"), dict) and schema["properties"]:
            return ("model", self.add_model(class_hint, schema, base))
        for combinator in ("anyOf", "oneOf"):
            if combinator in schema:
                alternatives = schema[combinator]
                # One object alternative among scalars (bool | {...}) keeps the plain name;
                # several are told apart by their `type` const or their position.
                objects = [alt for alt in alternatives if isinstance(alt.get("properties"), dict)]
                nodes: List[TypeNode] = []
                for index, alt in enumerate(alternatives):
                    suffix = "" if len(objects) == 1 else self.alt_suffix(alt, index)
                    nodes.append(self.type_of(alt, class_hint + suffix, base))
                return nodes[0] if len(nodes) == 1 else ("union", nodes)
        if "const" in schema:
            return ("literal", [schema["const"]])
        if "enum" in schema:
            return ("literal", list(schema["enum"]))
        json_type = schema.get("type")
        if isinstance(json_type, list):
            return (
                "union",
                [self.type_of({**schema, "type": t}, class_hint, base) for t in json_type],
            )
        if json_type == "array":
            items = schema.get("items")
            inner = (
                self.type_of(items, class_hint + "Item", base)
                if isinstance(items, dict)
                else ("name", "Any")
            )
            return ("list", inner)
        if json_type == "object":
            additional = schema.get("additionalProperties")
            if isinstance(additional, dict) and additional:
                return ("dict", self.type_of(additional, class_hint + "Value", base))
            return ("dict", ("name", "Any"))
        if json_type in PRIMITIVES:
            return ("name", PRIMITIVES[json_type])
        return ("name", "Any")

    @staticmethod
    def alt_suffix(alt: Dict[str, Any], index: int) -> str:
        """Name an anyOf alternative after its `type` const when it has one, else its position."""
        props = alt.get("properties")
        if isinstance(props, dict):
            const = props.get("type", {}).get("const")
            if isinstance(const, str):
                return pascal(const)
        return str(index + 1)

    def add_model(self, name: str, schema: Dict[str, Any], base: str) -> str:
        if any(m.name == name for m in self.models):
            raise ValueError(f"duplicate model name {name}; nested naming must be unique")
        required = set(schema.get("required") or [])
        fields: List[FieldDef] = []
        for wire_name, prop in schema["properties"].items():
            node = self.type_of(
                prop if isinstance(prop, dict) else {}, name + pascal(wire_name), base
            )
            fields.append(
                FieldDef(
                    wire_name, prop if isinstance(prop, dict) else {}, wire_name in required, node
                )
            )
        doc = schema.get("description") or ""
        self.models.append(ModelDef(name, doc, fields, base))
        return name

    # ---- type tree -> annotation source -----------------------------------------

    @classmethod
    def render_type(cls, node: TypeNode, widen_models: bool) -> str:
        kind = node[0]
        if kind == "name":
            return str(node[1])
        if kind == "model":
            return f"Union[{node[1]}, Dict[str, Any]]" if widen_models else str(node[1])
        if kind == "list":
            return f"List[{cls.render_type(node[1], widen_models)}]"
        if kind == "dict":
            return f"Dict[str, {cls.render_type(node[1], widen_models)}]"
        if kind == "literal":
            return "Literal[" + ", ".join(py_literal(v) for v in node[1]) + "]"
        if kind == "union":
            parts: List[str] = []
            for inner in node[1]:
                rendered = cls.render_type(inner, widen_models)
                # flatten nested unions and drop duplicates, keeping order
                for piece in cls._union_pieces(rendered):
                    if piece not in parts:
                        parts.append(piece)
            return parts[0] if len(parts) == 1 else "Union[" + ", ".join(parts) + "]"
        raise ValueError(f"unknown type node {node!r}")

    @staticmethod
    def _union_pieces(rendered: str) -> List[str]:
        if not rendered.startswith("Union["):
            return [rendered]
        inner = rendered[len("Union[") : -1]
        pieces: List[str] = []
        depth = 0
        current = ""
        for ch in inner:
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
            if ch == "," and depth == 0:
                pieces.append(current.strip())
                current = ""
            else:
                current += ch
        pieces.append(current.strip())
        return pieces

    # ---- emitters -------------------------------------------------------------------

    def render_model(self, model: ModelDef) -> str:
        lines = [f"class {model.name}({model.base}):"]
        if model.doc:
            lines.append(f"    {docstring(model.doc)}")
        if not model.fields:
            lines.append("    pass")
        for f in model.fields:
            annotation = self.render_type(f.type_node, widen_models=False)
            if not f.required:
                annotation = f"Optional[{annotation}]"
            lines.append(f"    {f.name}: {annotation} = Field({', '.join(f.field_kwargs())})")
        return "\n".join(lines) + "\n"

    def render_signature_params(self, model: ModelDef) -> List[str]:
        params: List[str] = []
        for f in model.fields:
            annotation = self.render_type(f.type_node, widen_models=True)
            params.append(f"{f.wire_name}: Optional[{annotation}] = None")
        return params


def docstring(text: str) -> str:
    text = text.replace("\\", "\\\\").replace('"""', "'''")
    return f'"""{text}"""'


def used_typing_names(source: str) -> List[str]:
    names = []
    for name in ("Any", "Dict", "List", "Literal", "Optional", "Union", "cast"):
        if re.search(rf"\b{name}\b", source):
            names.append(name)
    return names


def request_schema_name(tool_post: Dict[str, Any]) -> str:
    ref = tool_post["requestBody"]["content"]["application/json"]["schema"]["$ref"]
    return str(ref).rsplit("/", 1)[1]


def tools_in_spec(spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    """One record per POST /tools/<tool>, in spec order. Prices come only from x-credits."""
    tools = []
    for path, item in spec["paths"].items():
        match = re.fullmatch(r"/tools/([a-z0-9_]+)", path)
        if not match or "post" not in item:
            continue
        post = item["post"]
        credits = post["x-credits"]
        if (
            isinstance(credits, bool)
            or not isinstance(credits, (int, float))
            or credits != int(credits)
        ):
            raise ValueError(f"{path}: x-credits must be a whole number, got {credits!r}")
        tools.append(
            {
                "name": match.group(1),
                "operation_id": post["operationId"],
                "summary": post.get("summary") or "",
                "credits": int(credits),
                "credits_note": post.get("x-credits-note"),
                "docs_url": post.get("x-docs-url") or "",
                "request_schema": request_schema_name(post),
                "example": post["requestBody"]["content"]["application/json"].get("example"),
            }
        )
    return tools


HEADER = "# Generated from openapi.json by scripts/generate.py. Do not edit by hand.\n"


def generate_models(spec: Dict[str, Any]) -> str:
    schemas = spec["components"]["schemas"]
    gen = Generator(spec)
    gen.add_model("ToolInfo", schemas["ToolInfo"], "_ResponseModel")
    for tool in tools_in_spec(spec):
        name = tool["request_schema"]
        gen.add_model(name, schemas[name], "_RequestModel")

    body = "\n\n".join(gen.render_model(m) for m in gen.models)
    request_names = [tool["request_schema"] for tool in tools_in_spec(spec)]
    all_names = ["ToolInfo"] + [m.name for m in gen.models if m.name != "ToolInfo"]
    typing_names = used_typing_names(body)

    out = [
        HEADER,
        '"""Pydantic v2 models for the CrawlForge REST API request bodies and ToolInfo."""\n',
        "",
        f"from typing import {', '.join(typing_names)}",
        "",
        "from pydantic import BaseModel, ConfigDict, Field",
        "",
        "__all__ = [",
        *[f"    {json.dumps(n)}," for n in all_names],
        "]",
        "",
        "",
        "class _RequestModel(BaseModel):",
        '    """A request body. Unknown keys are rejected: a misspelled argument fails locally."""',
        "",
        '    model_config = ConfigDict(extra="forbid", populate_by_name=True)',
        "",
        "",
        "class _ResponseModel(BaseModel):",
        '    """A response body. Unknown keys are kept so a newer server still parses."""',
        "",
        '    model_config = ConfigDict(extra="allow")',
        "",
        "",
        body,
        "",
        "REQUEST_MODELS = (",
        *[f"    {n}," for n in request_names],
        ")",
        "",
    ]
    return "\n".join(out)


def generate_tools(spec: Dict[str, Any]) -> str:
    schemas = spec["components"]["schemas"]
    tools = tools_in_spec(spec)
    gen = Generator(spec)
    by_name: Dict[str, ModelDef] = {}
    for tool in tools:
        name = tool["request_schema"]
        gen.add_model(name, schemas[name], "_RequestModel")
        by_name[tool["name"]] = next(m for m in gen.models if m.name == name)

    def method(tool: Dict[str, Any], is_async: bool) -> str:
        model = by_name[tool["name"]]
        params = gen.render_signature_params(model)
        prefix = "async " if is_async else ""
        await_ = "await " if is_async else ""
        note = f" plus {tool['credits_note']}" if tool["credits_note"] else ""
        unit = "credit" if tool["credits"] == 1 else "credits"
        price = f"Costs {tool['credits']} {unit}{note}. Docs: {tool['docs_url']}"
        doc = f"{tool['summary']}\n\n        {price}\n        "
        lines = [
            f"    {prefix}def {tool['name']}(",
            "        self,",
            f"        request: Optional[Union[{model.name}, Dict[str, Any]]] = None,",
            "        /,",
            *(["        *,"] if params else []),
            *[f"        {p}," for p in params],
            "    ) -> ToolResult:",
            f"        {docstring(doc)}",
            f"        return {await_}self._run_tool(",
            f"            {json.dumps(tool['name'])},",
            "            request,",
            "            {",
            *[f"                {json.dumps(f.wire_name)}: {f.wire_name}," for f in model.fields],
            "            },",
            "        )",
        ]
        return "\n".join(lines) + "\n"

    sync_methods = "\n".join(method(t, False) for t in tools)
    async_methods = "\n".join(method(t, True) for t in tools)
    table_rows = []
    for t in tools:
        table_rows.append(
            "    "
            + json.dumps(t["name"])
            + ": ToolSpec(\n"
            + f"        name={json.dumps(t['name'])},\n"
            + f"        credits={t['credits']},\n"
            + f"        credits_note={py_literal(t['credits_note'])},\n"
            + f"        docs_url={json.dumps(t['docs_url'])},\n"
            + f"        summary={json.dumps(t['summary'])},\n"
            + f"        request_model={t['request_schema']},\n"
            + "    ),"
        )
    source_for_imports = sync_methods + async_methods
    typing_names = used_typing_names(source_for_imports)
    # Every model a signature or the table names, top-level and nested, in definition order.
    model_imports = ",\n".join(
        f"    {name}"
        for name in sorted(m.name for m in gen.models)
        if re.search(rf"\b{name}\b", source_for_imports)
    )

    out = [
        HEADER,
        '"""One typed method per tool, generated from openapi.json, as client mixins."""\n',
        "",
        f"from typing import {', '.join(typing_names)}",
        "",
        "from crawlforge._generated.models import (",
        model_imports + ",",
        ")",
        "from crawlforge.types import ToolResult, ToolSpec",
        "",
        "TOOLS: Dict[str, ToolSpec] = {",
        "\n".join(table_rows),
        "}",
        '"""Every tool in the spec, keyed by name; credits are the operation\'s x-credits."""',
        "",
        "",
        "class SyncToolsMixin:",
        '    """Typed tool methods for CrawlForge. The client supplies _run_tool."""',
        "",
        "    def _run_tool(self, tool: str, request: Any, params: Dict[str, Any]) -> ToolResult:",
        "        raise NotImplementedError",
        "",
        sync_methods,
        "",
        "class AsyncToolsMixin:",
        '    """Typed tool methods for AsyncCrawlForge. The client supplies _run_tool."""',
        "",
        "    async def _run_tool(",
        "        self, tool: str, request: Any, params: Dict[str, Any]",
        "    ) -> ToolResult:",
        "        raise NotImplementedError",
        "",
        async_methods,
    ]
    return "\n".join(out)


def generate_readme_table(spec: Dict[str, Any]) -> str:
    rows = ["| Method | Credits | Note | Docs |", "|---|---|---|---|"]
    for t in tools_in_spec(spec):
        note = t["credits_note"] or ""
        rows.append(f"| `{t['name']}` | {t['credits']} | {note} | [docs]({t['docs_url']}) |")
    return "\n".join(rows) + "\n"


def load_spec(path: str) -> Dict[str, Any]:
    with open(path, encoding="utf-8") as fh:
        spec: Dict[str, Any] = json.load(fh)
    return spec


__all__ = [
    "generate_models",
    "generate_tools",
    "generate_readme_table",
    "load_spec",
    "tools_in_spec",
    "python_field_name",
    "RESERVED_FIELD_NAMES",
]
