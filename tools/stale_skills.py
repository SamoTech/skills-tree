#!/usr/bin/env python3
"""
stale_skills.py

Detects skill files whose dependencies have not been reviewed for more than
--stale-days days, based on the `last_reviewed` field in YAML frontmatter.

Called by .github/workflows/stale-skills.yml on a weekly schedule.

Outputs:
  - stdout: human-readable summary
  - --output <path>: JSON report consumed by the GitHub Actions script step
  - GITHUB_OUTPUT: stale_count=N (for conditional step execution)

Usage:
    python tools/stale_skills.py \\
        --skills-root skills/ \\
        --stale-days 180 \\
        --output stale-report.json

    # Dry run (report only, no GH output writes)
    python tools/stale_skills.py --skills-root skills/ --dry-run
"""

import json
import os
import re
import sys
import argparse
from datetime import datetime, timezone, date
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install PyYAML", file=sys.stderr)
    sys.exit(1)

try:
    from common import skill_path_to_badge_key
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from common import skill_path_to_badge_key


# ---- Frontmatter parsing -------------------------------------------------

def _parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter. Returns {} on failure."""
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}
    try:
        result = yaml.safe_load(m.group(1))
        return result if isinstance(result, dict) else {}
    except yaml.YAMLError:
        return {}


# ---- Date helpers --------------------------------------------------------

def _parse_date(value) -> date | None:
    """Parse a date value from frontmatter. Accepts date objects and YYYY-MM-DD strings."""
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%Y-%m"):
            try:
                return datetime.strptime(value.strip(), fmt).date()
            except ValueError:
                continue
    return None


def _days_since(d: date) -> int:
    return (date.today() - d).days


# ---- Staleness detection -------------------------------------------------

def find_stale_skills(skills_root: Path, stale_days: int) -> list[dict]:
    """
    Walk all skill .md files and return those that are stale.

    A skill is stale when:
      - It has a `dependencies.packages` block in frontmatter (has deps), AND
      - Its `last_reviewed` field is older than stale_days OR missing entirely.
    """
    stale = []
    today = date.today()

    for md_path in sorted(skills_root.rglob("*.md")):
        if md_path.name.lower() == "readme.md":
            continue

        text = md_path.read_text(encoding="utf-8", errors="ignore")
        fm = _parse_frontmatter(text)

        # Only skills with declared dependencies are eligible for staleness
        pkgs = fm.get("dependencies", {}).get("packages", [])
        if not pkgs:
            continue

        last_reviewed_raw = fm.get("last_reviewed")
        last_reviewed_date = _parse_date(last_reviewed_raw)

        if last_reviewed_date is None:
            days_stale = stale_days + 1  # treat missing as overdue
        else:
            days_stale = _days_since(last_reviewed_date)

        if days_stale >= stale_days:
            stale.append({
                "key": skill_path_to_badge_key(str(md_path)),
                "path": str(md_path),
                "title": fm.get("title", md_path.stem),
                "last_reviewed": str(last_reviewed_raw) if last_reviewed_raw else None,
                "days_stale": days_stale,
                "dep_count": len(pkgs),
            })

    # Most stale first
    stale.sort(key=lambda x: x["days_stale"], reverse=True)
    return stale


# ---- GitHub Actions output -----------------------------------------------

def _write_gh_output(key: str, value: str) -> None:
    gh_output = os.environ.get("GITHUB_OUTPUT")
    if gh_output:
        with open(gh_output, "a") as fh:
            fh.write(f"{key}={value}\n")
    else:
        print(f"[local] output: {key}={value}", file=sys.stderr)


# ---- Main ----------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect stale AI skill files based on last_reviewed frontmatter."
    )
    parser.add_argument("--skills-root", default="skills/",
                        help="Root directory containing skill .md files")
    parser.add_argument("--stale-days", type=int, default=180,
                        help="Days without review before a skill is considered stale")
    parser.add_argument("--output", default="stale-report.json",
                        help="Path to write the JSON stale report")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report results without writing files or GH outputs")
    args = parser.parse_args()

    skills_root = Path(args.skills_root)
    if not skills_root.exists():
        print(f"ERROR: skills root '{skills_root}' not found.", file=sys.stderr)
        return 1

    print(f"[stale_skills] Scanning {skills_root} for skills stale after {args.stale_days} days...")
    stale = find_stale_skills(skills_root, args.stale_days)
    print(f"[stale_skills] Found {len(stale)} stale skill(s).")

    if stale:
        for s in stale[:10]:  # show top 10 in CI log
            reviewed = s["last_reviewed"] or "never"
            print(f"  {s['days_stale']:>4}d stale — {s['path']} (last reviewed: {reviewed})")
        if len(stale) > 10:
            print(f"  ... and {len(stale) - 10} more.")

    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "stale_days_threshold": args.stale_days,
        "stale_count": len(stale),
        "stale_skills": stale,
    }

    if args.dry_run:
        print("[stale_skills] DRY RUN — not writing report or GH outputs.")
        print(json.dumps(report, indent=2))
        return 0

    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"[stale_skills] Wrote report to {args.output}")

    _write_gh_output("stale_count", str(len(stale)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
