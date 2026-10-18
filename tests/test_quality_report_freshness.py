"""Freshness contract for the committed skill-quality report.

`meta/QUALITY-REPORT.md` is a generated projection of the canonical
`skills/` corpus, republished through the quality-report automation PR.
Nothing on CI verifies the committed copy: the report is regenerated
out-of-band by automation, so a corpus change that outlives its
quality-report automation PR - or any manual edit of the generated
report - would stay CI-green, in the same defect class that the
search-index freshness contract (PR #616) closed for
`docs/search-index.json` / `data/search-index.json`.

This module closes that gap in the established pattern of the Skills-API
(PR #581), graph (PR #582), and search-index (PR #616) freshness
contracts: it re-derives the report in-memory from the canonical corpus
on every push via the shared `tools/check_skill_quality.py` boundary
(deterministic sorted iteration, no file writes, no second classifier
introduced) and requires the committed `meta/QUALITY-REPORT.md` to be
byte-identical to `render_report()`'s canonical output. The report
contains no git-derived timestamp fields, so no exclusions are required.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REPORT_PATH = ROOT / "meta" / "QUALITY-REPORT.md"


def _fresh_report() -> str:
    from tools.check_skill_quality import classify, iter_skill_files, render_report

    reports = [classify(p) for p in iter_skill_files()]
    return render_report(reports)


def _summary(report: str) -> str:
    for line in report.splitlines():
        if line.startswith("- **Total skill files:**") or line.startswith("- "):
            first = [
                ln for ln in report.splitlines()
                if ln.startswith("- ") and ("**" in ln)
            ]
            return " | ".join(first)
    return ""


def test_quality_report_is_fresh_projection_of_canonical_corpus() -> None:
    fresh = _fresh_report()
    committed = REPORT_PATH.read_text(encoding="utf-8")

    assert committed == fresh, (
        "meta/QUALITY-REPORT.md is stale relative to skills/; merge the "
        "pending quality-report automation PR (or re-run "
        "tools/check_skill_quality.py) and commit its output unchanged. "
        f"committed summary: {_summary(committed)} | "
        f"corpus summary: {_summary(fresh)}"
    )
