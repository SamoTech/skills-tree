"""Deterministic search over the canonical generated search documents.

This module consumes the projection loaded by cli.search_runtime. It does not
parse Markdown, build an index, or introduce a second search data source.
"""

from __future__ import annotations

import re
from typing import Any, Iterable

_TOKEN_RE = re.compile(r"[\w]+", re.UNICODE)

# Contract: higher-value metadata fields outrank long free-form body text.
FIELD_WEIGHTS = {
    "title": 8,
    "tags": 6,
    "category": 4,
    "description": 3,
    "body": 1,
}

DEFAULT_LIMIT = 20
MAX_LIMIT = 100


def tokenize(text: str) -> tuple[str, ...]:
    """Return deterministic Unicode word tokens, case-insensitive."""
    return tuple(token.casefold() for token in _TOKEN_RE.findall(text))


def _field_tokens(document: dict[str, Any], field: str) -> tuple[str, ...]:
    value = document.get(field, [])
    if isinstance(value, list):
        value = " ".join(str(item) for item in value)
    return tokenize(str(value))


def score_document(document: dict[str, Any], query_tokens: Iterable[str]) -> int:
    """Score one document using the documented field-weight contract.

    Each distinct query token can contribute at most once per field. Repeated
    occurrences in a field do not inflate the score.
    """
    query = set(query_tokens)
    if not query:
        return 0

    score = 0
    for field, weight in FIELD_WEIGHTS.items():
        tokens = set(_field_tokens(document, field))
        score += weight * len(query & tokens)
    return score


def search_documents(
    query: str,
    documents: list[dict[str, Any]],
    *,
    limit: int = DEFAULT_LIMIT,
) -> list[dict[str, Any]]:
    """Return deterministically ranked matching documents."""
    query_tokens = tokenize(query)
    if not query_tokens:
        raise ValueError("search query must contain at least one word")

    if not 1 <= limit <= MAX_LIMIT:
        raise ValueError(f"limit must be between 1 and {MAX_LIMIT}")

    ranked: list[tuple[int, dict[str, Any]]] = []
    for document in documents:
        score = score_document(document, query_tokens)
        if score > 0:
            ranked.append((score, document))

    ranked.sort(
        key=lambda item: (
            -item[0],
            str(item[1].get("title", "")).casefold(),
            str(item[1].get("id", "")),
        )
    )

    results: list[dict[str, Any]] = []
    for score, document in ranked[:limit]:
        results.append(
            {
                "id": document["id"],
                "title": document["title"],
                "category": document["category"],
                "level": document["level"],
                "stability": document["stability"],
                "description": document["description"],
                "score": score,
            }
        )
    return results
