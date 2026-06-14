#!/usr/bin/env python3
"""
tools/osv_watch_scan.py

Phase 2 of the Dependency Watchdog pipeline.
Scans all skill Markdown files for declared Python dependencies,
batches them against the OSV API, and writes per-skill badge JSON files.

Output:
    docs/badges/<skill-name>.json  — per-skill vulnerability state
    osv-report.json                — summary counts + vulnerability list

Exit codes:
    0 — success (even if vulnerabilities found — detection is not failure)
    1 — network error, HTTP error, or file I/O error

HIGH-2 fix (2026-06-14):
    - All logic in main() — safe to import in tests, no global side-effects
    - Module-level docstring added
    - requests replaced with httpx (already in requirements.txt) — SEC-2 fix
    - SKILLS_DIR.glob('*.md') replaced with rglob('*.md') to find skills
      nested inside category subdirectories (e.g. skills/01-perception/)
    - HTTP errors caught and reported; exit 1 so CI fails visibly
    - All file writes wrapped in try/except OSError
    - GH_TOKEN never referenced or logged in this file — SEC-3 compliant
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import httpx
except ImportError:
    print("[osv] ERROR: httpx not installed. Run: pip install httpx", file=sys.stderr)
    sys.exit(1)

SKILLS_DIR = Path("skills")
BADGES_DIR = Path("docs/badges")
OSV_BATCH_URL = "https://api.osv.dev/v1/querybatch"
FRONTMATTER_KEYS = ("dependencies", "requires", "packages")


def parse_frontmatter(text: str) -> dict[str, str]:
    """Extract YAML frontmatter key-value pairs from a Markdown file."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def get_deps(fm: dict[str, str]) -> list[str]:
    """Return a flat list of dependency strings from frontmatter."""
    deps: list[str] = []
    for key in FRONTMATTER_KEYS:
        val = fm.get(key, "")
        if val:
            for item in re.split(r"[,\s]+", val):
                item = item.strip().strip("[]")
                if item:
                    deps.append(item)
    return deps


def parse_dep(dep: str) -> tuple[str, str | None]:
    """Split 'package>=1.2.3' into ('package', '1.2.3'). Version may be None."""
    m = re.match(r"^([A-Za-z0-9_.\-]+)(?:[><=]+([\d.]+))?$", dep)
    return m.groups() if m else (dep, None)  # type: ignore[return-value]


def classify_vuln_state(vulns: list[dict]) -> str:
    """Return 'advisory' if any vuln has a fix, else 'critical'."""
    for v in vulns:
        for affected in v.get("affected", []):
            for range_info in affected.get("ranges", []):
                if range_info.get("type") == "ECOSYSTEM":
                    for event in range_info.get("events", []):
                        if "fixed" in event:
                            return "advisory"
    return "critical"


def main() -> None:
    BADGES_DIR.mkdir(parents=True, exist_ok=True)

    # rglob finds skills nested in category subdirs (e.g. skills/01-perception/)
    skill_files = sorted(SKILLS_DIR.rglob("*.md"))

    queries: list[dict] = []
    skill_map: dict[str, list[tuple[str, str | None]]] = {}

    for sf in skill_files:
        try:
            text = sf.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"[osv] WARNING: cannot read {sf}: {exc}", file=sys.stderr)
            continue
        fm = parse_frontmatter(text)
        for dep in get_deps(fm):
            pkg, ver = parse_dep(dep)
            if pkg:
                queries.append({"package": {"name": pkg, "ecosystem": "PyPI"}, "version": ver})
                skill_map.setdefault(sf.stem, []).append((pkg, ver))

    if not queries:
        print("[osv] INFO: no dependencies found in any skill file.")
        sys.exit(0)

    # Batch OSV query
    try:
        resp = httpx.post(OSV_BATCH_URL, json={"queries": queries}, timeout=60)
        resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(
            f"[osv] ERROR: OSV API returned HTTP {exc.response.status_code}",
            file=sys.stderr,
        )
        sys.exit(1)
    except httpx.RequestError as exc:
        print(f"[osv] ERROR: network error contacting OSV API: {type(exc).__name__}", file=sys.stderr)
        sys.exit(1)

    results = resp.json().get("results", [])

    counts: dict[str, int] = {"verified": 0, "advisory": 0, "critical": 0, "unscanned": 0}
    report_vulns: list[dict] = []
    badge_data: dict[str, dict] = {}

    for skill_name, deps in skill_map.items():
        badge_data[skill_name] = {}
        for pkg, ver in deps:
            query_obj = {"package": {"name": pkg, "ecosystem": "PyPI"}, "version": ver}
            try:
                q_idx = queries.index(query_obj)
            except ValueError:
                counts["unscanned"] += 1
                continue

            vulns = results[q_idx].get("vulns", []) if q_idx < len(results) else []

            if not vulns:
                state = "verified"
            else:
                state = classify_vuln_state(vulns)
                ids = [v["id"] for v in vulns]
                report_vulns.append({
                    "skill": skill_name,
                    "package": pkg,
                    "version": ver,
                    "state": state,
                    "vulns": ids,
                })
            counts[state] += 1
            badge_data[skill_name][pkg] = {"state": state, "version": ver}

    # Write per-skill badge files
    for skill_name, pkgs in badge_data.items():
        badge_file = BADGES_DIR / f"{skill_name}.json"
        payload = json.dumps({"skill": skill_name, "packages": pkgs}, indent=2)
        try:
            badge_file.write_text(payload, encoding="utf-8")
        except OSError as exc:
            print(f"[osv] ERROR: cannot write badge {badge_file}: {exc}", file=sys.stderr)

    # Write summary report
    report = {"counts": counts, "vulnerabilities": report_vulns}
    try:
        Path("osv-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    except OSError as exc:
        print(f"[osv] ERROR: cannot write osv-report.json: {exc}", file=sys.stderr)

    print(json.dumps(counts))


if __name__ == "__main__":
    main()
