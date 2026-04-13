#!/usr/bin/env python3
"""
write_badge.py

Low-level utility for reading and writing badge JSON files on the badge-data branch.
Used by all Watchdog workflows to transition badge states.

Usage examples:

  # Mark a skill as verified
  python tools/write_badge.py --skill skills/03-memory/memory-injection.md --status verified

  # Mark a skill as advisory (with CVE)
  python tools/write_badge.py --skill skills/07-tool-use/github-api.md --status advisory --advisory CVE-2026-12345

  # Apply all advisories from an osv-hits.json file
  python tools/write_badge.py --advisory-file osv-hits.json

  # Reset a skill to unscanned
  python tools/write_badge.py --skill skills/03-memory/memory-injection.md --status unscanned
"""

import json
import argparse
import sys
from pathlib import Path

BADGE_STATES = {
    "unscanned": {
        "schemaVersion": 1, "label": "deps", "message": "unscanned",
        "color": "lightgrey", "style": "flat-square",
    },
    "machine-inferred": {
        "schemaVersion": 1, "label": "deps", "message": "machine-inferred",
        "color": "yellow", "style": "flat-square",
    },
    "verified": {
        "schemaVersion": 1, "label": "deps", "message": "✔ verified",
        "color": "22c55e", "style": "flat-square", "namedLogo": "checkmarx",
    },
}


def skill_path_to_badge_key(skill_path: str) -> str:
    return str(skill_path).replace("\\", "/").replace("/", "-").replace(".md", "")


def build_advisory_badge(cve_id: str) -> dict:
    return {
        "schemaVersion": 1, "label": "deps",
        "message": f"⚠️ {cve_id}",
        "color": "critical", "style": "flat-square",
    }


def main():
    parser = argparse.ArgumentParser(description="Update a badge JSON on the badge-data branch.")
    parser.add_argument("--skill", help="Skill file path (e.g. skills/03-memory/memory-injection.md)")
    parser.add_argument("--status", choices=["unscanned", "machine-inferred", "verified", "advisory"],
                        help="New badge state")
    parser.add_argument("--advisory", help="CVE ID (required when --status=advisory)")
    parser.add_argument("--advisory-file", help="JSON file from osv_check.py to apply all advisories")
    parser.add_argument("--output-dir", default="badge-data-output",
                        help="Directory to write badge JSONs (default: badge-data-output)")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Batch mode: apply all advisories from osv-hits.json
    if args.advisory_file:
        data = json.loads(Path(args.advisory_file).read_text())
        written = 0
        for hit in data.get("hits", []):
            cve_ids = ", ".join(v["id"] for v in hit.get("vulns", [])[:2])
            badge = build_advisory_badge(cve_ids)
            for skill_path in hit.get("usedIn", []):
                key = skill_path_to_badge_key(skill_path)
                (output_dir / f"{key}.json").write_text(json.dumps(badge, indent=2))
                written += 1
                print(f"  advisory → {key}.json")
        print(f"Written {written} advisory badges from {args.advisory_file}")
        return 0

    # Single skill mode
    if not args.skill or not args.status:
        parser.error("--skill and --status are required (or use --advisory-file for batch mode)")

    key = skill_path_to_badge_key(args.skill)
    badge_file = output_dir / f"{key}.json"

    if args.status == "advisory":
        if not args.advisory:
            parser.error("--advisory CVE-ID is required when --status=advisory")
        badge = build_advisory_badge(args.advisory)
    else:
        badge = BADGE_STATES[args.status].copy()

    badge_file.write_text(json.dumps(badge, indent=2))
    print(f"✅ {args.skill} → {args.status}")
    print(f"   Written: {badge_file}")
    return 0


if __name__ == "__main__":
    exit(main())
