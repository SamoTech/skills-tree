#!/usr/bin/env python3
"""
tools/sync_badges.py

Reconciles docs/badges/ against the current skill inventory in skills/.
Creates missing badge JSON files with 'unscanned' state.
Removes orphan badge files for skills that no longer exist.

Called by .github/workflows/sync-badges.yml.

CRITICAL-1 fix (2026-06-14): Replaces inline Python heredoc in sync-badges.yml.
CRITICAL-3 fix (2026-06-14): Uses docs/badges/ as the single canonical badge
  directory, consistent with osv_watch_scan.py and bootstrap_badges.py.

Exit codes:
    0 — success
    1 — I/O error reading skills or writing badge files
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SKILLS_ROOT = Path("skills")
BADGE_DIR = Path("docs/badges")  # single canonical location — CRITICAL-3

UNSCANNED_BADGE: dict = {
    "schemaVersion": 1,
    "label": "deps",
    "message": "unscanned",
    "color": "lightgrey",
    "style": "flat-square",
}


def skill_to_badge_key(md_path: Path) -> str:
    """Convert a skill path to its canonical badge key (filename without .json)."""
    return str(md_path).replace("\\", "/").replace("/", "-").replace(".md", "")


def main() -> None:
    try:
        BADGE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"[sync-badges] ERROR: cannot create {BADGE_DIR}: {exc}", file=sys.stderr)
        sys.exit(1)

    # Collect all skill keys via rglob — handles nested category subdirs
    try:
        skill_keys = {
            skill_to_badge_key(md)
            for md in SKILLS_ROOT.rglob("*.md")
        }
    except OSError as exc:
        print(f"[sync-badges] ERROR: cannot read {SKILLS_ROOT}: {exc}", file=sys.stderr)
        sys.exit(1)

    created = 0
    errors = 0

    # Create missing badge files
    for key in sorted(skill_keys):
        badge_path = BADGE_DIR / f"{key}.json"
        if not badge_path.exists():
            try:
                badge_path.write_text(json.dumps(UNSCANNED_BADGE, indent=2), encoding="utf-8")
                created += 1
                print(f"  CREATED: {badge_path.name}")
            except OSError as exc:
                print(f"[sync-badges] ERROR: cannot write {badge_path}: {exc}", file=sys.stderr)
                errors += 1

    # Remove orphan badge files
    removed = 0
    try:
        existing = list(BADGE_DIR.glob("*.json"))
    except OSError as exc:
        print(f"[sync-badges] ERROR: cannot list {BADGE_DIR}: {exc}", file=sys.stderr)
        sys.exit(1)

    for badge_file in existing:
        if badge_file.stem not in skill_keys:
            try:
                badge_file.unlink()
                removed += 1
                print(f"  REMOVED: {badge_file.name}")
            except OSError as exc:
                print(f"[sync-badges] ERROR: cannot remove {badge_file}: {exc}", file=sys.stderr)
                errors += 1

    print(f"\nSync complete. Created: {created}, Removed: {removed}, Errors: {errors}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
