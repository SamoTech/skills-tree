"""Freshness contract for the published Skills API projection.

``docs/api/`` is a generated projection of the canonical ``skills/`` corpus,
republished through the export-skills automation PR. The existing contract
tests (``tests/test_search_index_contract.py``) compare the generated
artifacts against each other; this test closes the remaining gap by
re-deriving the projection in-memory from the canonical corpus on every
push and requiring equality with the committed artifacts. A corpus change
that outlives its export automation PR therefore fails CI instead of
publishing a stale public API.

Git-derived timestamp fields (``generated``, ``dateModified``) are excluded
from the comparison: they are deterministic from repository history, but a
shallow CI checkout cannot re-derive them.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

API_INDEX = ROOT / "docs" / "api" / "skills.json"
API_YAML = ROOT / "docs" / "api" / "skills.yaml"
API_SCHEMA = ROOT / "docs" / "api" / "skills-schema.json"
JSONLD_ROOT = ROOT / "docs" / "api" / "jsonld"
JSONLD_INDEX = JSONLD_ROOT / "index.jsonld"


def _fresh_projection(monkeypatch: pytest.MonkeyPatch) -> list:
    monkeypatch.chdir(ROOT)
    from tools.export_skills import build_index

    return build_index()


def _describe_drift(committed_envelope: dict, fresh_skills: list) -> str:
    committed_by_path = {skill["path"]: skill for skill in committed_envelope["skills"]}
    fresh_by_path = {skill["path"]: skill for skill in fresh_skills}
    missing = sorted(set(fresh_by_path) - set(committed_by_path))
    stale = sorted(set(committed_by_path) - set(fresh_by_path))
    drifted = sorted(
        path
        for path in set(committed_by_path) & set(fresh_by_path)
        if committed_by_path[path] != fresh_by_path[path]
    )
    return (
        f"missing-from-api: {missing[:10]} "
        f"stale-in-api: {stale[:10]} "
        f"drifted: {drifted[:10]}"
    )


def test_skills_json_is_fresh_projection_of_canonical_corpus(monkeypatch: pytest.MonkeyPatch) -> None:
    fresh_skills = _fresh_projection(monkeypatch)
    committed = json.loads(API_INDEX.read_text(encoding="utf-8"))

    assert committed["count"] == len(committed["skills"]) == len(fresh_skills), (
        "docs/api/skills.json count does not match the canonical corpus: "
        f"committed={committed['count']} corpus={len(fresh_skills)}"
    )
    committed_without_generated = {k: v for k, v in committed.items() if k != "generated"}
    fresh_without_generated = {"count": len(fresh_skills), "skills": fresh_skills}
    assert committed_without_generated == fresh_without_generated, (
        "docs/api/skills.json is stale relative to skills/; merge the pending "
        "export automation PR (or re-run tools/export_skills.py). "
        + _describe_drift(committed, fresh_skills)
    )


def test_skills_yaml_matches_json_projection() -> None:
    pytest.importorskip("yaml")
    import yaml

    committed_yaml = yaml.safe_load(API_YAML.read_text(encoding="utf-8"))
    committed_json = json.loads(API_INDEX.read_text(encoding="utf-8"))
    assert committed_yaml == committed_json, (
        "docs/api/skills.yaml does not match docs/api/skills.json"
    )


def test_skills_schema_json_matches_generator_constant() -> None:
    from tools.export_skills import SKILL_SCHEMA

    committed = json.loads(API_SCHEMA.read_text(encoding="utf-8"))
    assert committed == SKILL_SCHEMA, (
        "docs/api/skills-schema.json does not match the generator constant in "
        "tools/export_skills.py"
    )


def test_jsonld_index_is_fresh_projection_of_canonical_corpus(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(ROOT)
    from tools.export_skills import build_index, build_jsonld_index

    fresh_index = build_jsonld_index(build_index())
    committed = json.loads(JSONLD_INDEX.read_text(encoding="utf-8"))

    fresh_without_dates = {k: v for k, v in fresh_index.items() if k != "dateModified"}
    committed_without_dates = {k: v for k, v in committed.items() if k != "dateModified"}
    assert committed_without_dates == fresh_without_dates, (
        "docs/api/jsonld/index.jsonld is stale relative to skills/; merge the "
        "pending export automation PR (or re-run tools/export_skills.py)"
    )


def test_per_skill_jsonld_files_are_fresh_and_complete(monkeypatch: pytest.MonkeyPatch) -> None:
    fresh_skills = _fresh_projection(monkeypatch)
    from tools.export_skills import build_skill_jsonld

    expected_paths: set[str] = set()
    for skill in fresh_skills:
        category = skill.get("category_dir") or "uncategorized"
        relative = f"{category}/{skill['id']}.jsonld"
        expected_paths.add(relative)
        projection_path = JSONLD_ROOT / relative
        assert projection_path.is_file(), f"missing JSON-LD projection: {relative}"
        committed = json.loads(projection_path.read_text(encoding="utf-8"))
        fresh = build_skill_jsonld(skill)
        assert {k: v for k, v in committed.items() if k != "dateModified"} == {
            k: v for k, v in fresh.items() if k != "dateModified"
        }, f"stale JSON-LD projection: {relative}"

    committed_paths = {
        path.relative_to(JSONLD_ROOT).as_posix()
        for path in JSONLD_ROOT.rglob("*.jsonld")
        if path.name != "index.jsonld"
    }
    assert committed_paths == expected_paths, (
        "JSON-LD projection set does not match the canonical corpus; "
        f"leftover files: {sorted(committed_paths - expected_paths)[:10]}"
    )
