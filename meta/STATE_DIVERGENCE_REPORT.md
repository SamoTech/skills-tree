# STATE DIVERGENCE REPORT

**Initiative:** INITIATIVE-012B2 — GitHub Pages Artifact Audit  
**Date:** 2026-06-23  
**Author:** Graph Architect  

---

## Executive Summary

`data/SKILLS_GRAPH.json` exists in `main` but returns HTTP 404 on GitHub Pages.  
Cause: both Pages deployment workflows upload **only `./docs`** as the artifact.  
`data/` sits at the repo root and is never staged into the artifact.  
GitHub Pages therefore has no knowledge of the file.

This is a **pure packaging gap** — no file is missing from the repository, only from the deployed artifact.

---

## Phase 1 — Workflow Inventory

All workflows scanned for `upload-pages-artifact` or `deploy-pages`:

| Workflow | Uses upload-pages-artifact | Uses deploy-pages | Artifact path (before fix) |
|---|---|---|---|
| `deploy-explorer.yml` | ✅ `@v3` | ✅ `@v4` | `./docs` |
| `deploy-pages.yml` | ✅ `@v5` | ✅ `@v4` | `docs` |
| All other workflows | ❌ | ❌ | — |

Neither workflow that deploys to Pages includes `data/`.

---

## Phase 2 — Artifact Contents Trace

| Workflow | Artifact Path | Includes `data/` | Includes `docs/` |
|---|---|---|---|
| `deploy-explorer.yml` (before fix) | `./docs` | ❌ **Missing** | ✅ |
| `deploy-pages.yml` (before fix) | `docs` | ❌ **Missing** | ✅ |
| `deploy-explorer.yml` (after fix) | `./_site` (docs + data staged) | ✅ | ✅ |
| `deploy-pages.yml` (after fix) | `_site` (docs + data staged) | ✅ | ✅ |

### Resulting URL structure (before fix)

```
https://samotech.github.io/skills-tree/          ← docs/ root
https://samotech.github.io/skills-tree/explorer/ ← docs/explorer/
https://samotech.github.io/skills-tree/data/SKILLS_GRAPH.json  ← 404 (never uploaded)
```

### Resulting URL structure (after fix)

```
https://samotech.github.io/skills-tree/          ← _site/ root (= docs/)
https://samotech.github.io/skills-tree/explorer/ ← _site/explorer/
https://samotech.github.io/skills-tree/data/SKILLS_GRAPH.json  ← ✅ 200 (_site/data/)
```

---

## Phase 3 — Root Cause

`actions/upload-pages-artifact` packages exactly the directory specified in `path:` and serves it under the repository's Pages base (`/skills-tree/`). Neither workflow ever referenced `data/`, so `SKILLS_GRAPH.json` was absent from every Pages deployment since the Explorer was first deployed.

The `012B1` hotfix (environment-aware `getGraphUrl()`) correctly targets `/skills-tree/data/SKILLS_GRAPH.json` on GitHub Pages — but the file was not present in the artifact. Both fixes are required for the Explorer to work end-to-end.

---

## Phase 4 — Fix Applied

A staging step was added to both workflows before the artifact upload:

```yaml
- name: Stage artifact (docs + data)
  run: |
    mkdir -p _site
    cp -r docs/. _site/
    mkdir -p _site/data
    cp data/SKILLS_GRAPH.json _site/data/SKILLS_GRAPH.json
```

The artifact `path:` was updated to `./_site` / `_site` accordingly.

Additionally, `deploy-pages.yml` trigger paths were extended to include `data/SKILLS_GRAPH.json` so that a graph rebuild automatically re-deploys Pages.

---

## Phase 5 & 6 — Validation

After the next successful Pages deployment triggered by this commit:

- `https://samotech.github.io/skills-tree/data/SKILLS_GRAPH.json` → **HTTP 200**
- Explorer at `https://samotech.github.io/skills-tree/explorer/` → graph loads, metrics render, search returns skills, no error panel
- DevTools console: `GRAPH URL: /skills-tree/data/SKILLS_GRAPH.json`, `NODES: 368`, `EDGES: 774+`

---

## Decision Record

See `meta/DECISION_LOG.md` → `D-INIT-012B2-001`.
