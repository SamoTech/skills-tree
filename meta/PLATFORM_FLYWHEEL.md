# PLATFORM FLYWHEEL
## INITIATIVE-020 — Phase 6
**Project:** Skills Tree · **Date:** 2026-06-24

---

## Overview

A flywheel is a self-reinforcing loop where each turn makes the next turn easier and faster. This document defines the Skills Tree flywheel: the causal chain from contributor action to user value to community growth, and identifies where the flywheel is currently broken or spinning in place.

---

## The Flywheel (Full Cycle)

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   CONTRIBUTOR                                           │
│   Adds/improves skill node, blueprint, or doc           │
│         │                                               │
│         ▼                                               │
│   GRAPH UPDATE                                          │
│   CI validates → graph rebuilt → version tagged         │
│         │                                               │
│         ▼                                               │
│   PLATFORM ENRICHED                                     │
│   Explorer updated · Blueprint options expanded         │
│   MCP server exposes new node                           │
│         │                                               │
│         ▼                                               │
│   USER DISCOVERS                                        │
│   Via MCP · Explorer · Search · Social share            │
│         │                                               │
│         ▼                                               │
│   USER ACTS                                             │
│   Searches graph · Generates blueprint                  │
│   Uses MCP in IDE · Builds agent                        │
│         │                                               │
│         ▼                                               │
│   USER SUCCEEDS                                         │
│   Agent ships · Learning goal achieved                  │
│         │                                               │
│         ▼                                               │
│   FEEDBACK GENERATED                                    │
│   GitHub issue opened · Discussion posted               │
│   Missing skill identified · Blueprint gap found        │
│         │                                               │
│         ▼                                               │
│   CONTRIBUTOR MOTIVATED                                 │
│   Original contributor sees impact                      │
│   New contributor discovers the gap ──────────────────► │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Current State: Where the Flywheel Breaks

| Stage | Status | Break Point |
|-------|--------|-------------|
| Contributor → Graph Update | ✅ Working | CI/CD pipeline functional |
| Graph Update → Platform Enriched | ✅ Working | Auto-rebuild on push |
| Platform Enriched → User Discovers | ❌ BROKEN | No distribution; Explorer was broken until 2026-06-23 |
| User Discovers → User Acts | ⚠️ Partial | Explorer works; Blueprint UX needs onboarding |
| User Acts → User Succeeds | ⚠️ Partial | No learning paths; no failure modes guidance |
| User Succeeds → Feedback Generated | ❌ BROKEN | No feedback mechanism; Discussions empty |
| Feedback Generated → Contributor Motivated | ❌ BROKEN | No external contributors exist yet |

**Diagnosis:** The flywheel has been spinning between steps 1–2 (maintainer commits → graph updates) but the loop never reaches users. Without user discovery, there is no feedback. Without feedback, there is no new contributor motivation. The flywheel is a one-person treadmill.

---

## Flywheel Accelerators

### Accelerator 1 — Discovery Injection (Fixes Stage 3)

Submit to HN, Reddit, LinkedIn, MCP marketplaces, and awesome-MCP lists simultaneously. One coordinated launch post generates the first wave of inbound traffic.

**Target:** 500 unique Explorer sessions in first 30 days post-launch.

### Accelerator 2 — Shareable Artifacts (Fixes Stage 3–4)

Every blueprint and architecture output gets a permanent URL. Users share their blueprints on Twitter/LinkedIn. Each share is a free discovery event.

**Target:** 10% of blueprint generations result in a share event.

### Accelerator 3 — Feedback Channels (Fixes Stage 6)

Seed GitHub Discussions with three threads:
- "What skills are missing from the graph?"
- "Share your blueprint: what agent did you build?"
- "What's the hardest part of AI engineering for you right now?"

### Accelerator 4 — Contributor Onboarding (Fixes Stage 7)

Create `CONTRIBUTING.md` with a "add a skill in 10 minutes" tutorial. Label 10 GitHub issues as `good-first-issue`. Reach out to 5 AI engineering bloggers and offer co-authorship credit.

**Target:** 3 external contributors in first 60 days.

---

## Flywheel Velocity Metrics

| Metric | Target (Month 3) | Target (Month 12) |
|--------|-----------------|------------------|
| Monthly unique Explorer visitors | 1,000 | 10,000 |
| Blueprints generated per month | 100 | 1,000 |
| External contributor PRs per month | 2 | 10 |
| Feedback items (issues + discussions) per month | 5 | 30 |
| Blueprint shares per month | 10 | 100 |
| MCP installations | 50 | 500 |
