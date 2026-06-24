# Launch Asset Pack

**Initiative:** INITIATIVE-014A.2 — Phase 5  
**Date:** 2026-06-24  
**Status:** READY FOR REVIEW  

---

## Show HN — Title Variants

Ranked by predicted HN performance (clarity + specificity + low hype):

1. **[PRIMARY]** `Show HN: Skills Tree – open-source taxonomy of 368 AI agent capabilities with graph explorer`
2. `Show HN: I built a versioned index of 368 AI agent skills so builders stop reinventing them`
3. `Show HN: Skills Tree – the missing skill OS for AI agents (368 skills, graph explorer, Python API)`
4. `Show HN: An open-source map of everything an AI agent can do (368 skills, 774 edges, MIT)`
5. `Show HN: Skills Tree – structured agent capabilities with benchmarks and failure modes`

**Recommendation:** Use variant #1. HN rewards precision and scale numbers. "Graph explorer" signals interactive demo which increases click-through.

---

## Show HN — Body Text

```
Hi HN,

I've been building AI agents for the past year and kept running into the same problem: 
every agent builder rediscovers the same skills from scratch. Someone figures out memory 
injection at 2am. Someone else spends a week benchmarking ReAct vs LATS and never shares 
the results. That collective knowledge disappears into Slack threads and private repos.

Skills Tree is my attempt to fix that.

It's an open, versioned index of AI agent capabilities — 368 skills across 17 categories. 
Each skill has typed I/O, runnable Python code, failure modes, and head-to-head benchmark 
results where applicable.

The interactive graph explorer lets you visualize skill dependencies — 368 nodes, 774+ edges. 
You can see which skills compose into which systems, follow learning paths, and discover 
adjacent capabilities you didn't know existed.

There's also a blueprint generator (50 production agent architectures) and a Python package 
(`pip install skills-tree`) for programmatic access.

Live graph: https://samotech.github.io/skills-tree/explorer/
Repo: https://github.com/SamoTech/skills-tree

The taxonomy is intentionally incomplete — about 85% of skills are stubs waiting for community 
contributions. The battle-tested 15% are production-ready and copy-paste safe.

Happy to answer questions about the taxonomy design, the dependency graph structure, or how 
we benchmark skills head-to-head.
```

---

## Reddit — r/MachineLearning & r/LocalLLaMA

### Title
`Skills Tree: Open-source taxonomy of 368 AI agent capabilities with dependency graph and benchmarks [OC]`

### Body
```
Built this to solve a problem I kept hitting: every AI agent project rediscovers the same 
capabilities from scratch. There's no shared vocabulary, no comparison data, and no place 
that tells you which skills depend on which.

Skills Tree is an open MIT-licensed index of agent capabilities:

- 368 atomic skills across 17 categories (perception, reasoning, memory, tool use, security, etc.)
- Dependency graph: 774+ edges showing which skills compose
- Interactive graph explorer: https://samotech.github.io/skills-tree/explorer/
- Head-to-head benchmarks (ReAct vs LATS +8.3%, HyDE RAG +12% recall, etc.)
- Runnable Python code + typed I/O for every battle-tested skill
- Python package: pip install skills-tree
- Blueprint generator: 50 production agent architectures

The taxonomy covers everything from ReAct loops and RAG pipelines to computer use, 
multi-agent orchestration, and security sandboxing.

About 85% is community-driven stubs — the goal is to make this the canonical reference 
that the community builds on, tests, and evolves together.

Live demo: https://samotech.github.io/skills-tree/explorer/
GitHub: https://github.com/SamoTech/skills-tree
```

---

## LinkedIn Version

