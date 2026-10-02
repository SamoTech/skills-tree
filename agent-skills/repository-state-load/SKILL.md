---
name: repository-state-load
description: Load and reconcile authoritative repository state before meaningful AI execution.
metadata:
  source: skills/15-orchestration/repository-state-load.md
  category: 15-orchestration
---

# Repository State Load

## Description

Load the repository's authoritative governance, current-state, decisions, and task-relevant technical evidence before making consequential changes. The goal is to establish a verified baseline rather than infer state from partial context.

1. Establish the current main SHA from GitHub.
2. Read authoritative governance and state documents.
3. Compare documented state with live GitHub metadata and generated reports.
4. Treat live repository evidence as authoritative when historical snapshots conflict.
5. Record material divergence before making consequential changes.
6. Do not execute against incomplete or contradictory state without resolving or escalating the divergence.

## Runnable example

```bash
git fetch origin main --depth=1
git rev-parse origin/main
git diff --name-only origin/main...HEAD
```

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Main branch reference | Verified baseline SHA | Main SHA cannot be established |
| Governance documents | Authoritative operating rules | Required document is missing |
| GitHub metadata and CI | Current implementation evidence | Evidence is stale or incomplete |
| Current-state and decisions | Continuation context | Documentation contradicts live state |

## Failure modes

- Stale CURRENT-STATE data: refresh it before declaring state.
- Historical decision mistaken for current state: verify against current main and PR/CI evidence.
- Missing authoritative document: record the blocker and escalate.
- Partial retrieval: do not infer unseen repository state.

## Related

- `documentation-drift-resolution.md`
- `evidence-verification.md`
- `execution-handoff.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- meta/AGENT_OPERATING_MODEL.md
- meta/CURRENT-STATE.md
- meta/memory/DECISIONS.md
