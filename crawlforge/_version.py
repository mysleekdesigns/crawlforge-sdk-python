"""The installed package version, with a fallback for a source checkout."""

from importlib.metadata import PackageNotFoundError, version

FALLBACK_VERSION = "0.2.0"

try:
    __version__ = version("crawlforge")
except PackageNotFoundError:  # running from a checkout that is not installed
    __version__ = FALLBACK_VERSION
