# Growth Baseline — Verified Measurements

Collected 2026-11-27 (UTC) during the Organic Growth & Discoverability V1 kickoff (issue #719).
Every metric records its source, collection date, measurement window, and limitations.
Never fabricate unavailable analytics; gaps are recorded as gaps.

## Repository (GitHub)

| Metric | Value | Source / window | Limitations |
|---|---|---|---|
| Stars | 4 | GitHub REST search API, 2026-11-27 | point-in-time |
| Forks | 3 | GitHub REST search API, 2026-11-27 | point-in-time |
| Open issues+PRs | 6 | GitHub REST search API, 2026-11-27 | includes PRs |
| Traffic / unique visitors | NOT COLLECTIBLE | traffic API needs owner-scoped auth; not exposed by available tooling | documented gap (owner can export from Insights) |
| Clones | NOT COLLECTIBLE | same as above | documented gap |
| Contributors list | NOT COLLECTIBLE | contributors API blocked from available tooling | documented gap |
| Repo description / topics | 7 topics: agent, ai, ai-agents, markdown, md, memory-management, skills | GitHub REST, 2026-11-27 | under-utilized; update is an owner-admin action (proposed values in #719) |
| Social preview | custom image configured and visually confirmed by owner | owner confirmation, 2026-11 | — |

## Corpus and product

| Metric | Value | Source / window | Limitations |
|---|---|---|---|
| Public skills | 2488 across 17 categories | meta/QUALITY-REPORT.md + SKILLS_GRAPH.json (PR #716 reconciliation) | CI-verified |
| Quality | battle-tested 2422 / enriched 66 / stub 0 / invalid 0 | same | CI-verified |
| Graph | 3877 edges, 0 warnings | same | CI-verified |
| Latest release | v1.116.1 (2026-11-27T01:00Z) | GitHub Releases | zero-touch pipeline |
| PyPI downloads | 101/day, 277/week, 2713/month | pypistats.org API, 2026-11-27 | includes CI mirrors; not unique users |

## Discoverability

| Metric | Value | Source / window | Limitations |
|---|---|---|---|
| Search indexing | site + PyPI indexed (home, quickstart, architecture, why, use-cases, explorer pages) | Bing/Google spot checks via site fetches, 2026-11-27 | point-in-time; stale "360+ skills" string across indexed pages fixed by PR #720 |
| Website | https://samotech.github.io/skills-tree/ (mkdocs-material) | fetched 2026-11-27 | static; robots.txt + llms.txt + sitemap.xml live after PR #720 |
| External mentions / backlinks | not systematically collected | — | collection method pending |
| AI discovery interfaces | root llms.txt, .well-known/agent-skills/index.json, docs/api/skills.json served | fetched 2026-11-27 | formal verification tests pending (backlog) |

## Known gaps that limit measurement

1. Repository traffic/clones/contributors require owner-scoped auth the available tooling does not have.
2. No search-impression data available without site-operator tools (no GSC access configured).
3. PyPI download stats include CI mirrors and cannot be attributed to adoption.
