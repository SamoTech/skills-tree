# DECISION LOG

_Append-only. Newest entries at top._

---

## D-INIT-012B1-001

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-012B.1 — Explorer Loader Hotfix  
**Decision:** Replace hardcoded `GRAPH_URL` with environment-aware `getGraphUrl()`  
**Rationale:** The hardcoded relative path `../../data/SKILLS_GRAPH.json` resolves correctly on localhost (from repo root) but escapes the GitHub Pages base path `/skills-tree/`, causing an HTTP 404 on every production visit. A hostname check at runtime is the minimal, zero-dependency solution that covers both environments without build-time configuration.  
**Alternatives rejected:**
- Symlink / redirect in `docs/` — fragile, GitHub Pages does not follow symlinks reliably.
- Build-step path replacement — adds tooling complexity for a trivial runtime check.
- `<base href>` in HTML — would affect all relative URLs in the page and introduce unintended side-effects.

**Status:** Implemented in `docs/explorer/app.js`  
**Evidence:** `meta/EXPLORER_LOADER_FORENSICS.md`, `meta/EXPLORER_HOTFIX_REPORT.md`

---

_Previous entries: see git history_
