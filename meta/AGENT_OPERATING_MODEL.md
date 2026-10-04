# AGENT OPERATING MODEL

**Status:** ACTIVE  
**Authority:** `AI_CONSTITUTION.md`, `AGENTS.md`, `meta/COO_MASTER_MISSION.md`

---

## Agent lifecycle

Every agent follows:

`READ → UNDERSTAND → INSPECT → DECIDE → IMPLEMENT → TEST → FIX → VERIFY → DOCUMENT → RE-READ → IMPROVE → VERIFY → CONTINUE`

Repository state and authoritative documentation are the source of truth. Conversation history is not required for execution.

## Mandatory state loading

Before meaningful work, read at minimum:

1. `AI_CONSTITUTION.md`
2. `AGENTS.md`
3. `meta/COO_MASTER_MISSION.md`
4. `meta/CURRENT-STATE.md`
5. `meta/memory/DECISIONS.md`
6. `meta/ROADMAP.md`
7. `meta/EVIDENCE_MODEL.md`
8. `meta/MOST-WANTED-SKILLS.md`
9. `meta/AGENT_OPERATING_MODEL.md`
10. `meta/AGENT_HANDOFF_PROTOCOL.md`
11. `SECURITY.md`
12. `CONTRIBUTING.md`

Then inspect the implementation, schemas, generators, workflows, tests, release mechanisms, generated artifacts, and relevant documentation.

Never rely on the obsolete `meta/MEMORY_STATE.md` or `meta/DECISION_LOG.md` as authoritative state unless the repository explicitly restores them.

## Execution rules

- Inspect live branches, commits, open PRs, CI, tests, generated artifacts, and documentation before deciding.
- Prefer existing mechanisms over duplication.
- Treat `skills/` as the canonical skill source; generated representations are projections.
- Use evidence proportional to the claim.
- Preserve security, validation, provenance, reproducibility, and read-only boundaries.
- Do not invent demand, adoption, benchmarks, compatibility, or production-readiness claims.
- Do not expose private chain-of-thought.

## Verification

Testing must match change risk. Use focused tests plus repository CI where applicable.

Do not claim a test, CI run, merge, release, or deployment occurred without live evidence.

A green suite is not sufficient by itself; verify the changed behavior and resulting repository state independently.

## Documentation gate

A meaningful task is not COMPLETE until:

**Implementation + Verification + Documentation + Repository State**

are synchronized.

After a merge:

1. verify live `main`;
2. synchronize `meta/CURRENT-STATE.md` if the merge changed verified state;
3. re-read affected architecture/decision/roadmap documents;
4. verify no known documentation drift remains;
5. record the next justified action.

## Decision and escalation

Normal repository execution decisions may be made autonomously within documented authority.

Escalate when a decision changes strategic direction, fundamental architecture, destructive operations, significant security posture, breaking interfaces, business/product direction, or another decision reserved by `AI_CONSTITUTION.md`.

Important architectural decisions belong in `meta/memory/DECISIONS.md`.

## Handoff

Every meaningful work session must leave enough repository information for the next agent to determine:

- what changed;
- why it changed;
- what was verified;
- what remains;
- what is blocked;
- what decision was made;
- what should happen next.

The repository must remain understandable without this conversation.

## Completion rule

Never declare COMPLETE while tests/CI are pending, documentation is stale, generated artifacts are unverified, a required merge is incomplete, or a material known defect remains.

## Core Agentic Execution Loop

The agent operates as a bounded autonomous execution loop. A user goal is the objective; each verified result becomes evidence for the next decision rather than requiring a new user prompt.

Canonical cycle:

`OBSERVE → ASSESS → PLAN → EXECUTE → VERIFY → RECORD → DECIDE`

- **OBSERVE:** load live repository state, authoritative documentation, relevant code, generated artifacts, CI/PR state, and prior cycle evidence.
- **ASSESS:** compare observed state with the goal, explicit invariants, acceptance criteria, and known risks.
- **PLAN:** choose the smallest evidence-backed next action. Do not invent work merely to keep the loop active.
- **EXECUTE:** perform the selected repository action within documented authority.
- **VERIFY:** test the changed behavior and independently inspect the resulting state. A failure is evidence, not a terminal response.
- **RECORD:** preserve the objective, action, evidence, result, failure classification, and remaining work in the appropriate repository record.
- **DECIDE:** choose exactly one of `CONTINUE`, `BLOCKED`, or `DONE`.

### Failure-driven continuation

A failed test, CI job, generated-artifact mismatch, documentation drift finding, or runtime defect becomes an input to the next cycle. The agent MUST inspect the failure before selecting the next action. It must not repeat an identical failed action without new evidence or a changed precondition.

### Bounded-loop safeguards

The loop is autonomous but not unbounded. Every execution cycle MUST maintain an iteration counter, a current objective, and a next-action record. The default operational ceiling is 12 iterations per goal unless the governing task explicitly defines a lower limit. Repeated identical action/failure signatures require diagnosis or escalation rather than repetition. If no safe evidence-backed next action exists, the state is `BLOCKED`.

### Completion contract

The agent may select `DONE` only when the goal and applicable invariants are verified, required tests/CI are complete, generated artifacts are synchronized, authoritative documentation is synchronized, and no material known defect remains. `DONE` is not inferred from a single green check or a mergeable GitHub state.

### Authority boundary

The loop may autonomously execute normal repository work within documented authority. It MUST stop and escalate for strategic direction, fundamental architecture changes, destructive operations, significant security posture changes, breaking interfaces, or conflicting higher-priority decisions. The loop never fabricates evidence, success, approval, or completion.

### Continuation state

Each cycle should expose only structured operational state, not private chain-of-thought:

`GOAL | ITERATION | CURRENT STATE | EVIDENCE | LAST ACTION | RESULT | FAILURE/DELTA | NEXT ACTION | EXIT CONDITION`

This loop is the repository's core agent operating behavior. Specialist skills and workflows are execution mechanisms inside the loop, not competing orchestration systems.
