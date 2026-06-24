# MARKETING_OS_VISION.md

> Initiative: INITIATIVE-020  
> Owner: Graph Architect  
> Created: 2026-06-24  
> Status: ACTIVE

---

## Mission

Transform Skills Tree from an **AI Engineering Operating System** into a **business-facing AI Marketing Operating System** capable of generating marketing execution blueprints, media-buying workflows, campaign audits, and AI agent teams — ready for non-technical marketing practitioners.

---

## Strategic Context

Skills Tree v2 (INITIATIVE-014B) shipped the core Skills Graph (368 nodes, 774+ edges) and the Explorer UI. The graph contains the full vocabulary of AI capabilities. The Blueprint Generator (INITIATIVE-012B) proved that the graph can power contextual output.

The missing layer: **business-domain goals**. Engineering goals ("build a RAG pipeline") already work. Marketing goals ("launch a Meta Ads cold-traffic campaign") require a goal catalog, domain-specific agent teams, and KPI targets — none of which existed.

INITIATIVE-020 closes that gap by:
1. Defining 50+ marketing goals across 8 categories
2. Creating a domain-adapted agent architecture for media buying
3. Deploying a public Marketing AI OS product surface

---

## Product Vision

```
User Input        →  Goal Selector
Goal Selector     →  Blueprint Engine
Blueprint Engine  →  Agent Team + KPI Targets + Timeline
Output            →  Actionable 30-day execution plan
```

The system answers: *"I want to scale my Meta Ads. What AI agents do I need and what does week 1 look like?"* — in under one second, with no AI API cost.

---

## Reuse Architecture

| Existing Asset             | Reuse in INITIATIVE-020       |
|----------------------------|-------------------------------|
| SKILLS_GRAPH.json (368+)   | Skill resolution engine       |
| Blueprint Generator UX     | Goal → Blueprint pattern      |
| GitHub Pages deploy        | docs/marketing-os/ surface    |
| skills-tree semantic ver.  | Changelog + release tracking  |

---

## Success Criteria

- [ ] 50+ marketing goals catalogued
- [ ] 8 goal categories with agent teams
- [ ] Media buying agent architecture documented
- [ ] Public UI live at `/docs/marketing-os/`
- [ ] Competition submission ready before 2026-07-04
- [ ] README + Loom demo script complete

---

## Competitive Differentiation

- **Not a chatbot.** Zero LLM latency. Deterministic, auditable output.
- **Not a template pack.** Blueprints are generated from a live skill graph with semantic relationships.
- **Not a SaaS.** Fully open-source, self-hostable, forkable.
- **Real skill taxonomy.** 368+ skills with categories, tags, and edge data — not invented keywords.
