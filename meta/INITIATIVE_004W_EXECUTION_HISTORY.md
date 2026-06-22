# INITIATIVE-004W — Phase 2: Execution History Audit

**Date:** 2026-06-22  
**Evidence basis:** `git log` of `main` branch, 20 most recent commits. Workflow run records are not directly readable via available tooling; execution history is inferred from commit evidence (bot commits = successful workflow outputs).

---

## Commit Timeline (chronological, oldest first)

| Timestamp (UTC) | SHA (short) | Actor | Message (truncated) | skills/**/*.md changed? |
|---|---|---|---|---|
| 11:07:22 | `bf886854` | SamoTech | INITIATIVE-001 V3 Refoundation | YES — all skills/ |
| 11:07:39 | `245b47f2` | github-actions | chore(graph): auto-update generated graph artifacts [skip ci] | — |
| 11:09:01 | `38082503` | SamoTech | feat(governance): add INITIATIVE-001 proposal | NO |
| 11:16:26 | `847ae1e2` | SamoTech | fix(ci): align build-graph workflow | NO (`.github/` only) |
| 11:25:24 | `679a60d8` | SamoTech | docs(initiative-001c): graph quality audit | NO (meta/ only) |
| 11:32:35 | `38b9e4b1` | SamoTech | INITIATIVE-002A: Edge Discovery Audit | NO (meta/ only) |
| 11:37:59 | `0f0cfbc9` | SamoTech | INITIATIVE-002B: Dependency model strategy | NO (meta/ only) |
| 11:42:27 | `0a75b586` | SamoTech | INITIATIVE-003: Dependency schema evolution | NO (schema/ + meta/) |
| **11:42:42** | **`71e92bb6`** | **github-actions** | **chore(graph): auto-update generated graph artifacts [skip ci]** | **— (graph output)** |
| 11:48:56 | `bc973371` | SamoTech | **INITIATIVE-004: Dependency pipeline activation** | **YES — skills/00-sandbox/pipeline-test.md** |
| 11:49:07 | `8e851183` | github-actions | chore(search): rebuild search index [skip ci] | — |
| 11:49:11 | `beadae4d` | github-actions | chore(export): regenerate skills API — 368 skills [skip ci] | — |
| 11:49:17 | `0825dbb7` | github-actions | chore(quality): regenerate QUALITY-REPORT.md [skip ci] | — |
| 11:49:19 | `8f240959` | github-actions | chore(badges): sync badge files [skip ci] | — |
| 11:56:12 | `498d05b5` | SamoTech | INITIATIVE-004V: Live graph verification | NO (meta/ only) |

---

## Graph Build Events

| Event | Triggering commit | Graph version committed | SHA |
|---|---|---|---|
| Build 1 | `bf886854` (INITIATIVE-001, 11:07:22) | schema_version 3.0, 367 nodes, 773 edges | `245b47f2` (11:07:39) |
| Build 2 (LAST) | `0a75b586` or prior skills/ commit | schema_version 3.0, 367 nodes, 773 edges | `71e92bb6` (11:42:42) |
| **Build 3 (MISSING)** | `bc973371` (INITIATIVE-004, 11:48:56) — SHOULD HAVE TRIGGERED | **NOT FOUND in commit log** | — |

**Key observations:**

1. `bc973371` committed `skills/00-sandbox/pipeline-test.md` — this matches `skills/**/*.md`. The build-graph workflow **should** have been triggered.
2. Four bot commits followed within 23 seconds (`8e851183` through `8f240959`), all `[skip ci]`.
3. The concurrency group `build-graph-refs/heads/main` with `cancel-in-progress: true` means any of these subsequent workflow runs could have cancelled a build-graph run still in progress.
4. No `chore(graph): rebuild skills dependency graph` commit exists after `bc973371`.
5. The skills API export at `beadae4d` shows **368 skills** — confirming the export workflow ran and counted the pipeline-test fixture. The build-graph workflow did not produce a corresponding graph commit.

---

## Workflow Run Status by Initiative

| Initiative | Triggered build-graph? | Evidence |
|---|---|---|
| INITIATIVE-003 | YES | Graph commit `71e92bb6` at 11:42:42 |
| INITIATIVE-004 | LIKELY CANCELLED | No graph commit found after `bc973371`; four bot commits in 23 seconds; `cancel-in-progress: true` |
| INITIATIVE-004V | NO (correct) | Only touched `meta/` — no `skills/**/*.md` changes |
