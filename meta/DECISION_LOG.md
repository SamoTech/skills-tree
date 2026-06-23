# Decision Log

## D-INIT-012B-001 — Explorer V1 Architecture

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-012B  
**Decision:** Vanilla JS selected as frontend stack for Explorer V1.

**Options evaluated:**

| Stack | Bundle | Build | Pages compat | Decision |
|---|---|---|---|---|
| Vanilla JS | ~7KB | None | ✅ Native | ✅ Selected |
| Preact | ~4KB + components | esbuild | Needs CI | Rejected |
| React | ~45KB | CRA/Vite | Needs CI | Rejected |
| Svelte | ~10KB compiled | Vite | Needs CI | Rejected |

**Rationale:** GitHub Pages serves static files. No CI build step required. Zero npm dependencies. Full control over output. Easiest for contributors to modify.

**Reversible:** Yes. Svelte or Preact can replace in Explorer V2 if component complexity warrants it.

---

## D-INIT-012A-001 — Public Launch Foundation

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-012A  
**Decision:** Explorer-first launch strategy over Blueprint Generator or MCP Server.

**Rationale:** Explorer is fully static, reads existing graph, zero operational cost, most immediate viral surface (shareable skill URLs), lowest build cost. Blueprint Generator requires NLP layer. MCP Server requires packaging overhead.

---
