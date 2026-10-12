#!/usr/bin/env python3
"""Verify skill_view loads the three allowed skills and rejects an out-of-scope request.

Extracted verbatim from the "Restrict skill catalog to benchmark skills" step of
.github/workflows/skill-activation-runtime.yml (behavior-preserving
decomposition, 2026-10-12). Runs under the same interpreter, environment,
and working directory as the original inline heredoc.
"""

from tools.skills_tool import skill_view

allowed = {
    "skills-tree-rag": "RAG",
    "skills-tree-code-review": "Code Review",
    "skills-tree-web-search": "Web Search",
}
for name, expected_heading in allowed.items():
    result = skill_view(name)
    if expected_heading not in result:
        raise SystemExit(f"Allowed benchmark skill failed direct load: {name}")

forbidden = skill_view("hermes-agent-skill-authoring")
if "outside the activation benchmark allowlist" not in forbidden:
    raise SystemExit("Forbidden skill_view request was not blocked.")
print("PASS: skill_view loads all three allowed skills and rejects an out-of-scope skill.")
