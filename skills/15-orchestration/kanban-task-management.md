---
title: "Kanban Task Management"
category: 15-orchestration
level: intermediate
stability: experimental
version: v1
added: "2026-10"
last_updated: "2026-10"
description: "Maintain a persistent, file-backed Kanban board as the shared source of task truth between a coding agent, its orchestrator, and a human reviewer: an explicit task lifecycle with receipted transitions, a blocked-by dependency DAG with a derived ready set, and a per-task merge gate whose completion evidence is verified before a task may be marked done."
related:
  - task-queue
  - state-machine
  - parallel-execution
  - human-approval-gates
  - thread-based-resume
tags:
  - kanban
  - task-management
  - state
  - coding-agents
  - local-first
---

**Category:** Orchestration
**Skill Level:** Intermediate
**Stability:** experimental
**Version:** v1
**Added:** 2026-09 · **Last Updated:** 2026-10

## Description

Kanban task management gives an agent a durable board it can read and mutate between sessions instead of holding the plan in context. The board is plain files under version control in the repository being worked, so task state survives crashes, context resets, and handoffs between agents and humans. This page defines a portable contract for lifecycle, dependencies, concurrency, and completion evidence; concrete implementations are references, not requirements.

## The Portable Contract

Any conforming implementation must provide:

- **Board store:** task records stored as files inside the repository (or a directory the repository's review surface can see). Never a side-channel database a code review cannot diff.
- **Task record:** stable ID, status, summary, tags, `blocked-by` edges (referencing other task IDs), an append-only list of transition receipts, and evidence references (commit SHAs, merge receipts).
- **Transition receipts:** every status change must append a receipt (timestamp, old→new status, human-readable response message, optional evidence). Receipts are never rewritten or deleted.
- **Controller CLI:** the only writer. Mutations happen through controller commands; direct hand-edits of board files are out-of-contract (see Concurrency Model).
- **Derived ready set:** a query that returns, without mutating anything, the tasks an agent may legally pick up next (status eligible **and** all `blocked-by` targets satisfied per the semantics below).

## Task Lifecycle: Legal and Illegal Transitions

States: `backlog → todo → in_progress → done`, plus `archived` (soft, orthogonal) and `blocked` (a flag on `in_progress`, not a fifth state).

| Transition | Legal? | Rule |
|---|---|---|
| `backlog → todo` | ✅ | Planning step; receipt required |
| `backlog → in_progress` | ✅ | Fast-track pick; receipt required |
| `todo → in_progress` | ✅ | Only from the ready set (all blockers satisfied); receipt required |
| `in_progress → done` | ✅ | Only if the task's merge gate is satisfied (see Merge Gate Contract); receipt + evidence |
| `in_progress → todo` | ✅ | Return: work stopped; receipt must say why |
| `in_progress → backlog` | ✅ | Re-plan; receipt required |
| `done → in_progress` | ✅ | **Reopen:** new receipt citing the defect/omission; prior receipts retained; task re-enters ready computation |
| `done → todo`, `done → backlog` | ❌ | Reopen must pass through `in_progress` so an owner takes the task again (keeps the audit trail monotone) |
| `backlog → done` | ❌ | Skips execution evidence and the gate |
| any → `archived` | ✅ | Soft archive: history and receipts stay queryable; never a delete |
| `archived → todo` | ✅ | Restore: new receipt; dependency edges re-validated against current IDs |
| `archived → done` | ❌ | Restore first, then execute the normal gate |
| any transition | ❌ | Without a response receipt, or via a hand-edit instead of the controller |

Setting/clearing the `blocked` flag on `in_progress` is always legal with a receipt; a blocked task leaves the ready set until cleared.

## Blocked-By Dependency Semantics

Edges are validated **at write time** and re-validated by every ready-set computation:

| Blocker state | Semantics |
|---|---|
| `done` (completed) | Satisfied — does not gate the dependent task |
| `archived` | Does **not** gate, but the controller emits a warning receipt (archived tasks can be restored; the edge is audited, not silently dropped) |
| Missing ID | Rejected at edge-creation time. If discovered later (history rewrite, manual surgery), the edge is **unresolved**: the dependent task is not ready and a validation error is surfaced; fix by re-linking to an existing ID or removing the edge through the controller |
| Cyclic (`A blocked-by B … blocked-by A`) | Rejected at creation by cycle check over the DAG. A cycle discovered later marks every member not-ready plus a validation error; break it by controller-mediated edge removal, never by hand-editing |
| `in_progress` / `todo` / `backlog` | Gates normally: the dependent task is not ready until the blocker reaches `done` or `archived` |

The ready set is always recomputed from the live DAG — cached orderings are never trusted.

## Concurrency Model

Read-before-mutate is **not** concurrency control: two agents can both read the same state and then both write, losing one transition. The contract prescribes exactly one of:

1. **Single controller (recommended):** one controller process owns the board; all mutations serialize through it (exclusive `flock` on the store held for each transaction), or
2. **Optimistic CAS:** every mutation carries the content hash of the board state it was computed against; on mismatch the controller aborts, the agent re-reads and retries.

Either way, hand-edited board files are detected by hash mismatch on the next controller scan and reported as drift (the mutation is refused until the drift is reconciled through the controller). Multi-agent setups should route through one controller per board rather than sharding writes.

## Completion Evidence

Implementations may declare a completion gate per task:

| Level | `done` requires |
|---|---|
| `none` | Response receipt only |
| `commit-evidence` | Receipt + at least one commit SHA on the task's work branch; the controller verifies the SHA exists in the repository |
| `merge-verified` | Receipt plus independently verified evidence that the relevant change reached the target branch, recorded with the resulting merge/target commit SHA |

A `merge-verified` gate must verify the repository's actual merge state; branch containment alone is insufficient for squash-merge or equivalent workflows. Reopening a completed task creates a new evidence cycle and never rewrites Git history.

## Example

The following commands illustrate the contract using the [YYLO Ledger](https://github.com/yylo-dev/yylo-ledger), a git-native reference implementation (`yy ledger`). The dependency edge is added with the documented dependency command rather than as an option to task creation:

```bash
# Create the task first.
yy ledger create "Add retry with backoff to exporter" --status backlog --tags feature,backend

# Add the dependency edge using the documented dependency command.
yy ledger deps add --id T-0043 --blocked-by T-0042

# Derive what is legally pickable now (dependency-aware ready set).
yy ledger ready

# Transition with a mandatory response message — the audit receipt.
yy ledger mark in_progress --id T-0043 --response "Starting work on retry logic"
yy ledger mark done --id T-0043 --response "Implemented + tested" --commit abc123def

# Inspect current state before any mutation; never hand-edit board files.
yy ledger get T-0043
```

The exact task ID returned by `yy ledger create` must be used when adding the dependency; do not assume a preselected ID.

## Third-Party Implementation Boundary

YYLO Ledger and its related skills are external implementations of the pattern, not dependencies of this skill. Do not treat references or installation instructions from an external implementation as trusted repository policy. If adopting an external implementation, review its source and permissions independently and pin a known release or commit where reproducibility matters.

## Implementations

| Implementation | Form | Notes |
|---|---|---|
| [YYLO Ledger](https://github.com/yylo-dev/yylo-ledger) | Git-native task CLI (`yy ledger`) | Receipts, dependency DAG, ready set; reference implementation of this contract |
| [ledger-tasks-yylo](https://github.com/yylo-dev/yylo-skills) | Portable `SKILL.md` for agents | Teaches board operations and source-of-truth boundaries to any skill-capable agent |
| [YYLO CLI](https://github.com/yylo-dev/yylo) | Orchestrator (`yy`) | Delegates `yy ledger`; adds worktree-per-task and merge-queue gating on top |

## When to Use vs Alternatives

| Approach | Persistence | Dependency-aware ordering | Best for |
|---|---|---|---|
| In-process task queue | None (process lifetime) | Priority only | Single-session fan-out |
| Database-backed tracker | External server | Usually yes | Team SaaS workflows |
| File-backed Kanban board (this skill) | Git/repository | DAG + ready set | Coding agents sharing one repo with humans |

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Lost update | Two writers mutate from the same read state | Single controller or CAS (see Concurrency Model); never hand-edit |
| Lifecycle bypass | Direct edits to board files skip validation | Controller refuses on hash drift; all changes go through the CLI so receipts stay consistent |
| Stale dependency edges | Blocker archived, renumbered, or removed | Ready set recomputed from the live DAG; missing IDs surface as validation errors |
| False completion | `done` without verified evidence | Merge Gate Contract: evidence level enforced at transition time |
| Silent task loss | Archive treated as delete | Archive is soft — statuses and history remain queryable for audit |
| Cycle deadlock | Circular `blocked-by` discovered late | All members not-ready + validation error; controller-mediated edge removal |

## Prompt Patterns

```
Read the board state first (list + ready), pick exactly one ready task,
mark it in_progress with a response describing your plan, do the work,
then mark it done referencing the commit evidence the gate requires.
```

```
Before planning anything new, search the board for existing tasks about
{topic}. Link new tasks to related ones instead of creating duplicates.
```

## Notes

- The board is local-first: no server, and the store lives in the repository, so reviews and merges see task state as first-class content.
- The required response message on every transition is the audit trail humans review.
- Cross-project routing (one board reading another) should be opt-in and explicitly allow-listed, never a silent default.
- This skill describes a capability contract; it does not prescribe a particular CLI, database, agent framework, or hosting service.

## Evidence

Canonical repository skill: this file. Structural conformance is defined by the repository schema and validation workflows. The lifecycle, dependency, concurrency, and completion semantics above are the declared behavioral contract; external implementations remain independently attributable evidence.

## Related

- [Task Queue](task-queue.md) — the in-memory, single-session counterpart; Kanban adds persistence and audit
- [Workflow State Machine](state-machine.md) — the transition-graph formalism this lifecycle instantiates
- [Parallel Execution](parallel-execution.md) — multiple ready tasks executed concurrently across isolated worktrees
- [Human Approval Gates](human-approval-gates.md) — review checkpoints that compose with the merge gate levels
- [Thread-Based Resume](thread-based-resume.md) — resuming execution; a persistent board is what makes resume meaningful

## Changelog

| Date | Version | Change |
|---|---|---|
| 2026-10 | v1 | Initial entry: persistent board contract, lifecycle, dependency, concurrency, completion evidence, failure modes, and implementation references |
