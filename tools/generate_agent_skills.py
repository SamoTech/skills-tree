#!/usr/bin/env python3
"""Audit and deterministically project canonical Skills Tree entries to Agent Skills packages.

The canonical source remains skills/. Generation is explicit; CI uses --audit so
validation never mutates a contributor branch.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
PLACEHOLDER_RE = re.compile(r"(?i)^(stub|todo|tbd|placeholder|coming soon|add description)[.! ]*$")
BADGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)|\[[^\]]+\]\([^)]*badge[^)]*\)", re.I)


@dataclass(frozen=True)
class SkillProjection:
    source: Path
    name: str
    description: str
    version: str | None
    category: str
    eligible: bool
    blockers: tuple[str, ...]
    content: str


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key.strip()] = value
    return data, text[match.end() :]


def normalize_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def clean_description(value: str) -> str:
    value = BADGE_RE.sub("", value)
    value = re.sub(r"\s+", " ", value).strip(" -|")
    return value


def project(source: Path, root: Path) -> SkillProjection:
    text = source.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    name = normalize_name(source.stem)
    description = clean_description(fm.get("description", ""))
    category = source.parent.name
    blockers: list[str] = []

    if not name or not NAME_RE.fullmatch(name):
        blockers.append("invalid generated name")
    if not description:
        blockers.append("missing description")
    elif PLACEHOLDER_RE.fullmatch(description):
        blockers.append("placeholder description")
    elif len(description) > 1024:
        blockers.append("description exceeds 1024 characters")
    if "## Evidence" not in body:
        blockers.append("missing Evidence section")
    if len(body.splitlines()) > 500:
        blockers.append("body exceeds 500 lines")

    version = fm.get("version")
    version_yaml = f'  version: "{version}"\n' if version else ""
    package = (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "license: MIT\n"
        "metadata:\n"
        f"  source: {source.relative_to(root).as_posix()}\n"
        f"  category: {category}\n"
        f"{version_yaml}"
        "---\n\n"
        + body.lstrip()
    )
    return SkillProjection(
        source=source,
        name=name,
        description=description,
        version=version,
        category=category,
        eligible=not blockers,
        blockers=tuple(blockers),
        content=package,
    )


def audit(root: Path) -> dict:
    source_root = root / "skills"
    files = sorted(path for path in source_root.rglob("*.md") if path.name.lower() != "readme.md")
    projections = [project(path, root) for path in files]
    collisions: dict[str, list[str]] = {}
    for item in projections:
        collisions.setdefault(item.name, []).append(item.source.relative_to(root).as_posix())
    collisions = {name: paths for name, paths in collisions.items() if len(paths) > 1}
    eligible = [item for item in projections if item.eligible]
    report = {
        "source": "skills/",
        "total": len(projections),
        "eligible": len(eligible),
        "blocked": len(projections) - len(eligible),
        "name_collisions": collisions,
        "blockers": {
            item.source.relative_to(root).as_posix(): list(item.blockers)
            for item in projections
            if item.blockers
        },
    }
    return report


def write_projection(root: Path, item: SkillProjection) -> Path:
    destination = root / "agent-skills" / item.name / "SKILL.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(item.content.rstrip() + "\n", encoding="utf-8")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true", help="fail if any canonical entry is blocked")
    args = parser.parse_args()

    root = args.root.resolve()
    report = audit(root)
    if args.audit or not args.write:
        print(json.dumps(report, indent=2, sort_keys=True))
    if args.check and (report["blocked"] or report["name_collisions"]):
        return 1

    if args.write:
        projections = [
            project(path, root)
            for path in sorted(path for path in (root / "skills").rglob("*.md") if path.name.lower() != "readme.md")
        ]
        if any(not item.eligible for item in projections):
            print("Refusing to generate blocked canonical skills. Run --audit for details.", file=sys.stderr)
            return 2
        if report["name_collisions"]:
            print("Refusing to generate colliding skill names.", file=sys.stderr)
            return 2
        for item in projections:
            write_projection(root, item)
        print(f"Generated {len(projections)} Agent Skills packages.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
