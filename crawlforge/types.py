"""Result and catalogue types shared by the clients and the generated code."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel, ConfigDict, Field


class ToolResult(BaseModel):
    """A successful tool call.

    ``data`` is the tool's result and is untyped in this release: its shape is
    tool-specific and documented on each tool's docs page.
    """

    model_config = ConfigDict(extra="ignore")

    data: Dict[str, Any]
    credits_used: int
    credits_remaining: int
    processing_time: int
    warnings: List[str] = Field(default_factory=list)


@dataclass(frozen=True)
class ToolSpec:
    """One tool from the spec. ``credits`` is the operation's x-credits, never typed by hand."""

    name: str
    credits: int
    credits_note: Optional[str]
    docs_url: str
    summary: str
    request_model: Type[BaseModel]
