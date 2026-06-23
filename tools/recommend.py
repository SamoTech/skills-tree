#!/usr/bin/env python3
"""
tools/recommend.py — INITIATIVE-001 Phase G

Recommendation engine for skills-tree.

Input:
  A goal string (e.g. "build autonomous AI agent")
  Optionally: already known skills

Output:
  {
    "goal": "...",
    "skills": [list of recommended skill IDs],
    "dependencies": [edges needed to reach those skills],
    "learning_path": [ordered list from foundational to advanced],
    "estimated_depth": "shallow|medium|deep"
  }

Algorithm:
  1. Load SKILLS_GRAPH.json
  2. Keyword-match goal against skill titles, tags, and descriptions
  3. For each matched skill, perform backward BFS to collect REQUIRES dependencies
  4. Topological sort the dependency subgraph
  5. Return ordered learning path

Usage:
  python tools/recommend.py --goal "build autonomous AI agent"
  python tools/recommend.py --goal "structured data extraction" --known "02-reasoning/planning"
  python tools/recommend.py --goal "multimodal reasoning" --format markdown
"""

import argparse
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
GRAPH_PATH = REPO_ROOT / "data" / "SKILLS_GRAPH.json"


# ---------------------------------------------------------------------------
# Graph loader
# ---------------------------------------------------------------------------
def load_graph() -> tuple[dict, dict, dict]:
    """Load SKILLS_GRAPH.json. Returns (nodes_by_id, adj_forward, adj_backward)."""
    if not GRAPH_PATH.exists():
        print(f"ERROR: {GRAPH_PATH} not found. Run tools/build_graph.py first.", file=sys.stderr)
        sys.exit(1)

    data = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))

    # Check if file is a placeholder
    if isinstance(data, str):
        print("ERROR: SKILLS_GRAPH.json is a placeholder. Run tools/build_graph.py first.", file=sys.stderr)
        sys.exit(1)

    nodes_by_id = {n["id"]: n for n in data.get("nodes", [])}
    adj_fwd = defaultdict(list)   # source -> [targets]
    adj_bwd = defaultdict(list)   # target -> [sources that require it]

    for e in data.get("edges", []):
        adj_fwd[e["source"]].append((e["target"], e["type"]))
        adj_bwd[e["target"]].append((e["source"], e["type"]))

    return nodes_by_id, adj_fwd, adj_bwd


# ---------------------------------------------------------------------------
# Goal → skill matching
# ---------------------------------------------------------------------------
def match_goal_to_skills(goal: str, nodes_by_id: dict) -> list[str]:
    """Return skill IDs whose title/tags/id match goal keywords."""
    keywords = [w.lower() for w in re.split(r"\W+", goal) if len(w) > 2]
    matches = []
    for skill_id, node in nodes_by_id.items():
        haystack = " ".join([
            node.get("title", "").lower(),
            node.get("id", "").lower(),
            " ".join(node.get("tags", [])).lower(),
        ])
        score = sum(1 for kw in keywords if kw in haystack)
        if score > 0:
            matches.append((score, skill_id))
    matches.sort(reverse=True)
    return [skill_id for _, skill_id in matches[:10]]


# ---------------------------------------------------------------------------
# Dependency resolution (backward BFS)
# ---------------------------------------------------------------------------
def resolve_dependencies(seed_skills: list[str], adj_bwd: dict) -> set[str]:
    """BFS backwards over REQUIRES edges to find all prerequisites."""
    visited = set(seed_skills)
    queue = deque(seed_skills)
    while queue:
        skill = queue.popleft()
        for (prereq, edge_type) in adj_bwd.get(skill, []):
            if edge_type == "REQUIRES" and prereq not in visited:
                visited.add(prereq)
                queue.append(prereq)
    return visited


# ---------------------------------------------------------------------------
# Topological sort (Kahn's algorithm)
# INITIATIVE-008R Phase 3: Replaced silent cycle suppression with explicit
# ValueError. Previously the fallback `ready = [sorted(remaining)[0]]`
# silently picked an arbitrary node when no ready nodes existed (cycle),
# producing a corrupted learning path without any error signal.
# Now any cycle in the REQUIRES subgraph raises immediately.
# Changed: 2026-06-23 | Decision: D-INIT-008R-001
# ---------------------------------------------------------------------------
def topological_sort(skill_ids: set, adj_bwd: dict) -> list[str]:
    """Return topological order (prerequisites first) for the given skill set.

    Raises ValueError if a cycle is detected in the REQUIRES subgraph.
    A cycle means two or more skills mutually require each other, which is
    a graph integrity violation that must be fixed in the skill definitions.
    """
    result = []
    remaining = set(skill_ids)

    for _ in range(len(skill_ids) + 1):
        if not remaining:
            break

        ready = []
        for s in sorted(remaining):
            prereqs_in_set = [
                p for (p, et) in adj_bwd.get(s, [])
                if et == "REQUIRES" and p in remaining
            ]
            if not prereqs_in_set:
                ready.append(s)

        if not ready:
            # INITIATIVE-008R Phase 3: explicit failure — no silent recovery.
            # Previously: ready = [sorted(remaining)[0]]
            raise ValueError(
                f"Cycle detected in prerequisite graph. "
                f"The following skills are in a circular REQUIRES dependency "
                f"and cannot be topologically sorted: {sorted(remaining)}"
            )

        result.extend(ready)
        for s in ready:
            remaining.discard(s)

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Recommend a learning path for a given goal.")
    parser.add_argument("--goal", required=True, help="Learning goal description.")
    parser.add_argument("--known", nargs="*", default=[], help="Already known skill IDs to exclude.")
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    nodes_by_id, adj_fwd, adj_bwd = load_graph()

    # Match goal to skills
    seed_skills = match_goal_to_skills(args.goal, nodes_by_id)
    if not seed_skills:
        print(f"[recommend] No matching skills found for goal: '{args.goal}'", file=sys.stderr)
        result = {
            "goal": args.goal,
            "skills": [],
            "dependencies": [],
            "learning_path": [],
            "estimated_depth": "unknown",
        }
    else:
        # Resolve dependencies
        all_needed = resolve_dependencies(seed_skills, adj_bwd)
        all_needed -= set(args.known)

        # Build learning path
        learning_path = topological_sort(all_needed, adj_bwd)

        # Collect relevant edges
        dep_edges = []
        for skill in all_needed:
            for (prereq, et) in adj_bwd.get(skill, []):
                if prereq in all_needed and et == "REQUIRES":
                    dep_edges.append({"source": prereq, "target": skill, "type": et})

        depth = "shallow" if len(learning_path) <= 5 else ("medium" if len(learning_path) <= 15 else "deep")

        result = {
            "goal": args.goal,
            "skills": seed_skills,
            "dependencies": dep_edges,
            "learning_path": learning_path,
            "estimated_depth": depth,
        }

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"# Learning Path: {args.goal}")
        print(f"\n**Estimated depth:** {result['estimated_depth']}")
        print(f"**Skills in path:** {len(result['learning_path'])}")
        print("\n## Learning Path (prerequisites first)\n")
        for i, skill_id in enumerate(result["learning_path"], 1):
            node = nodes_by_id.get(skill_id, {})
            title = node.get("title", skill_id)
            level = node.get("level", "?")
            print(f"{i}. `{skill_id}` — **{title}** ({level})")


if __name__ == "__main__":
    main()
