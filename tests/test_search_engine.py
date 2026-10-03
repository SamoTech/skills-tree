from __future__ import annotations

import pytest

from cli.search_engine import search_documents, tokenize


DOCUMENTS = [
    {
        "id": "01-perception/image-understanding",
        "title": "Image Understanding",
        "category": "01-perception",
        "level": "intermediate",
        "stability": "stable",
        "tags": ["vision", "multimodal"],
        "description": "Interpret visual content.",
        "body": "Reason about images.",
    },
    {
        "id": "05-code/image-pipeline",
        "title": "Pipeline",
        "category": "05-code",
        "level": "advanced",
        "stability": "stable",
        "tags": ["vision"],
        "description": "Build processing pipelines.",
        "body": "Pipeline implementation details.",
    },
    {
        "id": "05-code/python-tools",
        "title": "Python Tools",
        "category": "05-code",
        "level": "basic",
        "stability": "stable",
        "tags": ["automation"],
        "description": "Build automation helpers.",
        "body": "Python scripting.",
    },
]


def test_tokenize_is_case_insensitive_and_punctuation_stable():
    assert tokenize("Image, VISION!") == ("image", "vision")


def test_title_match_outweighs_body_match():
    results = search_documents("image", DOCUMENTS)
    assert [result["id"] for result in results] == [
        "01-perception/image-understanding",
        "05-code/image-pipeline",
    ]
    assert results[0]["score"] > results[1]["score"]


def test_multiple_query_terms_accumulate_without_duplicate_token_inflation():
    results = search_documents("image vision", DOCUMENTS)
    assert results[0]["id"] == "01-perception/image-understanding"
    assert results[0]["score"] == 14


def test_ties_break_by_title_then_id():
    docs = [
        {**DOCUMENTS[1], "id": "z/image-pipeline"},
        {**DOCUMENTS[1], "id": "a/image-pipeline"},
    ]
    results = search_documents("pipeline", docs)
    assert [r["id"] for r in results] == ["a/image-pipeline", "z/image-pipeline"]


def test_limit_is_deterministic():
    assert len(search_documents("image", DOCUMENTS, limit=1)) == 1


@pytest.mark.parametrize("query", ["", "!!!", "   "])
def test_empty_or_non_word_query_is_rejected(query):
    with pytest.raises(ValueError, match="at least one word"):
        search_documents(query, DOCUMENTS)


def test_invalid_limit_is_rejected():
    with pytest.raises(ValueError, match="limit"):
        search_documents("image", DOCUMENTS, limit=0)
