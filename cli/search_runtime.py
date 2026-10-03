"""Deterministic access to the canonical generated search projection.

The search corpus is generated once from skills/ and published in two
delivery locations with identical bytes:
- docs/search-index.json for the static web experience
- data/search-index.json for the installable package

This module owns only artifact discovery/loading. It deliberately does not
define a second parser, index format, or ranking algorithm.
"""

from __future__ import annotations

import json
from pathlib import Path
import sysconfig
from typing import Any

_SEARCH_RELATIVE_PATH = Path("data") / "search-index.json"


def _source_checkout_path() -> Path:
    return Path(__file__).resolve().parents[1] / _SEARCH_RELATIVE_PATH


def _installed_path() -> Path:
    return Path(sysconfig.get_path("data")) / _SEARCH_RELATIVE_PATH


def search_index_path() -> Path:
    """Resolve the packaged/source search projection without network access."""
    source = _source_checkout_path()
    if source.is_file():
        return source

    installed = _installed_path()
    if installed.is_file():
        return installed

    raise FileNotFoundError(
        "Skills Tree search index is unavailable; expected "
        f"{source} or {installed}"
    )


def load_search_index() -> list[dict[str, Any]]:
    """Load the generated search projection in deterministic order."""
    path = search_index_path()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("Skills Tree search index must be a non-empty JSON array")

    required = {"id", "title", "category", "level", "stability", "tags", "description", "body"}
    for index, document in enumerate(data):
        if not isinstance(document, dict) or not required.issubset(document):
            raise ValueError(f"Invalid search index document at position {index}")

    return data
