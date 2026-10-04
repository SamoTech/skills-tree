#!/usr/bin/env python3
"""Reconcile canonical Skills Tree entries with existing Agent Skills packages."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.generate_agent_skills import project

LEGACY_SOURCE_ALIASES = {
    "github-api": "skills/07-tool-use/github-api.md",
    "web-search": "skills/07-tool-use/web-search.md",
}

NAME_RE = re.compile(r"^(?!.*--)[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
INTENTIONAL_AUXILIARY_PACKAGES = {"skills-tree-registry"}
FM_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)

def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

def parse_frontmatter(text: str) -> dict[str, str]:
    match = FM_RE.match(text)
    if not match:
        return {}
    result = {}
    section = ""
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        if line.startswith((" ", "\t")):
            key, value = line.strip().split(":", 1)
            if section == "metadata" and key.strip() == "source":
                result["source"] = value.strip().strip('"').strip("'")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        result[key] = value.strip().strip('"').strip("'")
        section = key if key == "metadata" else ""
    return result

def canonical_files(root: Path) -> list[Path]:
    return sorted(p for p in (root / "skills").rglob("*.md") if p.name.lower() != "readme.md")

def canonical_records(root: Path) -> list[dict]:
    records = []
    for path in canonical_files(root):
        rel = path.relative_to(root).as_posix()
        category_dir = path.parent.name
        category = re.sub(r"^\d+-", "", category_dir)
        stem = path.stem
        records.append({"source": rel, "id": stem, "base_name": normalize(stem), "category": category, "category_dir": category_dir})
    return records

def desired_names(records: list[dict]) -> tuple[dict[str, str], dict[str, list[str]]]:
    groups = {}
    for record in records:
        groups.setdefault(record["base_name"], []).append(record)
    desired, collisions = {}, {}
    for base, group in groups.items():
        if len(group) == 1:
            desired[group[0]["source"]] = base
            continue
        collisions[base] = [r["source"] for r in group]
        for record in group:
            candidate = normalize(f'{record["category"]}-{base}')
            desired[record["source"]] = candidate if NAME_RE.fullmatch(candidate) else normalize(f'{record["category_dir"]}-{base}')
    return desired, collisions

def existing_packages(root: Path) -> dict[str, dict]:
    result = {}
    for path in sorted((root / "agent-skills").glob("*/SKILL.md")):
        package = path.parent.name
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        source = fm.get("source", "")
        if not source:
            explicit = re.findall(r"(?im)^\s*(?:canonical source|canonical skill):\s*`?(skills/[^`\s]+\.md)", text)
            if len(set(explicit)) == 1:
                source = explicit[0]
        if not source and package in LEGACY_SOURCE_ALIASES:
            source = LEGACY_SOURCE_ALIASES[package]
        result[package] = {"package": package, "path": path.relative_to(root).as_posix(), "frontmatter_name": fm.get("name", ""), "source": source, "description": fm.get("description", "")}
    return result

def reconcile(root: Path) -> dict:
    records = canonical_records(root)
    desired, collisions = desired_names(records)
    existing = existing_packages(root)
    by_source = {r["source"]: r for r in records}
    by_desired = {desired[src]: src for src in desired}
    source_packages = {}
    for package, current in existing.items():
        if current["source"]:
            source_packages.setdefault(current["source"], []).append(current)

    matched, inferred, missing, rename_needed, drifted, blocked_existing, legacy_compatibility = [], [], [], [], [], [], []
    for source, record in by_source.items():
        expected = desired[source]
        candidates = source_packages.get(source, [])
        canonical = project(root / source, root, name_override=expected)
        expected_candidates = [item for item in candidates if item["package"] == expected]
        legacy_candidates = [item for item in candidates if item["package"] != expected]

        if len(expected_candidates) > 1:
            raise ValueError(f"multiple deterministic packages declare canonical source {source!r}")

        if expected_candidates:
            current = expected_candidates[0]
            item = {"source": source, "package": current["package"], "expected_package": expected, "match": "provenance"}
            matched.append(item)
            expected_content = canonical.content.rstrip() + "\n"
            actual_content = (root / current["path"]).read_text(encoding="utf-8")
            if canonical.eligible:
                if actual_content != expected_content:
                    drifted.append({"source": source, "package": current["package"], "reason": "content-differs-from-deterministic-projection"})
            else:
                blocked_existing.append({"source": source, "package": current["package"], "blockers": list(canonical.blockers)})
            for legacy in legacy_candidates:
                legacy_item = {**legacy, "expected_package": expected, "match": "legacy-compatibility"}
                legacy_compatibility.append(legacy_item)
                matched.append(legacy_item)
                rename_needed.append(legacy_item)
        elif legacy_candidates:
            for legacy in legacy_candidates:
                legacy_item = {**legacy, "expected_package": expected, "match": "legacy-compatibility"}
                legacy_compatibility.append(legacy_item)
                matched.append(legacy_item)
                if canonical.eligible:
                    rename_needed.append(legacy_item)
            if canonical.eligible:
                missing.append({"source": source, "package": expected, "eligible": True, "blockers": [], "reason": "deterministic-projection-missing; legacy-compatibility-package-present"})
            else:
                blocked_existing.append({"source": source, "package": legacy_candidates[0]["package"], "blockers": list(canonical.blockers)})
        elif expected in existing and not existing[expected]["source"]:
            inferred_item = {"source": source, "package": expected, "match": "name-only"}
            inferred.append(inferred_item)
            canonical = project(root / source, root)
            if canonical.eligible:
                actual_content = (root / existing[expected]["path"]).read_text(encoding="utf-8")
                expected_content = canonical.content.rstrip() + "\n"
                if actual_content != expected_content:
                    drifted.append({"source": source, "package": expected, "reason": "content-differs-from-deterministic-projection"})
            else:
                blocked_existing.append({"source": source, "package": expected, "blockers": list(canonical.blockers)})
        else:
            canonical = project(root / source, root)
            missing.append({"source": source, "package": expected, "eligible": canonical.eligible, "blockers": list(canonical.blockers)})

    extras, stale, ambiguous = [], [], []
    mapped_packages = {item["package"] for item in matched}
    mapped_packages.update(item["package"] for item in legacy_compatibility)
    for package, current in existing.items():
        if package in mapped_packages:
            continue
        source = current["source"]
        if source and source not in by_source:
            stale.append(current)
        elif package not in by_desired:
            extras.append(current)
        elif not source:
            inferred_sources = [src for src, name in desired.items() if name == package]
            if inferred_sources:
                continue
            extras.append(current)
        else:
            ambiguous.append({"package": package, "declared_source": source})

    desired_name_sources = {}
    for source, package in desired.items():
        desired_name_sources.setdefault(package, []).append(source)
    resolved_name_collisions = collisions
    unresolved_collisions = {
        package: sources
        for package, sources in desired_name_sources.items()
        if len(sources) > 1
    }
    unexpected = [
        item for item in [*extras, *stale]
        if item["package"] not in INTENTIONAL_AUXILIARY_PACKAGES
    ]

    return {
        "canonical_count": len(records),
        "existing_package_count": len(existing),
        "matched_by_provenance": matched,
        "matched_by_name_only": inferred,
        "legacy_compatibility": legacy_compatibility,
        "missing": missing,
        "rename_needed": rename_needed,
        "drifted": drifted,
        "blocked_existing": blocked_existing,
        "eligible_missing": [item for item in missing if item["eligible"]],
        "blocked_missing": [item for item in missing if not item["eligible"]],
        "extra": extras,
        "unexpected": unexpected,
        "stale": stale,
        "resolved_name_collisions": resolved_name_collisions,
        "unresolved_collisions": unresolved_collisions,
        "ambiguous": ambiguous,
        "collisions": collisions,
        "collision_resolution": {source: desired[source] for sources in collisions.values() for source in sources},
    }

def reconciliation_failures(report: dict) -> list[str]:
    failures = []
    for key in ("eligible_missing", "drifted", "stale", "ambiguous", "unexpected", "unresolved_collisions"):
        items = report.get(key, [])
        if items:
            failures.append(f"{key}: {len(items)}")
    return failures

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true", help="fail on reconciliation drift that invalidates the canonical projection")
    args = parser.parse_args()
    report = reconcile(args.root.resolve())
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    if args.check:
        failures = reconciliation_failures(report)
        if failures:
            print("Reconciliation check failed: " + ", ".join(failures), file=sys.stderr)
            return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
