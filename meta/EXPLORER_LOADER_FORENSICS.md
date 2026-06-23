# EXPLORER LOADER FORENSICS

**Initiative:** INITIATIVE-012B.1  
**Phase:** 1 — Forensic Audit  
**Date:** 2026-06-23  
**Author:** Graph Architect  

---

## 1. File Audited

`docs/explorer/app.js`  
SHA at audit time: `5966b00bcd19df52b9416365f57fdcff145e5bb4`

---

## 2. Exact Fetch URL (Before Hotfix)

```js
const GRAPH_URL = '../../data/SKILLS_GRAPH.json';
```

This path is **relative to `docs/explorer/`**, so it resolves to:

| Environment | Resolved URL | Status |
|---|---|---|
| `python3 -m http.server 8000` from **repo root** | `http://localhost:8000/data/SKILLS_GRAPH.json` | ✅ Works |
| `python3 -m http.server 8000` from **`docs/`** | `http://localhost:8000/SKILLS_GRAPH.json` | ❌ 404 |
| GitHub Pages `https://samotech.github.io/skills-tree/explorer/` | `https://samotech.github.io/SKILLS_GRAPH.json` | ❌ 404 |

**Root cause confirmed:** GitHub Pages serves the site at `/skills-tree/`, so `../../` climbs above the repo root, causing a guaranteed 404.

---

## 3. Execution Flow (Before Hotfix)

```
DOMContentLoaded
  └── loadGraph()
        ├── fetch('../../data/SKILLS_GRAPH.json')   ← HARDCODED
        ├── if (!res.ok) throw new Error('HTTP ' + res.status)
        │     → res.status = 404 on GitHub Pages
        │     → Error thrown
        └── catch(err)
              └── showError(err)
                    └── grid.innerHTML = 'Failed to load skills graph'  ← VAGUE
```

---

## 4. Error Handling (Before Hotfix)

```js
async function loadGraph() {
  try {
    const res = await fetch(GRAPH_URL);
    if (!res.ok) throw new Error('HTTP ' + res.status);  // no URL in message
    graph = await res.json();
    // no schema validation
    ...
  } catch (err) {
    showError(err);
  }
}

function showError(err) {
  console.error('[Explorer]', err);
  document.getElementById('skill-grid').innerHTML =
    '<div class="empty-state" role="alert">'
    + '<p class="empty-state-title">Failed to load skills graph</p>'
    + '<p>Run: <code>python3 -m http.server</code> from repo root, then open http://localhost:8000/docs/explorer/</p>'
    + '</div>';
  document.getElementById('results-count').textContent = 'Error';
}
```

**Problems identified:**

1. `GRAPH_URL` is a hardcoded relative path — breaks on GitHub Pages.
2. No environment detection — single path cannot serve both contexts.
3. `showError()` does not surface the attempted URL or HTTP status to the user.
4. No JSON schema validation — a malformed response would propagate as a silent TypeError downstream.
5. No `console.info` debug trace for URL or loaded counts.

---

## 5. Stack Trace Source (Before Hotfix)

```
TypeError / NetworkError originating in:
  loadGraph()  →  fetch(GRAPH_URL)  →  HTTP 404
  → caught in catch(err)  →  showError(err)
  → user sees: "Failed to load skills graph" (no URL, no status)
```

On GitHub Pages the browser console would show:
```
GET https://samotech.github.io/SKILLS_GRAPH.json 404 (Not Found)
[Explorer] Error: HTTP 404
```

The user-facing panel provided no actionable information.

---

## 6. Verdict

| Finding | Severity |
|---|---|
| Hardcoded relative path fails on GitHub Pages | P0 Critical |
| No environment detection | P0 Critical |
| Vague error panel — no URL, no status | P1 High |
| No schema validation | P1 High |
| No debug console output | P2 Medium |
