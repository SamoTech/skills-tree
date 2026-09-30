# Skills Tree — Live Repository State

> Maintained as a point-in-time operational snapshot. This file records verified state used for engineering and governance decisions.

## Verified snapshot

- Snapshot date: 2026-09-30
- Main HEAD: `ee427de8705dba318a32d8c7be82bbdac53f80f8`
- Skill files: 369
- Battle-tested: 60
- Enriched: 3
- Stubs: 303
- Invalid: 3
- PR #141: merged on 2026-09-30 as commit `e34d71e6cf7e980871bf71fb084b46c0f5617127`
- PR #150: closed as duplicate of PR #155
- Open substantive PRs requiring current-main revalidation: #145, #146, #155, #156, #142
- Governance implementation: `AI_CONSTITUTION.md` and `AGENTS.md` are merged to `main` via PR #158 at `ee427de8705dba318a32d8c7be82bbdac53f80f8`.

## Validation and CI state

PR #141 added and enforced the machine-readable Evidence contract at registry initialization and added regression coverage. It was merged after review because it was focused and GitHub reported it mergeable.

For the remaining open PRs, GitHub currently reports Vercel status failure with a deployment-rate-limit condition. This is infrastructure/quota noise rather than evidence of a repository test failure. Separately, their branches are stale relative to current main and several are non-mergeable, so they must be rebased/reconciled and revalidated before merge.

## Corpus modernization priority

The current quality distribution makes the remaining 303 stubs the dominant modernization target. Category `01-perception` contains 26 stubs; `09-agentic-patterns` contains 15 stubs and 2 invalid skills; `05-code` contains 23 stubs. Work should remain incremental and evidence-driven rather than attempting a corpus-wide rewrite.

## Governance state

The repository now has an explicit AI governance entrypoint:

- `AI_CONSTITUTION.md` — authority, escalation, documentation gate, decision record, handoff, and completion rules.
- `AGENTS.md` — AI-agent entrypoint and mandatory operating rules.
- `meta/AGENT_OPERATING_MODEL.md` — existing lifecycle and execution-chain specification.
- `meta/memory/DECISIONS.md` — authoritative decision record.
- `meta/CURRENT-STATE.md` — current verified state.

The authoritative-document map intentionally reuses existing repository documents instead of creating duplicate status, roadmap, architecture, testing, deployment, or security files.

## Operational rule

Do not treat historical snapshots in `PROJECT_MEMORY.md` or older audit documents as current truth when they conflict with current main SHA, current PR metadata, current CI results, or generated quality reports.

A meaningful task is not COMPLETE until implementation and required documentation are both verified.
