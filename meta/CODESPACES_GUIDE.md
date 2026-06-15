# GitHub Codespaces Guide

Sprint: **C-12**

---

## One-click Launch

1. Go to [github.com/SamoTech/skills-tree](https://github.com/SamoTech/skills-tree)
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Wait ~90 seconds for setup to complete
4. The terminal opens with `skills-tree` installed and validated

Direct link:

```
https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=SamoTech/skills-tree
```

---

## What postCreate.sh Does Automatically

| Step | Action |
|---|---|
| 1 | `pip install -e '.[dev]'` — installs package in editable mode with dev extras |
| 2 | `skills-tree validate` — verifies CLI is working |
| 3 | Python API smoke tests: `/health`, `/goals`, `/skills`, `/recommend` |
| 4 | `pytest tests/ -q` — runs full test suite |
| 5 | Prints welcome message with quick-start commands |

---

## First Commands

```bash
# Get recommendations
skills-tree recommend --goal "Coding Agent"

# Generate a blueprint
skills-tree blueprint --goal "RAG Assistant"

# List goals
skills-tree goals

# Full validate
skills-tree validate --goal "Coding Agent"

# Start the API server (port 8000 auto-forwarded)
uvicorn api.main:app --reload
# Swagger UI: https://<codespace>-8000.app.github.dev/docs

# Start MCP server
python -m mcp.server
```

---

## VS Code Extensions Pre-installed

- Python + Pylance
- Ruff (formatter + linter)
- Even Better TOML
- YAML

---

## Troubleshooting

**`skills-tree: command not found`**
```bash
pip install -e .[dev]
```

**API smoke test fails**
```bash
python -c "from tools.architect import GoalTaxonomyParser; print('engine ok')"
```

**Port 8000 not available in browser**
Open the Ports panel in VS Code and click the globe icon next to port 8000.
