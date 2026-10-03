from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
SEARCH_INDEX = ROOT / "docs" / "search-index.json"
SEARCH_SCHEMA = ROOT / "meta" / "search-index.schema.json"
API_INDEX = ROOT / "docs" / "api" / "skills.json"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_search_index_matches_declared_contract():
    schema = _load(SEARCH_SCHEMA)
    documents = _load(SEARCH_INDEX)

    Draft202012Validator.check_schema(schema)
    errors = sorted(Draft202012Validator(schema).iter_errors(documents), key=lambda e: list(e.path))
    assert not errors, "\n".join(error.message for error in errors[:10])


def test_search_index_is_a_deterministic_projection_of_canonical_paths():
    documents = _load(SEARCH_INDEX)
    api = _load(API_INDEX)

    ids = [doc["id"] for doc in documents]
    assert len(ids) == len(set(ids)), "search index contains duplicate IDs"

    search_paths = {f"skills/{doc['id']}.md" for doc in documents}
    api_paths = {skill["path"] for skill in api["skills"]}

    assert search_paths == api_paths
    assert len(documents) == api["count"] == len(api["skills"])


def test_search_index_entries_resolve_to_canonical_skill_files():
    documents = _load(SEARCH_INDEX)

    for doc in documents:
        canonical = ROOT / "skills" / f"{doc['id']}.md"
        assert canonical.is_file(), f"search entry does not resolve to canonical skill: {doc['id']}"

PACKAGE_INDEX = ROOT / "data" / "search-index.json"

def test_packaged_search_projection_matches_web_projection():
    assert PACKAGE_INDEX.read_bytes() == SEARCH_INDEX.read_bytes()


def test_search_runtime_resolves_canonical_projection():
    from cli.search_runtime import load_search_index, search_index_path

    assert search_index_path() == PACKAGE_INDEX
    documents = load_search_index()
    assert len(documents) > 0
    assert documents[0]["id"]

def test_search_runtime_falls_back_to_installed_data(monkeypatch, tmp_path):
    from cli import search_runtime

    installed = tmp_path / "data" / "search-index.json"
    installed.parent.mkdir()
    installed.write_bytes(PACKAGE_INDEX.read_bytes())

    monkeypatch.setattr(search_runtime, "_source_checkout_path", lambda: tmp_path / "missing.json")
    monkeypatch.setattr(search_runtime, "_installed_path", lambda: installed)

    assert search_runtime.search_index_path() == installed
    assert search_runtime.load_search_index()[0]["id"]
