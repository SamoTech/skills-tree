<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-dark.svg">
  <img src="https://raw.githubusercontent.com/SamoTech/skills-tree/main/docs/assets/logo-light.svg" alt="Skills Tree" width="120">
</picture>

# Skills Tree

### The AI Agent Skill OS — Build Smarter Agents, Faster

> **515+ production-ready skills. 16 categories. Every capability an AI agent needs — documented, versioned, and evolving.**

[![Stars](https://img.shields.io/github/stars/SamoTech/skills-tree?style=for-the-badge&color=22c55e&logo=github)](https://github.com/SamoTech/skills-tree/stargazers)
[![Forks](https://img.shields.io/github/forks/SamoTech/skills-tree?style=for-the-badge&color=3b82f6&logo=github)](https://github.com/SamoTech/skills-tree/network)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-515%2B-8b5cf6?style=for-the-badge)](skills/)
[![Version](https://img.shields.io/badge/Version-2.0-orange?style=for-the-badge)](meta/CHANGELOG.md)

**[🌐 Browse Live UI](https://samotech.github.io/skills-tree) · [🗺️ Systems](systems/) · [🏗️ Blueprints](blueprints/) · [📊 Benchmarks](benchmarks/) · [🔬 Labs](labs/) · [🤝 Contribute](CONTRIBUTING.md)**

</div>

---

## Why This Exists

Every agent builder rediscovers the same skills from scratch.

Someone learns RAG the hard way. Someone else figures out memory injection at 2am. A third person spends a week benchmarking ReAct vs LATS — and never shares the results.

**Skills Tree ends that.**

It's the shared operating system for AI agent capabilities — a living, versioned, community-powered index of everything an agent can do, how to implement it, and how it performs.

Stop reinventing. Start building on proven foundations.

---

## What's Inside

```
skills-tree/
│
├── skills/          → 515+ atomic skill files (the foundation)
├── systems/         → Multi-skill workflows (research agent, code reviewer...)
├── blueprints/      → Production architectures (RAG stack, orchestration patterns...)
├── benchmarks/      → Head-to-head skill comparisons (ReAct vs LATS, RAG variants...)
├── labs/            → Experimental & bleeding-edge skills
│
├── docs/            → Interactive web UI (GitHub Pages)
└── meta/            → Schema, glossary, frameworks, roadmap, changelog
```

---

## 🗂️ The 16 Skill Categories

| # | Category | Skills | What It Covers |
|---|---|---|---|
| 01 | 👁️ **Perception** | 36 | Text, images, PDFs, code, sensors, databases, screens |
| 02 | 🧠 **Reasoning** | 41 | Planning, deduction, abduction, causal chains, commonsense |
| 03 | 🗄️ **Memory** | 26 | Working, episodic, semantic, vector, injection, forgetting |
| 04 | ⚡ **Action Execution** | 37 | File I/O, HTTP, email, shell, database writes |
| 05 | 💻 **Code** | 42 | Write, run, debug, review, refactor, test, deploy |
| 06 | 💬 **Communication** | 28 | Summarize, translate, draft, argue, adapt tone |
| 07 | 🔧 **Tool Use** | 55 | 55+ APIs — GitHub, Slack, Stripe, OpenAI, MCP, A2A |
| 08 | 🎭 **Multimodal** | 25 | Images, audio, video, VQA, 3D, charts |
| 09 | 🤖 **Agentic Patterns** | 36 | ReAct, CoT, ToT, MCTS, LATS, RAG, Debate |
| 10 | 🖥️ **Computer Use** | 37 | Click, type, scroll, OCR, terminal, VM, a11y tree |
| 11 | 🌐 **Web** | 28 | Search, scrape, crawl, login, fill forms, parse RSS |
| 12 | 📊 **Data** | 18 | ETL, SQL, embeddings, time series, anomaly detection |
| 13 | 🎨 **Creative** | 27 | Copywriting, image prompts, SVG, music, scripts |
| 14 | 🔒 **Security** | 20 | Sandboxing, secret scanning, audit logs, rollback |
| 15 | 🎼 **Orchestration** | 29 | Multi-agent, state machines, retry, consensus |
| 16 | 🏺 **Domain-Specific** | 52 | Medical, legal, finance, DevOps, education, science |

---

## A Skill in 60 Seconds

Every skill file is production-ready and self-contained:

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

## Benchmarks  → See benchmarks/memory/injection-strategies.md
## Related     → working-memory.md · rag.md · vector-store-retrieval.md
## Changelog   → v1 (2025-03) · v2 (2026-04, added retrieval scoring)
````

---

## 🆕 What's New in v2.0

| Feature | Description |
|---|---|
| **`/systems`** | End-to-end multi-skill workflows — research agent, code reviewer, data pipeline |
| **`/blueprints`** | Reusable production architectures with deployment guides |
| **`/benchmarks`** | Quantitative skill comparisons (accuracy, cost, latency) |
| **`/labs`** | Experimental skills for bleeding-edge capabilities |
| **Skill Versioning** | Every skill now tracks v1→v2→v3 evolution with changelogs |
| **Viral Leaderboards** | Weekly top skills, most-improved, battle-tested rankings |
| **Skill Evolution** | Community can upgrade skills — best versions surface automatically |

---

## 🏆 This Week's Highlights

> Auto-updated weekly · [View all rankings →](meta/LEADERBOARD.md)

**🔥 Most Active Skills**
- `skills/09-agentic-patterns/react.md` — 12 community improvements
- `skills/03-memory/memory-injection.md` — new v2 with retrieval scoring
- `skills/02-reasoning/causal-reasoning.md` — new benchmark added

**⚡ Battle-Tested (used in 10+ public projects)**
- `ReAct` · `Chain of Thought` · `RAG Pipeline` · `Memory Injection` · `Tool Use`

**🔬 Hot in Labs**
- `labs/reasoning/tree-of-agents.md` — multi-agent tree search
- `labs/memory/episodic-compression.md` — lossy-but-useful memory compression

---

## 🗺️ Systems — Multi-Skill Workflows

Don't just pick skills — see how they combine into real systems:

| System | Skills Used | Use Case |
|---|---|---|
| [Research Agent](systems/research-agent.md) | Web search + RAG + Summarize + Cite | Deep research on any topic |
| [Code Reviewer](systems/code-reviewer.md) | Code reading + Reasoning + Comment gen | Automated PR reviews |
| [Data Pipeline Agent](systems/data-pipeline-agent.md) | DB reading + ETL + Anomaly detection | Automated data ops |
| [Customer Support Bot](systems/customer-support-bot.md) | Memory injection + Intent + Response gen | Personalized support |
| [Computer Use Agent](systems/computer-use-agent.md) | Screen reading + OCR + Click + Type | Full GUI automation |

---

## 🏗️ Blueprints — Production Architectures

Copy-paste architectures for common agent patterns:

| Blueprint | Description |
|---|---|
| [RAG Stack](blueprints/rag-stack.md) | Full RAG pipeline: embed → store → retrieve → generate |
| [Multi-Agent Mesh](blueprints/multi-agent-mesh.md) | N specialized agents coordinated by an orchestrator |
| [Human-in-the-Loop](blueprints/human-in-the-loop.md) | Approval gates, escalation triggers, audit trails |
| [Self-Healing Agent](blueprints/self-healing-agent.md) | Error detection, retry logic, rollback, alerting |
| [Memory-First Agent](blueprints/memory-first-agent.md) | Profile + episodic + vector memory working together |

---

## 📊 Benchmarks

We test skills so you don't have to:

| Benchmark | Winner | Margin | Link |
|---|---|---|---|
| ReAct vs LATS (HotpotQA) | LATS | +8.3% accuracy | [→](benchmarks/reasoning/react-vs-lats.md) |
| RAG retrieval strategies | HyDE | +12% recall | [→](benchmarks/memory/rag-retrieval-strategies.md) |
| Memory injection methods | Top-K semantic | Best cost/quality | [→](benchmarks/memory/injection-strategies.md) |
| Code gen: Claude vs GPT-4o | Claude 3.7 | +6% on HumanEval | [→](benchmarks/code/model-comparison.md) |

---

## Skill Versioning — How Evolution Works

Every skill follows semantic versioning:

```
v1 — Initial entry (description + basic example)
v2 — Enriched (better example + failure modes + related skills)
v3 — Battle-tested (benchmarks + model comparison + production notes)
```

**Upgrading a skill:** Bump the version in the frontmatter, add a changelog entry, open a PR titled `improve: skill-name — v1 → v2`.

The community votes with PRs. Best versions surface through merge frequency and usage in Systems/Blueprints.

---

## 🤝 How to Contribute

**4 contribution types — all welcome:**

| Type | What It Is | PR Title Format |
|---|---|---|
| **New Skill** | A capability not yet in the index | `feat: add [skill] to [category]` |
| **Skill Upgrade** | Bump v1→v2 with better content | `improve: [skill] — v1→v2` |
| **Benchmark** | Head-to-head comparison with real numbers | `benchmark: [skill-a] vs [skill-b]` |
| **System/Blueprint** | Multi-skill workflow or architecture | `system: add [name]` / `blueprint: add [name]` |

```bash
git clone https://github.com/SamoTech/skills-tree.git
cp meta/skill-template.md skills/05-code/my-new-skill.md
# Fill in the template → open a PR
```

📋 Full guide: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Quick Start

```bash
# Clone
git clone https://github.com/SamoTech/skills-tree.git

# Find a skill
grep -r "memory injection" skills/ --include="*.md" -l

# Browse a system end-to-end
cat systems/research-agent.md

# Run a benchmark comparison
cat benchmarks/reasoning/react-vs-lats.md
```

Or **[browse the live UI →](https://samotech.github.io/skills-tree)**

---

## Who This Is For

```
🏗️  Agent Builders       → Production skill patterns, ready to use
🔬  AI Researchers        → Benchmarks, taxonomy, capability coverage
📐  System Architects     → Blueprints for multi-agent systems
🎓  Learners              → Structured path from basic → advanced
🤝  Contributors          → A community that improves everything together
```

---

## Vision

> AI agents are becoming teammates, not tools.
>
> Skills Tree is the shared foundation they run on — a living OS of capabilities that the community builds, tests, and evolves together.
>
> Every skill added here saves every agent builder who comes after you.

---

<div align="center">

**[⭐ Star this repo](https://github.com/SamoTech/skills-tree) · [🌐 Browse Skills](https://samotech.github.io/skills-tree) · [🤝 Contribute](CONTRIBUTING.md) · [💖 Sponsor](https://github.com/sponsors/SamoTech)**

*The AI Agent Skill OS — built by the community, for the community.*

</div>
