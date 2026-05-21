#!/usr/bin/env python3
"""
osv_watch.py

Phase 2 of the Dependency Watchdog pipeline — called by osv-watch.yml.

Queries the OSV.dev batch API for every package referenced in the skills
SBOM and in per-skill dependency frontmatter, then writes badge JSON files
and a machine-readable JSON report.

This script supersedes osv_check.py, which used a different CLI interface.
osv_check.py is retained for backward compatibility during the transition
but is no longer called by any workflow.

Badge states written to --badge-output/<skill-key>.json:
  green  (verified)  — no known CVEs for the pinned version
  yellow (advisory)  — CVE exists but frontmatter pins a patched version
  red    (critical)  — active CVE in the pinned version
  grey   (unscanned) — no dependency data in frontmatter

Usage:
    python tools/osv_watch.py \\
        --sbom meta/skills-sbom.cdx.json \\
        --skills-root skills/ \\
        --badge-output docs/badges/ \\
        --report osv-report.json
"""

import json
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime, timezone

try:
    import httpx
except ImportError:
    print("httpx required: pip install httpx", file=sys.stderr)
    sys.exit(1)

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

OSV_BATCH_URL = "https://api.osv.dev/v1/querybatch"

# ---- Safe package name validation (SSRF hardening) ----------------------
_SAFE_PKG_RE = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$')


def _safe_package_name(name: str) -> str | None:
    """Return name if it looks like a valid PyPI package name, else None."""
    name = name.strip()
    if _SAFE_PKG_RE.match(name):
        return name
    return None


# ---- SBOM loading --------------------------------------------------------

def load_sbom(sbom_path: Path) -> list[dict]:
    """Load CycloneDX SBOM components from JSON."""
    if not sbom_path.exists():
        print(f"[osv_watch] SBOM not found at {sbom_path} — skipping SBOM scan.",
              file=sys.stderr)
        return []
    data = json.loads(sbom_path.read_text(encoding="utf-8"))
    return data.get("components", [])


# ---- Skill frontmatter parsing -------------------------------------------

