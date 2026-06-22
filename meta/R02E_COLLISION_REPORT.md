# R02E_COLLISION_REPORT.md

Mission: R-02E.1 — Collision Audit  
Date: 2026-06-22  
Status: **BLOCKED_BY_COLLISIONS**  
Graph writes: NOT PERFORMED

---

## Audit Scope

This report covers all skill files discovered across 6 enumerated categories:
- 3 categories in `data/SKILLS_GRAPH.json` (confirmed by R-02B): `01-perception`, `04-action-execution`, `05-code`
- 3 categories enumerated by R-02E (not yet written to graph): `11-web`, `12-data`, `13-creative`

Categories 02, 03, 06, 07, 08, 09, 10, 14, 15, 16, 17 are PENDING — not included in this audit scope.

---

## Metrics

| Metric | Value |
|---|---|
| RAW_NODES | 134 |
| UNIQUE_NODES | 133 |
| COLLISION_COUNT | 1 |
| Path collisions | 0 |
| Slug collisions | 1 |
| Categories audited | 6 of 17 |
| Categories pending | 11 |

---

## Collision Table

| Node ID | Path A | Path B | Category A | Category B |
|---|---|---|---|---|
| `skill:web-scraping` | `skills/04-action-execution/web-scraping.md` | `skills/11-web/web-scraping.md` | `04-action-execution` | `11-web` |

---

## Collision Detail

### COLLISION-001: skill:web-scraping

- **ID:** `skill:web-scraping`
- **Slug:** `web-scraping` (derived from filename `web-scraping.md`)
- **Path A:** `skills/04-action-execution/web-scraping.md` (in current graph, SHA `84765e6a...` confirmed by R-02E directory listing)
- **Path B:** `skills/11-web/web-scraping.md` (confirmed by R-02E GitHub API listing, SHA `84765e6a3da93b621c30a9726e22661f2eaa4df5`)
- **Category A:** `04-action-execution`
- **Category B:** `11-web`
- **Type:** Cross-category slug collision — same filename exists in two different category directories
- **Severity:** HIGH — under the current node ID rule (`skill:` + file slug), both files generate the same ID. Adding `11-web` nodes to the graph without resolution would create a duplicate ID.

---

## Severity Assessment

**HIGH** — This collision will cause a graph integrity violation if both files are registered under the same ID. The graph schema requires unique node IDs. One of the following resolutions must be applied before graph writes for `11-web` can proceed.

---

## Recommended Resolution Options

These are options only. No resolution is implemented by this audit mission. A governance decision (Decision Log entry) is required before any action is taken.

### Option A — Category-prefixed ID rule
Change the node ID rule to `skill:{category-prefix}:{slug}` for all new nodes going forward.
- Example: `skill:04:web-scraping` and `skill:11:web-scraping`
- **Downside:** Breaks ID consistency with 85 existing nodes that use unprefixed IDs. Requires a schema migration decision.

### Option B — Disambiguation suffix
Add a suffix to the `11-web` variant only.
- Example: `skill:web-scraping-tool` or `skill:web-scraping-agent`
- **Downside:** Requires renaming the node ID (not the file). Must be documented in Decision Log.
- **Upside:** Minimal disruption to existing 85-node graph.

### Option C — Accept the 04-action-execution version as canonical
Treat `skill:web-scraping` as belonging exclusively to `04-action-execution`. Do not register the `11-web/web-scraping.md` file as a separate node — instead, cross-reference it as an alias or related resource in the README.
- **Downside:** One file is not represented as a graph node.
- **Upside:** Zero schema changes needed.

### Option D — Rename one file in the repository
Rename `skills/11-web/web-scraping.md` to `skills/11-web/web-scraping-workflow.md` (or similar), giving it a unique slug.
- **Downside:** Modifies repository file structure.
- **Upside:** Fully resolves the collision at the source.

---

## Non-Collisions Confirmed

The following high-risk IDs were explicitly checked and found clean:

| Node ID | Categories checked | Result |
|---|---|---|
| `skill:web-search` | 11-web vs 01-perception, 04, 05 | CLEAN — unique to 11-web |
| `skill:dom-inspection` | 11-web vs `skill:url-dom-inspection` in 01-perception | CLEAN — different slugs |
| `skill:form-filling` | 11-web vs `skill:form-fill` in 04-action-execution | CLEAN — different slugs |
| `skill:url-fetching` | 11-web vs `skill:url-navigation` in 04-action-execution | CLEAN — different slugs |
| `skill:sql-execution` | 12-data vs `skill:sql-query-generation` in 05-code | CLEAN — different slugs |
| `skill:embedding-generation` | 12-data vs all others | CLEAN — unique |
| `skill:data-visualization` | 12-data vs all others | CLEAN — unique |
| `skill:social-media-post` | 13-creative vs `skill:social-media-reading` in 01-perception | CLEAN — different slugs |
| `skill:image-gen-prompt` | 13-creative vs `skill:image-understanding` in 01-perception | CLEAN — different slugs |

---

## Traceability

All 134 raw nodes are traceable to verified GitHub API directory listing responses from this session:
- `01-perception`: GitHub API response, R-02B session 2026-06-22
- `04-action-execution`: GitHub API response, R-02B session 2026-06-22
- `05-code`: GitHub API response, R-02B session 2026-06-22
- `11-web`: GitHub API response, R-02E session 2026-06-22 (17 files confirmed)
- `12-data`: GitHub API response, R-02E session 2026-06-22 (18 files confirmed)
- `13-creative`: GitHub API response, R-02E session 2026-06-22 (14 files confirmed)

No synthetic nodes. No estimated nodes. No inferred nodes.

---

## Status

**BLOCKED_BY_COLLISIONS**

Graph writes for `11-web`, `12-data`, and `13-creative` nodes are blocked until COLLISION-001 is resolved via a recorded governance decision.

`12-data` and `13-creative` contain zero collisions and could technically proceed independently. However, the block applies to all R-02E pending nodes until the collision policy is established, to prevent partial writes that assume a resolution that has not yet been decided.
