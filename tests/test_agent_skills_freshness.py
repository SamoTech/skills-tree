"""Freshness contract for the committed Agent Skills packages.

`agent-skills/<name>/SKILL.md` are generated projections of the
canonical `skills/` corpus, republished through the Agent Skills
distribution automation. The existing tests verify the generator's
unit behavior (`test_generate_agent_skills.py`), the discovery
index's count and digests of the committed copies
(`test_agent_skills_discovery.py`), and cross-artifact consistency
(`test_agent_skills_reconciliation.py`) - but nothing verifies the
committed packages against a fresh in-memory projection of the
canonical corpus. A corpus change that outlives its package
automation PR, a stale package after a skill edit (the drift class
demonstrated live during the 2026-10-18 slice-2 remediation, where
three packages had drifted from their edited canonical skills), or a
hand-edited generated package would stay CI-green.

This module closes that gap in the established pattern of the
Skills-API (PR #581), graph (PR #582), search-index (PR #616), and
quality-report (PR #626) freshness contracts: on every push it
re-derives every eligible package in-memory via the shared
`tools.generate_agent_skills.project` boundary (deterministic sorted
iteration, no file writes, no second projector introduced) and
requires the committed `agent-skills/<name>/SKILL.md` set to match the
eligible projection set exactly, with each committed package
byte-identical to the canonical projection output. The projection
carries no git-derived timestamp fields, so no exclusions are
required.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PACKAGES_DIR = ROOT / "agent-skills"


def _fresh_projections() -> dict:
    from tools.generate_agent_skills import project

    source_root = ROOT / "skills"
    files = sorted(
        path for path in source_root.rglob("*.md")
        if path.name.lower() != "readme.md"
    )
    projections = {}
    for path in files:
        item = project(path, ROOT)
        if item.eligible:
            projections[item.name] = item.content.rstrip() + "\n"
    return projections


def _committed_packages() -> dict:
    return {
        path.parent.name: path.read_bytes()
        for path in sorted(PACKAGES_DIR.glob("*/SKILL.md"))
    }


def test_agent_skills_packages_are_fresh_projection_of_canonical_corpus() -> None:
    fresh = _fresh_projections()
    committed = _committed_packages()

    missing = sorted(set(fresh) - set(committed))
    stale = sorted(set(committed) - set(fresh))
    assert not missing, (
        "agent-skills/ is missing packages for eligible canonical skills "
        "(merge the pending Agent Skills automation PR, or re-run "
        "tools/generate_agent_skills.py --write-eligible): "
        f"{missing[:10]}"
    )
    assert not stale, (
        "agent-skills/ contains packages with no eligible canonical "
        f"source; remove them: {stale[:10]}"
    )


def test_agent_skills_package_bytes_match_generator_output() -> None:
    fresh = _fresh_projections()
    committed = _committed_packages()
    drifted = sorted(
        name
        for name in set(fresh) & set(committed)
        if committed[name] != fresh[name].encode("utf-8")
    )
    assert not drifted, (
        "committed agent-skills packages are stale or hand-edited "
        "relative to the canonical skills/ corpus (merge the pending "
        "Agent Skills automation PR, or re-run "
        "tools/generate_agent_skills.py --write-eligible): "
        f"{drifted[:10]}"
    )
