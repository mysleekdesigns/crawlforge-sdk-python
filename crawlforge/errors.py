"""Error classes. None of them ever carries the API key.

An error response is never charged: the API deducts credits only after a tool
succeeded.
"""

from typing import Any, Dict, Mapping, Optional

__all__ = [
    "CrawlForgeError",
    "ValidationError",
    "AuthenticationError",
    "InsufficientCreditsError",
    "RateLimitError",
    "ToolError",
    "error_from_response",
]


class CrawlForgeError(Exception):
    """Base class for every error the SDK raises.

    ``status`` is the HTTP status (0 when no response was received), ``code``
    the API's error code (or NETWORK_ERROR / UNEXPECTED_RESPONSE), ``details``
    whatever structure the API attached, and ``request_id`` the response's
    x-vercel-id or x-request-id when present.
    """

    def __init__(
        self,
        status: int,
        code: str,
        message: str,
        details: Any = None,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.details = details
        self.request_id = request_id

    def __str__(self) -> str:
        prefix = f"[{self.status}] " if self.status else ""
        return f"{prefix}{self.code}: {self.message}"

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(status={self.status!r}, code={self.code!r}, "
            f"message={self.message!r}, request_id={self.request_id!r})"
        )


class ValidationError(CrawlForgeError):
    """400: the body did not match the request schema. ``details`` lists the issues."""


class AuthenticationError(CrawlForgeError):
    """401: MISSING_API_KEY or INVALID_API_KEY."""


class InsufficientCreditsError(CrawlForgeError):
    """402: INSUFFICIENT_CREDITS or SPEND_CAP_REACHED.

    ``auto_recharge_triggered`` mirrors the X-Auto-Recharge-Triggered header:
    when True a recharge was started and the call can be retried once it lands.
    """

    def __init__(
        self,
        status: int,
        code: str,
        message: str,
        details: Any = None,
        request_id: Optional[str] = None,
        *,
        auto_recharge_triggered: bool = False,
    ) -> None:
        super().__init__(status, code, message, details, request_id)
        self.auto_recharge_triggered = auto_recharge_triggered


class RateLimitError(CrawlForgeError):
    """429: RATE_LIMIT_EXCEEDED (your plan's limit) or HOST_BACKOFF (the target asked us to wait).

    ``retry_after`` is the Retry-After header in seconds, None when absent.
    """

    def __init__(
        self,
        status: int,
        code: str,
        message: str,
        details: Any = None,
        request_id: Optional[str] = None,
        *,
        retry_after: Optional[float] = None,
    ) -> None:
        super().__init__(status, code, message, details, request_id)
        self.retry_after = retry_after


class ToolError(CrawlForgeError):
    """Any other error status. ``blocked`` names a bot-defence vendor when the API reported one."""

    def __init__(
        self,
        status: int,
        code: str,
        message: str,
        details: Any = None,
        request_id: Optional[str] = None,
        *,
        blocked: Optional[Dict[str, Any]] = None,
        escalated: bool = False,
    ) -> None:
        super().__init__(status, code, message, details, request_id)
        self.blocked = blocked
        self.escalated = escalated


def _header(headers: Mapping[str, str], name: str) -> Optional[str]:
    for key, value in headers.items():
        if key.lower() == name:
            return value
    return None


def request_id_from(headers: Mapping[str, str]) -> Optional[str]:
    return _header(headers, "x-vercel-id") or _header(headers, "x-request-id")


def error_from_response(status: int, body: Any, headers: Mapping[str, str]) -> CrawlForgeError:
    """Map an ErrorResponse body to the error class for its status, then its code."""
    request_id = request_id_from(headers)
    error = body.get("error") if isinstance(body, dict) else None
    if not isinstance(error, dict) or not isinstance(error.get("code"), str):
        return CrawlForgeError(
            status,
            "UNEXPECTED_RESPONSE",
            f"HTTP {status} without an error envelope",
            body,
            request_id,
        )
    code = error["code"]
    message = str(error.get("message") or code)
    details = error.get("details")
    if status == 400:
        return ValidationError(status, code, message, details, request_id)
    if status == 401:
        return AuthenticationError(status, code, message, details, request_id)
    if status == 402:
        flag = (_header(headers, "x-auto-recharge-triggered") or "").strip().lower() == "true"
        return InsufficientCreditsError(
            status, code, message, details, request_id, auto_recharge_triggered=flag
        )
    if status == 429:
        return RateLimitError(
            status, code, message, details, request_id, retry_after=parse_retry_after(headers)
        )
    blocked = body.get("blocked") if isinstance(body, dict) else None
    return ToolError(
        status,
        code,
        message,
        details,
        request_id,
        blocked=blocked if isinstance(blocked, dict) else None,
        escalated=bool(body.get("escalated", False)) if isinstance(body, dict) else False,
    )


def parse_retry_after(headers: Mapping[str, str]) -> Optional[float]:
    """Retry-After in seconds: delta-seconds or an HTTP date. None when absent or unparseable."""
    from datetime import datetime, timezone
    from email.utils import parsedate_to_datetime

    raw = _header(headers, "retry-after")
    if raw is None:
        return None
    raw = raw.strip()
    try:
        return max(0.0, float(raw))
    except ValueError:
        pass
    try:
        when = parsedate_to_datetime(raw)
    except (TypeError, ValueError, IndexError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return max(0.0, (when - datetime.now(timezone.utc)).total_seconds())
