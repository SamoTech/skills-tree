"""
Skill-Aware OpenAI Agent

Demonstrates using Skills Tree to enrich OpenAI agent prompts
with structured skill context.

Usage:
    python agent.py "how do I build a RAG system?"

Requires:
    OPENAI_API_KEY environment variable
"""
from __future__ import annotations

import os
import sys
from typing import Optional

try:
    from skills_tree import SkillsTree
except ImportError:
    raise SystemExit("Run: pip install skills-tree")

try:
    from openai import OpenAI
except ImportError:
    raise SystemExit("Run: pip install openai")


def build_skill_context(st: SkillsTree, query: str, limit: int = 3) -> tuple[str, list[str]]:
    """Search Skills Tree and build a context block for the system prompt."""
    skills = st.search(query, limit=limit)
    if not skills:
        return "", []

    skill_ids = [s.id for s in skills]
    lines = ["## Relevant Skills\n"]
    for skill in skills:
        lines.append(f"### {skill.title} (`{skill.id}`)")
        lines.append(f"{skill.description}")
        if hasattr(skill, "code_example") and skill.code_example:
            lines.append(f"\n```python\n{skill.code_example}\n```")
        lines.append("")

    return "\n".join(lines), skill_ids


def run_agent(query: str, model: str = "gpt-4o-mini") -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Set OPENAI_API_KEY environment variable")

    st = SkillsTree()
    skill_context, skill_ids = build_skill_context(st, query)

    system_prompt = (
        "You are an expert AI agent architect.\n"
        "Answer the user's question using the skill context provided.\n"
        "Be concrete and include code examples where helpful.\n\n"
    )
    if skill_context:
        system_prompt += skill_context

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        temperature=0.3,
    )

    answer = response.choices[0].message.content
    print(answer)

    if skill_ids:
        print(f"\n\u2139\ufe0f  Grounded in skills: {', '.join(skill_ids)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python agent.py \"<your question>\"")
        sys.exit(1)
    run_agent(" ".join(sys.argv[1:]))
