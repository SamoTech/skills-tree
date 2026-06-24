# ARCHITECTURE BUILDER SPEC — V1
## INITIATIVE-020 — Phase 3
**Project:** Skills Tree · **Date:** 2026-06-24

---

## Overview

The Architecture Builder converts a natural-language agent goal into a complete engineering specification. It is the highest-complexity, highest-value feature on the platform roadmap. This document specifies V1: the minimum viable version that delivers genuine value without requiring a backend.

---

## Input Contract

```
Input: Natural language string describing the agent goal.

Examples:
  "I want a customer support agent."
  "Build me an agent that does competitive research."
  "I need an agent that monitors my infrastructure and opens tickets."
  "Multi-agent pipeline for code review."
```

No structured input required from the user. All parsing is done by the Builder engine.

---

## Output Contract

Every Architecture Builder output produces seven artifacts:

### 1. Architecture Diagram

A human-readable ASCII or SVG representation of the agent's component structure:

```
[User Input]
     ↓
[Intent Classifier]  ←──  [Context Memory]
     ↓
[Planner]            ←──  [Tool Registry]
     ↓
[Executor]
  ├── [Tool: Knowledge Base RAG]
  ├── [Tool: CRM API]
  └── [Tool: Escalation Router]
     ↓
[Response Formatter]
     ↓
[Output + Audit Log]
```

### 2. Skill Stack

Ordered list of skills required, with difficulty level and dependency chain.

### 3. Dependencies

Framework and infrastructure requirements (models, vector DBs, APIs, infrastructure).

### 4. Learning Path

Ordered curriculum to build the required skills from scratch, organized by week.

### 5. Blueprint JSON

Machine-readable full specification in the existing blueprint schema format.

### 6. Failure Modes

Documented failure modes with triggers and mitigations for the specific agent type.

### 7. Benchmark Recommendations

Relevant evaluation benchmarks for the agent's primary capabilities.

---

## V1 Implementation Plan

### Phase A — Static Rule Engine (Week 1–2)

Map 20 common agent goal patterns to pre-built architecture templates. No LLM required. Input parsing uses keyword matching.

```
"customer support" → TEMPLATE_CUSTOMER_SUPPORT
"research agent"   → TEMPLATE_RESEARCH_AGENT
"code review"      → TEMPLATE_CODE_REVIEW_AGENT
"monitoring"       → TEMPLATE_INFRA_MONITORING
"data pipeline"    → TEMPLATE_DATA_EXTRACTION
```

Each template contains all 7 output artifacts pre-authored.

### Phase B — LLM-Augmented Blending (Week 3–4)

When input does not match a known template, use GPT-4o/Claude 3.5 with a system prompt that includes the SKILLS_GRAPH.json as context. The LLM selects and combines nodes to generate a custom architecture.

### Phase C — Interactive Refinement (Week 5–6)

Allow users to modify the generated architecture in the UI: swap skills, add/remove tools, adjust learning path length. Each change triggers a re-validation against the dependency graph.

---

## UI Entry Point

```
Explorer Header:
[Search skills...]  |  [Build Architecture →]

Architecture Builder Modal:
┌─────────────────────────────────────────────┐
│  Describe what your agent should do:         │
│  ┌─────────────────────────────────────────┐ │
│  │ I want a customer support agent that... │ │
│  └─────────────────────────────────────────┘ │
│  [Generate Architecture]                     │
└─────────────────────────────────────────────┘
```

---

## Success Criteria

- V1 covers 20 common agent types with complete 7-artifact output
- Generation time < 2 seconds (static templates), < 8 seconds (LLM-augmented)
- Blueprint JSON passes schema validation
- Architecture diagram renders correctly in Explorer
- User can share architecture via URL
