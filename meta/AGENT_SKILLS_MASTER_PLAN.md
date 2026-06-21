# AGENT_SKILLS_MASTER_PLAN.md

**Version:** Post TASK-005B  
**Date:** 2026-06-21  
**Graph State:** 53 nodes / 108 edges

---

## Mission

Build the most complete, semantically rigorous, machine-readable graph of AI agent skills. Every node must have a real skill file. Every edge must reflect genuine dependency or recommendation.

---

## Phase 1: Foundation (COMPLETED)

- [x] TASK-001: Map 23 agentic-patterns skill files → graph nodes
- [x] TASK-002: Edge baseline + category structure
- [x] TASK-003: 9 reasoning nodes (02-reasoning)
- [x] TASK-004: PERCEPTION_AUDIT + NODE_SELECTION + GRAPH_DIFF_PLAN
- [x] TASK-005B: Implement 6 perception/data nodes + 15 edges

**Phase 1 result:** 53 nodes, 108 edges, 5 categories active.

---

## Phase 2: Skill File Coverage (ACTIVE)

Target: Every graph node has a corresponding skill file with:
- `id`, `name`, `category`, `level`, `stability`
- `description` (1-paragraph)
- `prerequisites` list
- `example_use_cases` list
- `related_skills` list

Nodes needing skill files (new from TASK-005B):
- [ ] `skill:structured-data-reading`
- [ ] `skill:database-reading`
- [ ] `skill:file-system-access`
- [ ] `skill:output-formatting`
- [ ] `skill:schema-validation`
- [ ] `skill:data-transformation`

---

## Phase 3: Category Expansion (PLANNED)

Next categories to populate:
- `01-perception` — visual, audio, multimodal input
- `06-planning` — advanced planning strategies
- `08-safety` — guardrails, alignment patterns
- `13-evaluation` — scoring, benchmarking

---

## Phase 4: Semantic Enrichment (PLANNED)

- Evidence counts from real skill files
- Confidence calibration across edges
- Contradiction detection (two nodes with same description)
- Graph export to RDF/OWL for interoperability

---

## Governance Rules

1. No node added without NODE_SELECTION audit
2. No category created without PROJECT_CONSTITUTION review
3. Collision review required for all 12-data cluster additions
4. Every task produces TASK_NNN_REPORT.md + TASK_NNN_SELF_REVIEW.md
5. MEMORY_STATE.md updated at task end
6. DECISION_LOG.md updated for every structural decision