def _parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter between --- delimiters. Returns {} on failure."""
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}
    try:
        result = yaml.safe_load(m.group(1))
        return result if isinstance(result, dict) else {}
    except yaml.YAMLError:
        return {}


def collect_skill_deps(skills_root: Path) -> list[dict]:
    """
    Walk every skill .md file and collect dependency entries from frontmatter.

    Expected frontmatter shape:
        dependencies:
          packages:
            - name: httpx
              pinned_version: 0.28.1
              tested_version: 0.28.1    # optional — used for advisory check

    Returns a flat list of dicts with keys:
        skill_path, skill_key, package, pinned_version, tested_version
    """
    deps = []
    for md_path in sorted(skills_root.rglob("*.md")):
        if md_path.name.lower() == "readme.md":
            continue
        text = md_path.read_text(encoding="utf-8", errors="ignore")
        fm = _parse_frontmatter(text)
        pkgs = fm.get("dependencies", {}).get("packages", [])
        if not pkgs:
            continue
        skill_key = skill_path_to_badge_key(str(md_path))
        for pkg in pkgs:
            if not isinstance(pkg, dict):
                continue
            name = _safe_package_name(str(pkg.get("name", "")))
            if not name:
                continue
            deps.append({
                "skill_path": str(md_path),
                "skill_key": skill_key,
                "package": name,
                "pinned_version": str(pkg.get("pinned_version", "")),
                "tested_version": str(pkg.get("tested_version", "")),
            })
    return deps


# ---- OSV query -----------------------------------------------------------

def query_osv_batch(queries: list[dict]) -> list[dict]:
    """Submit a batch query to OSV.dev and return raw results list."""
    if not queries:
        return []
    try:
        r = httpx.post(OSV_BATCH_URL, json={"queries": queries}, timeout=30.0)
        r.raise_for_status()
        return r.json().get("results", [])
    except httpx.HTTPError as exc:
        print(f"[osv_watch] OSV API error: {exc}", file=sys.stderr)
        return []


def scan_components(components: list[dict]) -> dict[str, list]:
    """
    Query OSV for a list of {name, version, purl} dicts.
    Returns {purl: [vuln, ...]} for packages that have hits.
    """
    versioned = [c for c in components if c.get("version") and c["version"] not in ("unknown", "")]
    if not versioned:
        return {}

    queries = [
        {"package": {"purl": c["purl"]}, "version": c["version"]}
        for c in versioned
    ]
    results = query_osv_batch(queries)

    if len(results) != len(versioned):
        n = min(len(results), len(versioned))
        print(f"[osv_watch] WARNING: OSV length mismatch ({len(results)} vs {len(versioned)}). "
              f"Processing first {n}.", file=sys.stderr)
        versioned = versioned[:n]
        results = results[:n]

    hits = {}
    for comp, result in zip(versioned, results):
        vulns = result.get("vulns", [])
        if vulns:
            hits[comp["purl"]] = vulns
    return hits


# ---- Badge helpers -------------------------------------------------------

def _badge(message: str, color: str) -> dict:
    return {
        "schemaVersion": 1,
        "label": "deps",
        "message": message,
        "color": color,
        "style": "flat-square",
    }


VERIFIED_BADGE  = _badge("\u2705 verified",   "brightgreen")
ADVISORY_BADGE  = _badge("\u26a0\ufe0f advisory", "yellow")
CRITICAL_BADGE  = _badge("\u{1F534} critical",  "critical")
UNSCANNED_BADGE = _badge("unscanned",            "lightgrey")


# ---- Main logic ----------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="OSV vulnerability watch — Phase 2 of the Dependency Watchdog."
    )
    parser.add_argument("--sbom",         default="meta/skills-sbom.cdx.json",
                        help="Path to CycloneDX SBOM JSON")
    parser.add_argument("--skills-root",  default="skills/",
                        help="Root directory containing skill .md files")
    parser.add_argument("--badge-output", default="docs/badges/",
                        help="Output directory for badge JSON files")
    parser.add_argument("--report",       default="osv-report.json",
                        help="Output path for machine-readable scan report")
    parser.add_argument("--dry-run",      action="store_true",
                        help="Print results without writing files")
    args = parser.parse_args()

    skills_root  = Path(args.skills_root)
    badge_output = Path(args.badge_output)
    sbom_path    = Path(args.sbom)

    # ------------------------------------------------------------------
    # 1. Collect all skill-level dependency declarations from frontmatter
    # ------------------------------------------------------------------
    print("[osv_watch] Collecting skill dependency declarations...")
    skill_deps = collect_skill_deps(skills_root)
    print(f"[osv_watch] Found {len(skill_deps)} package declarations across skill files.")

    # Build unique package+version set for OSV query
    # Prefer tested_version over pinned_version (tested = human-verified)
    seen_purls: dict[str, dict] = {}  # purl -> component
    skill_key_packages: dict[str, list[dict]] = {}  # skill_key -> [pkg_info]

    for dep in skill_deps:
        version = dep["tested_version"] or dep["pinned_version"]
        if not version:
            continue
        purl = f"pkg:pypi/{dep['package'].lower()}"
        if purl not in seen_purls:
            seen_purls[purl] = {"name": dep["package"], "purl": purl, "version": version}
        skill_key_packages.setdefault(dep["skill_key"], []).append({
            "purl": purl, "skill_path": dep["skill_path"]
        })

    # ------------------------------------------------------------------
    # 2. Also pull components from SBOM (for machine-inferred packages)
    # ------------------------------------------------------------------
    sbom_components = load_sbom(sbom_path)
    for comp in sbom_components:
        purl = comp.get("purl", "")
        if purl and purl not in seen_purls and comp.get("version"):
            name = _safe_package_name(comp.get("name", ""))
            if name:
                seen_purls[purl] = {"name": name, "purl": purl, "version": comp["version"]}

    # ------------------------------------------------------------------
    # 3. Query OSV
    # ------------------------------------------------------------------
    print(f"[osv_watch] Querying OSV for {len(seen_purls)} unique packages...")
    vuln_hits = scan_components(list(seen_purls.values()))
    print(f"[osv_watch] {len(vuln_hits)} packages with active advisories.")

    # ------------------------------------------------------------------
    # 4. Determine badge state per skill
    # ------------------------------------------------------------------
    # All skill keys that have any dependency declaration
    all_skill_keys_with_deps = set(skill_key_packages.keys())

    # Also collect all skill keys from the full skills tree
    all_skill_keys: set[str] = set()
    for md_path in sorted(skills_root.rglob("*.md")):
        if md_path.name.lower() != "readme.md":
            all_skill_keys.add(skill_path_to_badge_key(str(md_path)))

    badge_states: dict[str, dict] = {}
    counts = {"verified": 0, "advisory": 0, "critical": 0, "unscanned": 0}

    for key in all_skill_keys:
        pkgs = skill_key_packages.get(key, [])
        if not pkgs:
            badge_states[key] = UNSCANNED_BADGE
            counts["unscanned"] += 1
            continue

        has_critical = any(p["purl"] in vuln_hits for p in pkgs)
        if has_critical:
            # Check if any hit is specifically critical severity
            is_crit = False
            for p in pkgs:
                for vuln in vuln_hits.get(p["purl"], []):
                    sev = vuln.get("database_specific", {}).get("severity", "")
                    if sev.upper() in ("CRITICAL", "HIGH"):
                        is_crit = True
            if is_crit:
                badge_states[key] = CRITICAL_BADGE
                counts["critical"] += 1
            else:
                badge_states[key] = ADVISORY_BADGE
                counts["advisory"] += 1
        else:
            badge_states[key] = VERIFIED_BADGE
            counts["verified"] += 1

    # ------------------------------------------------------------------
    # 5. Write outputs
    # ------------------------------------------------------------------
    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "counts": counts,
        "vuln_packages": [
            {
                "purl": purl,
                "name": seen_purls[purl]["name"],
                "version": seen_purls[purl]["version"],
                "vuln_ids": [v["id"] for v in vulns],
            }
            for purl, vulns in vuln_hits.items()
            if purl in seen_purls
        ],
    }

    if args.dry_run:
        print(f"[osv_watch] DRY RUN — badge counts: {counts}")
        print(json.dumps(report, indent=2))
        return 0

    badge_output.mkdir(parents=True, exist_ok=True)
    for key, badge in badge_states.items():
        (badge_output / f"{key}.json").write_text(
            json.dumps(badge, indent=2), encoding="utf-8"
        )
    print(f"[osv_watch] Wrote {len(badge_states)} badge files to {badge_output}/")

    Path(args.report).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"[osv_watch] Wrote report to {args.report}")
    print(f"[osv_watch] Summary: {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
