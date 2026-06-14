# Launch Announcement Drafts

> These are ready-to-post drafts for Show HN, Reddit, and LinkedIn. Post after starring crosses 50+.

---

## Show HN Draft

**Title:** Show HN: Skills Tree – versioned, benchmarked index of AI agent capabilities (377+ skills)

**Body:**

Hey HN,

I've spent the past 6 months building Skills Tree — an open-source, community-powered index of AI agent capabilities. Think of it as the Wikipedia of what AI agents can do, where every skill is:

- **Versioned** (v1 stub → v2 with code → v3 battle-tested)
- **Benchmarked** (head-to-head comparisons with real datasets)
- **Documented** with runnable Python examples and failure modes
- **Structured** with typed I/O, related skills, and framework compatibility

**What's in it:**
- 377+ skills across 17 categories (perception, reasoning, memory, code generation, web browsing, tool use, etc.)
- 8 multi-skill system workflows (research agent, code reviewer, voice agent...)
- 7 copy-paste production architectures (RAG stack, multi-agent mesh...)
- 4 reproducible benchmarks
- JSON/YAML API for programmatic access
- GitHub Pages interactive UI with search, filtering, dark mode

**Why I built it:**
Every time I started a new agent project, I wasted days rediscovering patterns that already exist. ReAct vs LATS? Memory injection strategies? Structured output coercion? There's no canonical reference. I built Skills Tree to be that reference — versioned, quality-gated, community-maintained.

**GitHub:** https://github.com/SamoTech/skills-tree  
**Live UI:** https://samotech.github.io/skills-tree  
**API:** https://samotech.github.io/skills-tree/api/skills.json

Looking for contributors — especially people who want to be the "champion" of a skill category.

---

## Reddit r/MachineLearning Draft

**Title:** [Project] Skills Tree: open-source, versioned index of AI agent capabilities (377+ skills, benchmarks, production architectures)

**Body:**

Hey r/MachineLearning,

I've been building **Skills Tree** — an open-source index of AI agent capabilities with a quality-gate system that enforces versioning (v1 stub → v2 with runnable code → v3 battle-tested with benchmarks and model comparisons).

**What it contains:**
- 377+ skills across 17 categories: perception, reasoning, memory, code gen, web browsing, tool use, planning, communication, safety, and more
- 27 battle-tested v3 skills with full benchmarks and Claude/GPT-4o/Gemini comparisons
- 8 multi-skill workflow systems and 7 production architectures (RAG stack, human-in-the-loop, self-healing agent, etc.)
- 4 reproducible benchmark studies
- JSON/YAML export API for downstream tool integration

**Technical design:**
- Everything is Markdown with YAML frontmatter — no database, fully diffable, offline-usable
- 30 GitHub Actions workflows: schema validation, quality reports, auto-labeling, leaderboards, badge lifecycle
- CI blocks new stubs — all contributions must meet the quality bar

Looking for contributors, especially people who can upgrade stubs to v2/v3. Each upgrade is a concrete, citable contribution.

https://github.com/SamoTech/skills-tree

---

## LinkedIn Draft

**Headline:** I built the Wikipedia of AI agent capabilities — open source, versioned, community-powered.

**Body:**

For the past 6 months, I've been quietly building **Skills Tree** — an open-source index of what AI agents can actually do, documented in a way that's actually useful.

🌳 **What it is:** A versioned, benchmarked, community-maintained catalog of 377+ AI agent skills across 17 categories. Every skill has a v1→v3 upgrade path: from stub to battle-tested, with working code examples, failure modes, framework compatibility tables, and model comparisons.

🔧 **What makes it different:**
- Quality gate: CI blocks new stubs; every contribution is validated against JSON Schema
- Versioning: v1 (stub) → v2 (runnable code + failure modes) → v3 (benchmarked + model comparison)
- Production-ready content: 7 copy-paste architectures (RAG stack, multi-agent mesh, etc.)
- JSON/YAML API for programmatic access

🎯 **Why it matters:** Every AI agent builder rediscovers the same patterns. Skills Tree is the shared foundation so you don't have to.

**Live:** https://samotech.github.io/skills-tree  
**GitHub:** https://github.com/SamoTech/skills-tree

Looking for contributors and early users. If you've built anything with agent skills, drop a ⭐ and open a "used-in" issue.

---

*Post timing: Monday 9am EST for maximum reach. Tag with #AI #MachineLearning #OpenSource #AIAgents*
