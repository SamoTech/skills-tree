"""
Enterprise Agent Orchestrator

Skill-based routing, manifest validation, and audit logging
using Skills Tree as the governance layer.

Usage:
    python orchestrator.py --task "research AI safety papers"
    python orchestrator.py --audit
    python orchestrator.py --list-agents
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    from skills_tree import SkillsTree
except ImportError:
    raise SystemExit("Run: pip install skills-tree")


@dataclass
class AgentManifest:
    name: str
    skills: list[str]
    description: str = ""


@dataclass
class AuditLog:
    timestamp: str
    task: str
    routed_to: str
    skills_matched: list[str]
    score: int

    def display(self) -> None:
        print(f"\n[{self.timestamp}] Task routed to '{self.routed_to}'")
        print(f"  Task: {self.task}")
        print(f"  Skills matched: {', '.join(self.skills_matched) or 'none'}")
        print(f"  Match score: {self.score}")


# Built-in agent registry
DEFAULT_AGENTS = [
    AgentManifest("researcher", ["web-search", "rag", "summarization"], "Researches and summarizes topics"),
    AgentManifest("coder", ["code-generation", "code-review", "debugging"], "Writes and reviews code"),
    AgentManifest("planner", ["task-decomposition", "goal-setting", "reflection"], "Plans and decomposes tasks"),
    AgentManifest("analyst", ["data-analysis", "structured-output", "chain-of-thought"], "Analyzes data and produces reports"),
]


class SkillRouter:
    def __init__(self, agents: list[AgentManifest], st: Optional[SkillsTree] = None):
        self.agents = agents
        self.st = st or SkillsTree()

    def route(self, task: str) -> tuple[AgentManifest, AuditLog]:
        """Route a task to the best-matching agent."""
        required_skills = self.st.search(task, limit=5)
        required_ids = {s.id for s in required_skills}

        best_agent = self.agents[0]
        best_score = 0
        best_matched: list[str] = []

        for agent in self.agents:
            matched = list(required_ids.intersection(set(agent.skills)))
            score = len(matched)
            if score > best_score:
                best_score = score
                best_agent = agent
                best_matched = matched

        log = AuditLog(
            timestamp=datetime.now(timezone.utc).isoformat(),
            task=task,
            routed_to=best_agent.name,
            skills_matched=best_matched,
            score=best_score,
        )
        return best_agent, log

    def audit_manifests(self) -> dict[str, dict]:
        """Validate all agent manifests against the taxonomy."""
        results = {}
        for agent in self.agents:
            valid, unknown, deprecated = [], [], []
            for skill_id in agent.skills:
                skill = self.st.get(skill_id)
                if skill is None:
                    unknown.append(skill_id)
                elif getattr(skill, "tier", 2) < 2:
                    deprecated.append(skill_id)
                else:
                    valid.append(skill_id)
            results[agent.name] = {
                "valid": valid,
                "unknown": unknown,
                "deprecated": deprecated,
                "health": "ok" if not unknown else "warning",
            }
        return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Enterprise Agent Orchestrator")
    parser.add_argument("--task", help="Task to route and execute")
    parser.add_argument("--audit", action="store_true", help="Audit all agent manifests")
    parser.add_argument("--list-agents", action="store_true", help="List all agents and their skills")
    args = parser.parse_args()

    router = SkillRouter(DEFAULT_AGENTS)

    if args.list_agents:
        print("\n=== Agent Registry ===")
        for agent in DEFAULT_AGENTS:
            print(f"\n{agent.name}: {agent.description}")
            print(f"  Skills: {', '.join(agent.skills)}")
        return

    if args.audit:
        print("\n=== Manifest Audit ===")
        results = router.audit_manifests()
        for agent_name, result in results.items():
            status = "\u2705" if result["health"] == "ok" else "\u26a0\ufe0f"
            print(f"{status} {agent_name}")
            if result["unknown"]:
                print(f"   Unknown skills: {', '.join(result['unknown'])}")
            if result["deprecated"]:
                print(f"   Low-quality skills: {', '.join(result['deprecated'])}")
        return

    if args.task:
        agent, log = router.route(args.task)
        log.display()
        print(f"\n\U0001f916 Executing with agent: {agent.name}")
        print(f"   Description: {agent.description}")
        print("   (In production, this would invoke the actual agent.)")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
