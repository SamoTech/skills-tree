# MEMORY STATE

_Last updated: 2026-06-23_

---

## Active Initiatives

| ID | Name | Status | Owner |
|---|---|---|---|
| INITIATIVE-012B.1 | Explorer Loader Hotfix | ✅ COMPLETE | Graph Architect |
| INITIATIVE-012B.2 | GitHub Pages Artifact Audit | ✅ COMPLETE | Graph Architect |

---

## System State

- **Explorer UI:** Operational — graph loads on both localhost and GitHub Pages (pending next Pages deploy)
- **Path strategy:** `getGraphUrl()` — environment-aware, never hardcoded
- **Graph data:** `data/SKILLS_GRAPH.json`
- **Graph URL (localhost):** `../../data/SKILLS_GRAPH.json`
- **Graph URL (GitHub Pages):** `/skills-tree/data/SKILLS_GRAPH.json`
- **Pages artifact:** `_site/` staging dir containing `docs/` + `data/SKILLS_GRAPH.json`
- **Artifact trigger:** Both `docs/**` and `data/SKILLS_GRAPH.json` changes trigger Pages redeploy
- **Debug mode:** Active — `console.info` for GRAPH URL, NODES, EDGES on init
- **Error handling:** Resilient loader with HTTP status, attempted URL, and actionable checklist

---

## Completed Initiatives

| ID | Name | Date |
|---|---|---|
| INITIATIVE-012B.1 | Explorer Loader Hotfix | 2026-06-23 |
| INITIATIVE-012B.2 | GitHub Pages Artifact Audit | 2026-06-23 |
