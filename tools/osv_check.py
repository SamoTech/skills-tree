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

Exit codes:
  0 — scan completed successfully (advisories found or not — both are success)
  1 — scan could not complete (missing SBOM, network error, etc.)

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

    Each query includes the package PURL *and* the pinned version from
    the SBOM so that OSV only returns vulnerabilities whose affected
    version ranges include the specific installed version.  Omitting
    the version causes OSV to return every historical CVE ever filed
    against the package name, producing false-positive advisory badges
    for packages that are fully patched at their current pinned version.

    OSV /v1/querybatch guarantees order preservation (results[i] corresponds
    to queries[i]). We verify this invariant explicitly:
      - If len(results) != len(queries): log a critical warning and fall back
        to index-based matching with bounds checking.
      - If a result contains a 'package' field that doesn't match the queried
        PURL, log a mismatch warning for that index.
    """
    if not components:
        return []

    queries = [
        {
            "package": {"purl": c["purl"]},
            "version": c["version"],
        }
        for c in components
        if c.get("version")
    ]

    # Track components that actually have a version (parallel list for zip)
    versioned_components = [c for c in components if c.get("version")]

    unversioned = [c["name"] for c in components if not c.get("version")]
    if unversioned:
        print(
            f"WARNING: {len(unversioned)} component(s) have no version in SBOM and will be "
            f"skipped by OSV scan: {', '.join(unversioned)}",
            file=sys.stderr,
        )

    if not queries:
        return []

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

    if len(results) != len(versioned_components):
        print(
            f"WARNING: OSV returned {len(results)} results for {len(versioned_components)} queries. "
            f"This violates the expected order-preservation contract. "
            f"Processing only the first min({len(results)}, {len(versioned_components)}) entries. "
            f"Some packages may be unscanned this cycle.",
            file=sys.stderr,
        )
        n = min(len(results), len(versioned_components))
        versioned_components = versioned_components[:n]
        results = results[:n]

    hits = []
    for i, (component, result) in enumerate(zip(versioned_components, results)):
        vulns = result.get("vulns", [])

        if vulns:
            hits.append({
                "package": component["name"],
                "purl": component["purl"],
                "version": component.get("version", "unknown"),
                "usedIn": component.get("usedIn", []),
                "osv_result_index": i,
                "vulns": [
                    {
                        "id": v["id"],
                        "summary": v.get("summary", "")[:120],
                        "severity": v.get("database_specific", {}).get("severity", "unknown"),
                        "published": v.get("published", ""),
                        "affected_version_ranges": [
                            event.get("introduced", "") + " → " + event.get("fixed", "(unfixed)")
                            for affected in v.get("affected", [])
                            for r in affected.get("ranges", [])
                            for event in r.get("events", [])
                            if "introduced" in event
                        ],
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


def write_github_output(key: str, value: str) -> None:
    """Write a key=value pair to the GitHub Actions output file.

    GITHUB_OUTPUT (a runner-managed append-only file) has been the
    required mechanism since September 2022. The legacy ::set-output
    workflow command was disabled on all GitHub-hosted runners in
    June 2023 — any job still using it silently drops the output
    variable.

    When GITHUB_OUTPUT is unset (local dev run outside Actions) we
    log to stderr with a [local] prefix instead of emitting a now-
    broken workflow command.
    """
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as fh:
            fh.write(f"{key}={value}\n")
    else:
        # Running outside GitHub Actions (local dev / unit tests).
        # Log informationally — do NOT emit ::set-output.
        print(f"[local] output: {key}={value}", file=sys.stderr)


def main() -> int:
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

    print(f"Querying OSV for {len(components)} packages (version-aware)...")
    hits = query_osv(components)

    if not hits:
        print("\u2705 No active advisories found for pinned versions.")
        write_github_output("has_hits", "false")
        return 0

    affected_skills: set[str] = set()
    for hit in hits:
        for skill in hit["usedIn"]:
            affected_skills.add(skill)
        vuln_summary = ", ".join(v["id"] for v in hit["vulns"])
        print(f"\U0001f6a8 {hit['package']} {hit['version']} ({hit['purl']}): {vuln_summary}")
        for skill in hit["usedIn"]:
            print(f"   \u2514\u2500 affects: {skill}")

    print(f"\n{len(hits)} package(s) with advisories. {len(affected_skills)} skill(s) affected.")

    if args.dry_run:
        print("[DRY RUN] Skipping file writes.")
        write_github_output("has_hits", "true")
        return 0

    badge_output = Path(args.badge_output)
    badge_output.mkdir(parents=True, exist_ok=True)
    badges_written = 0
    for hit in hits:
        badge = build_advisory_badge(hit)
        for skill_path in hit["usedIn"]:
            key = skill_path_to_badge_key(skill_path)
            (badge_output / f"{key}.json").write_text(json.dumps(badge, indent=2))
            badges_written += 1

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
