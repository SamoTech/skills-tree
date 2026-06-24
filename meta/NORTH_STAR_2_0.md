# NORTH STAR 2.0
## INITIATIVE-020 — Phase 8
**Project:** Skills Tree · **Date:** 2026-06-24

---

## The Replacement

Repository metrics (stars, forks, commit count) measure activity. Platform metrics measure value delivered. Skills Tree is now a platform. It will be measured as one.

---

## Old Metrics (Retired)

| Metric | Why It's Insufficient |
|--------|----------------------|
| GitHub Stars | Vanity signal; doesn't correlate with actual use |
| Commit count | Measures maintainer activity, not user value |
| Fork count | Vanity; most forks are abandoned |
| File count / node count | Supply-side metric; says nothing about demand |
| CI pass rate | Infrastructure hygiene, not value creation |

---

## New North Star Metrics (Platform Metrics)

### Tier 1 — Primary Health Indicators

| Metric | Definition | Target Month 3 | Target Month 12 |
|--------|-----------|----------------|------------------|
| **Monthly Active Users (MAU)** | Unique users interacting with Explorer, Blueprint Generator, or MCP in 30-day window | 500 | 5,000 |
| **Blueprints Generated** | Total blueprint generation events per month | 100 | 1,000 |
| **Architectures Generated** | Total architecture builder outputs per month | 20 | 200 |
| **Returning Users (30-day)** | % of MAU who visited in the previous 30-day window | 15% | 30% |

**North Star formula:**
```
Platform Health Score = MAU × Returning User Rate × (Blueprints + Architectures) / MAU
```

---

### Tier 2 — Distribution & Reach Indicators

| Metric | Definition | Target Month 3 | Target Month 12 |
|--------|-----------|----------------|------------------|
| **MCP Installations** | Total active MCP server installations across all platforms | 50 | 500 |
| **External Integrations** | Distinct external tools/projects querying graph API | 5 | 25 |
| **Blueprint Shares** | Blueprint URLs shared externally per month | 10/month | 100/month |
| **Inbound Links** | External websites linking to Explorer or skill nodes | 10 | 100 |

---

### Tier 3 — Community Health Indicators

| Metric | Definition | Target Month 3 | Target Month 12 |
|--------|-----------|----------------|------------------|
| **Community Contributions** | PRs merged from non-maintainer contributors per month | 1 | 5 |
| **Discussion Threads** | Active GitHub Discussions threads | 3 | 20 |
| **Skill Gap Reports** | Issues requesting missing skills or blueprints per month | 2/month | 10/month |
| **External Citations** | Blog posts, papers, or projects citing Skills Tree | 2 | 20 |

---

### Tier 4 — Instrumentation Prerequisites

| Instrument | Platform | Priority |
|-----------|----------|----------|
| Page analytics | Plausible Analytics (privacy-first) on Explorer | P0 |
| Event tracking | node_click, search, blueprint_generate, share events | P0 |
| MCP telemetry | Anonymous install count via marketplace analytics | P0 |
| Blueprint counter | Serverless function incrementing on each generation | P1 |
| GitHub Insights | Enable Traffic tab monitoring | P0 — immediate |

---

## Dashboard Spec

A public-facing "Skills Tree Platform Health" dashboard displays MAU, Blueprints Generated, MCP Installs, Return Rate, Trending Skills, and Community metrics. This dashboard is public. Transparent metrics build trust with contributors and create accountability.
