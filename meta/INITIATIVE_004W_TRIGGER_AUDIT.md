# INITIATIVE-004W — Phase 1: Workflow Trigger Audit

**Date:** 2026-06-22  
**Source file:** `.github/workflows/build-graph.yml` SHA `d2f4ac36fc0fe57b99b267eb7ce5eadb4be4610c`  
**Evidence basis:** Direct file read only.

---

## Workflow Identity

| Field | Value |
|---|---|
| Name | `Build Dependency Graph` |
| File | `.github/workflows/build-graph.yml` |
| SHA | `d2f4ac36fc0fe57b99b267eb7ce5eadb4be4610c` |

---

## Trigger Configuration

### Push Trigger
```yaml
on:
  push:
    branches: [main]
    paths:
      - 'skills/**/*.md'
```

**Branch filter:** `main` only.  
**Path filter:** `skills/**/*.md` — fires ONLY when a push to `main` modifies at least one file matching this glob. Commits that touch only `tools/`, `meta/`, `schema/`, `data/`, `.github/` do NOT trigger this workflow.

### workflow_dispatch
```yaml
  workflow_dispatch:
```
Supported. No inputs required. Can be triggered via GitHub UI (Actions tab → "Build Dependency Graph" → "Run workflow") or via GitHub REST API with a PAT holding `actions:write` scope.

### Schedule Trigger
**ABSENT.** No `schedule:` block. The workflow never runs on a cron.

---

## Concurrency Configuration

```yaml
concurrency:
  group: build-graph-${{ github.ref }}
  cancel-in-progress: true
```

**Critical property:** `cancel-in-progress: true` means if a new workflow run starts while a previous run (same branch) is in progress, the **previous run is cancelled immediately**. This is the proven root cause of the missing graph rebuild (see Phase 3).

---

## Permissions

```yaml
permissions: {}      # workflow-level: no permissions

jobs:
  build:
    permissions:
      contents: write   # job-level: needed to push graph commit
  secret-scan:
    permissions:
      contents: read
```

**Assessment:** Permissions are correctly scoped. The `build` job has `contents: write` which is the minimum required to commit and push `data/SKILLS_GRAPH.json`.

---

## Build Command

```bash
python tools/build_graph.py \
  --output data/SKILLS_GRAPH.json
```

Command matches `tools/build_graph.py` argparse interface exactly. No mismatch (this was the INITIATIVE-001B bug; it is resolved).

---

## Commit Step

```bash
git add data/SKILLS_GRAPH.json
git diff --staged --quiet && echo "No graph changes." && exit 0
git commit -m "chore(graph): rebuild skills dependency graph [skip ci]"
git push origin main
```

**Note:** The `[skip ci]` tag on the auto-commit prevents the graph commit itself from triggering further workflow runs. This is correct behaviour.

---

## Summary

| Property | Value |
|---|---|
| Triggers on `skills/**/*.md` push to main | YES |
| workflow_dispatch supported | YES |
| Schedule trigger | NO |
| Concurrency cancel-in-progress | YES |
| Contents:write permission | YES (job level) |
| Build command correct | YES |
| [skip ci] on auto-commit | YES |
