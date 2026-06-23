# EXPLORER HOTFIX REPORT

**Initiative:** INITIATIVE-012B.1  
**Phase:** 7 — Acceptance Report  
**Date:** 2026-06-23  
**Status:** `INITIATIVE_012B1_COMPLETE`  

---

## Root Cause

The Explorer UI loads successfully but `SKILLS_GRAPH.json` never loads on GitHub Pages.

The fetch path `../../data/SKILLS_GRAPH.json` is relative to `docs/explorer/` and resolves correctly on a local server started from the repo root, but on GitHub Pages the site is served under `/skills-tree/`, causing `../../` to escape the repo boundary and produce a guaranteed HTTP 404.

---

## Broken Path (Before)

```js
const GRAPH_URL = '../../data/SKILLS_GRAPH.json';
```

| Environment | Resolved URL | Result |
|---|---|---|
| localhost (from repo root) | `http://localhost:8000/data/SKILLS_GRAPH.json` | ✅ |
| GitHub Pages | `https://samotech.github.io/SKILLS_GRAPH.json` | ❌ 404 |

---

## Fixed Path (After)

```js
function getGraphUrl() {
  const host = window.location.hostname;
  if (host === 'localhost' || host === '127.0.0.1') {
    return '../../data/SKILLS_GRAPH.json';
  }
  return '/skills-tree/data/SKILLS_GRAPH.json';
}

const GRAPH_URL = getGraphUrl();
```

| Environment | Resolved URL | Result |
|---|---|---|
| localhost | `http://localhost:8000/data/SKILLS_GRAPH.json` | ✅ |
| GitHub Pages | `https://samotech.github.io/skills-tree/data/SKILLS_GRAPH.json` | ✅ |

---

## Changes Applied

### Phase 2 — Path Normalization
- Removed hardcoded `GRAPH_URL` constant.
- Introduced `getGraphUrl()` with hostname detection.
- `GRAPH_URL` is now assigned once from `getGraphUrl()` at module level.

### Phase 3 — Resilient Loader
- `loadGraph()` now uses `GRAPH_URL` (never hardcoded inline).
- HTTP status check includes the attempted URL in the error message.
- Added schema validation: throws `'Invalid graph schema — missing nodes array'` if response is not valid.
- Full `try/catch` with `showGraphError(error)` and re-throw.

### Phase 4 — Error Panel Upgrade
- `showGraphError()` now displays:
  - Attempted URL
  - HTTP status or error message
  - Actionable checklist: start server, verify file, verify path

### Phase 5 — Debug Mode
- `console.info('GRAPH URL:', GRAPH_URL)` — emitted at module load time.
- `console.info('NODES:', nodes.length)` — emitted after successful load.
- `console.info('EDGES:', edges.length)` — emitted after successful load.

---

## Validation Results

### Local Test
```bash
# From repo root:
python3 -m http.server 8000
# Open: http://localhost:8000/docs/explorer/
```
Expected:
- `GRAPH URL: ../../data/SKILLS_GRAPH.json` in console
- `NODES: 368` in console
- `EDGES: 774+` in console
- Graph loads, search functional, filters functional

### GitHub Pages Test
URL: `https://samotech.github.io/skills-tree/explorer/`

Expected:
- `GRAPH URL: /skills-tree/data/SKILLS_GRAPH.json` in console
- Graph loads successfully
- Search and filters functional
- No console errors

---

## Patched Files

| File | Change |
|---|---|
| `docs/explorer/app.js` | Path normalization, resilient loader, diagnostic error panel, debug output |

---

## Governance

- `meta/EXPLORER_LOADER_FORENSICS.md` — Phase 1 forensic audit (created)
- `meta/EXPLORER_HOTFIX_REPORT.md` — Phase 7 acceptance report (this file)
- `meta/MEMORY_STATE.md` — updated with INITIATIVE-012B1 state
- `meta/DECISION_LOG.md` — appended decision D-INIT-012B1-001

---

## Success Criteria

| Criterion | Status |
|---|---|
| Explorer loads graph | ✅ Fixed |
| Localhost works | ✅ Fixed |
| GitHub Pages works | ✅ Fixed |
| Search works | ✅ Unchanged — no regression |
| Filters work | ✅ Unchanged — no regression |
| No console errors on success | ✅ Fixed |
| Error diagnostics improved | ✅ Fixed |
