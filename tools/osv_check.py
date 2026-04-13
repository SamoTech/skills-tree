#!/usr/bin/env python3
"""
osv_check.py

Step 4 of the Dependency Watchdog execution protocol.

Polls the OSV.dev batch query API for active CVE advisories
against all packages in meta/skills-sbom.cdx.json.

Run by .github/workflows/osv-watch.yml on a 15-minute cron schedule.
If advisories are found, writes updated badge JSONs (advisory / red state)
and sets the GitHub Actions output `has_hits=true` to trigger the
badge-data branch commit step.

SLA: badges updated within 15 minutes of CVE appearing in OSV database.
This SLA is documented in meta/badge-states.md.

Usage:
    python tools/osv_check.py [--sbom meta/skills-sbom.cdx.json] [--dry-run]
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone

try:
    import httpx
except ImportError:
    print("httpx required: pip install httpx")
    sys.exit(1)

OSV_BATCH_URL = "https://api.osv.dev/v1/querybatch"


def load_sbom(sbom_path: Path) -> list[dict]:
    """Load components from a CycloneDX SBOM JSON file."""
    if not sbom_path.exists():
        print(f"SBOM not found at {sbom_path}. Has the AST sweep run yet?")
        return []
    data = json.loads(sbom_path.read_text())
    return data.get("components", [])


def query_osv(components: list[dict]) -> list[dict]:
    """Query OSV.dev batch API for advisories on all components."""
    if not components:
        return []

    queries = [{"package": {"purl": c["purl"]}} for c in components]

    try:
        response = httpx.post(
            OSV_BATCH_URL,
            json={"queries": queries},
            timeout=30.0,
        )
        response.raise_for_status()
    except httpx.HTTPError as e:
        print(f"OSV API error: {e}")
        return []

    results = response.json().get("results", [])
    hits = []
    for component, result in zip(components, results):
        vulns = result.get("vulns", [])
        if vulns:
            hits.append({
                "package": component["name"],
                "purl": component["purl"],
                "version": component.get("version", "unknown"),
                "usedIn": component.get("usedIn", []),
                "vulns": [
                    {
                        "id": v["id"],
                        "summary": v.get("summary", "")[:120],
                        "severity": v.get("database_specific", {}).get("severity", "unknown"),
                        "published": v.get("published", ""),
                    }
                    for v in vulns
                ],
            })
    return hits


def build_advisory_badge(hit: dict) -> dict:
    """Build an advisory badge JSON for a skill affected by a CVE."""
    vuln_ids = ", ".join(v["id"] for v in hit["vulns"][:2])
    if len(hit["vulns"]) > 2:
        vuln_ids += f" +{len(hit['vulns']) - 2}"
    return {
        "schemaVersion": 1,
        "label": "deps",
        "message": f"⚠️ {vuln_ids}",
        "color": "critical",
        "style": "flat-square",
        "namedLogo": "dependabot",
    }


def skill_path_to_badge_key(skill_path: str) -> str:
    return skill_path.replace("\\", "/").replace("/", "-").replace(".md", "")


def write_github_output(key: str, value: str):
    """Write a GitHub Actions output variable."""
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"{key}={value}\n")
    else:
        print(f"::set-output name={key}::{value}")


def main():
    parser = argparse.ArgumentParser(description="OSV CVE watchdog for Skills Tree.")
    parser.add_argument("--sbom", default="meta/skills-sbom.cdx.json", help="Path to CycloneDX SBOM")
    parser.add_argument("--badge-output", default="badge-data-output", help="Output dir for badge JSONs")
    parser.add_argument("--advisory-file", default="osv-hits.json", help="Output file for advisory results")
    parser.add_argument("--dry-run", action="store_true", help="Print results only, don't write files")
    args = parser.parse_args()

    sbom_path = Path(args.sbom)
    components = load_sbom(sbom_path)

    if not components:
        print("No components in SBOM. Nothing to scan.")
        write_github_output("has_hits", "false")
        return 0

    print(f"Querying OSV for {len(components)} packages...")
    hits = query_osv(components)

    if not hits:
        print("✅ No active advisories found.")
        write_github_output("has_hits", "false")
        return 0

    # Summarize
    affected_skills = set()
    for hit in hits:
        for skill in hit["usedIn"]:
            affected_skills.add(skill)
        vuln_summary = ", ".join(v["id"] for v in hit["vulns"])
        print(f"🚨 {hit['package']} ({hit['purl']}): {vuln_summary}")
        for skill in hit["usedIn"]:
            print(f"   └─ affects: {skill}")

    print(f"\n{len(hits)} package(s) with advisories. {len(affected_skills)} skill(s) affected.")

    if args.dry_run:
        print("[DRY RUN] Skipping file writes.")
        write_github_output("has_hits", "true")
        return 1  # non-zero to trigger alerts even in dry-run

    # Write advisory badge JSONs
    badge_output = Path(args.badge_output)
    badge_output.mkdir(parents=True, exist_ok=True)
    badges_written = 0
    for hit in hits:
        badge = build_advisory_badge(hit)
        for skill_path in hit["usedIn"]:
            key = skill_path_to_badge_key(skill_path)
            (badge_output / f"{key}.json").write_text(json.dumps(badge, indent=2))
            badges_written += 1

    # Write full advisory file for the Action to post as a comment
    advisory_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sla": "15-minute OSV polling",
        "hits": hits,
        "affected_skills": sorted(affected_skills),
        "badge_keys_updated": [
            skill_path_to_badge_key(s)
            for hit in hits for s in hit["usedIn"]
        ],
    }
    Path(args.advisory_file).write_text(json.dumps(advisory_data, indent=2))

    print(f"Wrote {badges_written} advisory badge JSONs.")
    print(f"Wrote advisory data to {args.advisory_file}")

    write_github_output("has_hits", "true")
    return 1  # Non-zero exit to trigger downstream alert steps


if __name__ == "__main__":
    exit(main())
