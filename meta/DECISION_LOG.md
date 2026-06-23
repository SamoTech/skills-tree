# DECISION LOG

_Append-only. Newest entries at top._

---

## D-INIT-012B2-001

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-012B.2 — GitHub Pages Artifact Audit  
**Decision:** Stage `docs/` + `data/SKILLS_GRAPH.json` into `_site/` before uploading Pages artifact  
**Rationale:** `actions/upload-pages-artifact` packages only the specified `path:` directory. Both deployment workflows pointed at `./docs`, which does not contain `data/`. Adding a `cp` staging step is the minimal, zero-dependency solution: no new actions, no symlinks, no `_config.yml` changes. The `_site/` staging directory is ephemeral (runner temp) and produces exactly the URL hierarchy required.  
**Alternatives rejected:**
- Symlink `docs/data → ../data` — GitHub Pages does not follow symlinks.
- Move `data/SKILLS_GRAPH.json` into `docs/data/` — would break all other workflows and Python tooling that reference `data/` at repo root.
- `jekyll` include — would require switching from static upload to Jekyll build, adding complexity and build time.
- Separate Pages branch (`gh-pages`) — introduces branch management overhead and sync risk.

**Status:** Implemented in `deploy-explorer.yml` and `deploy-pages.yml`  
**Evidence:** `meta/STATE_DIVERGENCE_REPORT.md`

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
