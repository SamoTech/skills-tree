#!/usr/bin/env python3
"""Install the three benchmark skills into the Hermes runtime home.

Extracted verbatim from the "Install the three benchmark Skills into Hermes" step of
.github/workflows/skill-activation-runtime.yml (behavior-preserving
decomposition, 2026-10-12). Runs under the same interpreter, environment,
and working directory as the original inline heredoc.
"""

from pathlib import Path
import os

root = Path.cwd()
home = Path(os.environ["HERMES_HOME"])
specs = {
    "skills-tree-rag": (
        "03-memory/rag",
        "skills/03-memory/rag.md",
        "Retrieve and ground answers in a private corpus using retrieval-augmented generation. Use for private or known-source retrieval, grounding, and citation.",
    ),
    "skills-tree-code-review": (
        "05-code/code-review",
        "skills/05-code/code-review.md",
        "Review concrete source code or code changes for correctness, security, maintainability, tests, and repository conventions.",
    ),
    "skills-tree-web-search": (
        "11-web/web-search",
        "skills/11-web/web-search.md",
        "Search the open web for current information, ranked sources, freshness, and citations.",
    ),
}

for runtime_name, (canonical_id, source_rel, description) in specs.items():
    source = root / source_rel
    text = source.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    body = parts[2].lstrip() if len(parts) == 3 else text
    out = home / "skills" / runtime_name
    out.mkdir(parents=True, exist_ok=True)
    skill = "\n".join([
        "---",
        f"name: {runtime_name}",
        f"description: {description}",
        "metadata:",
        f"  skills_tree_canonical_id: {canonical_id}",
        "---",
        "",
    ]) + body
    (out / "SKILL.md").write_text(skill, encoding="utf-8")
