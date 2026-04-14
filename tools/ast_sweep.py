#!/usr/bin/env python3
"""
ast_sweep.py

Step 3 of the Dependency Watchdog execution protocol.

Parses Python code blocks in skill Markdown files using the AST module,
extracts third-party import statements, validates them against PyPI,
and generates draft dependency frontmatter + badge state updates.

Outputs:
  - meta/skills-sbom.cdx.json         (CycloneDX SBOM)
  - badges/<key>.json                  (updated badge JSONs, served via GitHub Pages on main)
  - sweep-report.md                    (human-readable PR description)

Usage:
    python tools/ast_sweep.py [--skills-root skills/] [--dry-run]

This script is also run by .github/workflows/ast-sweep.yml
"""

import ast
import asyncio
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import httpx
except ImportError:
    print("httpx required: pip install httpx")
    sys.exit(1)

try:
    from common import skill_path_to_badge_key, get_stdlib_modules
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from common import skill_path_to_badge_key, get_stdlib_modules

# ─── Constants ────────────────────────────────────────────────────────────────────────────────────

PYPI_BASE_URL = "https://pypi.org/pypi"

PYPI_ALIASES = {
    "langchain_core": "langchain-core",
    "langchain_community": "langchain-community",
    "langchain_openai": "langchain-openai",
    "sklearn": "scikit-learn",
    "cv2": "opencv-python",
    "PIL": "Pillow",
    "bs4": "beautifulsoup4",
    "yaml": "PyYAML",
    "dotenv": "python-dotenv",
    "attr": "attrs",
    "pkg_resources": "setuptools",
    "usaddress": "usaddress",
}

PSEUDO_CODE_SIGNALS = {
    "magic_", "your_", "custom_", "example_", "placeholder_",
    "coming_soon", "future_", "todo_",
}

# Resolved once at module load — no per-call overhead.
# Note: STDLIB_MODULES is used; STDBOST_MODULES was a typo and has been removed.
STDLIB_MODULES: frozenset[str] = get_stdlib_modules()


# ─── Code Block Extraction ────────────────────────────────────────────────────────────────────────────

def assess_block_confidence(block: str) -> float:
    """Return 0.0–1.0 confidence that this is real, executable Python code."""
    signals = {
        "has_complete_function": bool(re.search(r"def \w+\(", block)),
        "has_assignment": "=" in block and "==" not in block,
        "has_string_literal": bool(re.search(r'["\']', block)),
        "has_ellipsis": "..." in block,
        "has_coming_soon": "coming soon" in block.lower(),
        "has_pseudo_marker": "# pseudo" in block.lower() or "# conceptual" in block.lower(),
        "high_comment_ratio": block.count("#") > len(block.split("\n")) * 0.4,
    }
    if signals["has_coming_soon"] or signals["has_pseudo_marker"]:
        return 0.1
    if signals["has_ellipsis"] and not signals["has_complete_function"]:
        return 0.3
    if signals["high_comment_ratio"] and not signals["has_assignment"]:
        return 0.4
    if signals["has_complete_function"] and signals["has_assignment"]:
        return 0.9
    return 0.6


