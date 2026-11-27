---
description: A five-minute tour of Skills Tree: install the CLI, search 2,488 curated skills, get goal-based recommendations, and wire the machine-readable registry into your AI agent workflow.
---

# Give Your AI Agent a Shared Vocabulary: A Five-Minute Tour of Skills Tree

*Posted 2026-11-27 by the Skills Tree maintainers*

Every agent builder rediscovers the same capabilities from scratch. Someone learns RAG the hard way, someone else debugs memory injection at 2am, and the lessons end up scattered across Slack threads, private repos, and bookmarks. Skills Tree is an attempt to stop that leak: a public, MIT-licensed registry of **2,488 curated skills** (see the [live registry](https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/api/skills.json) for the current count) with evidence, dependencies, and quality metadata attached to every entry.

This post is a five-minute tour: what it is, how to use it from your terminal, and how to wire it into an AI agent workflow.

## What Skills Tree is

Three surfaces, one source of truth:

- **The canonical corpus** — every skill lives as a reviewed Markdown file under [skills/](https://github.com/SamoTech/skills-tree/tree/main/skills), organized in 17 categories, with category, maturity tier, evidence links, and dependencies recorded in frontmatter.
- **Agent Skills packages** — generated, validated, and reconciliation-gated packages in the [Agent Skills open format](https://agentskills.io) under [agent-skills/](https://github.com/SamoTech/skills-tree/tree/main/agent-skills), consumable by Claude Code, Codex, Cursor, and other compatible tools.
- **A machine-readable registry** — [docs/api/skills.json](https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/api/skills.json), plus per-skill JSON-LD and an `/.well-known/agent-skills/index.json` discovery endpoint, so an agent can resolve a capability deterministically instead of guessing.

Everything is freshness-gated in CI: derived projections (search index, packages, API, graph) are re-derived from the canonical corpus on every change, and a drift fails the build. The number you read is the number that exists.

## Five minutes from your terminal

Install the CLI (published releases are on [PyPI](https://pypi.org/project/skills-tree/); for a source checkout, `pip install -e .`):

```bash
pip install skills-tree
```

List the taxonomy goals and the graph skills:

```bash
skills-tree goals
skills-tree skills
```

Search the corpus with deterministic lexical ranking:

```bash
skills-tree search "memory injection"
skills-tree search "vision" --limit 10 --format table
```

Get skill recommendations for a goal:

```bash
skills-tree recommend --goal "Coding Agent"
skills-tree recommend --goal "RAG Assistant" --experience intermediate --time-budget 80
```

Generate an architecture blueprint for the same goal:

```bash
skills-tree blueprint --goal "Coding Agent"
```

Finally, health-check the CLI and API surface:

```bash
skills-tree validate
```

## Wiring it into an agent workflow

The README documents a discovery protocol built for machine consumers:

1. Search the machine-readable registry (`docs/api/skills.json`).
2. Match the user's task by name, description, category, and related skills.
3. Open the canonical `skills/<category>/<skill>.md` before relying on its instructions.
4. Check maturity, evidence, dependencies, and security boundaries.
5. Prefer the `agent-skills/<name>/SKILL.md` package when one exists.

One rule worth copying into any agent prompt: **a registry entry is not proof that a skill is safe, current, or production-ready**. Inspect the canonical source. If no matching skill exists, report the gap rather than inventing one.

## Honest boundaries

- The verified surface is the **CLI** (`search`, `recommend`, `blueprint`, `goals`, `skills`, `validate`). The historical `skills_tree.SkillsTree` Python API is documented as not implemented.
- Counts move; the [live registry](https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/api/skills.json) is authoritative.
- No invasive analytics anywhere: no tracking, no engagement purchases, no fabricated metrics. Growth is measured only against verifiable public signals.

## Get involved

Start with [contributing.md](contributing.md) and the curated [most-wanted skills list](https://github.com/SamoTech/skills-tree/blob/main/meta/MOST-WANTED-SKILLS.md) — recorded demand turns into expansion batches. The repository is MIT-licensed and community-governed; the [roadmap](roadmap.md) shows what is shipping next.
