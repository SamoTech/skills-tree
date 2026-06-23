# VIRAL SURFACE DESIGN

**Initiative:** INITIATIVE-011A  
**Date:** 2026-06-23  
**Purpose:** Design the five viral surfaces that transform skills-tree from a read-only repo into a living, shareable platform.

---

## Surface 1 — Interactive Skill Explorer

### Vision
A web-based, zero-install skill graph explorer. Users navigate 368 skills, filter by category, difficulty, maturity, and see the prerequisite graph live.

### Design Spec

**URL:** `https://samotech.github.io/skills-tree/explorer`

**Core features:**
- Force-directed graph visualization of all 368 nodes + 780 edges
- Click any node → skill detail panel (description, code example, failure modes, frameworks)
- Filter: category (17), difficulty (1–5), maturity (stub/verified/battle-tested)
- Path mode: select start skill + goal skill → highlight prerequisite path
- Share button: generates shareable URL for any skill or path (e.g., `?skill=rag&path=true`)
- "Contribute this skill" CTA linking to GitHub edit flow

**Viral mechanics:**
- Shareable URLs for every skill and learning path → social sharing loop
- Embedded screenshots shareable on Twitter/LinkedIn
- "Explore the graph" CTA in README → drives traffic
- Each visit = potential star + contributor

**Tech stack:** D3.js force graph or Cytoscape.js, built on GitHub Pages, no server required.

**Priority:** CRITICAL — single highest-ROI viral surface.

---

## Surface 2 — Learning Paths

### Vision
Pre-built, community-curated learning journeys from beginner to expert, powered by the prerequisite graph.

### Design Spec

**Location:** `paths/` directory + web UI tab

**Path format:**
```markdown
# Learning Path: RAG Engineer
Level: beginner → advanced
Estimated time: 6 weeks
Skills: 12

## Week 1: Foundations
- [ ] embedding-generation (prerequisite: none)
- [ ] vector-store-retrieval (requires: embedding-generation)
- [ ] rag (requires: vector-store-retrieval)

## Week 2: Advanced Retrieval
...
```

**Initial paths (10 to launch with):**
1. RAG Engineer (8 skills, 4 weeks)
2. Multi-Agent Orchestrator (10 skills, 5 weeks)
3. Code Agent Builder (8 skills, 4 weeks)
4. Computer Use Agent (7 skills, 3 weeks)
5. AI Security Specialist (6 skills, 3 weeks)
6. Reasoning & Planning Expert (9 skills, 5 weeks)
7. Multimodal Agent Builder (8 skills, 4 weeks)
8. Data Pipeline Architect (7 skills, 4 weeks)
9. LLM Production Engineer (8 skills, 4 weeks)
10. Full-Stack AI Agent Builder (15 skills, 8 weeks)

**Viral mechanics:**
- "Share my learning path" social CTA
- Progress badges embeddable in GitHub profiles
- Community can submit new paths via PR (low-friction contribution type)
- "You completed 3/12 skills" — gamification drives return visits

---

## Surface 3 — Goal-to-Blueprint Generator

### Vision
User describes what they want to build → system recommends the skill stack + blueprint + learning path.

### Design Spec

**URL:** `https://samotech.github.io/skills-tree/generator`

**Input:** Free-text goal (e.g., "I want to build an agent that researches topics and writes reports")

**Output:**
```
Recommended Blueprint: Research Agent
Core Skills Required: web-search, rag, summarization, planning
Prerequisite Skills: embedding-generation, vector-store-retrieval
Estimated complexity: Intermediate
Estimated build time: 2 weeks
Learning Path: → RAG Engineer (4 weeks)
Blueprint: → blueprints/research-agent.md
```

**Implementation options:**
- V1: Static keyword-matching rules (zero infra cost)
- V2: Embedding-based semantic matching against skill descriptions
- V3: LLM-powered (API call) with skills-tree as context

**Viral mechanics:**
- "I built this with Skills Tree" social share template
- Shareable output URLs
- Every generated blueprint links back to skills-tree
- Embeddable in blog posts and tutorials

**Priority:** HIGH — highest perceived magic. V1 can ship in days.

---

## Surface 4 — Public Roadmaps

### Vision
Transparent, public roadmaps that turn future work into contributor recruitment.

### Design Spec

**Location:** `meta/ROADMAP.md` (already exists) + GitHub Projects board

**Roadmap structure:**
```markdown
## Now (v3.x)
- [ ] 50 battle-tested skills (currently ~50)
- [ ] Learning paths (10 paths)
- [ ] Interactive explorer

## Next (v4.0)
- [ ] Goal-to-Blueprint generator
- [ ] 100 battle-tested skills
- [ ] Contributor scoreboard

## Later (v5.0)
- [ ] 500+ skills
- [ ] MCP registry listing
- [ ] LangChain Hub integration
```

**Viral mechanics:**
- "Help us get here" CTA next to each roadmap item
- GitHub Discussions thread per roadmap milestone
- Monthly roadmap update post (LinkedIn + X/Twitter)
- "This was on the roadmap 3 months ago — we shipped it" retrospective posts

---

## Surface 5 — Contributor Scoreboard

### Vision
Public leaderboard celebrating contributors — makes contribution visible, social, and rewarding.

### Design Spec

**Location:** `meta/CONTRIBUTORS.md` + README section + web UI tab

**Metrics tracked:**
- Skills authored (new skill files)
- Skills upgraded (v1→v2→v3)
- Benchmarks added
- Systems added
- Blueprints added
- Total contribution score

**Format:**
```markdown
## 🏆 Top Contributors

| Rank | Contributor | Skills | Benchmarks | Score |
|------|------------|--------|-----------|-------|
| 🥇 1 | @ossama | 12 | 3 | 84 |
| 🥈 2 | @contributor2 | 8 | 2 | 56 |
...
```

**Monthly recognition:**
- "Contributor of the Month" post on LinkedIn + X/Twitter
- Profile badge for top-10 contributors
- Special GitHub label: `🏆 Top Contributor`

**Viral mechanics:**
- Contributors share their rank on social media
- "I'm #3 on the Skills Tree contributor board" — credibility signal
- Drives competitive contribution loops
- Recognized contributors promote the repo organically

---

## Implementation Priority

| Surface | Effort | Viral ROI | Priority |
|---------|--------|-----------|----------|
| Interactive Skill Explorer | HIGH | CRITICAL | 1 |
| Learning Paths | MEDIUM | HIGH | 2 |
| Goal-to-Blueprint Generator V1 | LOW | HIGH | 3 |
| Contributor Scoreboard | LOW | HIGH | 4 |
| Public Roadmaps (enhance existing) | LOW | MEDIUM | 5 |

---

*All surfaces must be tracked in meta/VIRAL_GROWTH_ROADMAP.md timeline.*
