# Skills Tree — Growth & Discoverability Program

Authoritative execution board: issue #727 (Organic Growth & Discoverability V1 — mission board).
Repo state source of truth: `meta/CURRENT-STATE.md`. This file records growth strategy, verified baseline, experiments, and publishing evidence. It is maintained like every authoritative document: updated in the same cycle as verified state changes.

## Mandate

Improve the global discoverability, adoption, usability, credibility, and organic growth of Skills Tree through genuine utility. Zero advertising budget. No fabricated metrics, no engagement purchases, no fake accounts, no rank manipulation, no identical mass-posting.

## Verified baseline — 2026-11-27

| Metric | Value | Source | Limitations |
|---|---|---|---|
| GitHub stars | 4 | GitHub API | point-in-time |
| GitHub forks | 3 | GitHub API | point-in-time |
| Open issues (incl. PRs) | 4 | GitHub API | 0 open PRs at audit |
| PyPI downloads | 449 day / 713 week / 3,082 month | pypistats.org | includes mirrors/CI; not unique users |
| Repo traffic / clones / referrers | UNAVAILABLE | GitHub traffic API requires authenticated access not exposed by current tooling | BLOCKED — never fabricated |
| Site | Live, counts current (2488 skills) | samotech.github.io/skills-tree | no on-site analytics (by design) |
| Search indexing | PyPI page, Pages pages (quickstart, architecture, why, explorer), GitHub pages indexed; one third-party mirror detected | web search | impressions/clicks need Search Console (owner-only) |
| GitHub topics | 7 (agent, ai, ai-agents, markdown, md, memory-management, skills) | GitHub API | thin/weak set; update BLOCKED at connector level (owner action) |
| Community health | 7 issue templates + SECURITY.md present; CODE_OF_CONDUCT.md was missing → added in the kickoff PR | file audit | — |
| AI discoverability | llms.txt, docs/AI_DISCOVERY.md, docs/api/skills.json, /.well-known/agent-skills/index.json live | file + site audit | maintained by existing pipelines |

30-day aspirational targets (recalibrate after a full traffic-data window): 100 stars, 20 forks, 5,000 visits, 1,000 PyPI downloads/month, 5 external contributors, 30 original publications. Objectives, not guarantees; optimized for genuine usage.

## Strategy

1. **Discovery surfaces first** (highest leverage, fully in-repo): README conversion, Quick Start, Pages SEO, AI/agent discovery surfaces. Make every visitor path verifiable and fast.
2. **Community credibility**: complete community-health standards so the repository reads as a serious, governed open-source project.
3. **Organic distribution**: original, technically useful English content adapted per platform; directory/Awesome-List submissions only where rules permit; every blocker documented.
4. **Measurement**: experiments logged here with hypothesis/baseline/window/result/limitation/next action; distinguish downloads, visits, stars, and actual adoption.

## Experiment log

| ID | Hypothesis | Target | Implementation | Baseline | Window | Result | Next |
|---|---|---|---|---|---|---|---|
| E1 | Completing community standards (CoC) + richer repo topics improves first-impression conversion and external contribution rate | All visitors | CoC added; topic set proposed to owner (B1) | 4 stars / 3 forks / 4 open issues | 30 days post-application | PENDING | Apply topics (owner), re-measure |

## Publishing log

| Date | Channel | Item | Link | Notes |
|---|---|---|---|---|
| — | — | — | — | No publications yet; baseline cycle in progress |

## Blockers

- **B1**: Repository settings (description, website URL, topics, social preview) are not writable via the available GitHub connector. Owner action required; proposed topic list recorded on issue #727.
- **B9 (data)**: GitHub traffic/clones/referrers and Search Console metrics are owner-only. Baseline records what is verifiable; nothing is fabricated.

## Next executable actions

1. Owner: apply proposed repo topics (B1).
2. B4: clean-environment verification of the 60-second quick-start path.
3. B5: Pages technical SEO audit (titles, meta, canonical, OG, sitemap, robots, structured data).
4. B6/B7: first organic publications + directory submissions where permitted.
