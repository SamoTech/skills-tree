---
hide:
  - navigation
  - toc
---

# Skills Tree

<div class="hero" markdown>

**The AI Agent Skill OS** — 360+ skills, versioned, benchmarked, and openly evolving.

[![PyPI version](https://img.shields.io/pypi/v/skills-tree?style=for-the-badge&color=22c55e&logo=pypi&logoColor=white)](https://pypi.org/project/skills-tree/)
[![Downloads](https://img.shields.io/pypi/dm/skills-tree?style=for-the-badge&color=3b82f6&logo=pypi&logoColor=white)](https://pypi.org/project/skills-tree/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://github.com/SamoTech/skills-tree/blob/main/LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/SamoTech/skills-tree/validate-skills.yml?branch=main&style=for-the-badge&label=CI&logo=github-actions&logoColor=white)](https://github.com/SamoTech/skills-tree/actions)

[Get Started](quickstart.md){ .md-button .md-button--primary }
[Browse on GitHub](https://github.com/SamoTech/skills-tree){ .md-button }
[PyPI Package](https://pypi.org/project/skills-tree/){ .md-button }

</div>

---

## What is Skills Tree?

Skills Tree is the shared operating system for AI agent capabilities. It is a living, versioned, community-powered index of everything an agent can do — documented with working code, real benchmarks, failure modes, and evolution history.

<div class="grid cards" markdown>

- :material-lightning-bolt: **360+ Skills**  
  17 categories covering every AI agent capability from perception to orchestration.

- :material-chart-bar: **Real Benchmarks**  
  Head-to-head comparisons with reproducible methodology and datasets.

- :material-source-branch: **Versioned Evolution**  
  Skills evolve from v1 (stub) to v3 (battle-tested) with full audit trail.

- :material-puzzle: **MCP Integration**  
  Built-in Model Context Protocol server for runtime capability discovery.

- :material-package: **Python Package**  
  `pip install skills-tree` — CLI and API included.

- :material-account-group: **Community Governed**  
  Quality gates, PR templates, and contributor guides for collaborative improvement.

</div>

---

## Quick Install

```bash
pip install skills-tree
```

```python
from skills_tree import SkillsTree

st = SkillsTree()
skill = st.get("rag")           # fetch a skill by ID
results = st.search("memory")   # search across 360+ skills
cats = st.categories()          # list all 17 categories
```

See the full [Quick Start guide](quickstart.md) or [CLI reference](cli.md).

---

## The 17 Skill Categories

| # | Category | Skills |
|---|---|---|
| 01 | 👁️ Perception | 36 |
| 02 | 🧠 Reasoning | 39 |
| 03 | 🗄️ Memory | 19 |
| 04 | ⚡ Action Execution | 21 |
| 05 | 💻 Code | 28 |
| 06 | 💬 Communication | 15 |
| 07 | 🔧 Tool Use | 32 |
| 08 | 🎭 Multimodal | 14 |
| 09 | 🤖 Agentic Patterns | 23 |
| 10 | 🖥️ Computer Use | 20 |
| 11 | 🌐 Web | 17 |
| 12 | 📊 Data | 18 |
| 13 | 🎨 Creative | 14 |
| 14 | 🔒 Security | 13 |
| 15 | 🎼 Orchestration | 22 |
| 16 | 🏺 Domain-Specific | 28 |
| 17 | 🛠️ Infrastructure | 1 |
