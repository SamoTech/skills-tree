# Quick Start

Get up and running with Skills Tree in under 5 minutes.

## 1. Install

```bash
pip install skills-tree
```

## 2. Use the CLI

```bash
# Search for a skill
skills-tree search "memory injection"

# Show a full skill spec
skills-tree show rag

# List all skills in a category
skills-tree list --category reasoning

# List all 17 categories
skills-tree categories
```

## 3. Use the Python API

```python
from skills_tree import SkillsTree

st = SkillsTree()

# Get a skill by ID
skill = st.get("rag")
print(skill.title)       # "Retrieval-Augmented Generation"
print(skill.level)       # "intermediate"
print(skill.stability)   # "stable"
print(skill.version)     # "v3"

# Search skills
results = st.search("memory")
for r in results:
    print(r.id, r.title)

# List all categories
categories = st.categories()
for cat in categories:
    print(cat.id, cat.name, cat.skill_count)

# Get all skills in a category
memory_skills = st.get_category("memory")
```

## 4. Use the MCP Server

Skills Tree includes a built-in MCP server for agent-to-agent capability discovery:

```bash
# Start MCP server
skills-tree mcp serve --port 8080
```

```python
# Query from an agent
import httpx

resp = httpx.get("http://localhost:8080/skills/search", params={"q": "web search"})
for skill in resp.json()["results"]:
    print(skill["id"], skill["title"])
```

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
