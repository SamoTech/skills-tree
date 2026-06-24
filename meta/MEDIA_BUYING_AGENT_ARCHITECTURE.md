# MEDIA_BUYING_AGENT_ARCHITECTURE.md

> Initiative: INITIATIVE-020  
> Created: 2026-06-24  
> Status: REFERENCE

---

## Overview

A media buying AI agent team is a **multi-agent system** where each agent owns a distinct phase of the campaign lifecycle. The supervisor orchestrates handoffs; specialist agents execute bounded tasks; the evaluator closes the feedback loop.

---

## Agent Roles

### 1. Campaign Orchestrator (Supervisor)
- **Role:** Plans the campaign, assigns tasks, routes outputs
- **Pattern:** Supervisor agent (LangGraph `StateGraph` or AutoGen `GroupChat`)
- **Skills:** `multi-agent-orchestration`, `task-decomposition`, `planning`
- **Trigger:** User goal input
- **Output:** Task queue dispatched to specialist agents

### 2. Audience Analyst (Specialist)
- **Role:** Builds audience segments, lookalikes, exclusions
- **Pattern:** Tool-calling agent with access to platform APIs
- **Skills:** `audience-segmentation`, `embedding-generation`, `data-analysis`
- **Input:** Campaign brief, first-party data
- **Output:** Audience segment definitions (JSON)

### 3. Creative Strategist (Specialist)
- **Role:** Generates creative briefs, copy variants, hook frameworks
- **Pattern:** RAG-augmented generation agent
- **Skills:** `creative-testing`, `summarization`, `rag`
- **Input:** Audience segments, product context
- **Output:** Creative brief + 5 copy variants per format

### 4. Bidding Strategist (Specialist)
- **Role:** Sets bid strategy, budget allocation, pacing rules
- **Pattern:** Reasoning agent with structured output
- **Skills:** `bid-optimization`, `data-analysis`, `reasoning`
- **Input:** KPI targets, historical ROAS data
- **Output:** Bid strategy config (JSON)

### 5. Performance Evaluator (Evaluator)
- **Role:** Reviews live data, triggers optimizations, escalates anomalies
- **Pattern:** Reflection agent on scheduled cadence
- **Skills:** `data-analysis`, `audit-logging`, `reflection`
- **Input:** Platform performance reports
- **Output:** Optimization action list or escalation to Orchestrator

---

## Handoff Protocol

All inter-agent messages use a typed envelope:

```json
{
  "from": "campaign-orchestrator",
  "to": "audience-analyst",
  "task": "build_audience_segment",
  "payload": {
    "goal": "cold-traffic-prospecting",
    "budget_usd": 5000,
    "kpi_target": { "roas": 3.0, "cpa": 45 }
  },
  "context_window": "conversation_id_xyz"
}
```

---

## Orchestration Pattern

```
User Goal
    │
    ▼
Campaign Orchestrator
    │
    ├──► Audience Analyst ──────► Segment JSON
    │
    ├──► Creative Strategist ───► Brief + Copy
    │
    ├──► Bidding Strategist ────► Bid Config
    │
    └──► Performance Evaluator ─► Optimization Loop
            │
            └──► (feedback) ──► Campaign Orchestrator
```

---

## Recommended Stack

| Layer | Tool | Notes |
|-------|------|-------|
| Orchestration | LangGraph or AutoGen | Stateful multi-agent graph |
| LLM Backbone | GPT-4o or Claude 3.5 Sonnet | Reasoning + tool calls |
| Memory | Upstash Redis | Shared state across agents |
| Data Pipeline | Python + pandas | Performance data ingestion |
| Platform APIs | Meta Marketing API, Google Ads API | Live data access |
| Observability | LangSmith or Helicone | Trace all agent calls |

---

## KPI Targets by Campaign Type

| Campaign Type | ROAS Target | CPA Target | CTR Floor | CPM Ceiling |
|---------------|-------------|------------|-----------|-------------|
| Cold Traffic | ≥ 2.5× | < $60 | 1.2% | $15 |
| Retargeting | ≥ 5.0× | < $25 | 2.5% | $18 |
| Brand Awareness | N/A | N/A | 0.8% | $8 |
| Lead Gen (B2B) | N/A | < $120 | 0.5% | $25 |

---

## Deployment Notes

- All agent state persists in Redis (Upstash serverless tier sufficient for prototype)
- Evaluator agent runs on a cron schedule (every 6 hours for active campaigns)
- Supervisor pattern prevents agent loops with a `max_turns: 10` hard limit
- All agent outputs are logged to `audit-log.jsonl` for compliance
