# AGENT OPERATING MODEL

**Initiative:** INITIATIVE-010A  
**Created:** 2026-06-23  
**Status:** ACTIVE

---

## Agent Lifecycle

Every agent follows this lifecycle without exception:

```
STATE_LOAD → MISSION_RECEIVE → EXECUTE → VALIDATE → COMMIT → HANDOFF
```

1. **STATE_LOAD** — Read `meta/MEMORY_STATE.md` and `meta/DECISION_LOG.md`. Verify metrics match `data/SKILLS_GRAPH.json`. If divergence found, create `meta/STATE_DIVERGENCE_REPORT.md` and stop.
2. **MISSION_RECEIVE** — Accept mission assignment from Program Director. Confirm scope, inputs, and success criteria.
3. **EXECUTE** — Perform specialist work. All reads from repository only. No external state.
4. **VALIDATE** — Run self-validation checks per agent spec. Produce evidence artifacts.
5. **COMMIT** — Commit only if Quality Auditor gate passes and Governance Officer has signed off on D2+ decisions.
6. **HANDOFF** — Write handoff packet per `meta/AGENT_HANDOFF_PROTOCOL.md` and pass to next agent.

---

## Mission Assignment Flow

```
Program Director
  → identifies next initiative from MEMORY_STATE.md
  → writes initiative charter
  → assigns to Specialist Agent with scope + success criteria
  → logs assignment in DECISION_LOG.md
```

The specialist agent may NOT begin execution until it has confirmed:
- [ ] MEMORY_STATE.md loaded and verified
- [ ] Mission charter received from Program Director
- [ ] Required authoritative files identified

---

## Execution Flow

```
Specialist Agent
  → reads required files
  → performs analysis / generation
  → produces output artifacts
  → runs internal validation
  → produces evidence package
```

If any required file is missing or unreadable, the agent must:
1. Log the blocker in the handoff packet
2. Escalate to Program Director
3. Stop — do not proceed with incomplete state

---

## Validation Flow

```
Specialist Agent output
  → Quality Auditor checks:
      - Output completeness
      - Schema conformance
      - No phantom metrics
      - Evidence files present
  → PASS → proceed to commit
  → FAIL → return to Specialist Agent with failure report
```

Quality gate is mandatory. The Release Manager will not commit without a Quality Auditor PASS signal.

---

## Commit Flow

```
Quality Auditor PASS
  → D0/D1: Release Manager commits directly
  → D2–D5: Governance Officer sign-off required first
  → Release Manager:
      - updates meta/MEMORY_STATE.md
      - appends to meta/DECISION_LOG.md
      - updates meta/CHANGELOG.md
      - creates git tag if release
      - writes handoff packet
```

---

## Governance Checkpoints

| Checkpoint | Trigger | Handler |
|-----------|---------|--------|
| G1 — State Verification | Every mission start | All agents (self-check) |
| G2 — Evidence Gate | Before any D2+ proposal | Specialist Agent |
| G3 — Decision Approval | Before D2+ commit | Governance Officer |
| G4 — Quality Gate | Before any commit | Quality Auditor |
| G5 — Release Gate | Before version tag | Release Manager + Governance Officer |

---

## Required Execution Chain

For all D2–D5 decisions:

```
Program Director
  → Specialist Agent (execution)
  → Governance Officer (approval)
  → Quality Auditor (quality gate)
  → Release Manager (commit + state update)
```

For D0–D1 decisions:

```
Program Director
  → Specialist Agent (execution)
  → Quality Auditor (quality gate)
  → Release Manager (commit + state update)
```

No agent may shortcut this chain.

---

## Agent Responsibilities Summary

| Agent | Executes | Approves | Commits |
|-------|---------|---------|--------|
| Program Director | Initiative charters | D0–D1 | No |
| Specialist Agents | Domain work | D0–D1 within scope | No |
| Governance Officer | Constitution review | D2–D5 | No |
| Quality Auditor | Quality checks | Gates only | No |
| Release Manager | State updates | None | YES — final committer |

---

*All agents must load this file before beginning execution.*
