# MEMORY STATE

_Last updated: 2026-06-23_

---

## Active Initiatives

| ID | Name | Status | Owner |
|---|---|---|---|
| INITIATIVE-012B.1 | Explorer Loader Hotfix | ✅ COMPLETE | Graph Architect |

---

## System State

- **Explorer UI:** Operational — graph loads on both localhost and GitHub Pages
- **Path strategy:** `getGraphUrl()` — environment-aware, never hardcoded
- **Graph data:** `data/SKILLS_GRAPH.json`
- **Graph URL (localhost):** `../../data/SKILLS_GRAPH.json`
- **Graph URL (GitHub Pages):** `/skills-tree/data/SKILLS_GRAPH.json`
- **Debug mode:** Active — `console.info` for GRAPH URL, NODES, EDGES on init
- **Error handling:** Resilient loader with HTTP status, attempted URL, and actionable checklist

---

## Completed Initiatives

| ID | Name | Date |
|---|---|---|
| INITIATIVE-012B.1 | Explorer Loader Hotfix | 2026-06-23 |
