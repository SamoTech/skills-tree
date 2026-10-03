# Quick Start

Get up and running with Skills Tree in under 5 minutes.

## 1. Install from the repository

```bash
pip install -e .
```

The historical `skills_tree.SkillsTree` Python API is not currently implemented in the repository. Use the verified CLI/API surface documented in [CLI Reference](cli.md).

## 2. Use the CLI

The verified CLI currently exposes `recommend`, `blueprint`, `goals`, `skills`, and `validate`. See [CLI Reference](cli.md) for the current boundary.

```bash
skills-tree goals
skills-tree skills
skills-tree recommend --goal "Coding Agent"
skills-tree blueprint --goal "Coding Agent"
skills-tree validate
```

## 3. Machine-readable discovery

Use the generated registry for deterministic discovery, then inspect the canonical skill before use:

```text
docs/api/skills.json
skills/<category>/<skill>.md
agent-skills/<name>/SKILL.md
```

See [Python API Status](api.md) for the verified boundary. The historical `skills_tree.SkillsTree` API is not currently implemented.

## 4. Use the MCP Server

The repository contains MCP-related examples and skills, but the current verified CLI does not expose an `mcp serve` command. Verify the example implementation before relying on it.

## 5. Browse the Taxonomy

Explore the skill files directly:

```bash
# Clone the repo
git clone https://github.com/SamoTech/skills-tree.git

# Find a skill by keyword in the source
grep -r "memory injection" skills/ --include="*.md" -l

# Read a full system end-to-end
cat systems/research-agent.md

# See benchmark results
cat benchmarks/tool-use/function-calling-comparison.md
```

## Next Steps

- [Architecture overview](architecture.md) — understand how Skills Tree is structured
- [CLI reference](cli.md) — full CLI documentation
- [Python API reference](api.md) — full API documentation
- [Contributing guide](contributing.md) — how to add or improve skills