def extract_imports_from_block(code: str) -> list[str]:
    """Parse a Python code block and return third-party package names."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    packages = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name.split(".")[0]
                packages.add(name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                name = node.module.split(".")[0]
                packages.add(name)

    result = []
    for pkg in packages:
        if not pkg:
            continue
        if pkg in STDLIB_MODULES:
            continue
        if pkg.startswith("_"):
            continue
        normalized = PYPI_ALIASES.get(pkg, pkg.replace("_", "-"))
        is_pseudo = any(normalized.lower().startswith(s) for s in PSEUDO_CODE_SIGNALS)
        if not is_pseudo:
            result.append(normalized)

    return sorted(set(result))


def parse_skill_file(skill_path: Path) -> dict:
    """Extract imports from a skill Markdown file."""
    content = skill_path.read_text(encoding="utf-8", errors="ignore")
    code_blocks = re.findall(r"```python\n(.*?)```", content, re.DOTALL)

    all_packages: set[str] = set()
    low_confidence_packages: set[str] = set()

    for block in code_blocks:
        confidence = assess_block_confidence(block)
        imports = extract_imports_from_block(block)

        if confidence >= 0.5:
            all_packages.update(imports)
        elif confidence >= 0.2:
            low_confidence_packages.update(imports)

    return {
        "path": str(skill_path),
        "packages": sorted(all_packages),
        "low_confidence": sorted(low_confidence_packages - all_packages),
        "code_block_count": len(code_blocks),
    }


# ─── PyPI Validation ───────────────────────────────────────────────────────────────────────────────────────

async def check_pypi_package(client: "httpx.AsyncClient", package: str) -> dict:
    """Query PyPI JSON API to check if a package exists and get its latest version.

    Security notes:
    - follow_redirects=False: PyPI's JSON API never legitimately redirects.
      Following redirects blindly opens SSRF vectors — a compromised mirror,
      DNS-rebinding, or a malicious /etc/hosts entry could redirect to the
      cloud IMDS endpoint (169.254.169.254) or an internal service.
      A redirect response is treated as exists=None (transient error).
    - Content-Type check: validates the response is actually JSON before
      calling r.json(), preventing parse errors from leaking HTML bodies
      (e.g. from a redirect landing on a login page).
    """
    url = f"{PYPI_BASE_URL}/{package}/json"
    try:
        r = await client.get(url, timeout=8.0, follow_redirects=False)

        if r.status_code == 200:
            # Validate Content-Type before deserialising to avoid leaking
            # HTML error pages or internal service responses in error fields.
            ct = r.headers.get("content-type", "")
            if not ct.startswith("application/json"):
                return {
                    "package": package,
                    "exists": None,
                    "latest": None,
                    "error": f"unexpected content-type: {ct[:80]}",
                }
            data = r.json()
            return {
                "package": package,
                "exists": True,
                "latest": data["info"]["version"],
                "summary": data["info"].get("summary", "")[:100],
            }
        elif r.status_code == 404:
            return {"package": package, "exists": False, "latest": None}
        elif r.is_redirect:
            # Redirects are unexpected from pypi.org — treat as transient.
            return {
                "package": package,
                "exists": None,
                "latest": None,
                "error": f"unexpected redirect to {r.headers.get('location', '?')[:120]}",
            }
        else:
            return {
                "package": package,
                "exists": None,
                "latest": None,
                "error": f"HTTP {r.status_code}",
            }
    except httpx.TimeoutException:
        return {"package": package, "exists": None, "latest": None, "error": "timeout"}
    except Exception as exc:
        return {"package": package, "exists": None, "latest": None, "error": str(exc)}


async def validate_packages(packages: list[str]) -> dict[str, dict]:
    """
    Validate all unique packages against PyPI with bounded concurrency.

    Semaphore(20) limits concurrent coroutines to 20 at a time.
    httpx.Limits(max_connections=20) matches the semaphore so the
    connection pool never becomes the bottleneck.
    """
    unique = list(set(packages))
    semaphore = asyncio.Semaphore(20)

    async def check_safe(client: "httpx.AsyncClient", pkg: str) -> dict:
        async with semaphore:
            return await check_pypi_package(client, pkg)

    limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)
    async with httpx.AsyncClient(limits=limits) as client:
        tasks = [check_safe(client, pkg) for pkg in unique]
        results = await asyncio.gather(*tasks)

    return {r["package"]: r for r in results}


# ─── Badge State Computation ────────────────────────────────────────────────────────────────────────────

def compute_badge_state(skill_result: dict, pypi_results: dict) -> dict:
    """Determine the badge JSON for a skill based on its packages and PyPI results."""
    packages = skill_result["packages"]

    if not packages:
        return {
            "schemaVersion": 1, "label": "deps", "message": "unscanned",
            "color": "lightgrey", "style": "flat-square",
        }

    unknown  = [p for p in packages if pypi_results.get(p, {}).get("exists") is False]
    uncertain = [p for p in packages if pypi_results.get(p, {}).get("exists") is None]
    confirmed = [p for p in packages if pypi_results.get(p, {}).get("exists") is True]

    if unknown:
        return {
            "schemaVersion": 1, "label": "deps",
            "message": f"\u26a0\ufe0f {len(unknown)} unknown pkg{'s' if len(unknown) > 1 else ''}",
            "color": "orange", "style": "flat-square",
        }
    elif uncertain and not confirmed:
        return {
            "schemaVersion": 1, "label": "deps", "message": "pypi-uncertain",
            "color": "grey", "style": "flat-square",
        }
    else:
        pkg_count = len(confirmed)
        return {
            "schemaVersion": 1, "label": "deps",
            "message": f"machine-inferred \u00b7 {pkg_count} pkg{'s' if pkg_count != 1 else ''}",
            "color": "yellow", "style": "flat-square",
        }


# ─── SBOM Generation ─────────────────────────────────────────────────────────────────────────────────────────

def generate_sbom(all_skill_results: list[dict], pypi_results: dict) -> dict:
    """
    Generate a CycloneDX-format SBOM from sweep results.

    Only includes packages where pypi_results[pkg]["exists"] is True.
    Unknown packages (Orange badges) are excluded — they don't exist on
    PyPI and including them would pollute the SBOM and waste osv_check calls.
    """
    components: dict[str, dict] = {}

    for skill in all_skill_results:
        for pkg in skill["packages"]:
            pypi_info = pypi_results.get(pkg, {})
            if pypi_info.get("exists") is not True:
                continue
            purl = f"pkg:pypi/{pkg}"
            if purl not in components:
                components[purl] = {
                    "type": "library",
                    "name": pkg,
                    "purl": purl,
                    "version": pypi_info.get("latest", "unknown"),
                    "usedIn": [],
                    "pypiConfirmed": True,
                }
            components[purl]["usedIn"].append(skill["path"])

    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tools": [{"name": "skills-tree/ast_sweep", "version": "1.1.0"}],
            "component": {"type": "library", "name": "SamoTech/skills-tree"},
        },
        "components": list(components.values()),
    }


# ─── Report Generation ─────────────────────────────────────────────────────────────────────────────────────

def generate_report(all_skill_results, pypi_results, badge_states) -> str:
    total  = len(all_skill_results)
    yellow = sum(1 for b in badge_states.values() if "machine-inferred" in b.get("message", ""))
    orange = sum(1 for b in badge_states.values() if "unknown" in b.get("message", ""))
    grey   = sum(1 for b in badge_states.values() if b.get("message") == "unscanned")

    all_pkgs: dict[str, list[str]] = {}
    for s in all_skill_results:
        for p in s["packages"]:
            all_pkgs.setdefault(p, []).append(s["path"])

    unknown_pkgs = [p for p, info in pypi_results.items() if info.get("exists") is False]

    lines = [
        "# AST Sweep Report -- Machine-Generated Draft",
        "",
        "> WARNING: This PR is a **draft**. Do NOT merge without reviewing Orange badges and unknown packages.",
        "> Badge promotions from Yellow -> Green require a separate human verification PR.",
        "",
        "## Summary",
        "",
        "| State | Count |",
        "|---|---|",
        f"| Yellow Machine-inferred (pypi-confirmed) | {yellow} |",
        f"| Orange Unknown packages (pypi-unknown) | {orange} |",
        f"| Grey Unscanned (no imports found) | {grey} |",
        f"| **Total skills processed** | **{total}** |",
        "",
        "## Package Coverage",
        "",
        f"- **{len(all_pkgs)} unique packages** extracted across all skills",
        f"- **{len(pypi_results) - len(unknown_pkgs)} packages** confirmed on PyPI",
        f"- **{len(unknown_pkgs)} packages** NOT found on PyPI -- require author annotation",
        "",
    ]

    if unknown_pkgs:
        lines += [
            "## Unknown Packages (Require Author Action)",
            "",
            "These packages were not found on PyPI. Each skill using them has an Orange badge.",
            "Skill authors should add `type: illustrative` to the relevant code block, or fix the package name.",
            "",
        ]
        for pkg in sorted(unknown_pkgs):
            skills_using = all_pkgs.get(pkg, [])
            lines.append(f"- `{pkg}` -- used in: {', '.join(f'`{s}`' for s in skills_using[:3])}")
            if len(skills_using) > 3:
                lines.append(f"  *(+{len(skills_using) - 3} more)*")

    lines += [
        "",
        "## Next Steps",
        "",
        "1. Review Orange badges and add `type: illustrative` annotations or fix package names",
        "2. SBOM has been written to `meta/skills-sbom.cdx.json` (confirmed packages only)",
        "3. Badge JSONs have been written to `badges/` -- served directly via GitHub Pages on main",
        "4. See `meta/badge-states.md` for verification PR template",
        "",
        f"*Generated by `tools/ast_sweep.py` on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*",
    ]

    return "\n".join(lines)


# ─── Main ────────────────────────────────────────────────────────────────────────────────────────────

async def async_main(args):
    skills_root = Path(args.skills_root)
    if not skills_root.exists():
        print(f"ERROR: '{skills_root}' not found. Run from repo root.")
        return 1

    # Log stdlib source here (inside async_main) rather than at module load
    # so it doesn't fire on every import in test environments.
    print(
        f"[ast_sweep] STDLIB_MODULES loaded: {len(STDLIB_MODULES)} names "
        f"({'sys.stdlib_module_names' if hasattr(sys, 'stdlib_module_names') else 'fallback'})",
        file=sys.stderr,
    )

    skill_files = sorted(skills_root.rglob("*.md"))
    print(f"Scanning {len(skill_files)} skill files...")

    all_results = []
    for f in skill_files:
        result = parse_skill_file(f)
        all_results.append(result)
        if result["packages"]:
            print(f"  {f}: {result['packages']}")

    all_packages = list({p for r in all_results for p in r["packages"]})
    print(f"\nValidating {len(all_packages)} unique packages against PyPI...")
    pypi_results = await validate_packages(all_packages)

    confirmed = sum(1 for v in pypi_results.values() if v.get("exists") is True)
    unknown   = sum(1 for v in pypi_results.values() if v.get("exists") is False)
    print(f"  Confirmed: {confirmed}  |  Unknown: {unknown}  |  Uncertain: {len(all_packages) - confirmed - unknown}")

    if args.dry_run:
        print("\n[DRY RUN] Skipping file writes.")
        return 0

    badge_states: dict[str, dict] = {}
    for result in all_results:
        key = skill_path_to_badge_key(result["path"])
        badge_states[key] = compute_badge_state(result, pypi_results)

    badge_output = Path(args.badge_output)
    badge_output.mkdir(parents=True, exist_ok=True)
    for key, badge in badge_states.items():
        (badge_output / f"{key}.json").write_text(json.dumps(badge, indent=2), encoding="utf-8")
    print(f"\nWrote {len(badge_states)} badge JSONs to {badge_output}/")

    sbom = generate_sbom(all_results, pypi_results)
    sbom_path = Path(args.sbom_output)
    sbom_path.parent.mkdir(parents=True, exist_ok=True)
    sbom_path.write_text(json.dumps(sbom, indent=2), encoding="utf-8")
    print(f"Wrote SBOM to {sbom_path} ({len(sbom['components'])} confirmed packages)")

    report = generate_report(all_results, pypi_results, badge_states)
    Path("sweep-report.md").write_text(report, encoding="utf-8")
    print("Wrote sweep-report.md")

    return 0


def main():
    parser = argparse.ArgumentParser(description="AST dependency sweep for Skills Tree.")
    parser.add_argument("--skills-root", default="skills", help="Path to skills/ directory")
    parser.add_argument("--badge-output", default="badges", help="Output dir for badge JSONs")
    parser.add_argument("--sbom-output", default="meta/skills-sbom.cdx.json", help="Output path for SBOM")
    parser.add_argument("--dry-run", action="store_true", help="Print results only, don't write files")
    args = parser.parse_args()
    return asyncio.run(async_main(args))


if __name__ == "__main__":
    exit(main())
