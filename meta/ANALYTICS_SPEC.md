# Analytics Foundation Specification

**Initiative:** INITIATIVE-014A.2 — Phase 4  
**Date:** 2026-06-24  
**Lead Agent:** Analytics Architect  
**Status:** SPEC — Implementation in next cycle  

---

## Philosophy

Zero-infrastructure analytics only. Skills Tree is a static GitHub Pages site with no backend. All analytics must be:
- Client-side only
- Privacy-respecting (no PII)
- Free tier (no paid plans at launch)
- Opt-out friendly

---

## Tier 1 — Immediate (Pre-Launch)

### Tool: Plausible Analytics (community.plausible.io — free self-hosted or $9/mo cloud)

Alternative: **Umami Cloud (free tier)** — recommended for zero-infra setup.

**Events to track:**

| Event | Trigger | Properties |
|-------|---------|------------|
| `explorer_open` | Explorer page load | referrer, source |
| `blueprint_generated` | `selectGoal()` called | goal_id, goal_title |
| `blueprint_shared` | `shareBlueprint()` called | goal_id |
| `blueprint_exported_md` | `exportMarkdown()` called | goal_id |
| `blueprint_exported_json` | `exportJson()` called | goal_id |
| `skill_searched` | Explorer search input (debounced 500ms) | query (no PII) |
| `skill_selected` | Node click in Explorer | skill_id, category |
| `graph_load_success` | Graph fetch completes | node_count, edge_count |
| `graph_load_error` | Fetch fails | error_type, url |

**Implementation snippet (add to each app.js):**
```js
function trackEvent(name, props = {}) {
  if (typeof plausible === 'function') plausible(name, { props });
  if (typeof umami === 'object' && umami.track) umami.track(name, props);
}
```

---

## Tier 2 — Post-Launch (Week 2+)

### GitHub Traffic API
- Use `GET /repos/SamoTech/skills-tree/traffic/views` (requires token)
- Log weekly in `meta/TRAFFIC_LOG.md`
- Track: unique visitors, page views, referring sites, popular content

### GitHub Stars Velocity
- Track daily star count delta using GitHub API
- Log in `meta/STAR_VELOCITY_LOG.md`
- Alert threshold: >50 stars/day = viral event, trigger Show HN follow-up post

---

## North Star Metrics

| Metric | Current | 30-day target | 90-day target |
|--------|---------|--------------|---------------|
| Explorer sessions/month | 0 (no tracking) | 200 | 2,000 |
| Blueprint generations/month | 0 | 150 | 1,500 |
| Most generated goal | unknown | — | top 3 identified |
| Top search query | unknown | — | top 10 identified |
| Share rate | unknown | — | >3% of generations |
| GitHub stars | baseline | +100 | +1,000 |

---

## Privacy Policy

Add to both Explorer and Blueprint Generator pages:
```
This tool uses privacy-respecting analytics (no cookies, no personal data).
```
