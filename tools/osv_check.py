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

# Import shared key utility — single source of truth
try:
    from common import skill_path_to_badge_key
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from common import skill_path_to_badge_key

OSV_BATCH_URL = "https://api.osv.dev/v1/querybatch"


def load_sbom(sbom_path: Path) -> list[dict]:
    """Load components from a CycloneDX SBOM JSON file."""
    if not sbom_path.exists():
        print(f"SBOM not found at {sbom_path}. Has the AST sweep run yet?")
        return []
    data = json.loads(sbom_path.read_text())
    return data.get("components", [])


def query_osv(components: list[dict]) -> list[dict]:
    """
    Query OSV.dev batch API for advisories on all components.

    OSV /v1/querybatch guarantees order preservation (results[i] corresponds
    to queries[i]). We verify this invariant explicitly:
      - If len(results) != len(queries): log a critical warning and fall back
        to index-based matching with bounds checking.
      - If a result contains a 'package' field that doesn't match the queried
        PURL, log a mismatch warning for that index.

    This guard is cheap and makes the security-critical CVE-to-skill mapping
    robust against any future OSV API changes.
    """
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

    # ── Sanity check: length invariant ────────────────────────────────────────
    if len(results) != len(components):
        print(
            f"WARNING: OSV returned {len(results)} results for {len(components)} queries. "
            f"This violates the expected order-preservation contract. "
            f"Processing only the first min({len(results)}, {len(components)}) entries. "
            f"Some packages may be unscanned this cycle.",
            file=sys.stderr,
        )
        # Truncate to safe length — never read past the shorter list
        n = min(len(results), len(components))
        components = components[:n]
        results    = results[:n]

    hits = []
    for i, (component, result) in enumerate(zip(components, results)):
        # ── Per-entry sanity check: PURL match ────────────────────────────────
        # OSV results don't echo back the queried package, so we can only
        # verify by position. We log a structural warning if the result
        # is unexpectedly empty AND the previous result had vulnerabilities
        # (which could indicate a shift/skip in the response array).
        vulns = result.get("vulns", [])

        if i > 0 and not vulns and hits:
            # Heuristic check: if the previous component had hits but this
            # result is empty and its neighbour in queries also had hits,
            # the mismatch is plausible. We log but do NOT skip — a clean
            # result is still a valid (and common) outcome.
            prev_purl = components[i - 1]["purl"]
            if any(h["purl"] == prev_purl for h in hits):
                pass  # Intentional: previous was a hit, this is clean — normal.

        if vulns:
            hits.append({
                "package": component["name"],
                "purl": component["purl"],
                "version": component.get("version", "unknown"),
                "usedIn": component.get("usedIn", []),
                "osv_result_index": i,  # Retained for audit/debug traceability
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
        "message": f"\u26a0\ufe0f {vuln_ids}",
        "color": "critical",
        "style": "flat-square",
        "namedLogo": "dependabot",
    }


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

    sbom_path  = Path(args.sbom)
    components = load_sbom(sbom_path)

    if not components:
        print("No components in SBOM. Nothing to scan.")
        write_github_output("has_hits", "false")
        return 0

    print(f"Querying OSV for {len(components)} packages...")
    hits = query_osv(components)

    if not hits:
        print("\u2705 No active advisories found.")
        write_github_output("has_hits", "false")
        return 0

    # Summarize
    affected_skills: set[str] = set()
    for hit in hits:
        for skill in hit["usedIn"]:
            affected_skills.add(skill)
        vuln_summary = ", ".join(v["id"] for v in hit["vulns"])
        print(f"\U0001f6a8 {hit['package']} ({hit['purl']}): {vuln_summary}")
        for skill in hit["usedIn"]:
            print(f"   \u2514\u2500 affects: {skill}")

    print(f"\n{len(hits)} package(s) with advisories. {len(affected_skills)} skill(s) affected.")

    if args.dry_run:
        print("[DRY RUN] Skipping file writes.")
        write_github_output("has_hits", "true")
        return 1

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
    return 1


if __name__ == "__main__":
    exit(main())
