# Launch Asset Pack

**Initiative:** INITIATIVE-014A.2 — Phase 5  
**Date:** 2026-06-24  
**Lead Agent:** Content Architect + Release Manager  
**Status:** READY FOR USE  

---

## Show HN — Title Variants

Ranked by click-through potential:

1. `Show HN: Skills Tree – A graph of 368 skills every AI agent needs (interactive explorer + blueprint generator)`
2. `Show HN: Skills Tree – Open-source taxonomy of 368 AI agent capabilities with interactive graph explorer`
3. `Show HN: I mapped 368 AI agent skills into a dependency graph with a blueprint generator`
4. `Show HN: Skills Tree – The missing skill OS for AI agents (368 nodes, MIT, no auth)`

**Recommended:** Option 1 — most specific, leads with concrete number, names both surfaces.

---

## Show HN — Submission Body

```
Hi HN,

I've been building Skills Tree — an open-source, structured taxonomy of everything 
an AI agent can do, organized as a dependency graph.

The core problem: every AI agent builder rediscovers the same capabilities from 
scratch. Someone learns RAG the hard way. Someone else figures out memory injection 
at 2am. That collective knowledge disappears into Slack threads and private repos.

Skills Tree is the shared foundation. It currently has:
- 368 skills across 17 categories (Perception → Reasoning → Memory → Action → Code → ...)
- 780 prerequisite edges encoding what to learn before what
- An interactive graph explorer (D3, zero auth, click to explore)
- A blueprint generator: type a goal ("build a RAG assistant") → get an ordered 
  learning path of required skills
- MIT licensed, static GitHub Pages, no backend

Two live surfaces:
- Explorer: https://samotech.github.io/skills-tree/explorer/
- Blueprint Generator: https://samotech.github.io/skills-tree/blueprints/

The blueprint generator now covers 50 goals — from "Coding Agent" to 
"Cyber Threat Intelligence Agent" to "Graph RAG Agent".

Looking for feedback on:
1. What skills or categories are missing?
2. Is the blueprint output actually useful for your workflow?
3. Would you use this via an MCP server (queryable inside Claude/Cursor)?

Repo: https://github.com/SamoTech/skills-tree
```

---

## Reddit — r/MachineLearning Post

**Title:** `[D] Skills Tree: open-source dependency graph of 368 AI agent capabilities with interactive explorer`

**Body:**
```
I've been working on an open-source project called Skills Tree — a structured, 
versioned taxonomy of AI agent capabilities organized as a prerequisite dependency graph.

**What it is:**
- 368 skills across 17 categories (Perception, Reasoning, Memory, Action, Code, 
  Orchestration, Security, etc.)
- Each skill has: description, level (basic/intermediate/advanced), stability rating, 
  and prerequisite edges
- Interactive graph explorer: https://samotech.github.io/skills-tree/explorer/
- Blueprint generator (type a goal → get ordered learning path): 
  https://samotech.github.io/skills-tree/blueprints/

**Why it might be interesting:**
The graph encodes pedagogical ordering — 780 edges that say "learn X before Y". 
This makes it useful for curriculum design, agent capability auditing, and LLM 
tool routing decisions.

**Technical details:**
- Data: JSON graph (nodes + edges) with schema versioning
- Frontend: vanilla JS + D3.js, no backend, GitHub Pages
- Python package available: `pip install skills-tree`
- MIT license

Repo: https://github.com/SamoTech/skills-tree

Feedback very welcome — especially on missing skills, wrong dependency edges, 
or use cases I haven't considered.
```

---

## LinkedIn Post

```
I shipped something that's been living in my head for months.

Skills Tree — an open-source dependency graph of 368 AI agent capabilities.

The idea: every AI agent builder rediscovers the same skills from scratch. 
RAG, memory injection, tool calling, multi-agent orchestration — the knowledge 
exists, but it's scattered. Skills Tree centralizes it as a structured graph.

What's live today:
→ 368 skills, 17 categories, 780 prerequisite edges
→ Interactive graph explorer (zero auth, click to explore)
→ Blueprint generator: describe your agent goal → get an ordered skill curriculum
→ 50 agent blueprints including RAG systems, coding agents, security scanners, 
  Graph RAG, medical triage, and more

Fully open source (MIT). No backend. Static GitHub Pages.

Explore it: https://samotech.github.io/skills-tree/explorer/
Generate a blueprint: https://samotech.github.io/skills-tree/blueprints/
GitHub: https://github.com/SamoTech/skills-tree

If you're building AI agents and this helps — star it, share it, or open a PR.

#AI #LLM #OpenSource #AIAgents #MachineLearning
```

---

## X/Twitter Thread (5 tweets)

**Tweet 1 (hook):**
```
I mapped 368 AI agent skills into a dependency graph.

Every skill has: what to learn first, what level it is, how stable it is.

And I built an interactive explorer + blueprint generator on top of it.

All open source. Zero auth. Here's what it looks like 🧵
```

**Tweet 2 (explorer):**
```
The Explorer is a live D3 force graph of 368 skills across 17 categories.

Perception → Reasoning → Memory → Action → Code → Orchestration → Security

Click any skill. See its prerequisites. See what depends on it.

https://samotech.github.io/skills-tree/explorer/
```

**Tweet 3 (blueprint generator):**
```
The Blueprint Generator is my favorite part.

Type a goal: "build a RAG assistant" or "security scanning agent"
→ Get an ordered learning path of every skill you need
→ Phases, difficulty, estimated time
→ Export as Markdown or JSON
→ Share with a URL

https://samotech.github.io/skills-tree/blueprints/
```

**Tweet 4 (technical):**
```
Under the hood:
- 368 nodes, 780 prerequisite edges
- Schema-versioned JSON graph
- Vanilla JS + D3, no backend
- Python package: pip install skills-tree
- MIT license

Next: MCP server so you can query it directly inside Claude/Cursor

https://github.com/SamoTech/skills-tree
```

**Tweet 5 (CTA):**
```
If you're building AI agents and this is useful:
→ ⭐ Star it: https://github.com/SamoTech/skills-tree
→ 🔀 What skills are missing? Open a PR
→ 💬 What goals should be in the blueprint generator?

Building in public. Every PR merged within 48h.
```

---

## GitHub Discussion Announcement

**Title:** `🚀 Skills Tree is now publicly launched — Explorer + Blueprint Generator live`

**Body:**
```
After months of building, Skills Tree is publicly launched.

## What shipped

- **368 skills** across 17 categories with prerequisite dependency graph
- **Interactive Explorer**: https://samotech.github.io/skills-tree/explorer/
- **Blueprint Generator** (50 goals): https://samotech.github.io/skills-tree/blueprints/
- **Python package**: `pip install skills-tree`

## How to contribute

The easiest contribution: add a skill that's missing.

1. Copy `meta/skill-template.md`
2. Fill in description, level, prerequisites, stability
3. Open a PR — merged within 48h

See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full guide.

## Feedback wanted

- What skills are missing?
- Are the blueprint outputs useful?
- Would you use an MCP server version?

Comment below or open an issue.
```
