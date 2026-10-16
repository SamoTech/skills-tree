"""Freshness contract for the published search-index projection.

`docs/search-index.json` and `data/search-index.json` are generated
projections of the canonical `skills/` corpus, republished through the
generate-search-index automation PR. The existing contract tests
(`tests/test_search_index_contract.py`) compare the generated artifacts
against each other (pair byte-equality, schema, canonical path sets) but
cannot detect staleness or corruption shared by both copies — demonstrated
live on 2026-10-15, when an automation relay encoding defect double-encoded
non-ASCII bytes in the pushed search-index copy and CI stayed green. This
module closes that gap by re-deriving the projection in-memory from the
canonical corpus on every push and requiring equality with the committed
artifacts, in the established pattern of the Skills-API (PR #581) and graph
(PR #582) freshness contracts.

The projection contains no git-derived timestamp fields, so no exclusions
are required (unlike the `generated`/`dateModified` exclusions in #581
and #582). Beyond parsed equality, the committed bytes must be
byte-identical to the generator's canonical serialization: equal parsed
values reached through a different encoding (`\\uXXXX` escapes,
double-encoded UTF-8 mojibake, or any other serialization drift) still
fail, because the committed artifact must be the exact output of
`tools/build_search_index.py`.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

WEB_INDEX = ROOT / "docs" / "search-index.json"
PACKAGE_INDEX = ROOT / "data" / "search-index.json"


def _fresh_projection() -> list:
    from tools.build_search_index import build_index

    return build_index(ROOT / "skills")


def _describe_drift(committed_documents: list, fresh_documents: list) -> str:
    committed_by_id = {doc["id"]: doc for doc in committed_documents}
    fresh_by_id = {doc["id"]: doc for doc in fresh_documents}
    missing = sorted(set(fresh_by_id) - set(committed_by_id))
    stale = sorted(set(committed_by_id) - set(fresh_by_id))
    drifted = sorted(
        doc_id
        for doc_id in set(committed_by_id) & set(fresh_by_id)
        if committed_by_id[doc_id] != fresh_by_id[doc_id]
    )
    return (
        f"missing-from-index: {missing[:10]} "
        f"stale-in-index: {stale[:10]} "
        f"drifted: {drifted[:10]}"
    )


def test_search_index_is_fresh_projection_of_canonical_corpus() -> None:
    fresh_documents = _fresh_projection()
    committed = json.loads(WEB_INDEX.read_text(encoding="utf-8"))

    assert len(committed) == len(fresh_documents), (
        "docs/search-index.json count does not match the canonical corpus: "
        f"committed={len(committed)} corpus={len(fresh_documents)}"
    )
    assert committed == fresh_documents, (
        "docs/search-index.json is stale relative to skills/; merge the "
        "pending search-index automation PR (or re-run "
        "tools/build_search_index.py). "
        + _describe_drift(committed, fresh_documents)
    )


def test_packaged_search_index_is_fresh_projection_of_canonical_corpus() -> None:
    fresh_documents = _fresh_projection()
    committed = json.loads(PACKAGE_INDEX.read_text(encoding="utf-8"))

    assert len(committed) == len(fresh_documents), (
        "data/search-index.json count does not match the canonical corpus: "
        f"committed={len(committed)} corpus={len(fresh_documents)}"
    )
    assert committed == fresh_documents, (
        "data/search-index.json is stale relative to skills/; merge the "
        "pending search-index automation PR (or re-run "
        "tools/build_search_index.py). "
        + _describe_drift(committed, fresh_documents)
    )


def test_search_index_artifacts_are_byte_identical_to_generator_output() -> None:
    fresh_documents = _fresh_projection()
    canonical_payload = json.dumps(fresh_documents, ensure_ascii=False, indent=2) + "\n"
    canonical_bytes = canonical_payload.encode("utf-8")

    for artifact in (WEB_INDEX, PACKAGE_INDEX):
        committed_bytes = artifact.read_bytes()
        assert committed_bytes == canonical_bytes, (
            f"{artifact.relative_to(ROOT)} does not byte-match the canonical "
            "output of tools/build_search_index.py; the committed artifact "
            "was written with a different encoding or serialization and "
            "must be regenerated"
        )
