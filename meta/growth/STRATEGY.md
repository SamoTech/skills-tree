# Growth Strategy — Organic, Zero-Budget

Operates under issue #719 (tracking) and this directory as the persistent memory.
No paid advertising; no fake activity; no unsupported claims. Owner approval is required
for financial expenditure, account creation requiring identity verification, and
anything listed in the campaign's autonomy limits.

## Positioning

"Stop rebuilding AI agent capabilities from scratch." Skills Tree is a public, trusted,
machine-discoverable source of AI skills: versioned, benchmarked, openly evolving.
Claims must match the verified corpus (2488 skills, 17 categories, CI-gated quality).

## Audiences (priority order)

1. AI agent developers building tool-using agents.
2. Software engineers evaluating skill/prompt registries.
3. Open-source contributors (skill authors, reviewers).
4. AI researchers comparing reasoning/agentic patterns.
5. Automation engineers and technical founders.

## Channels

| Channel | Fit | Status |
|---|---|---|
| GitHub itself (README, topics, releases, discussions) | primary; where the audience already is | active |
| DEV Community / Hashnode tutorials | technical walkthroughs; canonical, linkable | pending account check |
| LinkedIn | release announcements, engineering notes | pending account check |
| Reddit (r/LangChain, r/LocalLLaMA, r/AI_Agents) | genuine participation, follow self-promotion rules | pending; strict rules |
| Hacker News (Show HN) | one well-timed Show HN when the story is strong | pending |
| X / Twitter | short demos, release notes | pending account check |
| Awesome lists / directories | submission where the project genuinely qualifies | backlog |
| AI newsletters | only with something genuinely newsworthy | backlog |

Rules: adapt content per platform; never mass-post identical promotional messages;
never purchase engagement or manufacture social proof; document blockers and move on.

## Content plan (first wave)

1. Tutorial: "Discover, inspect, and consume an AI skill from Skills Tree in 60 seconds" (CLI + registry).
2. Architecture note: how the dependency graph and evidence classifications work.
3. Release announcements: only for releases with user-visible improvements.
4. Skill-highlight series drawn from the (now working) weekly highlights.

## 30-day targets — recalibrated against the verified baseline

Original aspirational targets from the campaign brief: 100 stars, 20 forks, 5000 visits,
1000 PyPI downloads, 5 external contributors, 30 publications, zero ad spend.

Recalibration rationale (baseline 2026-11-27): 4 stars, 3 forks, ~2713 PyPI downloads/month,
traffic API not collectible, zero publishing history, no external contributor pipeline yet.
A 100-star month (25x current total) is not achievable organically from a cold start without
fabricating activity; the original list stays the aspirational ceiling, and the committed
targets are:

| Target | Committed 30-day | Aspirational | Rationale |
|---|---|---|---|
| GitHub stars | 10 (2.5x total) | 100 | organic only; content-driven |
| Forks | 6 (2x total) | 20 | follows from skill-authoring onboarding |
| Repository visits | NOT MEASURABLE with current tooling | 5000 | owner must enable/export traffic data |
| PyPI downloads | 3400/month (+25%) | +1000/mo | baseline growth rate unknown; conservative |
| External contributors | 2 | 5 | contribution paths just being repaired |
| Original publications | 8 | 30 | quality over volume; zero budget |
| Ad spend | 0 | 0 | hard rule |

These are objectives, not guarantees. Re-evaluate at day 14 against the dashboard.

## Execution protocol

1. Independent tasks run in parallel; the backlog in issue #719 is the queue.
2. Repository changes follow the standard branch → PR → CI → exact-head squash-merge protocol; no gate is ever weakened.
3. Every claim needs evidence; update DASHBOARD.md and EXPERIMENTS.md in the same cycle.
4. Another agent can continue from this directory plus issue #719 without prior conversation history.
