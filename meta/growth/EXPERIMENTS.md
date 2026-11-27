# Growth Experiments Log

One entry per experiment. Distinguish downloads, visits, stars, and actual adoption.
An experiment is not "successful" until its metric moves against the baseline with evidence.

## EXP-001 — Site technical SEO pass (robots.txt, llms.txt, live-count site_description)

- **Hypothesis:** removing the placeholder analytics config, adding robots.txt + llms.txt, and correcting the site_description count improves crawlability and the accuracy of shared/search snippets.
- **Target audience:** search engines and AI agents discovering the Pages site.
- **Implementation:** PR #720 (merged 19e54718): count-sync patches mkdocs.yml site_description, placeholder GA block removed, docs/robots.txt + docs/llms.txt added, workflow staging + tests.
- **Baseline:** no robots.txt, no site llms.txt, "360+ skills" site_description, placeholder G-XXXXXXXXXX config.
- **Measurement window:** 2026-11-27 onward; next crawl/index spot-check at 7 and 30 days.
- **Results (2026-11-27):** robots.txt + llms.txt verified live on the Pages host; home page serves the 2488 count. Indexing effect not yet measurable.
- **Limitations:** no search-console data; indexing checks are spot checks.
- **Next action:** re-crawl spot-check on 2026-12-04; verify stale "360+" snippets drop out of indexes.

## EXP-002 — Weekly-highlights generator repair (agent-skills layout)

- **Hypothesis:** the README weekly block only ever listed skills from the canonical skills/ layout; counting agent-skills/<name>/SKILL.md touches makes "Most Active Skills" reflect real PR activity, which is more compelling social proof for visitors.
- **Target audience:** first-time README visitors evaluating the project's activity.
- **Implementation:** PR #721 (merged d54af92d): is_skill_file()/skill_display_name()/collect_skill_counts() helpers, 4 tests, README block refreshed to 2026-11-27. PR #722 (merged d3284c5f): same count-sync authority extended to docs/architecture.md.
- **Baseline:** block frozen at 2026-10-26; weekly bot PRs closed unmerged.
- **Measurement window:** next Monday scheduled run (2026-12-01 05:00 UTC) must produce a correct block via the automation PR.
- **Results:** pending the 2026-12-01 run.
- **Limitations:** generator output depends on the weekly PR being merged; merge automation PRs each cycle (recorded in #719).
- **Next action:** verify the 2026-12-01 automation PR content; merge it green.

## EXP-003 — Organic publishing (planned)

- **Hypothesis:** technically useful content (skill discovery walkthrough, agent integration example) on developer platforms drives stars/forks/PyPI installs.
- **Target audience:** AI agent developers, automation engineers.
- **Implementation:** pending; channels evaluated per STRATEGY.md; publishing only through connected, authorized accounts and platform rules.
- **Baseline:** PUBLISHING-LOG.md (currently empty).
- **Measurement window:** to be defined at first publication.
- **Results:** none yet.
- **Limitations:** account access; no paid promotion.
