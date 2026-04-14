#!/usr/bin/env python3
"""
bootstrap_badges.py

Step 2 of the Dependency Watchdog execution protocol.

Generates one badge JSON file per skill in the `badge-data` branch,
initializing all badges to state `unscanned` (grey).

Run once to bootstrap. After this, the OSV cron and AST sweep
will update individual badge JSONs as coverage progresses.

Output: writes JSON files to ./badge-data-output/ (local preview).
The GitHub Action (deploy-badge-data.yml) pushes these to the badge-data branch.

Usage:
    python tools/bootstrap_badges.py --dry-run   # preview counts only
    python tools/bootstrap_badges.py             # write files to badge-data-output/
"""

import json
import argparse
import sys
from pathlib import Path

# Import shared key utility — single source of truth
try:
    from common import skill_path_to_badge_key
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from common import skill_path_to_badge_key

UNSCANNED_BADGE = {
    "schemaVersion": 1,
    "label": "deps",
    "message": "unscanned",
    "color": "lightgrey",
    "style": "flat-square",
    "namedLogo": "dependabot",
    "logoColor": "white",
}


def main():
    parser = argparse.ArgumentParser(description="Bootstrap badge-data branch with unscanned badges.")
    parser.add_argument("--dry-run", action="store_true", help="Print counts only, don't write files.")
    parser.add_argument("--skills-root", default="skills", help="Path to skills/ directory (default: skills/)")
    parser.add_argument("--output-dir", default="badge-data-output", help="Local output directory for badge JSONs")
    args = parser.parse_args()

    skills_root = Path(args.skills_root)
    if not skills_root.exists():
        print(f"ERROR: skills directory '{skills_root}' not found. Run from repo root.")
        return 1

    skill_files = sorted(skills_root.rglob("*.md"))
    print(f"Found {len(skill_files)} skill files in {skills_root}/")

    if args.dry_run:
        print("\n[DRY RUN] Would create these badge keys:")
        for f in skill_files[:10]:
            print(f"  {skill_path_to_badge_key(f)}.json")
        if len(skill_files) > 10:
            print(f"  ... and {len(skill_files) - 10} more")
        print(f"\nTotal: {len(skill_files)} badge files. Run without --dry-run to write.")
        return 0

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0
    for skill_path in skill_files:
        badge_key = skill_path_to_badge_key(skill_path)
        badge_file = output_dir / f"{badge_key}.json"

        if badge_file.exists():
            skipped += 1
            continue

        badge_file.write_text(json.dumps(UNSCANNED_BADGE, indent=2))
        written += 1

    print(f"\nBootstrap complete:")
    print(f"  Written : {written} new badge files")
    print(f"  Skipped : {skipped} already existed")
    print(f"  Output  : {output_dir}/")
    print(f"\nNext step: commit output to badge-data branch and push to origin.")
    print(f"           See .github/workflows/deploy-badge-data.yml")
    return 0


if __name__ == "__main__":
    exit(main())
