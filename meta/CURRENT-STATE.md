# Skills Tree — Live Repository State

> Maintained as a point-in-time operational snapshot. This file records verified state used for engineering and governance decisions.

## Verified snapshot

- Snapshot date: 2026-09-30
- Main HEAD: verified on 2026-09-30; see the repository default branch for the current SHA.
- Skill files: 369
- Battle-tested: 74
- Enriched: 2
- Stubs: 293
- Invalid: 0
- Stub migration: batch 01 merged as PR #164 at `424fb43bee42545ac09f4683adb1127dfa97bcda` (10 perception skills)
- DevLens health: 87/100 (README badge, updated 2026-09-30)
- PR #141: merged on 2026-09-30 as commit `e34d71e6cf7e980871bf71fb084b46c0f5617127`
- PR #150: closed as duplicate of PR #155
- Stale substantive PRs remain open only where GitHub safety controls prevented bulk disposition; they are not merge candidates until reconciled against current `main`.
- Governance implementation: `AI_CONSTITUTION.md` and `AGENTS.md` are merged to `main` via PR #158 at `ee427de8705dba318a32d8c7be82bbdac53f80f8`.
- Source-of-truth cleanup: PR #162 merged on 2026-09-30 as `33b36dfa02b5acb87d517a5669f1a9eca3b50626`.
- Security/distribution consolidation: PR #163 merged on 2026-09-30 as `2a6d2dfe50006746d7866df6890691f154840dfb`.

## Validation and CI state

The current generated `meta/QUALITY-REPORT.md` still reflects the pre-batch snapshot (74 battle-tested, 2 enriched, 293 stubs, 0 invalid). Batch 01 is merged, but the connector-visible Actions state has not produced a refreshed quality report yet; therefore the 293-stub count is not being presented as current post-migration evidence.

PR #141 added and enforced the machine-readable Evidence contract at registry initialization and added regression coverage. It was merged after review because it was focused and GitHub reported it mergeable.

The repository no longer depends on Vercel or an external project dashboard. GitHub is the authoritative operational source; `README.md` is the public source guide. CI, issues, pull requests, releases, generated reports, and repository files are the evidence surfaces.

## Corpus modernization priority

The current quality distribution makes the remaining 293 stubs the dominant modernization target. Migration is incremental and evidence-driven. Batch 01 merged 10 perception skills and added standards-compatible `SKILL.md` projections plus an automated evidence/security validation gate. No skill is promoted to battle-tested solely because it has been rewritten; reproducible benchmark evidence is required for that claim.

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

## Source of truth

- Canonical source: GitHub repository `SamoTech/skills-tree`.
- Public source guide: `README.md`.
- Operational state: `meta/CURRENT-STATE.md` and GitHub CI/PR state.
- Strategic decisions: `meta/memory/DECISIONS.md`.
- Quality evidence: generated repository reports.
- External dashboards and Vercel deployments are not authoritative and are not part of the project architecture.

## Distribution readiness

- Canonical skill source: `skills/` in GitHub.
- Machine-readable projection: `docs/api/skills.json`, generated from canonical skill content.
- Standards-compatible seed: `agent-skills/skills-tree-registry/SKILL.md`.
- Distribution contract: `docs/AGENT_SKILLS_DISTRIBUTION.md`.
- GitHub raw content is the repository-native machine-readable distribution surface; no external dashboard is authoritative.
- Full `/.well-known/agent-skills/index.json` publication remains a release-engineering task until reproducible artifact generation and SHA-256 verification are implemented.

## Security hardening

- Skill validation is read-only and does not mutate contributor branches.
- Dependabot automation does not auto-approve or auto-merge dependency updates.
- Agent-facing skill instructions are explicitly treated as a supply-chain/security surface.
