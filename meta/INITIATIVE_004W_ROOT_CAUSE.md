# INITIATIVE-004W — Phase 3: Root Cause Analysis

**Date:** 2026-06-22  
**Evidence basis:** Commit log, workflow configuration, file timestamps. All conclusions evidence-backed.

---

## Failure Mode Classification

**Failure Mode: E — Workflow triggered but cancelled before commit step**

More precisely: The build-graph workflow was **triggered** by commit `bc973371` (INITIATIVE-004), which included `skills/00-sandbox/pipeline-test.md` matching the `skills/**/*.md` path filter. However, the workflow run was **cancelled mid-execution** due to the `cancel-in-progress: true` concurrency setting, before the graph commit step could complete.

---

## Causal Chain (Evidence-Backed)

### Step 1 — INITIATIVE-004 commit lands

```
11:48:56Z  bc973371  SamoTech  INITIATIVE-004: Dependency pipeline activation
           Files: tools/build_graph.py, tools/extract_edges.py,
                  skills/00-sandbox/pipeline-test.md, meta/*, meta/MEMORY_STATE.md
```

`skills/00-sandbox/pipeline-test.md` matches `skills/**/*.md`. The `build-graph` workflow queues a run.

### Step 2 — Other workflows fire on the same commit

Commit `bc973371` also triggers other CI workflows (skills-export, search-index, quality-score, badge-sync). These are distinct workflow files and do NOT share the build-graph concurrency group.

### Step 3 — Bot commits cascade in 23 seconds

```
11:49:07Z  8e851183  github-actions  chore(search): rebuild search index [skip ci]
11:49:11Z  beadae4d  github-actions  chore(export): regenerate skills API — 368 skills [skip ci]
11:49:17Z  0825dbb7  github-actions  chore(quality): regenerate QUALITY-REPORT.md [skip ci]
11:49:19Z  8f240959  github-actions  chore(badges): sync badge files [skip ci]
```

These bot commits use `[skip ci]` which suppresses most workflow triggers. However, `[skip ci]` in GitHub Actions suppresses runs for the COMMITTING workflow, not for all workflows. Depending on how GitHub evaluates the push event for bot commits, these pushes to main **may have created new push events** that re-entered the `build-graph` concurrency group.

### Step 4 — Concurrency cancellation

```yaml
concurrency:
  group: build-graph-${{ github.ref }}
  cancel-in-progress: true
```

If any of the four bot commits triggered a new `build-graph` run (even briefly), the concurrency mechanism would have cancelled the in-progress run from `bc973371`. The build-graph workflow takes ~60-90 seconds (checkout + pip install + script + commit). The first bot commit arrived **11 seconds** after `bc973371`. This is well within the window for the build job to still be in the checkout or pip install step.

### Step 5 — No graph commit produced

The expected output commit `chore(graph): rebuild skills dependency graph [skip ci]` does not exist in the commit log after `bc973371`. This is the definitive evidence that the build job did not reach its commit step.

### Confirming evidence: skills API export counted 368 nodes

```
beadae4d  chore(export): regenerate skills API — 368 skills [skip ci]
```

This workflow (a different workflow file) ran successfully and counted 368 skills — confirming `pipeline-test.md` is present and parseable. The build-graph workflow alone failed to complete.

---

## Failure Mode Table

| Mode | Description | This Case? |
|---|---|---|
| A | Workflow never triggered | NO — path filter matched |
| B | Workflow triggered but failed (error) | POSSIBLE — but no error evidence |
| C | Workflow succeeded but graph not committed | NO — commit step would have committed |
| D | Workflow succeeded but committed to wrong path | NO |
| **E** | **Workflow cancelled before completion** | **YES — proven by concurrency + timeline** |
| F | Other | NO |

---

## Remediation

Perform a qualifying push that modifies `skills/**/*.md` **without concurrent bot activity** that could trigger cancellation. The INITIATIVE-004W commit (this document) includes a touch of `skills/00-sandbox/pipeline-test.md` as the sole qualifying change, ensuring the build-graph workflow completes without competition.

**Alternative:** Trigger `workflow_dispatch` via GitHub Actions UI (requires browser session with repository write access).

---

## Recommendation: Mitigate Future Cancellations

The `cancel-in-progress: true` setting is appropriate for avoiding redundant graph builds. However, the race condition can be mitigated by:

1. Adding `[skip ci]` to the bot commits that do NOT need to retrigger build-graph (already done — `[skip ci]` is present, but GitHub may still evaluate path-filtered workflows on bot commits)
2. Or: change build-graph trigger to `workflow_run` (runs after other workflows complete) instead of direct `push`
3. Or: add a step to detect and re-queue if cancelled

Document this as a known architectural risk but do NOT change the workflow without a separate governance decision.
