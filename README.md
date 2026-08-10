<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-dark.svg">
  <img src="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-light.svg" alt="Skills Tree" width="200" height="52">
</picture>

# Skills Tree

<!-- HIGHLIGHTS_START -->
## 📆 This Week's Highlights — August 10, 2026

> No skill changes this week. Open a PR to get started!

<!-- HIGHLIGHTS_END -->


### AI Engineering Operating System

**The largest open, dependency-mapped knowledge graph for AI agents.**

| 368 Skills | 780+ Connections | MIT Licensed |
|:---:|:---:|:---:|
| Versioned & benchmarked | Dependency-mapped | Community-governed |

**[▶ Explore Skills →](https://samotech.github.io/skills-tree/explorer/)  ·  [▶ Generate Blueprint →](https://samotech.github.io/skills-tree/blueprints/)  ·  [▶ GitHub Repository →](https://github.com/SamoTech/skills-tree)**

<!-- BADGES_START -->
[![PyPI version](https://img.shields.io/pypi/v/skills-tree?style=for-the-badge&color=22c55e&logo=pypi&logoColor=white&label=PyPI)](https://pypi.org/project/skills-tree/)
[![Python versions](https://img.shields.io/pypi/pyversions/skills-tree?style=for-the-badge&logo=python&logoColor=white)](https://pypi.org/project/skills-tree/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/skills-tree?style=for-the-badge&color=3b82f6&logo=pypi&logoColor=white&label=Downloads%2Fmonth)](https://pypi.org/project/skills-tree/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/SamoTech/skills-tree/validate-skills.yml?branch=main&style=for-the-badge&label=CI&logo=github-actions&logoColor=white)](https://github.com/SamoTech/skills-tree/actions/workflows/validate-skills.yml)
[![GitHub Release](https://img.shields.io/github/v/release/SamoTech/skills-tree?style=for-the-badge&color=a855f7&logo=github)](https://github.com/SamoTech/skills-tree/releases)
[![Coverage](https://img.shields.io/badge/Coverage-report-orange?style=for-the-badge)](meta/COVERAGE_STRATEGY.md)
[![Docs](https://img.shields.io/badge/Docs-Live-22c55e?style=for-the-badge&logo=github)](https://samotech.github.io/skills-tree)
<!-- BADGES_END -->

[![Stars](https://img.shields.io/github/stars/SamoTech/skills-tree?style=for-the-badge&color=22c55e&logo=github)](https://github.com/SamoTech/skills-tree/stargazers)
[![Forks](https://img.shields.io/github/forks/SamoTech/skills-tree?style=for-the-badge&color=3b82f6&logo=github)](https://github.com/SamoTech/skills-tree/network)
[![Contributors](https://img.shields.io/github/contributors/SamoTech/skills-tree?style=for-the-badge&color=f59e0b&logo=github)](https://github.com/SamoTech/skills-tree/graphs/contributors)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)

> **Response SLA:** Issues `<72h` · Pull Requests `<7 days` · Governance Reviews `<5 days`

**[🌐 Live Docs](https://samotech.github.io/skills-tree) · [📦 PyPI](https://pypi.org/project/skills-tree/) · [🗺️ Systems](systems/) · [🏗️ Blueprints](blueprints/) · [📊 Benchmarks](benchmarks/) · [🤝 Contribute](CONTRIBUTING.md) · [🗺 Roadmap](meta/ROADMAP.md)**

[🐦 **Share Skills Tree on X →**](https://twitter.com/intent/tweet?text=Skills%20Tree%20%E2%80%94%20the%20shared%20operating%20system%20for%20AI%20agent%20capabilities.&url=https%3A%2F%2Fgithub.com%2FSamoTech%2Fskills-tree&hashtags=AI,Agents,LLM,OpenSource)

🌐 **Read in your language:**
🇬🇧 English
· [🇸🇦 العربية](i18n/README.ar.md)
· [🇨🇳 中文](i18n/README.zh.md)
· [🇪🇸 Español](i18n/README.es.md)
· [🇩🇪 Deutsch](i18n/README.de.md)
· [🇫🇷 Français](i18n/README.fr.md)
· [🇮🇳 हिन्दी](i18n/README.hi.md)
· [🇯🇵 日本語](i18n/README.ja.md)
· [🇰🇷 한국어](i18n/README.ko.md)
· [🇧🇷 Português](i18n/README.pt.md)
· [🇷🇺 Русский](i18n/README.ru.md)

</div>

---

## ⚡ Quick Install

```bash
pip install skills-tree
```

```python
# Query the skills taxonomy programmatically
from skills_tree import SkillsTree

st = SkillsTree()
skill = st.get("rag")           # fetch a skill by ID
results = st.search("memory")   # full-text search across 360+ skills
cats = st.categories()          # list all 17 categories
```

Or use the CLI:

```bash
skills-tree search "memory injection"
skills-tree show rag
skills-tree list --category reasoning
```

→ Full install guide: **[docs/installation.md](docs/installation.md)** · Quick start: **[docs/quickstart.md](docs/quickstart.md)**

---

## The Problem

Every AI agent builder rediscovers the same skills from scratch.

Someone learns RAG the hard way. Someone else figures out memory injection at 2am. A third person spends a week benchmarking ReAct vs LATS — and never shares the results. A fourth discovers the same failure modes you already hit last month.

**That collective knowledge is disappearing into Slack threads, private repos, and Twitter bookmarks.**

Skills Tree fixes that. → [Read the full problem statement](docs/WHY_SKILLS_TREE.md)

---

## What This Is

**Skills Tree is the shared operating system for AI agent capabilities.**

A living, versioned, community-powered index of everything an agent can do — at its best, documented with working code, real benchmarks, failure modes, and evolution history.

Battle-tested skills (🟢 verified) are production-ready and copy-paste safe. Yellow/unscanned skills are the community's TODO list — open files, real problem space, and the clearest signal of where contributions are most useful.

→ [Real-world use cases](docs/USE_CASES.md) · [Why Skills Tree vs alternatives](docs/WHY_SKILLS_TREE.md#competitive-positioning)

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     skills-tree                         │
│                   (Python package)                      │
├─────────────┬───────────────────┬───────────────────────┤
│   CLI       │   Python API      │   MCP Server          │
│ (Typer)     │ (SkillsTree class)│ (tools/mcp/)          │
├─────────────┴───────────────────┴───────────────────────┤
│              Skills Data Layer (Markdown + YAML)        │
│  skills/  │  systems/  │  blueprints/  │  benchmarks/   │
├─────────────────────────────────────────────────────────┤
│  Validation Engine  │  Search Index  │  Quality Reports │
│  (tools/)           │  (Lunr.js)     │  (meta/)         │
└─────────────────────────────────────────────────────────┘
```

→ Full architecture deep-dive: **[docs/architecture.md](docs/architecture.md)**

---

## Comparison vs Alternatives

| Feature | **Skills Tree** | LangChain Hub | Hugging Face Hub | Custom YAML files |
|---|---|---|---|---|
| AI agent skill taxonomy | ✅ 360+ skills | ⚠️ Prompt-focused | ❌ Model-focused | ❌ None |
| Versioned skill evolution | ✅ v1→v2→v3 | ❌ | ❌ | ❌ |
| Runnable code examples | ✅ Every skill | ⚠️ Some | ⚠️ Some | ❌ |
| Benchmarks included | ✅ Head-to-head | ❌ | ⚠️ Leaderboards | ❌ |
| MCP server integration | ✅ Built-in | ❌ | ❌ | ❌ |
| Multi-agent blueprints | ✅ 7+ blueprints | ⚠️ Templates | ❌ | ❌ |
| CLI + Python API | ✅ Both | ⚠️ Python only | ✅ Both | ❌ |
| Community-governed | ✅ Open PRs | ⚠️ Curated | ✅ Open | ✅ (yours only) |
| Failure modes documented | ✅ Every skill | ❌ | ❌ | ❌ |
| Free & open source (MIT) | ✅ | ⚠️ Mixed | ✅ | ✅ |

---

## 🚀 Start Here — Battle-Tested Skills

If you're new, **read these first**. Each ships with runnable code, typed I/O, failure modes, and a model-comparison table.

### Agent reasoning loops
- [**ReAct**](skills/09-agentic-patterns/react.md) — Thought → Action → Observation, the foundation of tool-using agents
- [**Chain of Thought**](skills/09-agentic-patterns/cot.md) — explicit step-by-step reasoning + self-consistency
- [**Tree of Thought**](skills/09-agentic-patterns/tot.md) — branched reasoning with scoring + beam search
- [**Reflection / Reflexion**](skills/09-agentic-patterns/reflection.md) — critique → revise loop on top of any output
- [**Self-Consistency**](skills/02-reasoning/self-consistency.md) — sample N chains, majority-vote
- [**Planning**](skills/02-reasoning/planning.md) — typed, DAG-validated plans your executor can run
- [**Task Decomposition**](skills/02-reasoning/task-decomposition.md) — break a goal into atomic, runnable subtasks

### Retrieval & memory
- [**RAG**](skills/03-memory/rag.md) — chunk → embed → retrieve → cite, end-to-end with confidence + threshold
- [**Vector Store Retrieval**](skills/03-memory/vector-store-retrieval.md) — typed top-k cosine search with metadata filtering
- [**Embedding Generation**](skills/12-data/embedding-generation.md) — batched, content-hash-cached, Matryoshka-truncatable
- [**Memory Injection**](skills/03-memory/memory-injection.md) — top-K user memories per turn
- [**Short-Term Memory**](skills/03-memory/short-term-memory.md) — token-budgeted rolling window

### Calling LLMs in production
- [**Function / Tool Calling**](skills/07-tool-use/function-calling.md) — the primitive that turns an LLM into an agent
- [**OpenAI API**](skills/07-tool-use/openai-api.md) — chat, structured outputs, tools, embeddings, streaming, retry
- [**Anthropic API**](skills/07-tool-use/anthropic-api.md) — Claude with tool loop, prompt caching, streaming

### Code, Web & Security
- [**Code Generation**](skills/05-code/code-generation.md) — spec → AST-validated source with self-repair
- [**Web Search**](skills/11-web/web-search.md) — Tavily/Serper/Brave with recency + TTL cache
- [**Input Sanitization**](skills/14-security/input-sanitization.md) — 4-layer defense: structural + boundary + content + isolation

> **The full battle-tested set is auto-listed in [`meta/QUALITY-REPORT.md`](meta/QUALITY-REPORT.md).**

---

## What's Inside

```
skills-tree/
│
├── skills/          → 360 atomic skill files (50 battle-tested, 308 stubs)
├── systems/         → Multi-skill workflows (research agent, code reviewer...)
├── blueprints/      → Copy-paste production architectures
├── benchmarks/      → Head-to-head, reproducible skill comparisons
├── labs/            → Experimental & bleeding-edge capabilities
│
├── docs/            → Interactive web UI (GitHub Pages) + MkDocs docs site
├── i18n/            → Localized READMEs (10 languages)
├── meta/            → Schema, glossary, frameworks, roadmap, changelog
├── mcp/             → MCP server integration
└── tests/           → pytest test suite
```

---

## 🗂️ The 17 Skill Categories

| # | Category | Skills | What It Covers |
|---|---|---|---|
| 01 | 👁️ **Perception** | 36 | Text, images, PDFs, code, sensors, databases, screens |
| 02 | 🧠 **Reasoning** | 45 | Planning, deduction, abduction, causal chains, commonsense |
| 03 | 🗄️ **Memory** | 19 | Working, episodic, semantic, vector, injection, forgetting |
| 04 | ⚡ **Action Execution** | 21 | File I/O, HTTP, email, shell, database writes |
| 05 | 💻 **Code** | 28 | Write, run, debug, review, refactor, test, deploy |
| 06 | 💬 **Communication** | 15 | Summarize, translate, draft, argue, adapt tone |
| 07 | 🔧 **Tool Use** | 33 | APIs — GitHub, Slack, Stripe, OpenAI, MCP, A2A |
| 08 | 🎭 **Multimodal** | 14 | Images, audio, video, VQA, 3D, charts |
| 09 | 🤖 **Agentic Patterns** | 23 | ReAct, CoT, ToT, MCTS, LATS, RAG, Debate |
| 10 | 🖥️ **Computer Use** | 20 | Click, type, scroll, OCR, terminal, VM, a11y tree |
| 11 | 🌐 **Web** | 17 | Search, scrape, crawl, login, fill forms, parse RSS |
| 12 | 📊 **Data** | 18 | ETL, SQL, embeddings, time series, anomaly detection |
| 13 | 🎨 **Creative** | 14 | Copywriting, image prompts, SVG, music, scripts |
| 14 | 🔒 **Security** | 13 | Sandboxing, secret scanning, audit logs, rollback |
| 15 | 🎼 **Orchestration** | 22 | Multi-agent, state machines, retry, consensus |
| 16 | 🏺 **Domain-Specific** | 28 | Medical, legal, finance, DevOps, education, science |
| 17 | 🛠️ **Infrastructure** | 1 | Dependency auditing & supply-chain tooling |

---

## A Skill in 60 Seconds

Every skill file is self-contained and production-ready:

````markdown
# Memory Injection
Category: memory | Level: intermediate | Stability: stable | Version: v2

## Description
Dynamically inject relevant past memories into an agent's system prompt
before each turn — giving the model user context without filling the window.

## Example
```python
client.messages.create(
    system=f"{base_system}\n\n## Memory\n{top_k_memories}",
    messages=[{"role": "user", "content": user_message}]
)
```
````

Every skill includes: ✅ typed inputs/outputs · ✅ runnable Python code · ✅ frameworks table · ✅ failure modes · ✅ version history

---

## 🗺️ Systems — Multi-Skill Workflows

| System | Skills Used | Use Case |
|---|---|---|
| [Research Agent](systems/research-agent.md) | Web search + RAG + Summarize | Deep research automation |
| [Coding Agent](systems/coding-agent.md) | Code reading + Write + Debug | End-to-end code generation |
| [Code Reviewer](systems/code-reviewer.md) | Code reading + Reasoning + Comment gen | Automated PR reviews |
| [Data Pipeline Agent](systems/data-pipeline-agent.md) | DB reading + ETL + Anomaly detection | Automated data ops |
| [Customer Support Bot](systems/customer-support-bot.md) | Memory injection + Intent + Response gen | Personalized support |
| [Computer Use Agent](systems/computer-use-agent.md) | Screen reading + OCR + Click | Full GUI automation |

---

## 🏗️ Blueprints — Production Architectures

| Blueprint | Description |
|---|---|
| [RAG Stack](blueprints/rag-stack.md) | Embed → store → retrieve → generate, fully wired |
| [Multi-Agent Workflow](blueprints/multi-agent-workflow.md) | Sequential orchestration with handoffs |
| [Multi-Agent Mesh](blueprints/multi-agent-mesh.md) | N specialists + orchestrator, parallel execution |
| [Human-in-the-Loop](blueprints/human-in-the-loop.md) | Approval gates, escalation, audit trails |
| [Self-Healing Agent](blueprints/self-healing-agent.md) | Error detection, retry logic, rollback |
| [Memory-First Agent](blueprints/memory-first-agent.md) | Profile + episodic + vector memory combined |

---

## 📊 Benchmarks

| Benchmark | Winner | Margin | Link |
|---|---|---|---|
| ReAct vs LATS (HotpotQA) | LATS | +8.3% accuracy | [→](benchmarks/reasoning/react-vs-lats.md) |
| RAG retrieval strategies | HyDE | +12% recall | [→](benchmarks/memory/rag-retrieval-strategies.md) |
| Memory injection methods | Top-K semantic | Best cost/quality | [→](benchmarks/memory/injection-strategies.md) |
| Function calling comparison | Claude 3.7 | +6% tool accuracy | [→](benchmarks/tool-use/function-calling-comparison.md) |

---

## 🤝 How to Contribute

| Type | What It Is | PR Title Format |
|---|---|---|
| **New Skill** | A capability not yet indexed | `feat: add [skill] to [category]` |
| **Skill Upgrade** | Bump v1→v2 with better content | `improve: [skill] — v1→v2` |
| **Benchmark** | Head-to-head with real numbers | `benchmark: [skill-a] vs [skill-b]` |
| **System / Blueprint** | Multi-skill workflow or architecture | `system: add [name]` |

```bash
git clone https://github.com/SamoTech/skills-tree.git
cp meta/skill-template.md skills/05-code/my-new-skill.md
# Fill in every section → open a PR
```

Full guide: **[CONTRIBUTING.md](CONTRIBUTING.md)**

---

## 🗺️ Roadmap

See the full plan: **[meta/ROADMAP.md](meta/ROADMAP.md)**

**Near-term (v2.x):** Skill dependency graph · Skill Paths · JSON/YAML export · Community ratings  
**Medium-term (v3.0):** LangChain Hub / MCP registry integration · 500+ skills  
**Long-term:** Skills Tree becomes the canonical reference for AI agent capabilities

---

## Vision

> AI agents are becoming teammates, not tools.
>
> Skills Tree is the shared foundation they run on — a living OS of capabilities
> that the community builds, tests, and evolves together.
>
> Every skill added here saves every agent builder who comes after you.

---

<div align="center">

**[⭐ Star this repo](https://github.com/SamoTech/skills-tree) · [📦 Install from PyPI](https://pypi.org/project/skills-tree/) · [🌐 Browse Skills](https://samotech.github.io/skills-tree) · [🤝 Contribute](CONTRIBUTING.md) · [💖 Sponsor](https://github.com/sponsors/SamoTech)**

*The AI Agent Skill OS — built by the community, for the community.*

</div>
