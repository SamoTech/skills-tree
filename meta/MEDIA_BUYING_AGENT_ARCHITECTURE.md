# MEDIA BUYING AGENT ARCHITECTURE

_Initiative: INITIATIVE-020 | Date: 2026-06-24_

---

## Overview

A media buying AI agent team is a multi-agent system where specialist agents cover distinct phases of a paid advertising campaign: strategy, audience, creative, bidding, and measurement. This document specifies the canonical architecture, agent roles, skill requirements, communication protocol, and tool contracts.

---

## Agent Team Structure

```
┌──────────────────────────────┐
│     CAMPAIGN ORCHESTRATOR         │  ← Supervisor agent
└──────────────────────────────┘
         │           │            │
    ┌───┴───┐   ┌─┴───┐   ┌───┴───┐
    │AUDIENCE │   │CREATIVE│   │ BIDDING │
    │ ANALYST │   │ TESTER │   │STRATEGIST│
    └────────┘   └───────┘   └───────┘
                                    │
                              ┌───┴───┐
                              │PERFORMANCE│
                              │ ANALYST   │
                              └────────┘
```

---

## Agent Role Specifications

### Agent 1 — Campaign Orchestrator

| Property | Value |
|---|---|
| **Role** | Supervisor / Planner |
| **Responsibility** | Receives campaign goal, decomposes into tasks, assigns to specialist agents, aggregates outputs into final blueprint |
| **Required Skills** | `task-decomposition`, `multi-agent-orchestration`, `planning`, `handoff` |
| **Inputs** | Marketing goal, budget, timeline, platform mix |
| **Outputs** | Task assignment manifest, final campaign blueprint |
| **Tools** | Goal parser, Blueprint assembler, Handoff protocol |

### Agent 2 — Audience Analyst

| Property | Value |
|---|---|
| **Role** | Audience Specialist |
| **Responsibility** | Builds audience segmentation strategy: cold, warm, and retargeting layers. Outputs audience spec with platform-specific configuration. |
| **Required Skills** | `audience-segmentation`, `embedding-generation`, `data-analysis`, `reasoning` |
| **Inputs** | Product description, target persona, platform |
| **Outputs** | Audience spec: cold traffic tiers, lookalike seeds, retargeting windows, exclusion lists |
| **Tools** | Persona builder, Lookalike calculator, Exclusion recommender |

### Agent 3 — Creative Tester

| Property | Value |
|---|---|
| **Role** | Creative Specialist |
| **Responsibility** | Designs A/B testing matrix for ad creatives. Specifies variable isolation, test duration, minimum significance threshold, and promotion criteria. |
| **Required Skills** | `creative-testing`, `data-analysis`, `summarization`, `intent-classification` |
| **Inputs** | Audience spec, platform, product offer |
| **Outputs** | Creative testing matrix: format variants, hook variants, CTA variants, test schedule |
| **Tools** | Creative matrix builder, Statistical significance calculator, Fatigue detector |

### Agent 4 — Bidding Strategist

| Property | Value |
|---|---|
| **Role** | Bid & Budget Specialist |
| **Responsibility** | Recommends bidding strategy, daily budget allocation across ad sets, scaling triggers, and kill thresholds. |
| **Required Skills** | `bid-optimization`, `data-analysis`, `reasoning`, `audit-logging` |
| **Inputs** | Total budget, campaign objective, target CPA or ROAS |
| **Outputs** | Bid strategy spec: bid type, budget allocation per ad set, scaling rules, kill rules |
| **Tools** | Budget allocator, Scaling rule generator, Threshold calculator |

### Agent 5 — Performance Analyst

| Property | Value |
|---|---|
| **Role** | Measurement & Reporting Specialist |
| **Responsibility** | Defines KPI framework, reporting cadence, attribution model, and generates performance summaries. |
| **Required Skills** | `data-analysis`, `summarization`, `rag`, `audit-logging` |
| **Inputs** | Campaign objectives, platform data (simulated or live) |
| **Outputs** | KPI dashboard spec, attribution model recommendation, weekly reporting template |
| **Tools** | KPI selector, Attribution modeler, Report generator |

---

## Workflow Protocol

```
STEP 1: Orchestrator receives goal
  ↓
STEP 2: Orchestrator calls Audience Analyst → returns audience_spec
  ↓
STEP 3: Orchestrator calls Creative Tester (with audience_spec) → returns creative_matrix
  ↓
STEP 4: Orchestrator calls Bidding Strategist (with budget + objective) → returns bid_spec
  ↓
STEP 5: Orchestrator calls Performance Analyst (with objectives) → returns kpi_spec
  ↓
STEP 6: Orchestrator assembles Blueprint from {audience_spec + creative_matrix + bid_spec + kpi_spec}
  ↓
STEP 7: Blueprint rendered in Marketing OS UI
```

---

## Communication Schema

All inter-agent messages use a typed handoff envelope:

```json
{
  "from": "campaign-orchestrator",
  "to": "audience-analyst",
  "task_id": "media-buying-001",
  "payload": {
    "goal": "Launch DTC skincare brand on Meta",
    "budget_daily_usd": 500,
    "platform": "meta",
    "objective": "purchase",
    "timeline_days": 30
  },
  "expected_output": "audience_spec"
}
```

---

## Skills Graph Mapping

Every agent role maps to specific skill nodes in `SKILLS_GRAPH.json`:

| Agent | Primary Skill Node | Connected Nodes |
|---|---|---|
| Campaign Orchestrator | `multi-agent-orchestration` | `task-decomposition`, `planning`, `handoff` |
| Audience Analyst | `audience-segmentation` | `embedding-generation`, `data-analysis` |
| Creative Tester | `creative-testing` | `data-analysis`, `intent-classification` |
| Bidding Strategist | `bid-optimization` | `data-analysis`, `audit-logging` |
| Performance Analyst | `data-analysis` | `summarization`, `rag`, `audit-logging` |

---

## Output Contract — Media Buying Blueprint

```
MEDIA BUYING BLUEPRINT
══════════════════════
■ Goal:              [campaign goal]
■ Platform:          [platform mix]
■ Daily Budget:      $[X]
■ Timeline:          [N] days

■ Audience Layer
  - Cold Traffic:     [audience description]
  - Lookalike:        [seed + % range]
  - Retargeting:      [window + exclusions]

■ Creative Matrix
  - Formats:          [static / video / carousel]
  - Hook Variants:    [N hooks to test]
  - CTA Variants:     [N CTAs to test]
  - Test Duration:    [N days per variant]

■ Bidding Strategy
  - Bid Type:         [lowest cost / cost cap / bid cap]
  - Daily Budget:     $[X] per ad set
  - Scale Trigger:    [rule]
  - Kill Threshold:   [rule]

■ KPIs
  - Primary:          [CPA / ROAS target]
  - Secondary:        [CTR, CPM benchmarks]
  - Reporting:        [cadence]

■ Required AI Skills
  [Ranked skill list with links to skill detail pages]
```

---

## Reuse from Existing Architecture

- `BLUEPRINT_CATALOG_V2.md` established the 50-goal scaffold; this document extends the pattern to marketing domain
- `BLUEPRINT_SCHEMA.md` defines the output contract; Media Buying Blueprint follows same structure
- `docs/blueprints/` hosts existing blueprint files; `docs/marketing-os/` hosts the marketing UI
- `SKILLS_GRAPH.json` is the unchanged data source; marketing domain adds label filters, not new nodes
