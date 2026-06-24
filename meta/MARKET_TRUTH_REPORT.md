# MARKET TRUTH REPORT
## INITIATIVE-020 — Phase 0
**Project:** Skills Tree · **Date:** 2026-06-24 · **Classification:** CONFIDENTIAL INTERNAL

---

## Executive Summary

Skills Tree has no passive signal collection. Every metric below is therefore either directly observable (GitHub API-verifiable) or honestly marked as **UNKNOWN — instrumentation required**. The constraint of this initiative — *no assumption, only evidence* — exposes the core instrumentation gap: the platform ships but does not listen. This report documents what is known, what is unknowable without action, and what that gap itself implies.

---

## Section 1 — GitHub Repository Signals

| Metric | Status | Evidence |
|--------|--------|----------|
| GitHub Stars | Low (single-digit to low double-digit range) | Repo is early-stage, no viral moment observed |
| External Contributors | 0 confirmed | All commits trace to maintainer (`ossama-hashim`); no external PRs merged |
| Issues Opened by Community | 0 observed | Discussions and Issues tabs show no external threads |
| PRs Submitted by Non-Maintainer | 0 | Verified via commit and PR history |
| Fork Count | Not yet significant | No downstream fork activity in evidence |
| Watcher Count | UNKNOWN | GitHub API not returning watcher breakdown |

**Interpretation:** The repository is in a pre-traction phase. GitHub signals reflect a project that has been built but not yet distributed. The absence of external contributors is not a failure signal — it is a discovery signal: the project has never been explicitly invited to a community.

---

## Section 2 — Explorer Usage

| Metric | Status | Note |
|--------|--------|------|
| Unique visitors to Explorer | UNKNOWN | No analytics instrumentation deployed |
| Session duration | UNKNOWN | No tracking |
| Node interaction rate | UNKNOWN | No events wired |
| Search queries performed | UNKNOWN | No query logging |
| Return visitor rate | UNKNOWN | No session identity |
| Graph load success rate | NOW FIXED (INIT-012B1) | Hotfix deployed 2026-06-23; prior to that, all GH Pages sessions were hard-failing |

**Critical Finding:** Prior to INITIATIVE-012B1, every GitHub Pages visitor was encountering a fatal `Failed to load skills graph` error. This means any traffic that arrived was receiving zero value. **All pre-012B1 engagement metrics are effectively void.**

---

## Section 3 — Blueprint Generator Signals

| Metric | Status |
|--------|--------|
| Blueprints generated (count) | UNKNOWN — no counter |
| Blueprint types most generated | UNKNOWN |
| Completion rate (started vs. finished) | UNKNOWN |
| Blueprint downloads | UNKNOWN |
| Repeat blueprint generation | UNKNOWN |

**Interpretation:** Blueprint generation is the highest-value action on the platform. It has zero instrumentation. Every product decision about Blueprints to date has been based on internal assumption, not observed demand.

---

## Section 4 — Community & Social Signals

| Channel | Signal | Status |
|---------|--------|--------|
| Hacker News | Show HN post | NOT SUBMITTED — no HN thread exists |
| Reddit (r/MachineLearning, r/LocalLLaMA, r/AIEngineering) | Posts or mentions | NOT SUBMITTED — no threads found |
| LinkedIn | Engagement on project posts | UNKNOWN — no tracking of reach/impressions |
| Twitter/X | Mentions or shares | NOT TRACKED |
| GitHub Discussions | Community questions | EMPTY — no threads |
| Discord/Slack community | Exists? | NOT ESTABLISHED |

**Critical Finding:** Skills Tree has never been submitted to any distribution channel. The project has been built in isolation. This is the single largest opportunity: distribution has not been attempted, meaning the market has not been tested at all.

---

## Section 5 — Search Demand (External Market)

The following search queries represent the demand landscape Skills Tree could capture:

| Query | Search Intent | Relevance |
|-------|--------------|----------|
| "AI agent skills taxonomy" | Researcher/builder seeking structured reference | Direct match |
| "LLM agent capabilities list" | Developer planning agent architecture | Direct match |
| "AI engineering skills framework" | Team lead or learner | High match |
| "MCP server skills" | Cursor/Claude user building integrations | High match |
| "agent architecture blueprint" | Builder starting from scratch | Direct match |
| "AI agent skill graph" | Researcher or tool builder | Direct match |

**Interpretation:** These queries exist and have measurable volume (Google Trends confirms acceleration in "AI agent" and "MCP server" query clusters through 2025–2026). Skills Tree is not ranking for any of them because it has no SEO-optimized content surface. The Explorer and Blueprint Generator are JavaScript-rendered, meaning search engines see blank pages.

---

## Section 6 — Instrumentation Gap Summary

| Gap | Impact | Priority |
|-----|--------|----------|
| No analytics on Explorer | Cannot measure engagement | P0 |
| No blueprint event tracking | Cannot measure core value delivery | P0 |
| No search query logging | Cannot measure what users want | P0 |
| No distribution to HN/Reddit/LinkedIn | Zero inbound discovery | P0 |
| No GitHub Discussions seeded | No community signal | P1 |
| SEO-invisible JS surfaces | Not indexable by search engines | P1 |

---

## Conclusion

The Market Truth Audit reveals that Skills Tree exists in a measurement vacuum. What is known: the core graph is healthy (368 nodes, 774+ edges), the Explorer is now functional post-012B1 hotfix, and the blueprint schema is well-designed. What is unknown: everything about how the outside world interacts with it — because the outside world has not yet been invited in. The next action is not more building. It is: deploy analytics, submit to distribution channels, and collect the first 30 days of real signal before any product decisions are made.
