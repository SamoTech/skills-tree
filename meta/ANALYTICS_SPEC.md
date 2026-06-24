# Analytics Foundation Specification

**Initiative:** INITIATIVE-014A.2 — Phase 4  
**Date:** 2026-06-24  
**Status:** BASELINE DESIGN — Zero-cost, privacy-preserving  

---

## Philosophy

Skills Tree is a static GitHub Pages site. There is no server, no database, and no budget for third-party analytics platforms at this stage. The analytics baseline must be:
- **Zero cost** — no SaaS analytics subscriptions
- **Privacy-preserving** — no PII collection, no IP storage
- **Actionable** — metrics that directly inform roadmap decisions
- **Incrementally upgradable** — can plug in Plausible/Fathom later without architecture change

---

## Tier 1 — GitHub Native (Available Now, Zero Cost)

### Traffic Analytics (GitHub Insights)

Available at `https://github.com/SamoTech/skills-tree/graphs/traffic`

| Metric | What It Tells Us |
|---|---|
| Repository views (14-day window) | Total HN/Reddit referral volume |
| Unique visitors (14-day) | True reach vs repeat visits |
| Referring sites | Which platforms drive traffic |
| Popular content (file views) | Which skill files get direct visits |
| Clone count | Developer intent signal (serious users clone) |

**Baseline action:** Screenshot traffic dashboard on launch day (T+0), T+1, T+3, T+7, T+30. Store in `meta/ANALYTICS_SNAPSHOTS/`.

### Stars / Forks / Watches

| Metric | Target at T+7 | Target at T+30 |
|---|---|---|
| Stars | 100 | 300 |
| Forks | 10 | 40 |
| Watchers | 20 | 60 |

Track via GitHub API: `GET /repos/SamoTech/skills-tree`

### PyPI Downloads

| Metric | Source | Frequency |
|---|---|---|
| Monthly downloads | `pypistats.org/api/packages/skills-tree/recent` | Daily during launch week |
| Version breakdown | pypistats `overall` endpoint | Weekly |

---

## Tier 2 — Explorer Client-Side Events (Low Cost)

Inject a minimal event emitter into `docs/explorer/app.js`. Events are sent to a free-tier endpoint (Cloudflare Worker + KV, or a single R2 bucket append) — or simply accumulated in `sessionStorage` and logged to console for local analysis during early stage.

### Events to Track

| Event | Trigger | Data Payload |
|---|---|---|
| `explorer_load` | Graph loads successfully | `{ nodeCount, edgeCount, loadTimeMs }` |
| `skill_select` | User clicks a node | `{ skillId, category, stability, source: 'click'\|'search'\|'featured'\|'random' }` |
| `search_query` | User types in search box (debounced 500ms) | `{ query, resultCount }` |
| `filter_apply` | User applies a category/stability filter | `{ filterType, filterValue }` |
| `path_select` | User clicks a Popular Path | `{ pathName }` |
| `surprise_me` | User clicks Surprise Me button | `{ selectedSkillId }` |
| `share_click` | User copies a skill share URL | `{ skillId }` |
| `blueprint_generate` | User generates a blueprint | `{ goal, matchedSkillCount }` |

### Implementation (Phase 1 — Console Only)

```javascript
// Paste into app.js — zero external dependencies
function trackEvent(name, data = {}) {
  const event = { event: name, ts: Date.now(), ...data };
  console.info('[ANALYTICS]', JSON.stringify(event));
  // Phase 2: replace console.info with fetch('/api/events', { method: 'POST', body: JSON.stringify(event) })
}
```

---

## Tier 3 — Top Searched Skills (Session Aggregation)

During Explorer sessions, accumulate all `search_query` events into `sessionStorage.searchLog`. On session end (beforeunload), POST the aggregated log to a Cloudflare Worker.

### Expected Top Searches at Launch

Based on the skill taxonomy and HN audience, predicted top 10 queries:
1. `rag`
2. `memory`
3. `react` / `react loop`
4. `tool calling`
5. `multi-agent`
6. `code generation`
7. `web search`
8. `planning`
9. `claude` / `anthropic`
10. `security`

---

## Tier 4 — Most Generated Goals

Blueprint Generator logs each goal selection to `localStorage.blueprintLog` (anonymized — no user ID, just goal string + timestamp).

```javascript
function logBlueprintGeneration(goal) {
  const log = JSON.parse(localStorage.getItem('blueprintLog') || '[]');
  log.push({ goal, ts: Date.now() });
  localStorage.setItem('blueprintLog', JSON.stringify(log.slice(-100))); // cap at 100
}
```

This data is local to each user's browser. For aggregate data, the Cloudflare Worker endpoint in Tier 3 handles remote aggregation.

---

## Tier 5 — Referral Tracking

All launch platform posts include UTM parameters:

| Platform | UTM Source | UTM Medium | UTM Campaign |
|---|---|---|---|
| Show HN | `hackernews` | `social` | `launch-014a2` |
| Reddit r/MachineLearning | `reddit` | `social` | `launch-014a2` |
| Reddit r/LocalLLaMA | `reddit` | `social` | `launch-014a2` |
| LinkedIn | `linkedin` | `social` | `launch-014a2` |
| X / Twitter | `twitter` | `social` | `launch-014a2` |

All links point to: `https://github.com/SamoTech/skills-tree?utm_source=<>&utm_medium=<>&utm_campaign=<>`

GitHub does not expose UTM data in their traffic dashboard, but Cloudflare Analytics (free tier) on the Pages site captures referrer headers.

---

## Dashboard Cadence

| When | Action |
|---|---|
| T-1 (day before launch) | Baseline screenshot: stars=X, clones=Y, traffic=Z |
| T+0 (launch day) | Hourly checks on GitHub traffic + HN comment count |
| T+1 | Full Tier 1 snapshot |
| T+3 | Tier 1 + PyPI download comparison |
| T+7 | Full analytics review → update NORTH_STAR_METRICS.md |
| T+30 | Monthly review → roadmap decision gate |

---

## Analytics Upgrade Path

| Stage | Tool | Cost | When |
|---|---|---|---|
| Now | GitHub Insights + console logs | Free | Launch |
| 100 stars | Cloudflare Pages Analytics | Free | T+7 |
| 500 stars | Plausible.io (self-hosted) | ~$9/mo | T+30 |
| 1000 stars | Custom event pipeline (Cloudflare Worker + D1) | ~$5/mo | T+60 |
