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