```
I spent the past year watching AI agent builders rediscover the same capabilities from scratch.

Someone figures out memory injection at 2am. Someone else benchmarks ReAct vs LATS and never 
shares. A third person hits the same failure modes you already documented last month.

So I built Skills Tree.

It's an open-source taxonomy of 368 AI agent capabilities:

→ 17 categories: from reasoning and memory to security and orchestration
→ 774+ dependency edges showing how skills compose into systems
→ Interactive graph explorer (link below)
→ Head-to-head benchmarks with real numbers
→ Python package + CLI for programmatic access
→ 50 production blueprint architectures

The live graph is the part I'm most proud of. You can visualize the entire capability space, 
follow paths from "ReAct" through "Multi-Agent Orchestration" to "Human-in-the-Loop", and 
discover adjacent skills you didn't know existed.

🌐 Graph: https://samotech.github.io/skills-tree/explorer/
📦 pip install skills-tree
⭐ GitHub: https://github.com/SamoTech/skills-tree

Looking for feedback on the taxonomy and what's missing.

#AIAgents #LLM #OpenSource #MachineLearning #Python
```

---

## X/Twitter Thread

**Tweet 1 (hook):**
```
Every AI agent builder rediscovers the same skills from scratch.

Memory injection at 2am.
RAG chunking strategies from scratch.
ReAct vs LATS benchmarks nobody shares.

I built an open OS to fix this: Skills Tree 🧵
```

**Tweet 2 (what it is):**
```
Skills Tree is an open-source taxonomy of 368 AI agent capabilities.

17 categories: reasoning, memory, tool use, security, orchestration...
Each skill: typed I/O + runnable Python + failure modes + version history

pip install skills-tree
```

**Tweet 3 (graph demo):**
```
The graph explorer is where it gets interesting.

368 nodes. 774+ edges showing which skills depend on which.

You can see how "RAG" connects to "Embedding Generation" → "Vector Store" → "Memory Injection" → "Short-Term Memory".

Live: https://samotech.github.io/skills-tree/explorer/
```

**Tweet 4 (benchmarks):**
```
We also benchmark skills head-to-head with real numbers:

• ReAct vs LATS on HotpotQA: LATS +8.3% accuracy
• RAG retrieval: HyDE +12% recall over naive chunking
• Function calling: Claude 3.7 +6% tool accuracy over GPT-4o

All reproducible. All linked.
```

**Tweet 5 (CTA):**
```
The taxonomy is intentionally 85% stubs — the community builds it out.

Every skill you add saves every agent builder who comes after you.

⭐ https://github.com/SamoTech/skills-tree

What skill is missing from your agent stack?
```

---

## GitHub Discussion Announcement

**Title:** `🚀 Skills Tree v2 is live — 368 skills, graph explorer, 50 blueprints`

**Body:**
```markdown
Hey everyone,

After months of building, we're announcing the public launch of Skills Tree v2.

## What's new

- **368 skills** across 17 categories (up from ~200 at v1)
- **Interactive graph explorer** — visualize 774+ skill dependency edges
  - Live: https://samotech.github.io/skills-tree/explorer/
- **50 blueprint architectures** across 8 agent categories
- **Python package** (`pip install skills-tree`) with full CLI support
- **MCP server** for direct agent integration
- **Head-to-head benchmarks** with reproducible results
- **i18n**: README in 10 languages

## What we need from you

1. **⭐ Star the repo** if Skills Tree is useful to you
2. **Add a missing skill** — 85% of skills are stubs waiting for your contribution
3. **Share your Use Case** — how are you using the taxonomy? Reply below
4. **Report gaps** — what agent capability is completely missing?

## Quick links

- Graph Explorer: https://samotech.github.io/skills-tree/explorer/
- pip install: `pip install skills-tree`
- Contributing guide: [CONTRIBUTING.md](../CONTRIBUTING.md)
- Roadmap: [meta/ROADMAP.md](ROADMAP.md)

Thank you to everyone who opened PRs, filed issues, and suggested improvements during the 
pre-launch period. This is a community project and it shows.

— Ossama
```

---

## Launch Timing Recommendation

| Platform | Optimal Time | Notes |
|---|---|---|
| Show HN | Tuesday 9–11am ET | Highest HN traffic window |
| Reddit | Tuesday 10am–12pm ET | Post Show HN first, Reddit 1hr later |
| LinkedIn | Tuesday 8–9am ET | Post before HN to warm network |
| X/Twitter | Tuesday 9am ET (thread) | Simultaneous with HN |
| GitHub Discussion | T-1 day (Monday) | Warm the community before public launch |

**Next launch window:** Tuesday, June 30, 2026, 9:00 AM ET (16:00 EEST)
