#!/usr/bin/env python3
"""Apply verified Agent Skills reconciliation and generate the eligible corpus."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.generate_agent_skills import project, write_projection
from tools.reconcile_agent_skills import reconcile


def _rewrite_package_name(text: str, package_name: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Agent Skill package is missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("Agent Skill package has unterminated YAML frontmatter") from exc
    for index in range(1, end):
        if lines[index].startswith("name:"):
            lines[index] = f"name: {package_name}"
            return "\n".join(lines) + "\n"
    raise ValueError("Agent Skill package frontmatter is missing name")

def apply(root: Path) -> tuple[int, int]:
    report = reconcile(root)
    renames = report["rename_needed"]

    for item in renames:
        source = root / "agent-skills" / item["package"] / "SKILL.md"
        target = root / "agent-skills" / item["expected_package"] / "SKILL.md"
        if not source.exists():
            raise FileNotFoundError(source)
        if target.exists() and target.resolve() != source.resolve():
            raise FileExistsError(f"rename target already exists: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        package_text = source.read_text(encoding="utf-8")
        package_text = _rewrite_package_name(package_text, item["expected_package"])
        target.write_text(package_text, encoding="utf-8")
        source.unlink()
        try:
            source.parent.rmdir()
        except OSError:
            pass

    generated = 0
    desired_names = report["collision_resolution"]
    for source in sorted(
        p for p in (root / "skills").rglob("*.md") if p.name.lower() != "readme.md"
    ):
        item = project(source, root, name_override=desired_names.get(source.relative_to(root).as_posix()))
        if item.eligible:
            write_projection(root, item)
            generated += 1

    return len(renames), generated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    renamed, generated = apply(args.root.resolve())
    print(f"Renamed {renamed} legacy Agent Skills packages.")
    print(f"Generated {generated} eligible canonical Agent Skills packages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
