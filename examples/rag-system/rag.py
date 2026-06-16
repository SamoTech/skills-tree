"""
Skills Tree RAG System

Uses Skills Tree as a structured knowledge layer for RAG.
Relevant skills and their prerequisites become structured context
for LLM responses.

Usage:
    python rag.py "how do I add memory to my agent?"
    python rag.py "explain chain of thought" --context-only
    python rag.py "how do I implement tool use?" --llm  # requires OPENAI_API_KEY
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Optional

try:
    from skills_tree import SkillsTree
except ImportError:
    raise SystemExit("Run: pip install skills-tree")


def build_rag_context(st: SkillsTree, query: str, limit: int = 3) -> tuple[str, list[str]]:
    """Build structured skill context for RAG."""
    skills = st.search(query, limit=limit)
    if not skills:
        return "", []

    skill_ids = [s.id for s in skills]
    lines = []

    for skill in skills:
        lines.append(f"## Skill: {skill.title} ({skill.id})")
        lines.append(f"**Description:** {skill.description}")

        # Add prerequisite context
        try:
            prereqs = st.get_prerequisites(skill.id)
            if prereqs:
                prereq_str = ", ".join(p.id for p in prereqs[:3])
                lines.append(f"**Prerequisites:** {prereq_str}")
        except Exception:
            pass

        if hasattr(skill, "code_example") and skill.code_example:
            lines.append(f"\n**Example:**\n```python\n{skill.code_example}\n```")

        lines.append("")

    return "\n".join(lines), skill_ids


def context_only_mode(st: SkillsTree, query: str) -> None:
    context, skill_ids = build_rag_context(st, query)
    print(f"Query: {query}\n")
    print("=== Structured Skill Context ===")
    print(context)
    print(f"Skills used: {', '.join(skill_ids)}")


def llm_mode(st: SkillsTree, query: str) -> None:
    try:
        from openai import OpenAI
    except ImportError:
        raise SystemExit("Run: pip install openai")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Set OPENAI_API_KEY environment variable")

    context, skill_ids = build_rag_context(st, query)
    system = (
        "You are a helpful AI agent expert.\n"
        "Use the following Skills Tree context to answer the user's question.\n\n"
        + context
    )

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": query}],
        temperature=0.2,
    )
    print(response.choices[0].message.content)
    if skill_ids:
        print(f"\n\u2139\ufe0f  Context from skills: {', '.join(skill_ids)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Skills Tree RAG System")
    parser.add_argument("query", help="Query to answer")
    parser.add_argument("--context-only", action="store_true", help="Show context without LLM")
    parser.add_argument("--llm", action="store_true", help="Use OpenAI to generate response")
    args = parser.parse_args()

    st = SkillsTree()

    if args.context_only:
        context_only_mode(st, args.query)
    elif args.llm:
        llm_mode(st, args.query)
    else:
        context_only_mode(st, args.query)


if __name__ == "__main__":
    main()
