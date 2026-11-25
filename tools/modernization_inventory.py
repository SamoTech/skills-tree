#!/usr/bin/env python3
"""Deterministic modernization inventory for the canonical skill corpus.

Owner-directed by issue #699 (2026-11-25): inventory every canonical skill in
skills/ and classify it into a transparent modernization state, so
modernization batches are selected from evidence instead of memory.

The tool builds ONLY on existing repository boundaries and never invents
freshness, compatibility, adoption, or quality facts:

- quality tier: tools.check_skill_quality.classify (battle_tested /
  enriched / stub / invalid / test_fixture),
- integrity findings: tools.audit_skill_corpus.audit_skill_files
  (duplicated titles/descriptions, stale version declarations, missing
  related-skill targets, syntax errors in fenced Python examples),
- dependency evidence: the canonical dependency badge
  docs/badges/<skills-<category>-<name>.json> (key produced by
  tools.sync_badges.skill_to_badge_key); only a green-family badge color
  counts as verified, anything else (including a missing badge file) is
  reported as needing dependency evidence.

Stable modernization states (resolved in this order):

1. test-fixture                  intentional pipeline fixture (not production)
2. needs-invalid-repair          schema/frontmatter repair required
3. needs-stub-repair             placeholder description or no runnable code
4. needs-integrity-remediation   one or more audit findings
5. needs-structural-upgrade      enriched tier (real description + runnable
                                 code, but below the battle-tested bar)
6. needs-dependency-evidence     battle-tested + no findings, dependency
                                 badge not verified
7. verified                      battle-tested + no findings + verified deps

The committed report meta/MODERNIZATION-INVENTORY.md carries no timestamps
and is byte-verified fresh by tests/test_modernization_inventory.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from tools.audit_skill_corpus import audit_skill_files
from tools.check_skill_quality import (
    REPO_ROOT,
    classify,
    iter_skill_files,
    parse_frontmatter,
)
from tools.sync_badges import skill_to_badge_key

INVENTORY_PATH = REPO_ROOT / "meta" / "MODERNIZATION-INVENTORY.md"
BADGE_DIR = REPO_ROOT / "docs" / "badges"
GREEN_COLORS = {"green", "brightgreen", "success"}
RED_COLORS = {"red", "critical", "important"}


@dataclass
class InventoryRecord:
    path: str
    category: str
    title: str
    quality: str
    version: str
    findings: list[str]
    reasons: list[str]
    dep_bucket: str
    dep_color: str
    dep_message: str
    state: str = ""


def dependency_evidence(rel_path: str) -> tuple[str, str, str]:
    """Return (bucket, color, message) from the canonical dependency badge."""
    badge_path = BADGE_DIR / (skill_to_badge_key(rel_path) + ".json")
    if not badge_path.exists():
        return "missing", "absent", "no badge file"
    try:
        data = json.loads(badge_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "unreadable", "unreadable", "badge file unreadable"
    color = str(data.get("color", "")).lower()
    message = str(data.get("message", ""))
    if color in GREEN_COLORS:
        bucket = "verified"
    elif color in RED_COLORS:
        bucket = "failed"
    else:
        bucket = "unverified"
    return bucket, color or "empty", message


def modernization_state(quality: str, findings: list[str], dep_bucket: str) -> str:
    if quality == "test_fixture":
        return "test-fixture"
    if quality == "invalid":
        return "needs-invalid-repair"
    if quality == "stub":
        return "needs-stub-repair"
    if findings:
        return "needs-integrity-remediation"
    if quality == "enriched":
        return "needs-structural-upgrade"
    if dep_bucket != "verified":
        return "needs-dependency-evidence"
    return "verified"


def build_records() -> list[InventoryRecord]:
    paths = list(iter_skill_files())
    audits = {r.path: r for r in audit_skill_files(paths)}
    records: list[InventoryRecord] = []
    for path in paths:
        rel = str(path.relative_to(REPO_ROOT))
        audit = audits[rel]
        report = classify(path)
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        version = fm.get("version") if isinstance(fm.get("version"), str) else ""
        bucket, color, message = dependency_evidence(rel)
        records.append(
            InventoryRecord(
                path=rel,
                category=path.parent.name,
                title=audit.title,
                quality=audit.quality,
                version=version,
                findings=list(audit.findings),
                reasons=list(report.reasons),
                dep_bucket=bucket,
                dep_color=color,
                dep_message=message,
            )
        )
    for record in records:
        record.state = modernization_state(record.quality, record.findings, record.dep_bucket)
    return records


STATE_ORDER = (
    "verified",
    "needs-dependency-evidence",
    "needs-structural-upgrade",
    "needs-integrity-remediation",
    "needs-stub-repair",
    "needs-invalid-repair",
    "test-fixture",
)

PLAN_TEXT = """## Prioritized modernization plan (owner directive, issue #699)

