# NEXT_TASK_PROMPT.md — Execution Prompt for TASK-002

> Generated: 2026-06-21 — Governance Reconciliation Phase 5  
> This prompt targets TASK-002 only — the highest-value next task by graph analysis.

---

```
MANDATORY EXECUTION MODE
Repository is the source of truth.
DO NOT design.
DO NOT plan.
DO NOT simulate.
Only commit real changes.
=================================================
PHASE 0 — AUTHORITATIVE STATE CHECK
Read:
  data/SKILLS_GRAPH.json
  meta/MEMORY_STATE.md
Measure directly from SKILLS_GRAPH.json:
  node count
  edge count
  schema version
Return measured values.
If graph is not exactly:
  47 nodes
  93 edges
  schema 1.3
STOP.
Create:
  meta/STATE_DIVERGENCE_REPORT.md
and terminate.
=================================================
TASK-002 EXECUTION
Implement exactly these 5 nodes:
  skill:context-window-management
  skill:prompt-caching
  skill:context-compression
  skill:system-prompt-design
  skill:retrieval-augmented-context

All nodes must have:
  category: "02-reasoning"
  type: "Skill"
  stability: "stable" or "evolving" as appropriate
  level: "beginner" | "intermediate" | "advanced"
  centrality block (calculate from edge counts)
=================================================
ANTI-DUPLICATE CHECK
Verify these already exist and MUST NOT be recreated:
  skill:context-management
  skill:prompt-engineering
  skill:rag-retrieval
  skill:llm-orchestration
Run duplicate analysis before writing.
=================================================
REQUIRED EDGES (~10–12)
Add edges connecting new nodes to:
  skill:prompt-engineering
  skill:context-management
  skill:rag-retrieval
  skill:embedding-generation
  skill:llm-orchestration
Edge types: REQUIRES, RECOMMENDED_WITH, LEARN_BEFORE only.
=================================================
GRAPH RULES
Modify existing graph only.
Never regenerate graph.
Allowed changes:
  add nodes
  add edges
Forbidden:
  remove nodes
  remove edges
  rename nodes
  rewrite graph
=================================================
REQUIRED OUTPUTS
Create:
  meta/TASK_002_REPORT.md (replace existing STATUS: OPEN version)
  meta/TASK_002_SELF_REVIEW.md
Update:
  meta/MEMORY_STATE.md
  meta/DECISION_LOG.md
  meta/AGENT_SKILLS_BACKLOG.md
  meta/AGENT_SKILLS_MASTER_PLAN.md
  meta/GRAPH_AUDIT.md
=================================================
MANDATORY COMMIT
Commit all changes.
Commit message:
  feat(graph): TASK-002 context engineering skills layer
=================================================
MANDATORY VERIFICATION
After commit:
  Re-read SKILLS_GRAPH.json
  Count nodes
  Count edges
  Verify all 5 new node IDs exist
  Verify commit SHA exists
Return ONLY:
  nodes before
  nodes after
  edges before
  edges after
  commit SHA
  files changed
If commit SHA is missing:
  TASK FAILED
```

---

*Prompt version: 1.0.0 — Generated 2026-06-21*
