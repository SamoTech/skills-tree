"""Freshness contract: the docs/badges inventory must cover the canonical corpus.

Byte-identity is intentionally NOT required: badge JSON files carry mutable
Watchdog security state (unscanned / machine-inferred / verified / advisory),
transitioned by tools/write_badge.py through the OSV-watch workflows, so
committed badge content is runtime state, not a pure projection of skills/.

The corpus-derived invariant is inventory coverage: the set of badge files in
docs/badges must exactly equal the set of badge keys derived from skills/ via
the shared tools/sync_badges.py boundary (skill_to_badge_key over every
skills/**/*.md file, including category READMEs and the 00-sandbox fixture).
This is the same reconciliation tools/sync_badges.py performs, but fail-closed
in CI: a corpus change that outlives its badge-sync automation PR, a manually
added stray badge, or a stale orphan for a deleted skill now fails CI instead
of waiting for the weekly self-heal (established pattern of #581/#582/#616 and
the quality-report freshness contract #626).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from sync_badges import skill_to_badge_key


def test_badge_inventory_covers_corpus_exactly():
    skills_root = ROOT / "skills"
    badge_dir = ROOT / "docs" / "badges"

    skill_keys = {
        skill_to_badge_key(md.relative_to(ROOT))
        for md in skills_root.rglob("*.md")
    }
    assert skill_keys, "canonical skills/ corpus unexpectedly empty"

    badge_keys = {f.stem for f in badge_dir.glob("*.json")}
    assert badge_keys, "docs/badges/ unexpectedly empty"

    missing = sorted(skill_keys - badge_keys)
    orphans = sorted(badge_keys - skill_keys)

    assert not missing, (
        "badge files missing for canonical skills "
        "(tools/sync_badges.py reconciliation has not run for a corpus "
        f"change): {len(missing)} missing, first: {missing[:10]}"
    )
    assert not orphans, (
        "orphan badge files for non-existent skills: "
        f"{len(orphans)} orphans, first: {orphans[:10]}"
    )
