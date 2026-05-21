#!/usr/bin/env python3
"""
ast_sweep.py

Step 3 of the Dependency Watchdog execution protocol.

Parses Python code blocks in skill Markdown files using the AST module,
extracts third-party import statements, validates them against PyPI,
and generates draft dependency frontmatter + badge state updates.

Outputs:
  - meta/skills-sbom.cdx.json         (CycloneDX SBOM)
  - badges/<key>.json                  (updated badge JSONs)
  - sweep-report.md                    (human-readable PR description)

Usage (legacy — scan all skills):
    python tools/ast_sweep.py [--skills-root skills/] [--dry-run]

Usage (per-PR mode — called by ast-sweep.yml):
    python tools/ast_sweep.py --files "path/a.md\npath/b.md" --output docs/sbom/
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

# ─── Constants ────────────────────────────────────────────────────────────────

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

STDLIB_MODULES: frozenset[str] = get_stdlib_modules()

# ─── Code Block Extraction ────────────────────────────────────────────────────

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


# ─── PyPI Validation ──────────────────────────────────────────────────────────

# Safe package name regex (SSRF hardening) — same as in osv_watch.py
_SAFE_PKG_RE = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$')


async def check_pypi_package(client: "httpx.AsyncClient", package: str) -> dict:
    """Query PyPI JSON API. Validates package name before constructing URL."""
    if not _SAFE_PKG_RE.match(package):
        return {"package": package, "exists": False, "latest": None,
                "error": "invalid package name"}
    url = f"{PYPI_BASE_URL}/{package}/json"
    try:
        r = await client.get(url, timeout=8.0, follow_redirects=False)
        if r.status_code == 200:
            ct = r.headers.get("content-type", "")
            if not ct.startswith("application/json"):
                return {"package": package, "exists": None, "latest": None,
                        "error": f"unexpected content-type: {ct[:80]}"}
            data = r.json()
            return {"package": package, "exists": True,
                    "latest": data["info"]["version"],
                    "summary": data["info"].get("summary", "")[:100]}
        elif r.status_code == 404:
            return {"package": package, "exists": False, "latest": None}
        elif r.is_redirect:
            return {"package": package, "exists": None, "latest": None,
                    "error": f"unexpected redirect to {r.headers.get('location', '?')[:120]}"}
        else:
            return {"package": package, "exists": None, "latest": None,
                    "error": f"HTTP {r.status_code}"}
    except httpx.TimeoutException:
        return {"package": package, "exists": None, "latest": None, "error": "timeout"}
    except Exception as exc:
        return {"package": package, "exists": None, "latest": None, "error": str(exc)}


async def validate_packages(packages: list[str]) -> dict[str, dict]:
    """Validate packages against PyPI with bounded concurrency (semaphore=20)."""
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


# ─── Badge State Computation ──────────────────────────────────────────────────

def compute_badge_state(skill_result: dict, pypi_results: dict) -> dict:
    """Determine the badge JSON for a skill based on its packages and PyPI results."""
    packages = skill_result["packages"]

    if not packages:
        return {"schemaVersion": 1, "label": "deps", "message": "unscanned",
                "color": "lightgrey", "style": "flat-square"}

    unknown   = [p for p in packages if pypi_results.get(p, {}).get("exists") is False]
    uncertain = [p for p in packages if pypi_results.get(p, {}).get("exists") is None]
    confirmed = [p for p in packages if pypi_results.get(p, {}).get("exists") is True]

    if unknown:
        return {"schemaVersion": 1, "label": "deps",
                "message": f"\u26a0\ufe0f {len(unknown)} unknown pkg{'s' if len(unknown) > 1 else ''}",
                "color": "orange", "style": "flat-square"}
    elif uncertain and not confirmed:
        return {"schemaVersion": 1, "label": "deps", "message": "pypi-uncertain",
                "color": "grey", "style": "flat-square"}
    else:
        pkg_count = len(confirmed)
        return {"schemaVersion": 1, "label": "deps",
                "message": f"machine-inferred \u00b7 {pkg_count} pkg{'s' if pkg_count != 1 else ''}",
                "color": "yellow", "style": "flat-square"}


# ─── SBOM Generation ─────────────────────────────────────────────────────────

def generate_sbom(all_skill_results: list[dict], pypi_results: dict) -> dict:
    """Generate a CycloneDX-format SBOM from sweep results."""
    components: dict[str, dict] = {}

    for skill in all_skill_results:
        for pkg in skill["packages"]:
            pypi_info = pypi_results.get(pkg, {})
            if pypi_info.get("exists") is not True:
                continue
            purl = f"pkg:pypi/{pkg}"
            if purl not in components:
                components[purl] = {
                    "type": "library", "name": pkg, "purl": purl,
                    "version": pypi_info.get("latest", "unknown"),
                    "usedIn": [], "pypiConfirmed": True,
                }
            components[purl]["usedIn"].append(skill["path"])

    return {
        "bomFormat": "CycloneDX", "specVersion": "1.5", "version": 1,
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tools": [{"name": "skills-tree/ast_sweep", "version": "1.2.0"}],
            "component": {"type": "library", "name": "SamoTech/skills-tree"},
        },
        "components": list(components.values()),
    }


# ─── Report Generation ────────────────────────────────────────────────────────

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
        "# AST Sweep Report -- Machine-Generated D