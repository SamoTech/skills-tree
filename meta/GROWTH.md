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
| GitHub topics | 7 (agent, ai, ai-agents, markdown, md, memory-management, skills); re-verified 2026-11-27: unchanged, website URL still unset | GitHub API | thin/weak set; update BLOCKED at connector level (owner action) |
| Name-collision landscape | 169 repositories match "skills-tree" in name | GitHub search API (`skills-tree in:name`), 2026-11-27 | substring match, includes unrelated projects; method: repository search API, first-page verification of SamoTech/skills-tree presence |
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
| E1 | Completing community standards (CoC) + richer repo topics improves first-impression conversion and external contribution rate | All visitors | CoC added; topic set proposed to owner (B1) | 4 stars / 3 forks / 4 open issues | 30 days post-application | PENDING | Re-verified 2026-11-27: topics + website URL NOT yet applied by owner; window has not started; re-measure 30 days after application |

## B5 — Pages technical SEO audit (2026-11-27)

Audit of the live Pages site (samotech.github.io/skills-tree), findings with verification method and limits:

| Item | Finding | Verification |
|---|---|---|
| robots.txt | Live: `User-agent: * / Allow: /` + sitemap reference | fetched from the live site |
| sitemap.xml | Live and fresh (lastmod = deploy date), covers site pages | fetched from the live site |
| Page titles | Subpages follow the clean "Page - Skills Tree" pattern (verified on quickstart, why, installation); homepage stays branded "Skills Tree" (a richer title would duplicate the site-name suffix) | fetched from the live site |
| Meta description | Global site_description present on every page; page-specific descriptions added in the same PR for index / quickstart / why | live fetch + mkdocs.yml |
| Canonical URLs | site_url configured in mkdocs.yml (theme emits canonical links from it); the raw <link> tag could NOT be independently verified: the available page-fetch tooling strips HTML | config-verified, not served-bytes-verified |
| Open Graph / Twitter meta | Theme-generated expectation only; same raw-HTML tooling limit as canonical | tooling-limited, disclosed |
| Structured data | Machine-readable registry surfaces live (skills.json, JSON-LD per skill, llms.txt, /.well-known/agent-skills/index.json); page-level schema.org JSON-LD not present (optional future work) | file/site audit |
| Build reproducibility | mkdocs-material was UNPINNED in deploy-pages.yml; pinned to 9.8.2 (PyPI latest at audit time) so meta/theme behavior is reproducible; CI `mkdocs build --strict` validates | workflow diff + CI |

## Two-track growth (P3, issue #730 plan)

Both tracks are recorded in this file only; there is no separate campaign file.

**Track A — users:** make the first five minutes genuinely useful: quickstart accuracy (B4 verification BLOCKED on a Python runtime in the agent sandbox; recorded, not claimed), Pages technical SEO (B5), machine-readable registry and discovery artifacts (live and freshness-gated), honest benchmark disclosure, organic technical content per platform, directory submissions only where rules permit.

**Track B — contributors:** community-health completeness (CoC added; templates + SECURITY.md live), clear contribution categories in README, batch content-quality contract for reviewers, responsive PR/issue triage (external PR #655 awaiting owner review), good-first-issue labeling when genuine beginner-sized work exists.

Each track feeds the same experiment log and baseline table above; no metric is fabricated and nothing is claimed before it is verified.

## Publishing log

| Date | Channel | Item | Link | Notes |
|---|---|---|---|---|
| — | — | — | — | No publications yet; baseline cycle in progress |

## Blockers

- **B1**: Repository settings (description, website URL, topics, social preview) are not writable via the available GitHub connector. Owner action required; proposed topic list recorded on issue #727.
- **B9 (data)**: GitHub traffic/clones/referrers and Search Console metrics are owner-only. Baseline records what is verifiable; nothing is fabricated.

## Next executable actions

1. Owner: apply proposed repo topics (B1). Re-verified 2026-11-27: still pending.
2. B4: clean-environment verification of the 60-second quick-start path. BLOCKED on a Python runtime in the agent sandbox; recorded as blocked, not executed.
3. B5: Pages technical SEO audit — DONE 2026-11-27 (see B5 section below); residual: page-level JSON-LD structured data not present (optional future work).
4. B6/B7: first organic publications + directory submissions where permitted.