The states above convert directly into the batch plan below. The plan fixes
the batch ORDER, not fixed batch contents: every batch selects its skills from
the current committed inventory at execution time, so the plan cannot go
stale, and every executed batch re-derives all four projection families on its
PR branch through the established temporary regen protocol (no manual
projection edits, exact-head CI before merge).

- P0 - Repair: any skill with state needs-integrity-remediation,
  needs-invalid-repair, or needs-stub-repair is remediated first; these are
  measured defect classes with a live CI audit, not opinion. Each remediated
  skill re-enters the audit with zero findings.
- P1 - Structural upgrade: skills with state needs-structural-upgrade
  (enriched tier) are upgraded to the battle-tested bar in bounded,
  reviewable batches (inputs/outputs/failure-modes table, 60+ lines, runnable
  verified example, dated evidence) in functional-cluster order: first
  07-tool-use, then 05-code, 09-agentic-patterns, 15-orchestration, 12-data,
  10-computer-use, then remaining categories. Identifiers, categories and
  provenance are preserved; a skill version moves only under the documented
  versioning conventions.
- P2 - Dependency evidence: skills with state needs-dependency-evidence are
  swept through the existing Dependency Watchdog pipeline
  (tools/dependency_auditor.py plus the badge scanner) in the same category
  clusters as P1, so each cluster ships structure plus dependency evidence
  together. The inventory never upgrades a badge itself.
- P3 - Evidence re-verification: for every upgraded or remediated skill, the
  dated Evidence lines are re-verified live at batch time; unverifiable
  citations are replaced per
  DECISION-2026-10-20-BOT-BLOCKED-EVIDENCE-URL-REPLACEMENT.

