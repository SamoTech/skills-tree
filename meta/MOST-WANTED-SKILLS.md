# Most-Wanted Skills — Demand Backlog

> Evidence-backed demand backlog for Skills Tree.
> This file intentionally contains no fabricated popularity ranking.

## Purpose

Identify important AI-agent capabilities that are missing, weakly represented, stale, duplicated, or insufficiently evidenced.

The backlog is a decision-support artifact. It separates observed demand signals from COO prioritization.

## Signal policy

Acceptable signals include:

- dated public GitHub references/search observations
- repository issues and discussions
- public package/ecosystem activity
- framework documentation showing recurring capability requirements
- public Agent Skills/MCP ecosystem activity
- repeated capability requests with traceable provenance
- internal repository dependency/coverage gaps

Do not use private user data. Do not represent search volume as adoption. Do not fabricate demand.

## Record format

For each candidate:

| Field | Requirement |
|---|---|
| Capability | normalized capability name |
| Demand signals | dated public signals and sources |
| Existing coverage | current Skills Tree coverage |
| Quality gap | documented quality deficiency |
| Evidence gap | missing evidence tier or proof |
| Implementation gap | missing/incomplete capability |
| Ecosystem relevance | documented compatibility/relevance |
| Proposed tier | A/B/C/D/E with rationale |
| Priority | transparent COO decision aid |
| Status | proposed/investigating/selected/in-progress/validated/deferred |
| Verified | date of latest verification |

## Initial backlog state

No capability is ranked here until a reproducible public-signal collection pass is performed.

The first implementation task is therefore to build the signal collection and verification path, then populate this backlog from evidence.

**2026-10-04 status:** `tools/collect_demand_signals.py`, `meta/demand-sources.json`, and the scheduled/manual `.github/workflows/demand-signals.yml` now provide the first reproducible public-signal path. The collector produces raw GitHub issue-search evidence only; it does not assign popularity, adoption, or priority. The first production snapshot is intentionally collected as a workflow artifact before being promoted into the curated backlog.

## Priority model

Use:

`Demand × capability importance × coverage gap × evidence gap × ecosystem relevance`

The result is a prioritization aid, not a claim of objective popularity or universal importance.

## Required next steps

1. Define reproducible signal collectors.
2. Record sources and observation dates.
3. Normalize capability names.
4. Compare signals against current registry coverage.
5. Identify quality/evidence gaps.
6. Produce the first verified demand cohort.
7. Convert selected gaps into migration issues/PRs.
8. Recompute when ecosystem evidence changes.
