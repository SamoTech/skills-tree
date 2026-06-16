"""
Skills Tree Learning Path Recommender

Generates personalized learning paths using the prerequisite dependency graph.

Usage:
    python recommend.py --current "python-basics,api-calls" --target "rag"
    python recommend.py --current "python-basics" --target "production-rag" --json
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Optional

try:
    from skills_tree import SkillsTree
except ImportError:
    raise SystemExit("Run: pip install skills-tree")


def get_learning_path(
    current: list[str],
    target: str,
    st: Optional[SkillsTree] = None,
) -> list[dict]:
    """Generate an ordered learning path from current skills to target skill."""
    if st is None:
        st = SkillsTree()

    current_set = set(current)

    # Get prerequisites chain for target
    try:
        prereqs = st.get_prerequisites(target)
    except Exception:
        prereqs = []

    # Filter out skills the user already has
    path = [s for s in prereqs if s.id not in current_set]

    # Include the target itself
    target_skill = st.get(target)
    if target_skill and target_skill.id not in current_set:
        path.append(target_skill)

    return [
        {
            "order": i + 1,
            "id": s.id,
            "title": s.title,
            "description": s.description,
            "estimated_hours": getattr(s, "estimated_hours", None),
            "tier": getattr(s, "tier", None),
        }
        for i, s in enumerate(path)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Skills Tree Learning Path Recommender")
    parser.add_argument("--current", required=True, help="Comma-separated list of current skill IDs")
    parser.add_argument("--target", required=True, help="Target skill ID")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    args = parser.parse_args()

    current_skills = [s.strip() for s in args.current.split(",")]
    path = get_learning_path(current_skills, args.target)

    if not path:
        print(f"You already have all prerequisites for '{args.target}' or the skill was not found.")
        sys.exit(0)

    if args.as_json:
        print(json.dumps(path, indent=2))
    else:
        print(f"\n\U0001f9ed Learning path to '{args.target}':\n")
        for step in path:
            hours = f" (~{step['estimated_hours']}h)" if step["estimated_hours"] else ""
            tier = f" [v{step['tier']}]" if step["tier"] else ""
            print(f"  {step['order']:2}. {step['title']}{tier}{hours}")
        print(f"\nTotal steps: {len(path)}")


if __name__ == "__main__":
    main()
