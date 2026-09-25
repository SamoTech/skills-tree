---
title: "Kanban Task Management"
category: 15-orchestration
level: intermediate
stability: stable
version: v2
added: "2026-09"
description: "Maintain a persistent, file-backed Kanban board as the shared source of task truth between a coding agent, its orchestrator, and a human reviewer — task lifecycle, dependency graphs, ready-set ordering, and merge gating that survive across sessions and CLI invocations."
related:
  - task-queue
  - sequential-workflow
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
**Stability:** stable
**Version:** v2
**Added:** 2026-09

### Description

Kanban task management gives an agent a durable board it can read and mutate between sessions instead of holding the plan in context. Tasks move through an explicit lifecycle (backlog → todo → in_progress → done) with a required human-readable response message on every transition, dependency edges (`blocked-by`) forming a DAG, and a derived ready set that tells the agent what it may legally pick up next. Because the board is plain files under version control, state survives crashes, context resets, and handoffs between agents and humans on the same repository. It is the persistence layer that turns a one-shot task queue into an auditable multi-session workflow.

### Example

Real commands from YYLO Ledger (`yy ledger`), a git-native implementation of this skill:

```bash
# Create a task with tags and a dependency edge
yy ledger create "Add retry with backoff to exporter" --status backlog --tags feature,backend --blocked-by T-0042

# Derive what is legally pickable now (dependency-aware ready set)
yy ledger ready

# Transition with a mandatory response message — the audit trail
yy ledger mark in_progress --id T-0043 --response "Starting work on retry logic"
yy ledger mark done --id T-0043 --response "Completed: implemented X, tested Y" --commit abc123def

# Inspect current state before any mutation; never hand-edit board files
yy ledger get T-0043
```

Agents without the YYLO runtime can install the portable skill that teaches this workflow to Claude Code, Codex, or Pi:

```bash
npx skills add yylo-dev/yylo-skills --skill ledger-tasks-yylo
```

### Implementations

| Implementation | Form | Notes |
|---|---|---|
| [YYLO Ledger](https://github.com/yylo-dev/yylo-ledger) | Git-native task/Record CLI (`yy ledger`) | Flat task commands + ID-first record groups; mutation receipts; dependency DAG |
| [ledger-tasks-yylo](https://github.com/yylo-dev/yylo-skills) | Portable `SKILL.md` for agents | Teaches board operations and source-of-truth boundaries to any skill-capable agent |
| [YYLO CLI](https://github.com/yylo-dev/yylo) | Orchestrator (`yy`) | Delegates `yy ledger`; adds worktree-per-task and merge-queue gating on top |

### When to Use vs Alternatives

| Approach | Persistence | Dependency-aware ordering | Best for |
|---|---|---|---|
| In-process task queue | None (process lifetime) | Priority only | Single-session fan-out |
| Database-backed tracker | External server | Usually yes | Team SaaS workflows |
| File-backed Kanban board | Git/repository | DAG + ready set | Coding agents sharing one repo with humans |

### Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Concurrent mutation | Two agents transition the same task without reading state first | Read current task state before every mutation; preserve mutation receipts; serialize through one controller CLI |
| Lifecycle bypass | Direct edits to board files skip validation | Never write board files by hand; all changes go through the board CLI so receipts and state machines stay consistent |
| Stale dependency edges | A `blocked-by` target is archived or renumbered | Recompute the ready set from the DAG instead of trusting cached order |
| Silent task loss | Archive treated as delete | Archive is soft — statuses and history remain queryable for audit |

### Prompt Patterns

```
Read the board state first (list + ready), pick exactly one ready task,
mark it in_progress with a response describing your plan, do the work,
then mark it done referencing the commit.
```

```
Before planning anything new, search the board for existing tasks about
{topic}. Link new tasks to related ones instead of creating duplicates.
```

### Notes

- The board is local-first: no server, and the store lives in the repository, so reviews and merges see task state as first-class content.
- The required `--response` message on every transition is the audit trail humans review.
- Cross-project routing (one board reading another) should be opt-in and explicitly allow-listed, never a silent default.

### Related Skills

- [Task Queue](task-queue.md) — the in-memory, single-session counterpart; Kanban adds persistence and audit
- [Sequential Workflow](sequential-workflow.md) — ordered execution when the DAG degenerates to a chain
- [Parallel Execution](parallel-execution.md) — multiple ready tasks executed concurrently across isolated worktrees
- [Human Approval Gates](human-approval-gates.md) — review checkpoints that gate task completion
- [Thread-Based Resume](thread-based-resume.md) — resuming execution; a persistent board is what makes resume meaningful

### Changelog

| Date | Version | Change |
|---|---|---|
| 2026-09 | v2 | Initial entry at v2: runnable CLI example, failure modes, implementation and comparison tables, related skills |