Corpus expansion is explicitly deprioritized while this modernization
initiative is open (issue #699: existing skills first).
"""


def render_markdown(records: list[InventoryRecord]) -> str:
    by_state: dict[str, list[InventoryRecord]] = {s: [] for s in STATE_ORDER}
    for r in records:
        by_state.setdefault(r.state, []).append(r)
    counts = {s: len(by_state[s]) for s in STATE_ORDER}
    quality = Counter(r.quality for r in records)
    versions = Counter(r.version or "(none)" for r in records)
    dep_buckets = Counter(r.dep_bucket for r in records)

    lines = [
        "# Skill Modernization Inventory",
        "",
        "> Auto-generated by tools/modernization_inventory.py. Do not edit by hand.",
        "> Owner-directed by issue #699 (2026-11-25): inventory the full canonical corpus and classify each skill into a transparent modernization state.",
        "> Conservative by construction: this inventory invents no freshness, adoption, or compatibility facts; every state is derived only from the boundaries listed below.",
        "",
        "## Calculation method (evidence sources)",
        "",
        "| Signal | Source | Meaning |",
        "|---|---|---|",
        "| Quality tier | tools/check_skill_quality.py classification | battle_tested / enriched / stub / invalid / test_fixture |",
        "| Integrity findings | tools/audit_skill_corpus.py | duplicated titles or descriptions, stale version declarations, missing related targets, syntax errors in Python examples |",
        "| Dependency evidence | docs/badges/ canonical badge color (key: tools/sync_badges.skill_to_badge_key) | green-family = verified; anything else, including a missing badge, = dependency evidence required |",
        "| Version | canonical frontmatter version field | declared version, as-is |",
        "",
        "## Summary dashboard",
        "",
        "- **Total canonical skill files:** %d" % len(records),
        "- **Verified (current and verified):** %d" % counts["verified"],
        "- **Dependency evidence required:** %d" % counts["needs-dependency-evidence"],
        "- **Structural upgrade required (enriched tier):** %d" % counts["needs-structural-upgrade"],
        "- **Integrity remediation required:** %d" % counts["needs-integrity-remediation"],
        "- **Stub repair required:** %d" % counts["needs-stub-repair"],
        "- **Invalid repair required:** %d" % counts["needs-invalid-repair"],
        "- **Test fixture (excluded from production metrics):** %d" % counts["test-fixture"],
        "- **Coverage:** %d/%d canonical files classified (100%%)" % (len(records), len(records)),
        "",
    ]
    lines.append("Per-quality baseline: " + ", ".join(k + "=" + str(quality[k]) for k in sorted(quality)) + ".")
    lines.append("")
    lines.append("Dependency-evidence buckets: " + ", ".join(k + "=" + str(dep_buckets[k]) for k in sorted(dep_buckets)) + ".")
    lines.extend(["", "| Declared version | Skills |", "|---|---:|"])
    for version in sorted(versions):
        lines.append("| " + version + " | " + str(versions[version]) + " |")
    lines.extend(["", PLAN_TEXT.rstrip(), ""])

    sections = (
        ("needs-integrity-remediation", "P0 - Integrity remediation required", "findings"),
        ("needs-invalid-repair", "P0 - Invalid/frontmatter repair required", "reasons"),
        ("needs-stub-repair", "P0 - Stub repair required", "reasons"),
        ("needs-structural-upgrade", "P1 - Structural upgrade required (enriched tier)", "reasons"),
        ("needs-dependency-evidence", "P2 - Dependency evidence required", "deps"),
    )
    for state, heading, mode in sections:
        lines.extend(["## " + heading + " (" + str(counts[state]) + ")", ""])
        group = by_state[state]
        if not group:
            lines.append("_None._")
            lines.append("")
            continue
        for r in group:
            if mode == "findings" and r.findings:
                lines.append("- [" + r.path + "](" + r.path + ") - " + ", ".join(r.findings))
            elif mode == "reasons" and r.reasons:
                lines.append("- [" + r.path + "](" + r.path + ") - " + "; ".join(r.reasons))
            elif mode == "deps":
                lines.append("- [" + r.path + "](" + r.path + ") - badge color " + r.dep_color + " (" + r.dep_message + ")")
            else:
                lines.append("- [" + r.path + "](" + r.path + ")")
        lines.append("")

    lines.extend([
        "## Verified - no modernization action required (" + str(counts["verified"]) + ")",
        "",
        "Counted here: quality tier battle_tested, zero integrity findings, dependency badge verified (green-family).",
        "The full battle-tested list is published by meta/QUALITY-REPORT.md and is intentionally not duplicated here.",
        "Membership of this state changes as P0/P1/P2 batches land; the per-category breakdown lives in the quality report.",
        "",
        "Test fixtures excluded from the states above: " + str(counts["test-fixture"]) + " (see meta/QUALITY-REPORT.md).",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true", help="Print the Markdown report without writing it.")
    args = parser.parse_args()

    records = build_records()
    markdown = render_markdown(records)
    if not args.no_write:
        INVENTORY_PATH.write_text(markdown, encoding="utf-8")
        print("Wrote " + str(INVENTORY_PATH.relative_to(REPO_ROOT)))
    counts = Counter(r.state for r in records)
    print("Summary:", dict(counts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
