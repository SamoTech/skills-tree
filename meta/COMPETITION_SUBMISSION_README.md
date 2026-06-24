# It's Today Media Build Challenge — Submission README

> Initiative: INITIATIVE-020  
> Submission Deadline: 2026-07-04  
> Builder: SamoTech / Ossama Hashim  
> Status: READY

---

## What I Built

**Marketing AI OS** — an open-source AI operating system for marketing teams that turns any marketing goal into a complete AI agent team, KPI targets, and 30-day execution blueprint in under one second.

### Live Demo
> `https://samotech.github.io/skills-tree/marketing-os/`

---

## The Problem

Marketing teams know they need AI agents. They don't know *which* agents, *how* to structure them, or *what KPIs to target*. Existing tools either require deep ML expertise or lock you into a specific platform.

---

## The Solution

Marketing AI OS provides:

1. **50 marketing goals** across 8 categories (Paid Social, Creative, Landing Page, Agent Teams, Analytics, Content & SEO, Acquisition, Strategy)
2. **AI agent team blueprints** — supervisor + specialists + evaluator for every goal
3. **KPI target matrices** — pre-loaded benchmarks per category
4. **30-day execution timelines** — 4-phase sprint plans
5. **Zero AI latency** — all output is deterministic and instant (no API call required at runtime)

---

## Technical Architecture

```
Skills Tree SKILLS_GRAPH.json (368+ nodes)
        ↓
Goal Catalog (50 goals × 8 categories)
        ↓
Blueprint Engine (app.js — 100% client-side)
        ↓
Marketing OS UI (docs/marketing-os/)
        ↓
GitHub Pages (static, zero backend)
```

### Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Zero runtime API calls | Eliminates latency, cost, and API key management |
| Client-side blueprint engine | Works offline, forkable, self-hostable |
| Skills graph reuse | 368+ AI skills = auditable, semantic skill assignment |
| GitHub Pages deploy | Free, reliable, no infrastructure to maintain |

---

## What Makes This Different

- **Not a chatbot.** Deterministic output with no hallucination risk.
- **Not a template.** Blueprints are generated from a live skill taxonomy with semantic edge data.
- **Not a SaaS.** Fully open-source. Fork it, extend it, deploy it yourself.
- **Built on real AI taxonomy.** The 368+ skills powering the blueprints come from a production-grade skills graph used by AI engineering teams.

---

## Repository

`https://github.com/SamoTech/skills-tree`

### Key Files

| File | Purpose |
|------|---------|
| `docs/marketing-os/index.html` | Marketing OS UI |
| `docs/marketing-os/app.js` | Blueprint generator engine |
| `docs/marketing-os/styles.css` | UI design system |
| `meta/MARKETING_GOAL_CATALOG.md` | 50 goal definitions |
| `meta/MEDIA_BUYING_AGENT_ARCHITECTURE.md` | Agent team architecture |
| `meta/MARKETING_OS_VISION.md` | Product vision document |
| `meta/LOOM_DEMO_SCRIPT.md` | Video walkthrough script |

---

## Loom Demo

> *[Link to be added after recording — see `meta/LOOM_DEMO_SCRIPT.md`]*
