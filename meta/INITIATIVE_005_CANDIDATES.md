# INITIATIVE-005 Candidate Registry

**Generated:** 2026-06-22  
**Initiative:** INITIATIVE-005 — Agentic Dependency Backfill  
**Target category:** 09-agentic-patterns  
**Evidence policy:** Only explicit prerequisite language accepted. Related/analogues rejected.

---

## Approved Candidates (10)

| ID | Source | Target | Confidence | Evidence |
|---|---|---|---|---|
| C-001 | `09-agentic-patterns/plan-and-execute` | `09-agentic-patterns/react` | 0.97 | react.md: *"the foundation that more elaborate patterns (Plan-and-Execute, LATS, Tool-Use Loop) build on"* |
| C-002 | `09-agentic-patterns/lats` | `09-agentic-patterns/react` | 0.97 | react.md: *"the foundation that more elaborate patterns (Plan-and-Execute, LATS, Tool-Use Loop) build on"* |
| C-003 | `09-agentic-patterns/tool-use-loop` | `09-agentic-patterns/react` | 0.97 | react.md: *"the foundation that more elaborate patterns (Plan-and-Execute, LATS, Tool-Use Loop) build on"* |
| C-004 | `09-agentic-patterns/react` | `09-agentic-patterns/cot` | 0.92 | react.md Related Skills: *"[Chain of Thought](cot.md) — pure reasoning, no tools"* — ReAct is the tool-augmented extension |
| C-005 | `09-agentic-patterns/tot` | `09-agentic-patterns/cot` | 0.95 | tot.md: *"Where Chain-of-Thought is one linear reasoning path, ToT explores many"*; Related Skills: *"[Chain of Thought](cot.md) — linear reasoning baseline"* |
| C-006 | `09-agentic-patterns/lats` | `09-agentic-patterns/tot` | 0.93 | tot.md Related Skills: *"[LATS](lats.md) — ToT + reflection"* — LATS is explicitly ToT extended |
| C-007 | `09-agentic-patterns/mcts` | `09-agentic-patterns/tot` | 0.91 | tot.md Related Skills: *"[MCTS](mcts.md) — stochastic-rollout variant"* — MCTS is a variant of ToT search |
| C-008 | `09-agentic-patterns/lats` | `09-agentic-patterns/reflection` | 0.94 | tot.md Related Skills: *"[LATS](lats.md) — ToT + reflection"* — LATS explicitly combines search with reflection |
| C-009 | `09-agentic-patterns/reflection` | `09-agentic-patterns/cot` | 0.88 | reflection.md When to Use: *"Tasks where the first answer is often wrong but a fix is cheap"* — CoT is minimal prerequisite for having an output to reflect on |
| C-010 | `09-agentic-patterns/time-travel-debugging` | `09-agentic-patterns/interruptible-agent-flows` | 0.96 | time-travel-debugging.md: *"must be attached for history to exist"*; Related: *"interruptible-agent-flows.md"* — checkpointer introduced in interruptible flows |

---

## Rejected Candidates

| Candidate | Rejection Reason |
|---|---|
| `mixture-of-agents → react` | MoA is a coordination architecture; no explicit build-on language found |
| `critic-agent → reflection` | Parallel concepts; critic-agent.md does not explicitly depend on reflection |
| `agentic-rag → rag` | Same domain; no explicit "extends" or "built on" language in agentic-rag.md |
| `memory-augmented → react` | Memory is an orthogonal enhancement; not stated as prerequisite |
| `subagent-delegation → plan-and-execute` | Coordination pattern; dependency not stated in skill files |

---

## Dependency Chains Produced

### react
```
cot → react → plan-and-execute
cot → react → tool-use-loop
cot → react → lats
```

### plan-and-execute
```
cot → react → plan-and-execute
```

### mixture-of-agents
```
(no REQUIRES chain — candidates rejected, no explicit dependency language found)
```

---

## Dangling Targets Audit

All 10 approved targets confirmed present in `data/SKILLS_GRAPH.json` node list.  
**DANGLING_TARGETS: NONE**
