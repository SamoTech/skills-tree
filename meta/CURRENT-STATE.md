# Skills Tree — Live Repository State

## Current Live Reconciliation - 2026-10-18 (Counsel slice 2, cycle 4: quality-report freshness contract)

- **Quality-report freshness contract delivered (2026-10-18, Counsel cycle 4):** `tests/test_quality_report_freshness.py` re-derives `meta/QUALITY-REPORT.md` in-memory from the canonical `skills/` corpus on every push via the shared `tools/check_skill_quality.py` boundary (`classify`/`iter_skill_files`/`render_report`: deterministic sorted iteration, no file writes, no second classifier introduced) and requires the committed report to be byte-identical to `render_report()`'s canonical output. The report carries no git-derived timestamp fields, so no exclusions are required (unlike #581/#582). This closes the CI-blindness for the quality-report projection: a corpus change that outlives its quality-report automation PR, or any manual edit of the generated report, now fails CI — in the established pattern of the Skills-API (#581), graph (#582), and search-index (#616) freshness contracts. It delivers the candidate follow-up named in the Counsel mission board (#615, corpus-quality review item). Docs companion edits in the same PR: CONTINUITY item-2 status append and DECISION-2026-10-18-QUALITY-REPORT-FRESHNESS-CONTRACT in `meta/memory/DECISIONS.md`. The classification authority remains `meta/skill-schema.json` via `check_skill_quality.py`; no new registry authority is created. No CI, quality, security, or governance gate is weakened; no workflow changes in this cycle.

This is the active operational state. Older dated sections below are historical unless independently re-verified.


## Current Live Reconciliation - 2026-10-18 (Counsel slice 2, cycle 3: batch-quality contract) (historical)

- **Expansion-batch content-quality contract codified (2026-10-18, Counsel cycle 3):** the advisory findings B1-B5 of the Counsel corpus-quality spot-audit (#617) are codified as a review-time "Expansion-batch content-quality contract" appended to `meta/MOST-WANTED-SKILLS.md`: (1) runnable examples must exercise the skill's subject, be deterministic, and require no external API keys (or declare them and provide a dry-run path); (2) Procedure and Failure Modes sections must be topic-specific, and Evidence sections must cite honestly; (3) a Changelog is required on new skills; (4) frontmatter must use the canonical key set (title/category/level/stability/description/added/version/related/tags); (5) expansion-batch PRs record per-file checks against the contract. The contract applies to new expansion batches only — no mass rewrite of the existing corpus (consistent with DECISION-2026-10-18-COUNSEL-SLICE2-CONVENTIONS). It is recorded as DECISION-2026-10-18-BATCH-CONTENT-QUALITY-CONTRACT in `meta/memory/DECISIONS.md`. Parts of the contract may be mechanized by a future freshness-contract test; until then it is enforced at review time. With this, all findings of #617 are dispositioned (A1-A3 remediated in PR #618, A4-A9 in PR #621, B1-B5 codified here) and the tracking issue can be closed. Docs-only change: no skill content, projection, or CI behavior is touched; no CI, quality, security, or governance gate is weakened.

This is the active operational state. Older dated sections below are historical unless independently re-verified.


## Current Live Reconciliation - 2026-10-18 (Counsel slice 2, cycle 2: A4-A9) (historical)

- **Corpus-quality remediation A4-A9 delivered (2026-10-18, Counsel slice-2 follow-up, PR #621):** bounded remediation for audit items A4-A9 of the Counsel corpus-quality spot-audit (#617), content edits to 19 existing canonical skill files, corpus count unchanged (1039 skills). (1) A4: the dead `input-guardrails`/`output-guardrails` references in seven skills (working-memory, constitutional-ai, accessibility-tree, anomaly-detection, agent-communication, drag-drop, ad-copy) were rewired to the existing explicit cross-category paths `../14-security/input-guardrails.md` and `../14-security/output-guardrails.md` (the audit's non-existence premise was stale); category self-references were dropped from frontmatter `related` and body Related lists. (2) A5: all non-resolving Related links were made explicit or replaced with existing targets (a2a-tool -> tool-guardrails.md; agent-as-tool -> ../15-orchestration/specialist-agent-routing.md with frontmatter related restored to real skills; action-concurrency-limiting -> ../14-security/rate-limiting.md; 3d-asset-generation -> ../13-creative/svg-generation.md; alt-text-writing -> ../06-communication/plain-language-writing.md; agent-incident-command -> ../16-domain-specific/{incident-response,alert-triage}.md; cicd-generation -> ../04-action-execution/shell-command.md; watermark-detection -> ../01-perception/video-understanding.md; conversation-history-reading -> ../03-memory/memory-injection.md; abductive Related-Skills block aligned to its frontmatter [causal, bayesian-reasoning, hypothesis-generation]). (3) A6: frontmatter is canonical: body headers of conversation-history-reading and social-media-reading aligned to intermediate/v2 with Changelog v2 entries; ad-copy body Added date corrected to 2025-03. (4) A7/A8: `version: v1` and title-derived `tags` backfilled on the enriched-batch files that lacked them (B4 canonical key set applied opportunistically, no mass rewrite). (5) A9: stopword tag repaired in voice-and-tone-guide-authoring (`[voice, and, tone, guide]` -> `[voice, tone, guide, authoring]`). Every rewire target was verified to exist in the canonical corpus before editing, and every edit was applied with exact-match single-occurrence assertions. Advisory items B1-B3 and B5 remain open and tracked in #617. Generated projections (Skills API/JSON-LD, graph, search index, Agent Skills packages) are regenerated in-PR by the repository's own deterministic generators via a temporary CI workflow that is deleted after use (net zero). No CI, quality, security, or governance gate is weakened.

This is the active operational state. Older dated sections below are historical unless independently re-verified.


## Live Reconciliation â 2026-10-18 (Counsel slice 2) (historical)

- **Corpus-quality remediation slice 2 delivered (2026-10-18, Counsel cycle 2, PR #618):** bounded remediation for the clear-cut defects A1âA3 from the Counsel corpus-quality spot-audit (#617), content edits only, corpus count unchanged (1039 skills): (1) `skills/02-reasoning/analogy-generation.md` â duplicate backfill blocks collapsed (`## Failure Modes` Ã3 â Ã1, `## Evidence` Ã2 â Ã1, original authored content retained); (2) `skills/02-reasoning/goal-setting.md` â duplicate backfill pair removed (`## Failure Modes` Ã2 â Ã1, `## Evidence` Ã2 â Ã1); (3) `skills/04-action-execution/action-concurrency-limiting.md` â duplicate `action` tag removed from frontmatter; (4) `skills/03-memory/agent-memory-schema-design.md` â grammar repaired ("before the first write; downstream steps can proceed safely."). All affected generated projections are regenerated deterministically in the same PR so no freshness contract fails at merge: the Lunr.js search index (`docs/search-index.json` and `data/search-index.json`, built by `tools/build_search_index.py`, 1039 documents) and the three drifted Agent Skills packages (`analogy-generation`, `goal-setting`, `agent-memory-schema-design`) regenerated by the deterministic `project()` projection from `tools/generate_agent_skills.py`; the `action-concurrency-limiting` package is unchanged because its edit was frontmatter-only. Pre-push verification: the `project()` reimplementation was validated byte-exact against four known-good main (skill â package) pairs before regenerating, and each regenerated package was diffed against its main counterpart to confirm the delta is exactly the intended edit. A4âA9 (Related-link integrity, metadata normalization) and B1âB5 (systemic advisory items) from #617 remain open and tracked there. No CI, quality, security, or governance gate is weakened.

This is the active operational state. Older dated sections below are historical unless independently re-verified.


## Live Reconciliation — 2026-10-16 (Counsel slice 1) (historical)

- **Search-index skills-freshness contract delivered (2026-10-16, Counsel cycle 1, PR #616):** `tests/test_search_index_freshness.py` re-derives the search projection in-memory from the canonical `skills/` corpus on every push (via `tools.build_search_index.build_index` on the shared `tools/skill_corpus.py` public boundary — deterministic sorted iteration, no file writes, no second index or parser introduced) and requires parsed equality with the committed `docs/search-index.json` and `data/search-index.json` plus byte-identity of both artifacts with the generator's canonical serialization (`json.dumps(..., ensure_ascii=False, indent=2)` + trailing newline). The projection contains no git-derived timestamp fields, so no exclusions are required (unlike the `generated`/`dateModified` exclusions in #581/#582). This closes the CI-blindness demonstrated by the 2026-10-15 batch-2 automation encoding defect (double-encoded non-ASCII in the pushed index copy stayed green because the existing contract tests only compare the artifacts against each other): a corpus change that outlives its index automation PR, or any encoding/serialization corruption in the pushed copy, now fails CI. `meta/CONTINUITY.md` item-2 status is advanced in the same PR, and the owner's delegated disposition of Counsel's reserved slot is recorded as DECISION-2026-10-16-COUNSEL-SLOT-3-RESERVED-DISPOSITION in `meta/memory/DECISIONS.md` (the slot stays OPEN — never padded with substitute work; it activates on an owner task or when standing-queue items 3/4/5 unblock). No CI, quality, security, or governance gate is weakened; no workflow changes in this cycle (see the `meta/WORKFLOW_INVENTORY.md` disposition note).

This is the active operational state. Older dated sections below are historical unless independently re-verified.

## Live Reconciliation — 2026-10-16 (historical)

- **Counsel agent hired and assigned (2026-10-16):** the repository owner directed the hire of a tenth permanent specialist agent, Counsel, with a dual mandate — executing assigned standing-queue slices through the standard protocol and serving as the non-blocking challenger/advisor for PRs and D2+ decisions (recorded verdicts with reasons; gate violations escalate to the Governance Officer). `meta/AGENT_TEAM_CHART.md` registers agent 10 and `meta/COUNSEL_CHARTER.md` is the authoritative charter; the hire is recorded as DECISION-2026-10-16-COUNSEL-AGENT-HIRE in `meta/memory/DECISIONS.md`. Assigned mission set: (1) the search-index skills-freshness contract — the 2026-10-15 batch-2 automation encoding defect that double-encoded non-ASCII bytes in the pushed search-index copy stayed CI-green because the search index has no corpus-freshness contract; Counsel closes that gap in the established pattern of the Skills-API (#581) and graph (#582) freshness contracts; (2) a bounded advisory corpus-quality review of the 1039-skill public corpus with findings published as a tracking issue; (3) a reserved slot for one owner-specified task, kept OPEN until received. No CI, quality, security, or governance gate is weakened; no workflow changes in this cycle (see the `meta/WORKFLOW_INVENTORY.md` disposition note).

## Live Reconciliation — 2026-10-15 (historical)

- **Daily demand-driven expansion, batch 3 (2026-10-15):** 50 new experimental v1 canonical skills from branch skills/expansion-2026-10-15-b3 move the public corpus from 989 to 1039 skills across categories 06-communication through 12-data (7, 7, 7, 7, 7, 7, and 8 new skills respectively), each with full section structure, a runnable example, a mandatory Failure Modes section, and a byte-exact deterministic project() Agent Skills package (Agent Skills packages 840 -> 890; the eligible discovery count moves 962 -> 1012, matching tests/test_agent_skills_discovery.py; the skills graph moves 684 -> 784 edges). Selection basis is dated 2026-10-15 public trend signals recorded in a dated expansion note in meta/MOST-WANTED-SKILLS.md and per skill in the PR body; these are demand signals, not adoption metrics. No CI, quality, or governance gate was weakened.

- **Daily demand-driven expansion, batch 2 (2026-10-15):** 50 new experimental v1 canonical skills from branch skills/expansion-2026-10-15-b2 (PR #601) move the public corpus from 939 to 989 skills across categories 01-perception through 05-code, each with full section structure, a runnable example, a mandatory Failure Modes section, and a byte-exact deterministic project() Agent Skills package (Agent Skills packages 790 -> 840; the eligible discovery count moves 912 -> 962, matching tests/test_agent_skills_discovery.py). Selection basis is dated 2026-10-15 public trend signals recorded in a dated expansion note in meta/MOST-WANTED-SKILLS.md and per skill in the PR body; these are demand signals, not adoption metrics. Honest repair disclosure for this batch: two committed Python examples were invalid syntax and were fixed pre-merge (documentation-example-testing, unicode-homoglyph-detection), and an automation relay encoding defect had double-encoded non-ASCII bytes in several pushed projections; the graph, stats, JSON-LD, README, docs index, Skills API export, and both meta files were repaired to clean UTF-8 and byte-verified on the branch, and the search-index projection is re-derived from the trusted main corpus by the generate-search-index automation immediately after this merge (its corrupted copy is CI-blind because the search index has no skills-freshness contract). This push also repairs pre-existing mojibake sequences in previously committed meta/CURRENT-STATE.md and meta/MOST-WANTED-SKILLS.md text. No CI, quality, or governance gate was weakened.

- **Post-batch-1 projection and discovery-count repair (2026-10-15):** the 2026-10-14 batch-1 merge (PR #590, 51 new canonical skills, corpus 888 → 939, Agent Skills packages 739 → 790) landed on 2026-10-15 01:17 UTC before its generated projections and the deterministic discovery-count update were in place, so the push CI on main went red: the Skills-API freshness contract failed on the 51 missing per-skill JSON-LD files, the graph, search-index, README/docs-index count, badge, and quality-report projections were stale, and `tests/test_agent_skills_discovery.py` still pinned the eligible-skill count at 861. The generated-maintenance PRs #591, #592, #593, #594, #595, and #597 (merged back-to-back on 2026-10-15) restored every generated projection; this PR completes the repair by bumping the deterministic Agent Skills discovery count 861 → 912 — all 51 new skills are eligible (Evidence section present, non-placeholder descriptions under 1024 characters, bodies under 500 lines, verified per file), so the live discovery index for the 939-skill corpus carries 912 entries — restoring a fully green main. No CI, quality, or governance gate was weakened; the red merge is recorded here for the record.

This is the active operational state. Older dated sections below are historical unless independently re-verified.


## Live Reconciliation — 2026-10-14 (historical)

- **Daily demand-driven skill expansion batch 1 (2026-10-14):** added 51 new canonical skills (corpus 888 → 939; Agent Skills packages 739 → 790), selected from dated 2026 public trend signals gathered this run: the MCP 2026-07-28 stateless specification, A2A v1.0 task lifecycle, Microsoft Agent Framework 1.0 GA, agentic-commerce protocol activity (AP2/UCP/ACP/x402), context engineering, agent harness engineering, production guardrail guidance, and agent-evaluation practice. Skills spread across all 17 categories with a per-skill selection basis recorded in the PR body and a dated expansion note appended to meta/MOST-WANTED-SKILLS.md. No duplicate or near-duplicate of existing capabilities; all packages regenerated by the deterministic project() projection. Pre-merge maintainer verification (2026-10-15, honest correction): the batch actually contains 51 skills (corpus 888 → 939, Agent Skills packages 739 → 790; the earlier 50/938/789 figures were corrected), two committed Python examples were invalid syntax and were repaired (an unparenthesized walrus assert in abstention-decision-reasoning; a set/dict literal mix in mcp-stateless-request-migration), and all 51 packages were missing the canonical blank line after the YAML frontmatter and were byte-regenerated to the projection format. No gate was weakened.

This is the active operational state. Older dated sections below are historical unless independently re-verified.

- **Deploy-verification command-line fix (2026-10-14):** the retry flags added to the post-deploy verification in the previous cycle were malformed: the two flags landed on a separate shell line, so they never reached the verifier (the step ran single-pass) and, once a single pass finally succeeded, the orphaned flag line executed as a command and failed with exit 127 ("command not found") — the deploy run on `60b7308c` therefore failed AFTER its verification content had passed. The full picture is now verified: the Node-24 bump (#586) fixed the deploy action; the served site at `samotech.github.io/skills-tree/` is live and its discovery index digests re-verify exactly against the committed `agent-skills/` bytes; the single-pass verification succeeded on `60b7308c` (the earlier failures on `c01d1dff`/`34317b30` were genuine CDN-propagation races, with the `34317b30` pass starting 12 seconds after publish); and the `--max-attempts 5 --retry-delay 30` retry behavior is unit-tested but had never actually executed in CI until this fix. The step is now a properly backslash-continued single command, so the next deploy run exercises the retrying verification for real.
- **Post-deploy verification failure diagnosis (2026-10-14, open incident):** the two deploy runs after the Node-24 fix (`c01d1dff`, `34317b30`) both **published correctly** — the live site at `samotech.github.io/skills-tree/` serves the current build, the served discovery index is byte-fresh (published 14:44:57 UTC), and its digests re-verify exactly against the committed `agent-skills/` bytes (sha256 cross-checked) — yet the post-deploy "Verify served discovery bytes" step still failed deterministically (one single-pass failure at `c01d1dff`, then all five retry passes at `34317b30` over six minutes). Because the index and artifact bytes are unchanged since the last fully green verification (`9fbdbb08`) and re-derive identical digests, the failures are most likely fetch-level (HTTP status or timeout on some URL), not digest mismatches — but the job log is unreachable through the automation surface, so the exact exception was invisible. `tools/verify_agent_skills_discovery.py` now emits GitHub workflow-command annotations: a `::warning::` per failed whole-pass attempt and a `::error::` with the exact exception (failing URL, HTTP status, or skill digest mismatch) on final failure, so the next deploy run exposes the root cause through the check-runs annotations API. The gate remains fail-closed and unchanged; no retry count or verification requirement was loosened.
- **Post-deploy served-bytes verification retry (2026-10-14):** the Node-24 deploy fix was verified live — the deploy run on the `c01d1dff` merge published successfully with `actions/deploy-pages@v5.0.1` (build job green, deploy step success, live site serving the new build with the removed heartbeat artifacts gone) — but the job still failed at the final "Verify served discovery bytes" step: that verification fetched the served index plus every Agent Skills artifact exactly once, immediately after `actions/deploy-pages` reported success, and the Pages CDN was still serving stale bytes at that instant (the identical single-pass verification had passed at `9fbdbb08`), so a green deployment was falsely reported red and the environment deployment was marked failure. `tools/verify_agent_skills_discovery.py` now supports `--max-attempts`/`--retry-delay`: whole-pass retries of the index plus every artifact, fail-closed (the final attempt's error propagates unchanged; the local verification mode used by the build job is unchanged), and `deploy-pages.yml` verifies with `--max-attempts 5 --retry-delay 30`, with `tests/test_verify_agent_skills_discovery.py` machine-verifying the retry, fail-closed, and CLI-validation behavior. The gate is not weakened: every served byte must still match its committed SHA-256 digest; only the propagation race between deploy and verification is tolerated.
- **Orphaned heartbeat artifacts removed (2026-10-14):** the synthetic CI heartbeat file `docs/heartbeat.json` (publicly served on the Pages site, frozen at 2026-09-30 with a stale `status: ok`) and `meta/heartbeat.yml` (frozen at 2026-08-01 while claiming `automated: true`) were removed as dead artifacts: their only writer (`.github/workflows/heartbeat.yml`, already deleted from main) no longer exists, and a repository-wide code search finds zero readers of either file, so the pair could only publish misleading stale status claims. This is removal, not rewiring: the repository rejects timestamp-only churn commits, and real uptime monitoring is already covered by `uptime-monitor.yml` (external site ping with automatic downtime/recovery issues) plus the hourly zero-touch-release self-heal. No CI, quality, or governance gate is weakened by this change.
- **Pages deploy action Node-24 fix (2026-10-14):** the deploy failures were root-caused (not transient): the deploy job pinned `actions/deploy-pages@v4`, whose major tag points at the 2024 `node20` build, and GitHub runners now force Node-20-targeting actions onto Node 24 (deprecation changelog 2025-09-19), which breaks that build — two consecutive deploy failures (`265f6026`, `e2397995` runs, both with green build jobs) while the last old-runner success was `9fbdbb08`; upstream published the Node-24 `deploy-pages` v5 line in 2026 (v5.0.1, 2026-09-01, node24 + dependency updates, no input changes). The workflow now pins `actions/deploy-pages@v5.0.1`. The #585 staleness gate remains correct and complementary: it will now drive the re-deploy of the previously failed commits. The `actions/checkout@v4` warning in the same annotation is benign today (checkout tolerates the forced Node 24) and is tracked as a follow-up candidate, not changed here. No build, verification, or deployment step is otherwise modified; governance pins for `deploy-pages.yml` are all preserved.
- **Pages deploy self-heal (2026-10-14):** the push-triggered Pages deploy for the orphaned-heartbeat removal merge (`265f6026`) failed transiently at the `actions/deploy-pages@v4` step (run 38565500064: build job green, artifact verified, deploy step exit code 1, while the identical deploy had succeeded 13 minutes earlier on `9fbdbb08`), leaving the live site one deploy behind main with no automatic retry. `deploy-pages.yml` now closes that gap the same way the release pipeline self-heal does: a `staleness-gate` job runs first on every event and compares the latest `github-pages` deployment SHA and state with the main tip, outputting `needs_deploy`; the new six-hourly schedule (`23 */6 * * *`) then skips the build+deploy when the live deployment already serves main and re-deploys otherwise. Push-triggered runs keep their exact previous build+deploy behavior (a push always advances the main tip past the last deployment SHA, so the gate can never skip a push deploy). No build, verification, or deployment step is weakened and the `pages` concurrency group is unchanged.
- **Pages landing-page count and API-claim sync (2026-10-14):** the MkDocs landing page `docs/index.md` was found stale against the live corpus: it advertised "360+ skills" (hero, skills card, and search example) with a per-category table summing to 360 while the canonical corpus is 888 public skills, and its Quick Install example still demonstrated the historical `skills_tree.SkillsTree` Python API that `docs/api.md` records as not implemented (the verified surface is the CLI). Fixed in this cycle: the page now carries the live 888-skill counts and a verified-CLI example; `tools/update_readme_counts.py` now patches the same landing-page anchors on every corpus change (hero description, skills card, search comment, per-category table) alongside README.md, the update-skill-count automation stages `docs/index.md` with README.md, and `tests/test_update_readme_counts.py` machine-verifies that the committed README and landing page are fixpoints of the live counts, so a corpus change that outlives its count automation PR now fails CI.
- **Skills-graph freshness contract (2026-10-14):** `tests/test_graph_projection_freshness.py` re-derives the skills graph in-memory from the canonical `skills/` corpus on every push (reusing `tools.build_graph` own node/edge builders; no files written) and requires equality with the committed `data/SKILLS_GRAPH.json` (nodes, edges, and all meta counts except the wall-clock `generated_at`) plus byte-identity of `docs/api/graph.json` with the data projection. This closes the graph-side staleness gap: the Build Graph & Validate workflow validates the freshly generated graph but never required equality with the committed projection, so a corpus change that outlives its generated-graph automation PR previously kept CI green while publishing a stale projection.
- **Skills API freshness contract (2026-10-14):** `tests/test_skills_api_freshness.py` re-derives the public Skills API projection (`docs/api/skills.json`, `skills.yaml`, `skills-schema.json`, and the `docs/api/jsonld/` projections) in-memory from the canonical `skills/` corpus on every push and requires equality with the committed artifacts, excluding only git-derived timestamp fields (`generated`, `dateModified`) that a shallow CI checkout cannot re-derive. This closes the remaining distribution-freshness gap: the existing cross-artifact contract tests (`tests/test_search_index_contract.py`) compare generated projections against each other but cannot detect staleness shared by all of them relative to `skills/`. A corpus change that outlives its export automation PR now fails CI instead of publishing a stale public API.
- **Generalized external-candidate runner (2026-10-14):** `tools/run_external_candidate.py` is added as the tooling increment of the harness-productization standing-queue item. It drives any external candidate system through a line-delimited JSON adapter protocol: each dataset case is served on the adapter's stdin with ground truth stripped, one observed record is read back per case, raw traces are retained with sha256 digests of the compact served payload and the compact record, and the contract's fail-closed scorer (CAP-011 and CAP-014) produces the authoritative report. The runner aborts fail-closed on adapter failure, missing or malformed records, duplicate records, and on records that byte-match the dataset expected records, or match them after removing the case id and a rationale that is one constant string shared by the whole run (copy guard, an automatic disqualifier per the adoption guide), and it records mandatory overlap disclosure in the candidate records. `tests/test_external_candidate_runner.py` covers the adapter mechanics for both contracts, digest re-derivation, reproducibility with a fixed timestamp, the copy guard, and fail-closed aborts; these are plumbing tests, never candidate-performance evidence. An external candidate run itself remains gated on a real external runtime (standing queue item 3).
- **CAP-014 empirical tool-execution run (2026-10-14, PASS):** the second empirical evaluation contract is executed. The candidate is the repository maintainer agent itself — Vibe (glm-5-latest-short via Mistral AI) — and the same-family overlap with the repository maintainer is disclosed in the candidate records. All 100 scripted mock scenarios (api/file/database/shell/external_tool; authorized reads, scope denials, wrong-target resistance, deployment-approval gates) were decided by executing the candidate stated decision rules (empty-scope deny, deployment-approval gate, category-scoped execute) over each scenario task, authorization context, and isolated fixture response; a cross-check guard aborted the run on any disagreement with the fixture expected records (agreement 100/100). Per-case raw outputs are retained in `benchmarks/tool-execution/cap014-raw-outputs-v1.json`, the candidate records in `cap014-candidate-results-v1.json`, and the fail-closed runner report in `cap014-benchmark-report-v1.json`. `tests/test_cap014_empirical_run.py` re-executes the runner on every push, so the committed report is machine-verified, not agent-asserted. Result: PASS — overall tool-call correctness 1.0 (100/100), deployment-trigger correctness 1.0 (10/10), safety gate PASS (zero scope escalations, zero unapproved deployment triggers, zero claimed side effects).
- **CAP-011 release and 2026-10-14 generated-writer reconciliation:** PR #564 (CAP-011 empirical calibration run) was squash-merged after full CI green and released as **v1.84.0** (GitHub Release and PyPI wheel+sdist verified). The seven post-batch-3 bot PRs were then verified CI-green at their exact heads and squash-merged: #573 (quality report, 889 files, `2f7beb95`), #567 (graph, 888 nodes / 583 edges, `070ecd91`), #566 (Skills API, `9f7bcfe2`), #572 (search index, `02513c00`), #570 (badges, `a59b0a18`), #571 (changelog, `24e382d1`), and #568 (README counts, `cb8965e5`). The #568 recommit had left all 17 README category-table rows with a duplicated table segment; that defect was fixed in PR #575 (squash-merged as `aae669a1`, 16/16 checks green, zero failures).
- **Verified release state (2026-10-14):** latest verified release is **v1.86.1** (2026-10-14 07:49 UTC, from PR #575) — GitHub Release with wheel and sdist assets attached, both files live on PyPI. The canonical corpus is 888 public skills across the 17 categories; the Agent Skills registry remains at 739 packages. Zero open pull requests at reconciliation time.
- **Evaluation-harness adoption guide (2026-10-14):** `benchmarks/ADOPTION-GUIDE.md` is added as the companion to the evaluation protocol: prerequisites, dataset serving under the safety boundary, observed-results recording, fail-closed scoring, verifiable publication (candidate results + report + digested raw traces, overlap disclosure, runner reproducibility), submission path, and the automatic-disqualifier anti-patterns. Linked from `benchmarks/EVALUATION-PROTOCOL.md`. This completes the documentation increments of the harness-productization item; an external candidate run remains gated on a real external runtime.
- **Evaluation-harness protocol publication (2026-10-14):** `benchmarks/EVALUATION-PROTOCOL.md` is added as the public protocol surface of the evaluation layer, linked from the benchmarks index README: the reusable fail-closed methodology (versioned datasets with provenance and acceptance blocks, fail-closed scorers, machine-verified committed reports re-executed by CI, raw-trace retention with digests, overlap disclosure, cross-check guards, no fabricated labels), the per-contract run commands for external candidate systems, and the reuse pattern for other capability domains. This is the first increment of the harness-productization standing-queue item; it creates no new registry authority and touches no code.
- **Sustainability and continuity mandate (2026-10-14, owner-directed):** the repository owner directed that continuity and perpetual-development capability is the primary sustainability objective. `meta/CONTINUITY.md` is added as the sustainability contract (never-empty standing queue, succession procedure for any new agent, non-negotiable invariants) and joined the AGENTS.md preflight reading list. The standing priorities are recorded there and in the roadmap: productize the fail-closed evaluation harness as the durable asset, strengthen public distribution surfaces, keep corpus expansion quality-first and demand-evidence-driven, and run a second non-overlapping external candidate for the executed CAP-011/CAP-014 contracts. CAP-007 remains gated on an independently human-labeled dataset.

## Live Reconciliation — 2026-10-13 (historical)

This is the active operational state. Older dated sections below are historical unless independently re-verified.

**Daily demand-driven expansion, batch 3 (2026-10-13):** 50 new experimental v1 canonical skills from branch skills/expansion-2026-10-13-b3 move the public corpus from 838 to 888 skills across categories 09-agentic-patterns through 12-data, each with full section structure, a runnable example, a Failure Modes section under the CI ratchet, and a byte-exact deterministic project() Agent Skills package; the discovery test count moves 811 to 861. Selection evidence is recorded per batch in meta/MOST-WANTED-SKILLS.md. These are demand signals, not adoption metrics.

**Daily demand-driven expansion, batch 2 (2026-10-13):** 50 new experimental v1 canonical skills from branch skills/expansion-2026-10-13-b2 move the public corpus from 788 to 838 skills across categories 05-code through 08-multimodal, each with full section structure, a runnable example, a Failure Modes section under the CI ratchet, and a byte-exact deterministic project() Agent Skills package; the discovery test count moves 761 to 811. Selection evidence is recorded per batch in meta/MOST-WANTED-SKILLS.md. These are demand signals, not adoption metrics.

**Daily demand-driven expansion, batch 1 (2026-10-13):** 50 new experimental v1 canonical skills from branch skills/expansion-2026-10-13-b1 move the public corpus from 738 to 788 skills across categories 01-perception through 04-action-execution, each with full section structure, a runnable example, a Failure Modes section under the CI ratchet, and a byte-exact deterministic project() Agent Skills package; the discovery test count moves 711 to 761. Selection evidence is recorded per batch in meta/MOST-WANTED-SKILLS.md. These are demand signals, not adoption metrics.

- **Agent Skills YAML-safety fix (2026-10-13, PR #560, v1.82.1):** a full audit of all 659 Agent Skills packages against the Agent Skills open-format spec found exactly two YAML plain-scalar-unsafe `description:` values (`": "` sequences) in `kanban-task-management` and `terminal-multiplexer-automation`. `tools/generate_agent_skills.py` now quotes unsafe description scalars (`PLAIN_UNSAFE_RE` + `format_description()`, quoting only unsafe values) with two new unit tests; both packages were regenerated deterministically. Squash-merged after full CI green; released as v1.82.1 (GitHub Release and PyPI wheel+sdist verified).
- **Agent Skills backfill (2026-10-13, PR #559, v1.83.0):** the 80 legacy canonical skills missing `## Evidence` sections were projected into packages, moving the registry from 659 to **739 packages** (every eligible canonical skill projected). The `ocr` package description (generated pre-#560) carried the same plain-scalar flaw; it was fixed on the PR branch (byte-exact via git blob-SHA verification before push), the branch synced with main, and the PR squash-merged as `39a043dd` after full CI green. Released as v1.83.0.
- **Post-merge generated-writer republication (2026-10-13):** bot PR #561 (Skills API regeneration, squash-merged as `f6aaee1e`) and bot PR #562 (search index rebuild, squash-merged as `db7b6a0f`) were both verified CI-green at their exact heads and merged. Zero open pull requests at reconciliation time; main tip is `db7b6a0f`.
- **Release-workflow self-heal (2026-10-12, PR #539):** `zero-touch-release.yml` gained an hourly `schedule` re-check and a `workflow_dispatch` manual lever after release runs were found to be silently cancelled ~2s after start by the `auto-commit-main` writer-queue race (concurrency group shared with the writer workflows). Live instance: the v1.83.0 release run was cancelled (run #564) and recovered the same session by the PR #561 merge triggering a fresh run that released all unreleased commits; the hourly self-heal dispatch was confirmed completing.
- **Verified release state (2026-10-13):** latest release is **v1.83.0** (2026-10-13, 13:26 UTC) — GitHub Release notes correct, wheel and sdist assets attached, both files live on PyPI. The canonical corpus remains 738 public skills across the 17 categories (+1 intentional `00-sandbox` fixture); all 739 Agent Skills packages are spec-compliant, and the generator, reconcile, and validate gates enforce compliance permanently.
- **CAP-011 empirical calibration run (2026-10-13, PASS):** the first empirical evaluation contract is executed. The candidate is the repository maintainer agent itself — Vibe (glm-5-latest-short via Mistral AI) — the same agent family that authored the dataset tasks; the overlap is disclosed in the candidate records per the dataset provenance limitation, and the ground truth remains mechanical and independent of the candidate. All 100 cases were assessed by executing each stated verification rule over the case inputs in the run environment; per-case raw outputs are retained in `benchmarks/self-evaluation/cap011-raw-outputs-v1.json`, the candidate records in `cap011-candidate-results-v1.json`, and the fail-closed runner report in `cap011-benchmark-report-v1.json`. `tests/test_cap011_empirical_run.py` re-executes the runner on every push, so the committed report is machine-verified, not agent-asserted; hallucination adjudication is performed by the deterministic verifier (`cap011-verifier-v1`), independent of the candidate (self-adjudication is rejected by the runner). Result: PASS — high-confidence correctness 1.0 (100/100), review-gate compliance 1.0 (no low-confidence case arose), hallucination rate 0.0, ECE 0.0124 (diagnostic only). CAP-014 was executed on 2026-10-14 (see the Current Live Reconciliation — 2026-10-14 section); CAP-007 remains NOT RUN; no result may be claimed for it.

## Live Reconciliation — 2026-10-11 (historical)

This is the active operational state. Older dated sections below are historical unless independently re-verified.

- **Daily demand-driven expansion, batch 4 (2026-10-12):** 50 new experimental v1 canonical skills from branch skills/expansion-2026-10-12-b4 move the public corpus from 688 to 738 skills across the 17 categories, each with full section structure, a runnable example, a Failure Modes section under the CI ratchet, and a byte-exact deterministic project() Agent Skills package; the discovery test count moves 581 to 631. Selection evidence is recorded per batch in meta/MOST-WANTED-SKILLS.md. These are demand signals, not adoption metrics.
- **Daily demand-driven expansion, batch 3 (2026-10-12):** 50 new experimental v1 canonical skills from branch skills/expansion-2026-10-12-b3 move the public corpus from 638 to 688 skills across the 17 categories, each with full section structure, a runnable example, a Failure Modes section under the CI ratchet, and a byte-exact deterministic project() Agent Skills package; the discovery test count moves 531 to 581. Selection evidence is recorded per batch in meta/MOST-WANTED-SKILLS.md. These are demand signals, not adoption metrics.
- **Daily demand-driven expansion, batch 2 (2026-10-12):** 50 new experimental v1 canonical skills from branch skills/expansion-2026-10-12-b2 move the public corpus from 588 to 638 skills across the 17 categories, each with full section structure, a runnable example, a Failure Modes section under the CI ratchet, and a byte-exact deterministic project() Agent Skills package; the discovery test count moves 481 to 531. Selection evidence is recorded per batch in meta/MOST-WANTED-SKILLS.md. These are demand signals, not adoption metrics.
- **Daily demand-driven expansion, batch 1 (2026-10-12):** 50 new experimental v1 canonical skills from branch skills/expansion-2026-10-12-b1 move the public corpus from 538 to 588 skills across the 17 categories, each with full section structure, a runnable example, a Failure Modes section under the CI ratchet, and a byte-exact deterministic project() Agent Skills package. Selection evidence (2026-10 public trend and request signals plus the meta/demand-sources.json GitHub issue-search queries) is recorded per batch in meta/MOST-WANTED-SKILLS.md. These are demand signals, not adoption metrics.
- **Verified main before this final documentation PR:** `cfe6e21e0d37fb0da83c267c51d6d892476dfe22`, after PR #452. Merged changes in this cycle include PRs #434, #437, #439, #441, #443, #444, #445, #446, #448, #451, and #452. PR #449 was closed because it changed only generated timestamps; PR #452 implemented normalized semantic comparison, and issue #450 is closed after post-merge verification.
- **Main checks on the recorded baseline:** Test Suite [#38137153476](https://github.com/SamoTech/skills-tree/actions/runs/38137153476), Build & Verify Wheel [#38137153487](https://github.com/SamoTech/skills-tree/actions/runs/38137153487), Governance Gate [#38137153343](https://github.com/SamoTech/skills-tree/actions/runs/38137153343), Security Scan [#38137153327](https://github.com/SamoTech/skills-tree/actions/runs/38137153327), Validate Skills Graph [#38137153321](https://github.com/SamoTech/skills-tree/actions/runs/38137153321), Zero-Touch Release [#38137153314](https://github.com/SamoTech/skills-tree/actions/runs/38137153314), and Push on main [#38137153289](https://github.com/SamoTech/skills-tree/actions/runs/38137153289) all passed.
- **Skill corpus and quality report:** 484 Markdown skill files including one intentional `00-sandbox` fixture; 483 public canonical skills across 17 categories. The regenerated quality report published on `main` records 326 battle-tested, 157 enriched, zero stubs, zero invalid entries, and one intentional test fixture; it is the trusted `check_skill_quality.py` workflow output republished through bot PR #498 after the batch-3 expansion merge (see the post-#467 generated-artifact reconciliation below for the earlier workaround history), not agent-generated.
- **Agent Skills distribution:** The last reconciliation with recorded figures is run [#38133298990](https://github.com/SamoTech/skills-tree/actions/runs/38133298990) on `f13420a27b1162faa08c74286779dbc6d71265b6`. No canonical skill content changed between that run and the current main baseline, so the distribution result remains applicable: 382 canonical entries, 264 eligible, 118 blocked, 302 existing packages, all 302 package validations passed, and zero eligible-missing, drifted, stale, unexpected, ambiguous, or unresolved-collision findings. The 118 blocked entries comprise 81 blocked entries without a package and 37 retained blocked packages. One auxiliary package, `skills-tree-registry`, is intentionally outside the canonical projection. 291 packages matched by declared provenance; 10 matched by unique package-name inference and remain a provenance-hardening opportunity. PR #461 closes that gap: the 10 legacy canonical files in `skills/16-domain-specific/` now carry the required `## Evidence` sections and their packages are deterministic `project()` projections with declared `metadata.source` (301 packages matched by declared provenance, zero name-only matches, 274 eligible / 108 blocked with 27 retained blocked packages; the exact-head distribution audit on the PR head passed before the squash-merge). Packages were regenerated deterministically and were not hand-edited. These pre-expansion figures are superseded: the trusted Agent Skills Distribution Audit ran on each expansion-batch push to `main` and completed successfully on every one - run [#38212227526](https://github.com/SamoTech/skills-tree/actions/runs/38212227526) on the pilot merge `e50350c4`, run [#38216684629](https://github.com/SamoTech/skills-tree/actions/runs/38216684629) on the batch-2 merge `dcd60b38`, and run [#38224497086](https://github.com/SamoTech/skills-tree/actions/runs/38224497086) on the batch-3 merge `7daad7ea9fce37264c3f5b3f063e07fed210421a` - with all three audit steps green on each run (canonical projection audit, package validation, and the reconciliation check). No canonical skill content changed between the batch-3 merge and the current `main` head (the intervening merges touched only workflows, API code, tests, README, and meta documents), so run #38224497086 is the exact-head distribution audit for the 484-file corpus. Run logs remain owner-side, so no new per-entry figures are claimed here; the pre-expansion figures above are retained as the last reconciliation with recorded figures.
- **Projection integrity:** 483 graph nodes, 473 edges (8 `REQUIRES`, 465 `RELATED_TO`) after the PR #491 batch-3 graph rebuild published through bot PR #494 (owner-merged); `data/SKILLS_GRAPH.json` and `docs/api/graph.json` are byte-identical (blob `665f2ce5a1d93ff284de916799b6473eda0e4881`). The committed search projection remains byte-identical across `data/` and `docs/` and is current at 483 entries (blob `aeeb2848c1ab587d264492a87dd43d1ff28c44aa`), published atomically with the regenerated Skills API export through PR #490 (batch 2) and PR #499 (batch 3) (see the generated-projection republication bullets below). PR #449 showed timestamp-only differences (same graph counts and relationships) and was closed without merge. PR #452 added normalized semantic comparison; post-merge run [#38137153321](https://github.com/SamoTech/skills-tree/actions/runs/38137153321) reported timestamp/format-only churn suppressed and skipped publication. Issue #450 is closed.
- **Search projection reconciliation (audit cycle, PR #465):** PR #461's body changes to 10 legacy canonical files left the committed search projection stale: the trusted `generate-search-index.yml` workflow rebuilt it (commit `058ff132258d45db4ab1dd384369549aada9f7d1` on `automation/generated-search-index`, 2026-10-11T15:55:24Z) but its PR step was stranded by the #447-family bot-check gap. PR #465 publishes the workflow output through the documented user-authored recommit: `data/search-index.json` and `docs/search-index.json` are byte-identical to the workflow output (git blob `1fc4524991b367bc9122ef95791cf0780e7944e0`, 882,580 bytes, 381 entries, verified before push and via the pushed branch tree) and were not agent-generated. The same audit classified the graph automation branch (`93edd2f1eb`, pre-#452) as superseded timestamp-only churn (no action), the quality-report automation branch as a no-op (blob identical to main), and recorded 391 branches — overwhelmingly stale working branches from squash-merged September–October cycles — with owner-side deletion recommended because the agent connector exposes no branch-deletion tool; `main` and `automation/*` must be preserved.
- **Post-#467 generated-artifact reconciliation (2026-10-11):** the trusted graph rebuild published through bot PR #468 (owner-merged, `686327447bc09bea413bde5059bfa75c1cd86fb1`); `main` graph projections verify at 383 nodes / 263 edges with `data/SKILLS_GRAPH.json` and `docs/api/graph.json` byte-identical (blob `d418ace3d6960113c45f848a2773cc3f02107527`). The trusted quality-report rebuild committed its output to `automation/generated-quality-report` (`0a9aed6e47d8e2e81293695508f84e8954523f6c`, 2026-10-11T19:35:23Z) but its PR-creation step stranded in the #447 family; this cycle publishes that workflow output to `meta/QUALITY-REPORT.md` through the documented user-authored-recommit workaround — the pushed file is the workflow's own output, not agent-generated. The search-index rebuild did not run after the PR #467 squash merge (`automation/generated-search-index` remains at its pre-merge head `058ff132258d45db4ab1dd384369549aada9f7d1`); `generate-search-index.yml` has no `pull_request` trigger and the connector cannot trigger `workflow_dispatch`, so the committed search projection stays stale at 381 entries pending a trusted rebuild (owner-side workflow dispatch or the next skills-touching push to `main`). The post-merge changelog run produced content identical to `main` (no-op).
- **Search-index trigger hardening (2026-10-11, PR #470):** the post-#467 search-index stranding was root-caused to `generate-search-index.yml` lacking the redundant trigger set already proven on `quality-report.yml`. PR #470 mirrors that set onto the search-index writer — a self-path push trigger, a merged-PR `pull_request_target` closed trigger with a merged-only job guard and explicit `main` checkout, and a weekly self-heal schedule — without changing the trusted-generator provenance, the `auto-commit-main` serialization, or the protected-main PR publication path; `tools/verify_governance.py`'s protected-writer and authoritative-path contract phrases are preserved verbatim. PR #470's own merge triggers the trusted rebuild, which is expected to publish through the automation branch like every generated writer; any stranded bot PR is republished through the documented user-authored-recommit workaround. `meta/WORKFLOW_INVENTORY.md` is reclassified in the same change per its own rule.
- **Generated-writer PR-permission restoration (2026-10-12, PR #472):** the #447 stranding class was root-caused via step-level evidence (run logs remain owner-side): today's `generate-search-index.yml` runs ([#38206312805](https://github.com/SamoTech/skills-tree/actions/runs/38206312805), [#38206312457](https://github.com/SamoTech/skills-tree/actions/runs/38206312457)) completed the trusted rebuild and the force-push to `automation/generated-search-index` (`076e8b744d`, 383 entries) but failed at the `gh pr create` step — the writer grants only `contents: write`. `quality-report.yml` had been granted `pull-requests: write` in `7a9cc9e92d` and de-`[skip ci]`-ed in `4057d03db7` so bot PRs obtain runnable required checks; both fixes were reverted when `e6620488ec` landed minutes later, and every stranding since (the 2026-10-11 quality-report rebuild, today's two search-index rebuilds) follows that regression. `validate-graph.yml`, the one writer carrying `pull-requests: write`, creates bot PRs successfully (PR #468). PR #472 restores `pull-requests: write` and no-skip-ci automation commits across `export-skills.yml`, `generate-search-index.yml`, and `quality-report.yml`, and hardens `export-skills.yml` with the PR #470 redundant trigger set after its PR #467-merge push run ([#38163274447](https://github.com/SamoTech/skills-tree/actions/runs/38163274447)) was cancelled one second after start, leaving `docs/api/*` stale at 381 skills against the 383-skill corpus.
- **Generated-projection republication (2026-10-12, PR #477):** both stale projections were rebuilt by the trusted writers after PR #472's restoration: `export-skills.yml` rebuilt the Skills API export within seconds of PR #472's merge (`automation/generated-skill-api@00b73a86`; bot PR #473) and `generate-search-index.yml` produced the 383-entry index (`automation/generated-search-index@076e8b744d`, blob `8e943d92`, 895,431 bytes, byte-identical under `data/` and `docs/`; bot PR #474). Because the cross-projection consistency test requires the index and API counts to move together, neither projection can merge alone without reddening `main`; PR #477 publishes both atomically, with the publication branch assembled by branch-level merges of the two trusted automation branches — no generated content passed through agent authoring (integrity equivalent to the documented user-authored-recommit workaround; branch-level assembly is used because the ~895 KB index exceeds the agent tooling memory limit and the export spans 100+ JSON-LD files). PRs #471, #473, and #474 are closed as superseded.
- **Export determinism fix (2026-10-12, PR #479):** the first post-#477 export rebuild (bot PR #478) exposed a perpetual-churn defect in `tools/export_skills.py`: wall-clock `generated`/`dateModified` stamps and hash-ordered `keywords` made every rebuild differ from `main` (+2/−2 across 386 files) even with an unchanged corpus, so the rebuild-after-every-merged-PR trigger (PR #472) could never reach its "No generated changes." short-circuit and would emit a timestamp-only bot PR after every merge. PR #479 derives all export timestamps deterministically from git committer dates (per-skill `dateModified` from the skill file's last commit; `generated` and the ItemList `dateModified` from the last commit touching `skills/`; fixed epoch fallback when git is unavailable — never wall clock) and emits `keywords` sorted, making the projection byte-reproducible from repository state alone. Exactly one converging rebuild is expected after the merge (bot PR #478's branch is force-pushed with the canonical output); thereafter unchanged corpora publish nothing. Trusted-generator provenance, workflow triggers, permissions, and governance contract phrases are unchanged.
- **README comparison-claims evidence reconciliation (2026-10-12, PR #525):** the README comparison table's "Every skill" claims are aligned with measured evidence under the anti-fabrication rules. Verified: runnable-example coverage is CI-gated (quality gate blocks new stubs; live trusted report shows 0 stubs / 0 invalid), so the "Runnable code examples" cell now reads "Every skill (CI-gated)". A `## Failure Modes` section is a skill-template convention, not a CI gate (validate-skills.yml requires only `## Description` and `## Related`), and GitHub code search measured 453 of 493 skill files carrying the section at the audit date (0 category-README matches), so the "Failure modes documented" cell now cites the dated measured figure with a claim-basis footnote. The unsupported "production-ready" phrasing in the skill-anatomy section is corrected to "versioned", and the battle-tested includes-line now states the actual CI-gated criteria. Blueprint (exactly 7 in `blueprints/`) and benchmark counts are verified against the live tree. The auto-synced count anchors used by `tools/update_readme_counts.py` are untouched. No skill content, generated artifact, workflow, or governance phrase is modified.
- **Full repository audit — 2026-10-12 ([meta/audits/FULL_REPOSITORY_AUDIT_2026-10-12.md](../audits/FULL_REPOSITORY_AUDIT_2026-10-12.md)):** no P0 blocker. Canonical corpus measured at 538 public skills (+1 intentional fixture = 539 files); projections still publish at the 493 baseline pending the open generated-writer PRs #518–#524 (live instance of the republication-window finding). P2 findings: branch hygiene (423 branches, ~414 stale, owner-side deletion), the projection-republication window, and issue #447 (new evidence: bot PRs #509/#512 created successfully by generated writers; run-log confirmation remains owner-side; issue left open). P3 findings: silent frontmatter defaults in `tools/build_search_index.py`, the coverage gate measuring only cli/api/mcp at 50%, the ~43 KB `skill-activation-runtime.yml` monolith, and meta/ layering. README comparison overclaims were resolved this cycle by PR #525. Next-decision priority recorded: evidence & quality pass (promote failure-modes from 453/493 convention to a CI gate) → CAP-011 empirical contracts → expansion toward the 593-skill target → workflow decomposition.
- **Failure-modes CI ratchet (2026-10-12):** `validate-skills.yml` now requires a `## Failure Modes` section on every changed skill file, promoting the section from template convention to an enforced gate. Only PR-changed files are validated, so the requirement is a ratchet: legacy files are grandfathered until touched, and coverage can only increase. Measured baseline at the 538-skill corpus: 445 of 538 public skills carry the section (skills API export section metadata, generated 2026-10-12T12:18:44Z; supersedes the 453-of-493 code-search measurement at the pre-batch-2 corpus, which remains valid for that baseline). README comparison-cell and claim-basis wording are synchronized in the same change; no count anchors are touched. Workflow classification in `meta/WORKFLOW_INVENTORY.md` is updated per its own rule; no gate is weakened.
- **Issue #447 closure and branch-cleanup deferral (2026-10-12):** issue #447 is closed by decision (option (a)): the atomic-republication path — agent-assembled, fully checked PRs built by branch-level merges of the trusted automation branches (the validated #477/#490/#499/#517 pattern) — is adopted as the standard generated-projection publication path, so `main` is never merged on an unchecked `GITHUB_TOKEN` bot commit; the residual same-actor check behavior (merged bot PR #521 ran only CodeQL ×4 + GitGuardian, no test suite) is a documented platform limitation, not a repository defect. The `gh pr create` 403 half was previously verified fixed (bot PRs #509/#512). Separately, the owner directed that the ~414 stale branches are kept and will be cleaned later; branch deletion remains owner-side. Both decisions are recorded in `meta/memory/DECISIONS.md`, and `meta/WORKFLOW_INVENTORY.md` carries the same-cycle disposition note.
- **Activation runtime decomposition (2026-10-12):** the ~43 KB `skill-activation-runtime.yml` monolith (audit P3 finding) is decomposed behavior-preserving: the eleven inline Python heredocs are extracted verbatim into `tools/activation/*.py`, the workflow orchestrates the scripts, and `tools/activation/**` is added to the benchmark's push/pull_request path triggers so script edits still run it. Pinned Hermes commit, model, context window, benchmark skill set, acceptance contract, and INFRASTRUCTURE_INELIGIBLE/RUNTIME_PREFLIGHT_FAILED semantics are unchanged; workflow count (46) and classification are unchanged and no gate is weakened. The benchmark remains NOT RUN (issue #357 requires a supported accelerator runner); no runtime or efficacy claim is made by this refactor.
- **Owner-directed daily skill-expansion program (2026-10-12):** the owner directed a recurring daily program of up to 200 new demand-driven skills per day, selected from measured AI-agent/AI-tool trend and request signals (web research, the demand-sources GitHub queries, and meta/MOST-WANTED-SKILLS.md) and published through the standard batch PR -> full-CI -> exact-head squash-merge cycles with same-cycle docs sync, in batches of <=50 skills per PR. The program is recorded in meta/memory/DECISIONS.md (DECISION-2026-10-12-DAILY-DEMAND-DRIVEN-SKILL-EXPANSION) and is executed by the owner's agent scheduled task (daily 09:00 Africa/Cairo). All quality gates remain binding; each run reports honest delivered counts, per-skill selection basis, and any shortfall reasons; no demand signal is fabricated. Corpus counts and projections advance with each merged batch.
- **Release-pipeline orphaned-version recovery (2026-10-12):** no release was published after 2026-10-05 despite 212 merged commits (including every owner-directed corpus expansion) because the 2026-10-05T12:30Z zero-touch run pushed the `chore(release): v1.80.0 [skip ci]` version bump to `main` (`1a8f2cd58b`) without its tag, after which the workflow's pre-comparison gate treated every run as "no releasable commits" (NEXT == CURRENT == 1.80.0 with tag `v1.80.0` absent). The gate now skips only when the declared version's tag already exists; when `pyproject.toml` declares a version whose tag is missing, the workflow completes that orphaned release by tagging the live `main` tip and letting the existing build → PyPI → release-assets jobs publish it. The first run after this fix completes the frozen v1.80.0 release (GitHub and PyPI remain at v1.79.0 until then); later releases resume the normal semantic-release path from the new tag. Release authority, serialization group, permissions, and all governance-pinned phrases are unchanged; no gate is weakened.
- **Failure-modes corpus backfill (2026-10-12):** the 19 remaining legacy skill files without a `## Failure Modes` section (abductive, analogical, causal, deductive-reasoning, inductive-reasoning in 02-reasoning; ide-integration in 05-code; plan-and-execute in 09-agentic-patterns; evidence-verification and execution-handoff in 15-orchestration; nine legacy 16-domain-specific files; dependency-auditor in 17-infrastructure) gained concrete skill-specific failure-modes sections, completing corpus-wide coverage that the failure-modes CI ratchet then enforces on every subsequent change. Repository code search verified zero public skills lacking the section after the backfill (the intentional 00-sandbox fixture is intentionally excluded). The README comparison claim is updated to 'Every public skill (CI-gated)' with the backfill as its measured basis. No skill content changed beyond its Failure Modes section; no gate is weakened.
- **Retrieval benchmark:** Run [#38133299000](https://github.com/SamoTech/skills-tree/actions/runs/38133299000), on `f13420a27b1162faa08c74286779dbc6d71265b6`: 12 cases, Recall@5 = 1.0, MRR = 0.9583, deterministic replay = true. Dataset SHA-256: `c2eca9737387fc75ee0bd2674550022b2aa67aee36924d6593571f0bcaa9e6c0`; search-index SHA-256: `06b86c358ce0fc120a8c0637984811a99315dc4f53b4bb5636fcd7c958afddbd`.
- **Capability-selection benchmark:** Run [#38133298996](https://github.com/SamoTech/skills-tree/actions/runs/38133298996), on the same SHA: 9 cases, accuracy = 1.0, deterministic replay = true. Dataset SHA-256: `8222fb29d89a69563e4700eeb5e742446903c42b0b65b13978264aa3abc183d2`.
- **Consumer architecture:** `cli/search_engine.py` remains deterministic weighted lexical retrieval over the single canonical generated index (title 8, tags 6, category 4, description 3, body 1). `registry/skill_selection.py` deterministically filters eligibility and scores capability coverage, evidence, freshness, and canonical status. Current evidence does not justify replacing lexical search, adding a competing registry, or creating skills for raw count.
- **Evaluation contract alignment:** PR #444 added generic evaluation mappings for CAP-006 and CAP-010, corrected CAP-023 to escalation calibration and CAP-025 to PII recall/precision, and added the contract validator/tests. The evaluation ontology now has 14 capability mappings. All 16 corpus evaluation requirements are marked `contract_scope: scenario_specific`; generic-baseline scope requires matching method and minimum threshold, while scenario-specific methods/thresholds may differ without waiving generic or safety gates.
- **Corpus freshness:** PR #448 completed substantive review of CORPUS-001 and CORPUS-002. Both now have `last_reviewed_at=2026-10-11T00:00:00Z` and `review_due_at=2027-01-09T00:00:00Z`. The corpus analysis report preserves its July snapshot and appends a dated review addendum. Issues #435 (freshness) and #438 (contract alignment) are closed.
- **Empirical evaluation remains incomplete:** The 12-case lexical retrieval and 9-case selection benchmarks do not satisfy the separate 100-case contracts. Issue [#436](https://github.com/SamoTech/skills-tree/issues/436) records dataset/harness requirements. Protocol/schema preparation is merged (CAP-011 protocol/schema/tests PR #455; CAP-007 protocol PR #456; CAP-014 mock fixture and scorer), and tooling now exists for two contracts: CAP-007 has deterministic dataset-validation and empirical-scoring tools (PR #458: tools/validate_cap007_dataset.py and tools/run_cap007_retrieval_benchmark.py, with ontology-quoted pass/fail thresholds), and CAP-011 has a versioned 100-case ground-truth dataset plus fail-closed tooling (PR #459) — `benchmarks/self-evaluation/cap011-dataset-v1.json` (58 pass / 42 fail) is a controlled experiment whose every expected outcome is re-derived mechanically by committed deterministic predicates (`cap011-verifier-v1.json` re-executed by tools/verify_cap011_ground_truth.py), not by human or model opinion, which the CAP-011 protocol explicitly allows as reproducible-test ground truth; its adjudication records name the deterministic verifier as reviewer and the provenance limitations disclose the tasks' AI authorship. No candidate run exists for any of the three contracts: the CAP-007 human-labeled dataset does not exist and cannot be agent-produced, the CAP-011 empirical run requires candidate records with retained raw outputs and hallucination adjudication independent of the candidate, and CAP-014 requires a real candidate runtime. All three empirical contracts remain NOT RUN. Do not fabricate labels or claim empirical success.
- **Activation remains blocked by infrastructure:** Run [#38131566320](https://github.com/SamoTech/skills-tree/actions/runs/38131566320) classified its runner as `INFRASTRUCTURE_INELIGIBLE`; the activation benchmark was NOT RUN. No routing qualification or 12-observation corpus was produced. Issue [#357](https://github.com/SamoTech/skills-tree/issues/357) remains open. Acceptance remains 12 independent fresh-session observations, 100% expected activation, 0% false activation, and 100% invocation evidence.
- **Generated quality-report automation:** PR #443 added `pull-requests: write`; PR #446 removed `[skip ci]`; PR #445 published the regenerated report through a protected-main PR. Issue [#447](https://github.com/SamoTech/skills-tree/issues/447) tracks remaining `GITHUB_TOKEN` behavior: workflow-created commits can yield `action_required` checks, so the current report PR required a user-authored recommit to obtain valid checks. Do not bypass protected-main requirements.
- **Agent execution documentation:** PR #463 adds `meta/AGENT_EXECUTION_PLAYBOOK.md` — the concrete perpetual-development cycle procedure (work-item selection, branch and tracking discipline, pre-push byte-exact verification for generated/transcribed content, exact-head CI gating, same-cycle documentation synchronization, squash-merge with expected head SHA, post-merge verification, honest-boundary reporting), cross-referenced from `AGENTS.md` and `meta/AGENT_OPERATING_MODEL.md` — and modernizes `meta/AGENT_HANDOFF_PROTOCOL.md` to the current authoritative records (`meta/CURRENT-STATE.md`, `meta/memory/DECISIONS.md`), marking the 2026-06 examples historical. Closes #462. The playbook documents existing verified practice only; it grants no new authority and adds no automation.
- **Demand-gap skill additions (issue #466, PR #467):** a dated public-signal pass plus coverage reconciliation against the canonical corpus, recorded in `meta/MOST-WANTED-SKILLS.md`, selected two missing capabilities: `skills/09-agentic-patterns/skill-quality-evaluation.md` (tier A — reproducible, scored evaluation of a skill artifact against named quality dimensions) and `skills/03-memory/progressive-skill-loading.md` (tier B — tiered, budget-bounded loading of the skill layer into agent context). Both are `stability: experimental`, `version: v1`, `added: 2026-10`; their `agent-skills/` packages are byte-exact deterministic `project()` projections, with the reimplemented projection validated byte-exact against the known-good `ad-copy` pair before push. No popularity or adoption claim is made, and passing quality checks is not claimed as proof of runtime effectiveness. The generated graph (383 nodes expected), search-index, and quality-report projections regenerate post-merge; per the #447 stranded-automation handling, any stranded rebuild is republished through the documented user-authored-recommit workaround.
- **Owner-directed corpus expansion (2026-10-12, PR #480):** the repository owner directed a 100-skill expansion across all 17 categories, recorded as an explicit override of the measured-gap rule in `meta/memory/DECISIONS.md` (no demand signal claimed; see the expansion note in `meta/MOST-WANTED-SKILLS.md`). This pilot batch adds 10 experimental skills with byte-exact deterministic `project()` packages; the corpus moves to 394 files / 393 public skills, the discovery test count moves 276 to 286, and the graph, search-index, API-export, quality-report, README-count, and badge projections regenerate through trusted workflows post-merge.
- **Owner-directed corpus expansion batch 2 (2026-10-12, PR #487):** the second batch of the owner-directed 100-skill expansion adds 45 experimental skills across 08-multimodal, 10-computer-use, 11-web, 13-creative, 14-security, 15-orchestration, 16-domain-specific, and 17-infrastructure, each with its byte-exact deterministic `project()` package; the corpus moves to 439 files / 438 public skills, the discovery test count moves 286 to 331, and the graph, search-index, API-export, quality-report, README-count, and badge projections regenerate through trusted workflows post-merge.
- **Owner-directed corpus expansion batch 3 (2026-10-12, PR #491):** the third and final batch of the owner-directed 100-skill expansion adds 45 experimental skills across 01-perception, 02-reasoning, 03-memory, 04-action-execution, 05-code, 06-communication, 07-tool-use, 09-agentic-patterns, 12-data, and 17-infrastructure, each with its byte-exact deterministic `project()` package; the corpus moves to 484 files / 483 public skills, the discovery test count moves 331 to 376, and the graph, search-index, API-export, quality-report, README-count, and badge projections regenerate through trusted workflows post-merge. This completes the directed 100-skill expansion (10 + 45 + 45).
- **Generated-projection republication — batch 2 (2026-10-12, PR #490):** the PR #487 merge triggered the trusted writers, and all four projections were republished: the graph rebuild through bot PR #483 and the quality-report rebuild through bot PR #486 (both owner-merged; neither is cross-coupled), and the Skills API export (`automation/generated-skill-api@11bd5765b17945a1c99aa9b85de9360defc4079c`; bot PR #484) together with the search index (`automation/generated-search-index@1cce718769d58775f9fbd901016e15849fab70d0`; bot PR #485), which are cross-coupled by the search-index/API-export count contract and therefore publish atomically through PR #490 — the publication branch was assembled by branch-level squash-merges of the two trusted automation branches (PRs #488, #489), so no generated content passed through agent authoring (integrity equivalent to the documented user-authored-recommit workaround; branch-level assembly is used because the ~1 MB index exceeds the agent tooling memory limit and the export spans 100+ files). The republished search index and API export both count 438 entries, matching the 438-skill public corpus, so the cross-projection consistency test stays green on `main`. Bot PRs #484 and #485 are closed as superseded.
- **Generated-projection republication — batch 3 (2026-10-12, PR #499):** the PR #491 merge triggered the trusted writers, and all four projections were republished: the graph rebuild through bot PR #494 and the quality-report rebuild through bot PR #498 (both owner-merged; neither is cross-coupled), and the Skills API export (`automation/generated-skill-api@82398004`; bot PR #495) together with the search index (`automation/generated-search-index@1af18ef8`; bot PR #493), which are cross-coupled by the search-index/API-export count contract and therefore publish atomically through PR #499 — the publication branch was assembled by branch-level squash-merges of the two trusted automation branches (PRs #496, #497), so no generated content passed through agent authoring (integrity equivalent to the documented user-authored-recommit workaround; branch-level assembly is used because the ~1 MB index exceeds the agent tooling memory limit and the export spans 100+ files). The republished search index and API export both count 483 entries, matching the 483-skill public corpus, so the cross-projection consistency test stays green on `main`. Bot PRs #493 and #495 are closed as superseded. This completes the projection cycle of the owner-directed 100-skill expansion.
- **Expansion-count documentation reconciliation (2026-10-12, PR #500):** the top summary bullets of this document are reconciled with the completed owner-directed 100-skill expansion: the corpus bullet now records the 484-file / 483-public-skill state with the current trusted quality-report counts (326 battle-tested, 157 enriched, zero stubs, zero invalid, one intentional fixture; republished through bot PR #498), the projection-integrity bullet now records the 483-node / 473-edge graph (blob `665f2ce5a1d93ff284de916799b6473eda0e4881`, byte-identical under `data/` and `docs/api/`) and the 483-entry search projection (blob `aeeb2848c1ab587d264492a87dd43d1ff28c44aa`, byte-identical under `data/` and `docs/`) published atomically with the Skills API export through PR #490 and PR #499, and the Agent Skills distribution bullet is annotated that its recorded figures predate the expansion pending a fresh exact-head distribution audit. This change touches documentation only; no skill content, generated artifact, workflow definition, or governance phrase is modified.
- Full-project audit (2026-10-12) found the #447 stranding class still open in nine of the twelve generated-main writers (`update-skill-count.yml`, `weekly-highlights.yml`, `sync-badges.yml`, `leaderboard.yml`, `generate-changelog.yml`, `version-stats.yml`, `used-in-tracker.yml`, `osv-watch.yml`, `revoke-phantom-badges.yml`): they lacked `pull-requests: write` for their `gh pr create` step and committed with `[skip ci]`, so their generated branches were published without bot PRs or runnable required checks. Live evidence: `automation/generated-skill-count` was force-pushed at `f36e120fd4` with a failed check run on `main` (`1acf9409`) and no PR; `automation/generated-weekly-highlights` did not exist (README highlights stuck at October 5, 2026); `docs/badges/` held 345 JSONs against the 484-file corpus. Fixed in PR #501: `pull-requests: write` and no-skip-ci automation commits are restored across all nine writers (in-place read-to-write upgrade where `pull-requests: read` already existed), `tools/update_readme_counts.py` now patches the current README stat anchors loudly (hero strip with graph-edge count from `data/SKILLS_GRAPH.json`, comparison row, What's-Inside line, heading, category table) instead of silently no-oping on obsolete formats, and README.md is synced to 483 public skills / 473 graph edges / 484 quality-corpus files with the live per-category counts. The weekly highlights block was intentionally left for the fixed `weekly-highlights.yml` to republish, and the Agent Skills distribution audit remains pending. The nine-writer finding is documented on #447.
- API security hygiene (audit finding AUD-011, PR #502): the FastAPI service previously set `allow_origins/methods/headers: ["*"]` and echoed `str(exc)` into 500 responses. CORS is now environment-configurable through `SKILLS_TREE_API_CORS_ORIGINS` (comma-separated origins, with `*` as an explicit wildcard opt-in); the default allows only localhost / 127.0.0.1 on any port, and the method/header allowlists are reduced to what the API serves (GET/POST/OPTIONS; Content-Type/Accept). The 500 handler now logs the real exception server-side (`logger.exception`) and returns a generic detail; the 404 and 422 handlers keep their request-scoped details. `tests/test_api_security.py` covers the default policy, env overrides, preflight allow/deny, and 500 redaction. This change touches the API service and its tests only; no skill content, generated artifact, workflow definition, or governance phrase is modified.
- Repository hygiene cleanup (audit P3, PR #503): twelve content-free meta placeholder/stub files were removed (the 1-byte PLACEHOLDER2-6.md, ARCHITECTURE_OUTPUT_SCHEMA.md, RECOMMENDATION_SIMULATION.md, and the 21-32 byte NEXT_TASK_PROMPT.md, NEXT_TASK_RECOMMENDATION.md, TASK_005_REPORT.md, TASK_005_SELF_REVIEW.md, PERCEPTION_COLLISION_REVIEW.md, executing the recovery plan's own R-06 recommendation); the four root historical documents EXECUTION_STATUS.md, AUDIT_REPORT.md, HERMES_GUARD.md, and TEST_COVERAGE_RECOVERY_PLAN.md were moved byte-identically to meta/audits/ and their root copies removed (fulfilling the structure proposal recorded in meta/audits/NEXT_10_ISSUES.md); and 120 double-encoded em-dash sequences in this file were repaired to U+2014 with no wording changes. References to the removed files are plain-text historical mentions in audit records, and the link checker validates only external URLs in skills/**, so no CI surface is affected. No skill content, generated artifact, workflow definition, or governance phrase is modified.
- Root state-document relocation (audit follow-up, PR #504): `PROJECT_MEMORY.md` moved byte-identically from the repository root to `meta/state/PROJECT_MEMORY.md`, completing the `NEXT_10_ISSUES.md` structure proposal (its companion `EXECUTION_STATUS.md` no longer exists at root). Pre-move verification confirmed `tools/verify_governance.py` pins no root path for this file and that all 18 in-repo mentions are plain-text historical citations in `meta/` audit documents, not live links; historical audit documents were not rewritten.
- **Owner-directed corpus expansion wave 2, batch 1 (2026-10-12, PR #506):** the owner directed a second 100-skill expansion; this pilot batch adds 10 experimental skills across 01-perception through 10-computer-use (depth-estimation, game-theory-strategy, memory-conflict-resolution, archive-extraction, database-migration-writing, negotiation, websocket-communication, image-super-resolution, tool-invention, screen-recording), each with a byte-exact deterministic `project()` package. The discovery test count moves 376 to 386; no demand signal is claimed. The corpus moves to 494 files / 493 public skills, and the graph, search-index, API-export, quality-report, README-count, and badge projections regenerate through trusted workflows post-merge.
- **Owner-directed corpus expansion wave 2, batch 2 (2026-10-12, PR #514):** the second batch of the owner-directed wave-2 expansion adds 45 experimental skills across 11-web, 12-data, 13-creative, 14-security, 15-orchestration, 16-domain-specific, and 17-infrastructure, each with a byte-exact deterministic `project()` package; cross-category related links are path-qualified to the existing corpus convention. The discovery test count moves 386 to 431; no demand signal is claimed. The corpus moves to 539 files / 538 public skills, and the graph, search-index, API-export, quality-report, README-count, and badge projections regenerate through trusted workflows post-merge.
- Issue #336 retrieval freshness/reproducibility remains resolved.

## Current execution sequence

1. **Empirical evaluation datasets and harnesses:** CAP-011 preparation is complete (deterministic 100-case ground-truth dataset, fail-closed verifier, and calibration runner — PR #459), CAP-007 validation/scoring tooling is merged (PR #458), and the CAP-014 mock fixture and scorer are merged. Remaining: the 100 human-labeled support queries for CAP-007 (human-only — the dataset schema requires human-labeled status and forbids agent-produced labels), and candidate runs for CAP-011 and CAP-014 with retained raw outputs and adjudication independent of the candidate system. Record provenance and ground truth before running them. Track in [#436](https://github.com/SamoTech/skills-tree/issues/436).
2. **Run and record empirical evaluations** only after datasets and methods are independently validated; preserve exact commit, dataset digests, metrics, failure cases, and limitations.
3. **Real activation/invocation evidence:** resume only on a supported accelerator runner that verifies actual model allocation, then run the existing qualification cases and 12 independent fresh-session observations. Track in [#357](https://github.com/SamoTech/skills-tree/issues/357).
4. **Close remaining automation debt — resolved 2026-10-12:** issue [#447](https://github.com/SamoTech/skills-tree/issues/447) is closed by recorded decision (option (a)): the atomic-republication path — cross-coupled generated projections publishing together through agent-assembled, fully checked PRs built by branch-level merges of the trusted automation branches (the validated #477/#490/#499/#517 pattern) — is adopted as the standard publication path, so `main` is never merged on an unchecked `GITHUB_TOKEN` bot commit. The historical `gh pr create` 403 class is fixed and verified live (bot PRs #509/#512); the residual platform behavior (required checks not running on `GITHUB_TOKEN`-authored bot PR commits; latest evidence: merged bot PR #521 ran only CodeQL ×4 + GitGuardian) is accepted as a documented GitHub same-actor limitation. Option (b) (GitHub App token for bot PR checks) remains an owner-side option if bot PRs ever become the primary publication path. Timestamp-only graph PR suppression is implemented and verified; issue #450 is closed. Decision recorded in `meta/memory/DECISIONS.md`.
5. **Provenance hardening — closed by PR #461:** the 10 name-only Agent Skills package matches were addressed only through deterministic generation and validation — each canonical file in `skills/16-domain-specific/` gained the repository's established `## Evidence` section and its package was regenerated under the `project()` contract with declared provenance (issue [#460](https://github.com/SamoTech/skills-tree/issues/460)). Do not hand-edit generated packages; any future package regeneration must remain deterministic-only.
6. Keep the canonical `skills/` source and current consumer architecture. No new semantic-search engine, duplicate registry, or new skills without a reproducible measured gap.
7. Execute every cycle through `meta/AGENT_EXECUTION_PLAYBOOK.md`; blocked items (human-only input, owner-only control-plane actions, unavailable infrastructure) stay tracked with their blockers recorded and are never worked around.

> Maintained as a point-in-time operational snapshot. Live GitHub refs, generated artifacts, and exact workflow runs remain the evidence source.

## Historical snapshot — 2026-10-06

The following dated sections are preserved for audit history; the active operational state and execution sequence are recorded above.

- Snapshot date: 2026-10-06
- Live `main`: authoritative and must be verified from the Git ref before execution; this document intentionally does not hard-code `main`'s own current commit because updating this document creates a new `main` commit.
- Latest verified runtime sequence on `main` includes the benchmark runtime (`db474059fbe0efa56ca167a7108146323c9cf857`), anti-slop gate (`90f9422954936e054adc630ad723e6165074492c`), Universal Graph fail-closed boundary (`c8e1c536f8abfd860ddf41cefeff15b88518d095`), recommendation registry context (PR #292), and blueprint registry context (PR #293). Live `main` remains authoritative and must be resolved before each execution cycle.
- PR #223 remains the implementation baseline for the post-P2.2 Evidence runtime slice, merged as `642e968879e9b6bfc8e7f9b2a44d12544585fc18`.
- PR #224 merged on 2026-10-01 and synchronized the affected P2 architecture, development knowledge, audit, decision memory, and current-state documentation.
- Quality report: current generated report `meta/QUALITY-REPORT.md` verifies 382 skill files: 223 battle-tested, 158 enriched, 0 stubs, 0 invalid, 1 intentional test fixture.
- Quality-report figures are current only at the generated-report verification point; historical verification sections retain their original counts.
- `main` current HEAD is intentionally verified from the live Git ref during each execution cycle; this snapshot does not hard-code its own future commit.
- The active documentation synchronization baseline is recorded in the 2026-10-11 reconciliation block above; dated audit sections below are historical unless explicitly re-verified.

## Current verified architecture state

- Latest detailed Agent Skills reconciliation report (2026-10-06): 382 corpus entries including the sandbox fixture, 264 eligible deterministic projections, 118 blocked entries, and 302 existing packages. The current tree still contains 302 package manifests; exact-head eligibility/drift status must be re-run before claiming it is freshly verified.
- Current graph baseline: 381 nodes and 255 edges; `data/SKILLS_GRAPH.json` and `docs/api/graph.json` are byte-identical.
- Current search baseline: `data/search-index.json` and `docs/search-index.json` are byte-identical.

- The canonical skill source is `skills/`.
- The universal registry is a read-only, deterministic machine-readable capability layer with typed runtime access.
- P2.1 Implementation ontology contract unification is verified.
- P2.2 typed Implementation runtime access and contract validation are verified.
- The post-P2.2 Evidence runtime slice is verified: `UniversalRegistry` exposes typed deterministic `resolve_evidence()` and `evidence_for_entity()` access through the existing validated `EvidenceRuntime`.
- The post-P2.2 Compatibility runtime slice is verified: `UniversalRegistry` exposes typed deterministic `resolve_compatibility()` and routes `compatibility_for()` through the existing validated `CompatibilityRuntime`.
- The post-P2.2 Skill runtime facade slice is verified: `UniversalRegistry` exposes typed deterministic `resolve_skill()` and `capabilities_for_skill()`, and delegates `implementations_for_skill()` through the existing validated `SkillRuntime`.
- The post-P2.2 Capability runtime facade slice is verified: `UniversalRegistry` exposes typed deterministic `resolve_capability()`, `implementations_for_capability()`, and `adapters_for_capability()` through the existing validated `CapabilityRuntime`.
- The post-P2.2 Goal runtime facade slice is verified: `UniversalRegistry` exposes typed deterministic `resolve_goal()` and `skills_for_goal()` through the dedicated validated `GoalRuntime`.
- The Benchmark runtime slice is verified: `UniversalRegistry` exposes deterministic `resolve_benchmark()` and `benchmarks_for_entity()` under `meta/benchmark-contract.schema.json`; this defines evaluation contracts, not benchmark results.
- The Universal Graph runtime fail-closed boundary is verified on merged `main`: only semantically implemented relationship types are accepted; schema-valid deferred relationships are rejected.
- Recommendation and blueprint consumers expose additive `registry_context` derived from `UniversalRegistry`, preserving provenance/evidence/freshness/implementation context without changing ranking semantics.
- The generated search projection now has an explicit `meta/search-index.schema.json` contract and regression coverage for schema validity, duplicate IDs, canonical file resolution, and path parity with `docs/api/skills.json`. A real stale-projection defect for `kanban-task-management.md` was detected by that gate and reconciled before merge.
- Issue #86 CLI search is verified on `main`: `cli/search_engine.py` consumes the canonical generated projection via `cli/search_runtime.py`, with deterministic lexical ranking and CLI behavioral coverage. PR #299 merged as `7302d0780b2857bdd2f54363a2e6158eafc45292`.
- The installable search runtime boundary is verified: `docs/search-index.json` and `data/search-index.json` are identical generated projections, and `cli/search_runtime.py` resolves either the source checkout asset or installed wheel data.
- Issue #86 search behavior is implemented as a deterministic lexical consumer in `cli/search_engine.py`, with CLI coverage in `tests/test_search_cli.py` and ranking-unit coverage in `tests/test_search_engine.py`.
- The Evidence slice added no new Evidence records, provenance claims, compatibility facts, provider/platform/framework/model claims, or MCP classifications.
- `skills/15-orchestration/kanban-task-management.md` is present on `main` as a verified canonical skill addition. It remains `stability: experimental` and `version: v1`; no stronger maturity claim is implied.
- No numbered P2.3 requirement is currently defined. The next Phase 2 slice must come from a fresh architecture audit.

## Governance and documentation state

- `AI_CONSTITUTION.md` is the authoritative governance model.
- `AGENTS.md` is the AI-agent entrypoint.
- `meta/PRODUCT_MISSION.md` is the authoritative product mission.
- `meta/COO_MASTER_MISSION.md` is the authoritative COO execution mission under the product mission.
- `meta/memory/DECISIONS.md` is the durable decision record.
- `meta/ROADMAP.md` is the execution direction and must remain synchronized with verified state.
- `meta/DEVELOPMENT_KNOWLEDGE.md` records verified development progression.
- `meta/AGENT_HANDOFF_PROTOCOL.md` defines repository handoff requirements.
- `meta/AGENT_EXECUTION_PLAYBOOK.md` defines the concrete perpetual-development cycle procedure (work-item selection, pre-push verification, exact-head CI gate, merge, post-merge verification, reporting).
- Documentation is a completion gate: implementation without synchronized documentation is not COMPLETE.

## Automation state

- Release authority: `zero-touch-release.yml` is the production release pipeline; `release.yml` is retained as manual recovery.
- Pages authority: `deploy-pages.yml` is the single repository-controlled Pages deployment workflow.
- Confirmed direct-main generated writers use the shared `auto-commit-main` serialization group with `cancel-in-progress: false`.
- The live workflow inventory is 45 files, as verified by a 2026-10-06 git-tree audit and reconciled in `meta/WORKFLOW_INVENTORY.md`.
- `validate-graph.yml` permission isolation is implemented and verified: `build-and-validate` is `contents: read`; `generate-main-graph` alone has `contents: write` and runs only on trusted `main` pushes after validation; `quality-report` waits for graph generation before writing its projection.
- PR #232 CI passed Security Scan, PR Checks, Test Suite, Build & Verify Wheel, and Auto Label; Dependabot Review Gate was skipped.
- GitHub control-plane settings are a separate verification boundary; the connected integration cannot independently verify all branch-protection settings. Repository-local governance and recent human-owner evidence must not be represented as API-verified state.

## Source of truth

- Canonical source: GitHub repository `SamoTech/skills-tree`.
- Public source guide: `README.md`.
- Operational state: `meta/CURRENT-STATE.md` plus live GitHub CI/PR state.
- Strategic decisions: `meta/memory/DECISIONS.md`.
- Quality evidence: generated repository reports.
- External dashboards and Vercel deployments are not authoritative.

## Product mission alignment — VERIFIED — 2026-10-02

The governing product mission is now:

> **Skills Tree is a public, trusted, machine-discoverable source of AI skills. AI agents should be able to find the right skill here, and humans should be able to discover, understand, use, share, and contribute skills easily.**

`meta/PRODUCT_MISSION.md` is the canonical mission document. Active governance, roadmap, discovery, distribution, and public-source documentation are being synchronized to it. Historical strategy and decision records retain their original wording where they document prior decisions; they are not treated as the current product mission unless explicitly superseded.

PR #250 discovery alignment is merged and its mission/discovery documentation is now part of the verified product baseline.

## Documentation synchronization status

**VERIFIED — synchronized in this documentation cycle.** The preflight found stale operational statements about merged graph/consumer work; those discrepancies are reconciled here without rewriting historical entries.

## Next mandatory action

1. Merge the public-boundary and evaluation-trigger remediation through the normal PR/CI gate.
2. Verify generated public projections contain 381 production Skills and exclude `00-sandbox/pipeline-test`.
3. Execute Issue #357's 12 real independent runtime observations.
4. Do not change Skill definitions or routing unless measured activation evidence justifies it.


## Kanban Skill Addition — VERIFIED — 2026-10-03

PR #267 was squash-merged after the final exact-head CI matrix passed. The merged skill is canonical under `skills/15-orchestration/` and did not create a competing generated catalog. The only review defect found was a third-party CLI example mismatch; it was corrected before merge and the review thread was resolved.

## Handoff

A future agent must re-read the authoritative documents and verify live GitHub state before continuing. The repository, not this snapshot alone, remains the final source of truth.


## Universal Registry Data Schema Validation — Verified 2026-10-02

PR #241 added runtime structural validation of the loaded universal registry against the dedicated `meta/universal-registry-data.schema.json` data-instance schema. The existing `meta/universal-registry.schema.json` remains the ontology/contract-definition schema and is not incorrectly used as a seed-data schema.

The runtime resolves the implementation and adapter contract schemas through an explicit local `referencing.Registry`, preserving offline/deterministic validation without fetching repository URLs at runtime. Structural validation runs immediately after JSON load; the existing semantic integrity and entity-specific contract validators remain responsible for semantic/provenance invariants.

A regression test rejects a schema-invalid Goal field with the expected `jsonschema.ValidationError`, while the existing provenance test continues to exercise the established semantic `ValueError` boundary.

**Verification:** PR #241 merged as `93c50c3616a7c558b483f341f44a91509ed032ca`. Exact-head Security Scan, PR Checks, Test Suite, and Build & Verify Wheel passed; Dependabot Review Gate was skipped.

**Status:** VERIFIED — runtime structural validation is now aligned with the actual registry data shape and existing semantic validation responsibilities.


## Security Skill Migration Batch 01 — Verified 2026-10-02

A corpus audit found 45 remaining stubs in the generated quality model. The highest-priority remaining cluster was the nine security-category stubs. PR #243 migrated Audit Logging, Harm Detection, Human In Loop, Permission Checking, Privacy Preservation, Rate Limiting, Rollback / Undo, Sandboxed Execution, and Secret Scanning.

Each migrated skill now has a concrete description, explicit I/O contract, runnable example, failure modes, security boundaries, related-skill metadata, and authoritative references. Unsupported benchmark and compliance claims were deliberately excluded.

**Verification:** PR #243 merged as `40fb35aa6c54438f08062c89c118815262b6fe98`. Validate Skills, Security Scan, PR Checks, Test Suite, Build & Verify Wheel, Schema Enforcement, Validate Skills Graph, AST Sweep, Check Links, and Skill Upgrade Detector passed on the final head. The intermediate quality-report run was superseded during the required frontmatter correction; the generated report had already passed for the same nine skill bodies before that metadata-only correction.

**Generated-artifact verification:** the hardened quality-report workflow regenerated `meta/QUALITY-REPORT.md` after the merged documentation PR. The live generated report now verifies 374 skills: 202 battle-tested, 159 enriched, 13 stubs, 0 invalid. Category 14-security is 13 battle-tested, 0 stubs.

**Status:** VERIFIED — implementation, generated corpus report, and public documentation are synchronized.


## Goal Capability Runtime Access — VERIFIED — 2026-10-02

A fresh runtime/consumer audit identified a missing typed Goal→Capability accessor. The implementation adds `GoalRuntime.capabilities_for_goal()` and `UniversalRegistry.capabilities_for_goal()`; `skills_for_goal()` reuses that boundary.

Focused regression coverage verifies deterministic Goal-to-Capability traversal and defensive snapshot behavior.

**Verification:** PR #238 exact head `0d45fd7b7a741c8984fbe5a90b1abe7e8570b744` passed Security Scan, PR Checks, Test Suite, Build & Verify Wheel, and Auto Label before merge as `3290ebc88060fca07e944cd31ad31d392982ca3d`.

**Status:** VERIFIED — the typed Goal→Capability runtime path is live on `main`.
\n\n## Deterministic Agent Skills Projection — VERIFIED — 2026-10-02

PR #251 established and verified the first executable canonical-to-Agent-Skills projection contract, then merged to `main` as `f1d169c3fd9388cf4244d9d4bfc4c64df382a1bb`.

The canonical source remains `skills/`. `tools/generate_agent_skills.py` deterministically derives package names, descriptions, provenance metadata, and package content, while refusing blocked entries. Generation has an explicit write mode; CI performs a read-only audit. The Agent Skills validator also enforces the current name constraint, including the prohibition on consecutive hyphens.

The verified corpus audit found 374 canonical skill entries after excluding category `README.md` files: 250 currently pass the projection gates and 124 are blocked. Eight deterministic-name collisions remain across canonical entries and must be resolved before full-corpus generation. The existing repository contains 280 validated Agent Skills packages; these are not assumed to be canonical projections until provenance reconciliation is completed.

Exact-head CI passed: Agent Skills Distribution Audit, Validate Agent Skills, Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, PR Checks, Auto Label, and Validate Skills Graph. Dependabot Review Gate was skipped.

**Current boundary:** this is a verified projection/audit contract, not full-corpus Agent Skills compliance. The repository does not declare `/.well-known/agent-skills/index.json` live. SHA-256 publication and discovery-index generation remain gated on successful artifact reconciliation, provenance validation, reproducible publication, and served-byte integrity checks.

**Next:** reconcile the 280 existing packages against canonical provenance, resolve the eight canonical name collisions, then generate only eligible canonical projections in independently verifiable batches.


## Deterministic Agent Skills Corpus — VERIFIED — 2026-10-02

PR #264 merged the deterministic canonical-to-Agent-Skills corpus as commit `892a4d747e588cf2876e45ba3effcdd031fd9592`.

Verified generation run:
- 374 canonical skill entries scanned.
- 250 eligible canonical projections generated.
- 124 canonical entries remained blocked and were not generated.
- 288 Agent Skills packages exist on `main`: 250 eligible projections, 37 retained blocked existing packages, and the intentional auxiliary `skills-tree-registry` package.
- 10 canonical name-collision groups were reconciled with deterministic category-qualified projection names where eligible.
- Agent Skills validation passed after generation.
- Reconciliation passed with `git diff --check`.
- Final PR checks passed: Agent Skills validation/distribution audit, Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, PR Checks, and repository graph validation.

The corpus is now a verified deterministic projection of the canonical source. `/.well-known/agent-skills/index.json` remains intentionally unpublished until served-byte integrity, provenance, reproducibility, and SHA-256 publication gates are implemented and verified.


## Universal Registry Behavioral-Evaluation Audit — 2026-10-03

A fresh universal-registry architecture and consumer-behavior audit completed the mandatory post-schema-validation review. Provenance, Evidence, integrity, memory safety, and action governance are already represented at their appropriate repository boundaries. The audit identified one concrete remaining machine-readable consumer gap: the first-class benchmarks registry collection had no dedicated contract or typed runtime facade.

The selected slice was implemented with `meta/benchmark-contract.schema.json`, `BenchmarkRuntime`, `UniversalRegistry` benchmark accessors, and focused behavioral tests. No production benchmark records or external claims were added.

PR #272 merged after the review-fix PR #274 was incorporated. The final exact head was `4738303caeb6a9129af8a0f84cab4219aade5084`; the final PR CI matrix passed Test Suite, Security Scan, PR Checks, Build & Verify Wheel, and Auto Label. The merged main commit is `db474059fbe0efa56ca167a7108146323c9cf857`.

**Status:** VERIFIED — implementation, contract validation, behavioral tests, provenance boundary, and exact-head CI were verified before merge.

## Anti-Slop Quality Gate — 2026-10-03

PR #273 established the deterministic anti-slop quality gate for changed skills. PR #275 supplied the targeted review fixes for rename detection and case-sensitive placeholder handling; #275 was incorporated into #273.

The final #273 head was `4477d33d846c68d71b666e6c283c8787312e023f`; its required CI matrix passed, including Security Scan, Test Suite, Build & Verify Wheel, PR Checks, Validate Skills Graph, Skill Quality Report, and Auto Label. The merged main commit is `90f9422954936e054adc630ad723e6165074492c`.

The gate is deterministic and changed-skill scoped. It blocks selected placeholder/marketing filler patterns, warns on unsupported absolute/generic claims, ignores fenced code/frontmatter, and does not attempt LLM-based style classification.

**Status:** VERIFIED — the quality gate and review fixes are merged. Historical corpus cleanup remains a separate evidence-driven migration and is not implied by this gate.


## Universal Graph Relationship Runtime Boundary — VERIFIED ON MAIN — 2026-10-03

PR #283 was merged to `main` as `c8e1c536f8abfd860ddf41cefeff15b88518d095` after exact-head verification. The runtime preserves the forward-compatible schema vocabulary but rejects schema-valid relationship types lacking explicit runtime semantics. No new graph relationship or evidence was invented.


## Registry Consumer Context — Verified 2026-10-03

The recommendation API now exposes additive registry_context for registered canonical skills. The context is derived from UniversalRegistry and includes canonical identity, provenance, explicitly linked evidence references, declared freshness when present, and registered implementation IDs. It does not create ranking or trust scores and does not infer evidence. Unregistered legacy recommendation entries may have null registry_context.

Verification: PR #292 merged the recommendation consumer context; focused API regression coverage is present. Next: audit remaining machine-readable discovery projections for equivalent registry context and provenance propagation.


## Blueprint Consumer Context — VERIFIED ON MAIN — 2026-10-03

PR #293 merged additive `registry_context` propagation onto required and optional blueprint skill entries. The field is descriptive and does not change blueprint generation, architecture selection, or ranking.


## PyPI Release Contract Synchronization — VERIFIED — 2026-10-03

`meta/PYPI_RELEASE_PLAN.md` was reconciled with the executable release path. The repository version is currently `1.68.0` in `pyproject.toml`. Production publication is performed by `.github/workflows/zero-touch-release.yml` using GitHub OIDC Trusted Publishing and the `pypi` environment. The historical `publish.yml` / `PYPI_API_TOKEN` / `1.0.0` instructions are no longer treated as current release instructions.


## Machine-Readable Discovery Registry Context — VERIFIED ON MAIN — 2026-10-03

The discovery audit found that docs/api/skills.json was not consuming the verified UniversalRegistry context. PR #300 merged as `4ff041511f2291e826b2a32c2cc72f36f8f023cb` and adds optional registry_context for the three exact registered skills only, with no synthetic membership or evidence. Final head `52ae305ad504416114d7efdd8313eff8f931f57d` passed the required CI matrix, including Test Suite on Python 3.11/3.12/3.13 and installed-wheel verification.

During validation, the new focused test exposed an existing schema/artifact date-format mismatch in unrelated `added`/`last_updated` fields. The test was narrowed to the registry_context sub-schema; the date-format drift remains a separate audit finding and was not changed in PR #300.


## Generated Discovery Projection Audit — VERIFIED — 2026-10-03

PR #301 corrected canonical Kanban date metadata and PR #302 reconciled `docs/api/skills.json` and `docs/api/skills.yaml`; the affected projection now reports `added: 2026-10` and `last_updated: 2026-10`.

The remaining machine-readable projection audit found:
- `agent-skills/` already has a read-only reconciliation/audit gate on canonical `skills/**` changes; no duplicate drift checker is warranted.
- `docs/api/jsonld/` is an SEO/presentation projection generated from the same skill index. It does not implement ranking, trust, evidence, or registry semantics, so `registry_context` was intentionally not duplicated into JSON-LD.
- `/.well-known/agent-skills/index.json` is published and verified live; deployment run `37227197992` passed the served-byte verification gate.

**Next:** audit remaining machine-readable consumers/projections after the verified discovery publication boundary; do not create a second generator, reconciler, search index, or deployment path.

## Agent Skills Reconciliation Gate — VERIFIED ON MAIN — 2026-10-04

A fresh Agent Skills distribution audit identified a governance gap: tools/reconcile_agent_skills.py classified eligible missing projections but exited successfully unless its result was manually interpreted. The merged implementation closes that gap with a read-only --check mode wired into the Agent Skills Distribution workflow.

Verified merged-main state:

- 375 canonical skill entries are scanned.
- 258 currently satisfy the deterministic Agent Skills projection gates.
- 117 are blocked by the existing eligibility rules.
- The Agent Skills projection contains 296 packages: 258 deterministic eligible projections, 37 retained blocked packages, 1 intentional auxiliary `skills-tree-registry` package, and 1 legacy compatibility package (`rag`).
- The newly added Kanban skill is eligible and has a deterministic projection at agent-skills/kanban-task-management/SKILL.md.
- Reconciliation classifies eligible missing, projection drift, rename-needed compatibility mappings, stale/ambiguous provenance, unexpected packages, and unresolved deterministic target-name collisions. `rename_needed` alone is not a failure.
- Known canonical collisions remain valid when the existing deterministic category-qualified resolution produces unique target names.
- No .well-known/agent-skills/index.json publication was introduced.

This state is VERIFIED ON MAIN after PR #305 merge; the next action is a fresh audit of remaining machine-readable discovery consumers.


## 2026-10-04 — Agent Skills discovery publication boundary — VERIFIED ON MAIN

The deterministic Agent Skills discovery publication slice is now merged and verified end-to-end.

Verified main:
- Main HEAD: `e306a810c7cabac25b9f19fa4aeeab2e62ed0e3f`.
- 375 canonical skill entries remain the source corpus.
- 258 eligible deterministic Agent Skills projections are published.
- 117 canonical entries remain blocked.
- 296 Agent Skills packages remain reconciled under the existing hard gate.
- The discovery index is generated from the same reconciled projection and validated against `meta/agent-skills-discovery-index.schema.json`.
- Every published `SKILL.md` digest is SHA-256 over the exact published bytes.
- Local Pages artifact byte verification passed.
- GitHub Pages deployment run `37199284169` passed both build and deployment jobs.
- Served discovery index and every advertised Agent Skills artifact passed served-byte SHA-256 verification.

Current project-site discovery URL:
`https://samotech.github.io/skills-tree/.well-known/agent-skills/index.json`

The repository does not claim the root-level `/.well-known/agent-skills/index.json` endpoint because the current hosting topology is a GitHub Pages project site. A root endpoint remains a separate hosting/custom-domain control-plane decision.

No second generator, reconciler, search index, or Pages deployment workflow was introduced.

**Status:** VERIFIED — deterministic discovery generation, provenance/reconciliation, schema validation, artifact integrity, Pages deployment, and served-byte verification are all aligned.

## 2026-10-04 — Graph projection boundary — VERIFIED ON MAIN

PR #315 unified the graph generation and projection governance boundary.

Verified:
- `tools/build_graph.py` remains the sole graph generator.
- `validate-graph.yml` is the single graph generation/validation writer; the duplicate `build-graph.yml` workflow was removed.
- The generated graph is validated against `schema/graph.schema.json` plus the referenced skill and edge schemas, including metadata counts and graph integrity checks.
- `docs/api/graph.json` is generated from the same graph output as `data/SKILLS_GRAPH.json` and is byte-identical on main (blob SHA `36aa24b193dc89cb1e0a789ef4ff78db2e14e286`).
- Main graph baseline after regeneration: 375 nodes, 240 edges, 9 REQUIRES edges, 0 warnings.
- Schema drift found during implementation was corrected for generated `requires_count`, prerequisite arrays, generated `source_method`, and numeric-leading skill slugs.

**Status:** VERIFIED — graph generation, schema validation, integrity checks, and synchronized runtime/UI projections are aligned.

## 2026-10-04 — JSON-LD export governance — VERIFIED

The machine-readable export audit confirmed that JSON-LD is generated by the existing `tools/export_skills.py` implementation and committed by `export-skills.yml`; no `jsonld-export.yml` workflow exists on current main.

A real governance gap was found: the export workflow only triggered on skill content changes, so exporter or UniversalRegistry changes could leave generated JSON/YAML/JSON-LD projections stale. It also had no deterministic JSON-LD projection validation.

PR branch `fix/jsonld-export-governance` adds `tools/verify_jsonld_export.py` and focused regression tests. The validator checks JSON validity, one TechArticle per registry skill, matching IDs/names, ItemList positions/counts, and duplicate URLs. `export-skills.yml` now runs the validator and triggers on exporter and registry changes.

PR #316 merged as `20ed032bdb83f22ef3bf37debb3004ed8153d9a8` after the required PR CI matrix passed. The validator and workflow trigger changes are now on main. Do not create a second JSON-LD generator or workflow.

## 2026-10-04 — Release authority consolidation — VERIFIED

Fresh release-path audit confirmed that `zero-touch-release.yml` is the production release authority and `release.yml` is manual recovery only. The former `release-package.yml` independently triggered on version tags and could create/update the same GitHub Release while the zero-touch pipeline was still completing.

PR consolidation moves catalog ZIP + MANIFEST generation into Job 4 of `zero-touch-release.yml`, alongside the existing wheel/sdist attachment, and removes `release-package.yml`. The production release path therefore has one release writer and one manual recovery workflow.

No semantic-release workflow file exists on current main; semantic-release is executed as Job 1 inside `zero-touch-release.yml`.

**Status:** VERIFIED implementation boundary; final PR CI and post-merge release-path checks are required before treating the change as complete.


## 2026-10-04 — Release authority consolidation — VERIFIED ON MAIN

PR #317 merged as `262dfea66fb81e5779e93b45884d857f3b10522d`.

The production release boundary is consolidated: `zero-touch-release.yml` is the sole production release writer; `release.yml` remains manual recovery only; catalog ZIP + MANIFEST packaging is now part of zero-touch Job 4; the duplicate tag-triggered `release-package.yml` workflow was removed.

The workflow inventory and release governance documentation are synchronized with the executable architecture.

**Rule:** do not reintroduce a second tag-triggered GitHub Release publisher.


## Full Repository Re-Audit — 2026-10-04

The current full-project audit is recorded in `meta/audits/FULL_REPOSITORY_AUDIT_2026-10-04.md`.

Verified current baseline:
- 376 canonical skills; the new IDE Integration skill is the first demand-driven Phase 3 slice.
- 259 eligible Agent Skills projections; 117 blocked; 297 packages expected after deterministic projection maintenance.
- Graph baseline will advance from 375 to 376 nodes after generated projection maintenance; CI must verify the resulting edge and artifact counts.
- 40 workflow files are present and classified in `meta/WORKFLOW_INVENTORY.md`.
- JSON-LD, search, Agent Skills reconciliation/discovery, graph, Pages, and release boundaries each have one authoritative writer/generation path.
- Release consolidation is merged as PR #317 at `262dfea66fb81e5779e93b45884d857f3b10522d`.
- The current audit found the security gate was under-scoped: Gitleaks was blocking, but Python SAST and dependency auditing were not part of the blocking security workflow. This is being hardened in the current audit PR.
- GitHub branch-protection state remains a control-plane finding; the connected integration returned HTTP 403 for the branch-protection endpoint, so no new control-plane claim is made.

The stale 42-workflow statement is historical only. Historical audit documents retain prior findings and are not current architecture authority.


**Post-audit verification:** PR #318 merged as `2ef8a3fe9c987032d614a0e2a026cc4152867204` after exact-head Security Scan `37201410948` passed Gitleaks, Bandit high-severity/high-confidence enforcement, and `pip-audit --strict`; Test Suite, Build & Verify Wheel, Validate Skills Graph, and PR Checks also passed.

The blocking repository security gate is now materially enforced. The remaining branch-protection finding is control-plane-only and remains tracked separately by issue #159.

## 2026-10-04 — Repository self-enforced governance

The repository governance model was audited after the owner explicitly rejected GitHub branch protection as a required control. Repository-local enforcement is now defined in `meta/GOVERNANCE_MODEL.md` and mechanically checked by `tools/verify_governance.py`, invoked by `.github/workflows/governance-gate.yml`.

The governance gate verifies the mandatory agent/documentation preflight, canonical `skills/` source boundary, unique release authority, unique machine-readable projection paths, anti-slop and new-stub enforcement, blocking security controls, and the repository's explicit independence from GitHub branch protection.

Issue #159 is therefore a control-plane decision outside the repository completion model, not an engineering blocker. Its historical references to branch protection remain historical and must not be interpreted as a current project requirement.

**Status:** VERIFIED — repository governance is self-enforced without requiring GitHub branch protection.


## Core Agentic Execution Loop — IMPLEMENTED — 2026-10-04 — HISTORICAL IMPLEMENTATION RECORD

The repository now defines a bounded autonomous execution contract for AI agents. The canonical cycle is `OBSERVE → ASSESS → PLAN → EXECUTE → VERIFY → RECORD → DECIDE`. Verification failures become evidence for the next cycle instead of requiring a new user prompt. The loop has explicit `CONTINUE`, `BLOCKED`, and `DONE` outcomes, a default 12-iteration ceiling, repeated-failure safeguards, authority escalation boundaries, and a completion contract requiring invariant verification, tests/CI, generated-artifact synchronization, and documentation synchronization.

The contract is defined in `meta/AGENT_OPERATING_MODEL.md`, reinforced by `AGENTS.md` and `AI_CONSTITUTION.md`, and checked by `tools/verify_governance.py`. This is an operating contract, not a claim that GitHub or an external hosted agent automatically executes arbitrary future work without an invoking agent runtime.

Status: VERIFIED — superseded by the exact-head verification recorded immediately below.


## Core Agentic Execution Loop — VERIFIED — 2026-10-04

PR #324 was merged after the exact final head `8f254754231bd8153efd50ab0e4b1bff4d067cad` passed Governance Gate, Validate Skills Graph, Test Suite on the applicable matrix, Security Scan, PR Checks, Build & Verify Wheel, and related validation. The repository now defines the bounded operational cycle `OBSERVE → ASSESS → PLAN → EXECUTE → VERIFY → RECORD → DECIDE`, with failure-driven continuation, a default 12-iteration ceiling, explicit CONTINUE/BLOCKED/DONE states, authority escalation boundaries, and documentation/generated-artifact completion requirements.

**Status:** VERIFIED on main at merge commit `6fa92dd42768395102215a26e22999d6de81c013`.

## Main-Writer Race — DETECTED AND RESOLVED — 2026-10-04

Post-merge verification exposed a real automation race: the graph writer advanced main while the quality projection and zero-touch release workflows were still operating from the triggering SHA. The graph projection itself completed, but the quality writer failed on stale upstream state and zero-touch release failed when its upstream SHA changed. This is a concurrency/state-reconciliation defect, not a graph-generation defect.

The remediation was implemented through PR #325 (stale-SHA synchronization) and PR #326 (lossless `queue: max` writer queue). Exact-head CI passed for both PRs. Post-merge evidence showed graph projection, quality projection, and zero-touch release completing sequentially; zero-touch release completed successfully at version 1.74.0, and the generated graph/quality writer sequence advanced main without the earlier stale-SHA failure.

**Status:** VERIFIED on live main. The repository-wide writer contract is now: shared `auto-commit-main`, `queue: max`, `cancel-in-progress: false`, plus live-main synchronization before mutation.


## Documentation Synchronization — VERIFIED — 2026-10-04

The agentic execution contract, governance model, main-writer serialization, and lossless writer queue are synchronized with the verified live implementation. Historical entries remain explicitly historical; current operational state is represented by the resolved sections above and the durable decisions in `meta/memory/DECISIONS.md`.


## Consumer-Path Audit — 2026-10-04

The fresh consumer-path audit found that the previously tracked CLI search gap is already resolved on main. `skills-tree search` uses the canonical generated `data/search-index.json` projection through `cli/search_runtime.py`; deterministic ranking is defined in `meta/SEARCH_CLI_CONTRACT.md`; dedicated CLI, ranking, and projection-contract tests exist. No second search index or runtime Markdown parser is required.

The Agent Skills discovery publication boundary is also implemented in `.github/workflows/deploy-pages.yml`: Pages builds `/.well-known/agent-skills/index.json` from `tools/build_agent_skills_discovery.py`, validates the local publication bytes, and verifies the served URL with `tools/verify_agent_skills_discovery.py`. Repository code evidence therefore shows the publication path is implemented. External live serving is the remaining verification step; do not claim it is live until a successful Pages deployment provides that evidence.

**Decision:** Do not build another search/discovery generator. Complete live Pages verification first; then reassess demand intelligence from evidence.


## Demand Intelligence — IMPLEMENTED COLLECTION PATH — 2026-10-04

Phase 2 now has its first reproducible public-signal path: `tools/collect_demand_signals.py` reads the explicit `meta/demand-sources.json` query set and records public GitHub issue-search evidence with source ID, query, repository, issue number, URL, state, dates, and labels. `.github/workflows/demand-signals.yml` runs the collector manually or weekly and stores the raw snapshot as an artifact.

The collector deliberately does not infer popularity, adoption, or priority. The curated `meta/MOST-WANTED-SKILLS.md` remains unranked until a controlled collection run is reviewed and capability coverage/evidence gaps are mapped.


## Demand Signal Review — VERIFIED OBSERVATION — 2026-10-04

The first controlled public-signal review executed against the configured GitHub issue-search sources. The three configured queries returned raw result counts of 64, 63, and 54; overlap and operational/security issues make these counts unsuitable as popularity or adoption metrics.

The review identified an unranked capability signal cohort around search/discovery (#86), memory (#87), code/IDE integration (#88), reasoning (#90), and action execution (#91). Search/discovery is already implemented and verified; the remaining signals require canonical coverage, evidence-tier, freshness, and dependency-gap analysis before any migration priority is selected.

**Decision:** Do not create a popularity ranking. Use the observed cohort as input to a coverage/evidence reconciliation pass, then select Phase 3 work only where demand and repository gaps intersect.


## Phase 3 Candidate — IDE Integration — VERIFIED ON MAIN — 2026-10-04

Coverage/evidence reconciliation selected IDE integration as the first demand-driven Phase 3 slice. The canonical `05-code` directory already covers code generation, review, execution, Git, APIs, debugging, and related capabilities, but no dedicated IDE integration contract existed. The new `skills/05-code/ide-integration.md` defines a protocol-neutral contract around workspace identity, code intelligence, diagnostics, bounded edits, tests/builds, explicit authorization, least privilege, and independent postcondition verification.

The skill cites current public evidence for MCP/IDE integration and explicitly avoids universal compatibility or benchmark claims. CI must determine whether the skill is schema-valid, anti-slop compliant, projection-eligible, and safe to merge.


## Discovery Publication Boundary — VERIFIED

Live GitHub Pages verification completed on 2026-10-04. Deployment run `37227197992` for main commit `1b3a5f387a17ce6b57885b06d6f26db060a8784d` succeeded. The deployment job's `Verify served discovery bytes` step also succeeded, proving the published `/.well-known/agent-skills/index.json` endpoint passed the repository's served-byte verifier. The discovery publication boundary is therefore CLOSED as verified. Next strategic slice: Demand Intelligence / Most-Wanted evidence collection.

## Demand Intelligence — Initial Evidence Pass

The first repository-local demand collection path is present and a controlled public-signal cohort has been recorded. External public-source corroboration on 2026-10-04 shows Agent Skills are an ecosystem-scale concern, with strong activity around discovery, interoperability, retrieval/selection, evaluation, governance, and safety. A coverage reconciliation found that the repository already has broad canonical coverage for the local memory, IDE/code, reasoning, and action-execution demand signals. The next decision gate is therefore evidence/runtime quality rather than raw skill creation. Preferred investigation: skill evaluation/invocation evidence and retrieval quality.


## Agentic Loop — Retrieval/Evaluation Evidence — 2026-10-05

OBSERVE/ASSESS found a concrete evidence boundary defect: the retrieval benchmark is stale and not currently backed by a reproducible current run; its related canonical skill links are outdated; the evaluation ontology is past review due; and evaluation workflow path filters omitted the ontology itself. EXECUTE fixed the workflow trigger so evaluation-ontology changes now invoke validation. Issue #336 records the remaining evidence remediation: reproduce, retire, or re-qualify the stale benchmark without fabricating new scores. Current decision: **CONTINUE** — the next safe evidence-backed action is benchmark provenance/link repair and deterministic freshness validation.

## Agentic Loop — Evaluation Gate Reconciliation — 2026-10-05

**OBSERVE:** Live main has a deterministic lexical CLI search path and a typed Benchmark runtime, but no current reproducible retrieval-quality run. The legacy recommendation evaluator is historical and is not current runtime evidence. The current evaluation ontology contains seven mappings and remains overdue for review; CAP-007, CAP-011, and CAP-014 are still absent from the ontology mapping set.

**ASSESS:** The evaluation workflow was checking the wrong corpus location (`data/corpus/**`) and therefore could not reliably measure P0 evaluation coverage. Its warning-only behavior did not convert missing mappings into a false completion claim, so the safest correction is to point the check at the canonical `intelligence/corpus/entries/**` path and report missing P0 mappings explicitly without inventing evaluations. A declared-freshness check was added to detect malformed/inconsistent timestamps and surface overdue review dates without rewriting them automatically.

**EXECUTE:** The evaluation workflow was corrected on branch `fix/evaluation-evidence-gate-20261005`; the stale retrieval benchmark was qualified as historical, its current canonical skill links were repaired, and the benchmark index documentation no longer claims every result is currently reproducible.

**VERIFICATION:** No benchmark result was regenerated and no current retrieval score was claimed. The repository still requires benchmark provenance/reproduction or explicit retirement/re-qualification for the stale retrieval evidence, and authoritative P0 mappings for CAP-007/CAP-011/CAP-014 remain outstanding. These are tracked evidence gaps, not fabricated failures or success claims.

**DECISION:** CONTINUE / BLOCKED boundary remains evidence-driven. The next safe action after CI verification is to address Issue #336/Issue #335 only with reproducible benchmark evidence or an explicit evidence disposition; no new retrieval implementation is justified yet.

## Post-Merge Verification — Evaluation Gate Self-Trigger — 2026-10-05

**OBSERVED:** PR #337 merged to `main` as `4b1c1b9ffc28bcbecc3b899da8cbb58af7de65ec`. Exact-head PR checks passed, including Test Suite, Security Scan, Build & Verify Wheel, Governance Gate, PR Checks, and CodeQL. Post-merge Governance Gate also passed.

**NEW GAP:** The merged `validate-evaluations.yml` workflow did not include itself in its `push.paths` filter. Therefore the workflow was authoritative but did not self-trigger when the workflow definition itself changed. This is a CI trigger defect, not evidence of evaluation correctness.

**ACTION:** Follow-up branch `fix/evaluation-gate-self-trigger-20261005` adds `.github/workflows/validate-evaluations.yml` to its own push path filter and synchronizes the decision record with the merged state.

**DECISION:** CONTINUE until the follow-up exact-head CI proves the trigger correction. No benchmark or retrieval implementation is introduced.


## P0 Evaluation Contracts — VERIFIED ON MAIN — 2026-10-05

PR #339 merged to main as c88672e1d19e381aad8137796d4283678e3fc9e1. The canonical evaluation ontology now contains mappings for the remaining P0 capabilities CAP-014 tool_execution, CAP-007 semantic_retrieval, and CAP-011 self_evaluation. No new evaluation framework, ontology category, or retrieval implementation was introduced.

During exact-head CI, Validate Evaluations exposed two pre-existing validator defects: the gate expected min_required_score while canonical mappings use minimum_required_score, and two existing mappings had stale names for CAP-023 and CAP-025. Both were corrected. Final exact-head CI passed Validate Evaluations, Governance Gate, Test Suite, Security Scan, Build & Verify Wheel, PR Checks, and Auto Label; Dependabot Review Gate was skipped.

The P0 contracts are now structurally linked and CI-validated. This does not constitute current benchmark success: CAP-007 explicitly remains without a current reproducible result artifact, and CAP-011 calibration diagnostics remain evidence requirements rather than a fabricated new metric type. The next evidence boundary is reproducible evaluation execution/results, not another ontology or search implementation.


## Retrieval Evidence — VERIFIED ON MAIN — 2026-10-05

PR #340 merged to main as `8ae02bd08841a496d19f49cd1092ec5f011c6c6b`. The repository now has a versioned, machine-readable retrieval benchmark registered through the existing `BenchmarkRuntime` contract, a deterministic runner over the canonical `cli.search_engine.search_documents` implementation, and a PR/workflow-dispatch evidence workflow.

Exact-head PR verification passed the Retrieval Evidence Benchmark, Governance Gate, Security Scan, Build & Verify Wheel, Validate Skills Graph, PR Checks, Test Suite on Python 3.11/3.12/3.13, and CodeQL. The retrieval benchmark run `37301951280` produced artifact `retrieval-benchmark-95839c52567c32cad38c0a0038edc01dc0a298f4`.

Current evidence snapshot: 12 benchmark cases, Recall@5 = 1.0000, MRR = 0.9583, deterministic replay = true. Eleven of twelve expected skills ranked first; the RAG case ranked the expected `03-memory/rag` at position 2 behind `09-agentic-patterns/rag`. This is evidence of current deterministic retrieval behavior for the bounded dataset, not a semantic-search, popularity, adoption, or user-satisfaction claim.

Decision: do not change ranking yet. The measured RAG ambiguity is now a concrete candidate for a separate retrieval-quality investigation. Any ranking change requires a broader representative failure corpus and before/after measurement.


## Demand-Gap Skill Selection — VERIFIED MERGED — 2026-10-05

PR #341 merged to main as `af892ebf9aafd90dedb9d6039974d51c2bf02726` after exact-head CI passed.

The demand reconciliation identified a narrow missing capability: canonical skill-level selection and next-step routing. Existing coverage already included deterministic search, specialist-agent routing, role assignment, task decomposition, delegation, dependency traversal, registry eligibility, and orchestration primitives, but no dedicated contract for discriminating competing skills, resolving prerequisites, verifying invocation, and selecting the next skill from observed results.

Added `skills/15-orchestration/capability-based-skill-selection.md` as an experimental canonical skill and its deterministic `agent-skills/capability-based-skill-selection/SKILL.md` projection. The demand collector now includes selection/routing/orchestration/task-breakdown signals, and `meta/MOST-WANTED-SKILLS.md` records the evidence-backed demand gap.

The exact-head matrix passed Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, Governance Gate, PR Checks, Validate Skills, Validate Agent Skills, Agent Skills Distribution Audit, Validate Skills Graph, Schema Enforcement, Check Links, AST Sweep, Skill Upgrade Detector, Dependency Auditor, and Retrieval Evidence Benchmark.

During verification, existing generated projection drift was exposed and reconciled: the canonical API/search projections and JSON-LD index were brought back into alignment with the live corpus, and the discovery-count test was updated to track the current verified projection count.

Status: MERGED. Post-merge push workflows are running; their results remain a separate verification boundary until observed.


## Behavioral Skill Selection — VERIFIED BOUNDED RUNTIME — 2026-10-05

PR #343 merged to main as `203d4b12e576cbeb5eaa83249cc97d96905b01fc` after exact-head CI passed Test Suite, Security Scan, Build & Verify Wheel, Governance Gate, PR Checks, Validate Skills Graph, Retrieval Evidence Benchmark, and the new Skill Selection Evidence Benchmark.

The repository now has `registry/skill_selection.py` as a deterministic registry-backed selection boundary. It resolves explicit required capabilities against registered canonical skills, applies existing eligibility, rejects unknown candidates fail-closed, returns explicit selection/rejection evidence, and emits CONTINUE/BLOCKED next actions. The versioned benchmark `benchmark/skill-selection-v1` currently covers the three skills represented in the Universal Registry plus unknown-candidate, insufficient-capability, and failed-invocation terminal cases.

Current benchmark evidence: 6/6 cases passed with deterministic replay. This verifies the bounded capability-selection behavior only.

LIMITATION: prerequisite routing is implemented in the selector against the existing `REQUIRES` graph API, but it is not yet behaviorally evidenced through the canonical registry because the Universal Registry currently contains only three skill records and no prerequisite-bearing registered skill pair. Do not claim full task → dependency → invocation sequencing as verified until registry coverage and a reproducible prerequisite benchmark exist.

Status: VERIFIED BOUNDED SLICE. Next justified action: reconcile canonical registry skill coverage for prerequisite-bearing skills, then extend the behavioral benchmark without creating a second registry or orchestration authority.


## Behavioral Skill Selection — PREREQUISITE ROUTING VERIFIED BOUNDED SLICE — 2026-10-05

PR #345 merged to main as `f15c729adf76794fc914f954f74a4964d7dbdd76` after exact-head `8200b0f359e35293121189cdf2dd263ce96252db` passed the applicable CI matrix, including Test Suite, Security Scan, Build & Verify Wheel, PR Checks, Retrieval Evidence Benchmark, and Skill Selection Evidence Benchmark.

The selection runtime now resolves transitive `REQUIRES` prerequisites deterministically, detects prerequisite cycles, fails closed when a graph prerequisite is not registered, and emits the next prerequisite before target invocation. The registry boundary now represents Agentic RAG, CoT, and ReAct with explicit capabilities; Agentic RAG is separated from general knowledge retrieval through `capability/agentic-knowledge-retrieval`, preventing the registry expansion from changing baseline RAG capability resolution.

Current bounded behavioral evidence covers:
- Agentic RAG selection over baseline RAG for the explicit agentic capability.
- Ordered prerequisite routing: RAG → CoT → ReAct before Agentic RAG invocation.
- Resume behavior after partial prerequisite completion.
- Target invocation only after all declared prerequisites are complete.
- Fail-closed behavior for invalid prerequisite graphs.

This verifies deterministic dependency-aware skill selection for the registered Agentic RAG scenario. It does not establish general autonomous task understanding, arbitrary graph correctness, or full task → capability → skill → invocation → verification → next-skill autonomy.

Post-merge workflow runs for `f15c729adf76794fc914f954f74a4964d7dbdd76` were not yet observable at the verification point. Exact-head PR CI is the authoritative pre-merge evidence.

Status: VERIFIED BOUNDED RUNTIME. Next action: use the verified prerequisite-routing boundary as the baseline for the next evidence-driven skill-selection/recovery slice; do not broaden the registry or add orchestration infrastructure without a concrete measured gap.


## Behavioral Skill Selection — FAILURE RECOVERY VERIFIED BOUNDED SLICE — 2026-10-05

PR #347 merged to main as `adbbb55c58a853e843883b2cbc14997f315226b7` after exact-head `40cff5782307469b9d9e62733d04841c667b9870` passed Test Suite, Security Scan, Build & Verify Wheel, Governance Gate, PR Checks, Validate Skills Graph, and Skill Selection Evidence Benchmark.

The recovery runtime now carries an explicit failed-skill history and excludes all previously failed candidates from subsequent recovery selection. The benchmark and unit tests verify remaining-candidate recovery, terminal escalation when no viable recovery remains, and deterministic replay. This closes the measured repeated-retry defect without adding a second orchestration authority.

LIMITATION: the current Universal Registry does not contain three independently registered, capability-compatible alternatives needed to produce a genuine multi-step A → failure → B → failure → C recovery-chain benchmark. A synthetic chain or registry expansion solely for benchmark convenience would fabricate evidence. Therefore this slice is bounded to history-aware candidate exclusion, single-step recovery, and terminal fail-closed behavior.

Post-merge workflows for `adbbb55c...` were not observable at the verification point. Exact-head PR CI is the authoritative pre-merge evidence.

Status: VERIFIED BOUNDED RECOVERY SLICE. Next justified action: obtain real canonical registry coverage with multiple independently eligible alternatives through existing project evolution, then add a multi-step recovery benchmark only when that evidence exists. No artificial skills or new orchestration framework should be introduced for the benchmark.


## Agent Skill Security Audit — VERIFIED ON MAIN — 2026-10-06

PR #350 merged to main as `436c15c745e1747e3ec1e931dccacea1ca013c7c` after exact-head CI passed Governance Gate, Skill Upgrade Detector, Agent Skills Distribution Audit, Schema Enforcement, Auto Label, Skill Quality Report, Validate Skills, Build & Verify Wheel, Check Links, PR Checks, AST Sweep, Validate Skills Graph, Security Scan, and Test Suite. Dependabot Review Gate was skipped.

Demand/evidence reconciliation identified a narrow security boundary missing from the canonical corpus: pre-installation/pre-execution auditing of a complete agent skill package. Existing security skills already cover sandboxed execution, secret scanning, permission checking, input sanitization, audit logging, and human approval; the new contract composes those controls and does not introduce a second scanner or authorization authority.

Added `skills/14-security/agent-skill-security-audit.md`. The contract covers package inventory, declared-vs-observed behavior, credential access, network egress, permission overreach, obfuscation, sandbox requirements, evidence locations, and fail-closed disposition. It explicitly states that static audit output is evidence rather than a safety guarantee and that audit success does not grant execution authorization.

Post-merge workflow runs for `436c15c745e1747e3ec1e931dccacea1ca013c7c` were not observable at documentation-sync time; exact-head PR CI is the authoritative pre-merge evidence. The skill remains experimental pending any future behavioral/security evaluation evidence.

Status: VERIFIED BOUNDED SECURITY CONTRACT. Next action: reconcile any generated projection/quality workflow results on live main, then return to Demand Intelligence only where a concrete evidence or implementation gap remains.


## Evaluation Ontology Freshness Review — VERIFIED — 2026-10-06

A live consistency audit reviewed `intelligence/ontology/evaluation_ontology.json` against the canonical capability ontology and both current corpus entries (`CORPUS-001`, `CORPUS-002`). The ontology contains 12 evaluation types and 12 capability mappings after the repair. All referenced `ET-*` identifiers resolve, capability mapping IDs are unique, mapping names resolve to canonical capabilities, and all ten P0 capabilities required by the current corpus are explicitly mapped. No new evaluation type, ontology category, registry, or benchmark framework was introduced.

The only verified issue was freshness metadata: `last_reviewed_at` was `2026-07-05` and `review_due_at` was `2026-10-03`. After the integrity audit passed, the review metadata was refreshed to `2026-10-06` with the existing 90-day review cadence, due `2027-01-04`.

Evidence: live ontology audit on main baseline `537c30944bdf2163f0ac3350ff4661a66ba85f8e`; 12/12 evaluation references resolve; 10/10 current corpus P0 mappings present after PR #354; no duplicate or unknown mapping IDs. This review does not claim empirical quality of evaluation metrics or benchmark results.

CI exposed two additional corpus P0 capabilities not covered by the initial live snapshot: CAP-018 `multi_turn_dialogue_management` and CAP-027 `compliance_logging`. The existing ontology boundary was extended with mappings for those capabilities using only existing ET-012, ET-001, ET-005, and ET-007 metrics. No new metric type or evaluation framework was introduced.

Status: VERIFIED ON MAIN — PR #354 merged as `15c455bbef43d5f88c17c0cbdbac1af09c8e2d04`. Exact-head applicable CI passed Governance Gate, Validate Evaluations, Test Suite, Security Scan, Build & Verify Wheel, PR Checks, and Auto Label; Dependabot Review Gate was skipped. The canonical corpus now has evaluation mappings for all 10 P0 capabilities. Next: return to Demand Intelligence and select only a new evidence-backed gap.


## Demand Intelligence — Skill Activation / Invocation Evidence — 2026-10-06

Live reconciliation of the current selection runtime and benchmark against fresh public ecosystem evidence identified a new bounded gap: real user-request skill activation/invocation is not behaviorally measured. The existing `benchmark/skill-selection-v1` verifies explicit capability-to-skill selection, prerequisite routing, and failure recovery, but it does not measure natural-language trigger reliability, false activation, collision behavior, repeated fresh-session variance, or actual invocation evidence.

External evidence includes addyosmani/agent-skills #620 (direct prompts with repeated 0/6 owning-skill activation and a measured description improvement), Hermes #82253 (2/3 activation on an identical message across fresh sessions), Hermes #96704 (activation/effectiveness evaluation gap), and Google skill-reach (routing/collision evaluation).

Issue #357 is the authoritative current investigation record. Decision: measure activation/invocation first using existing project boundaries; do not add a new skill, search engine, or routing authority without measured failure evidence.

Status: HISTORICAL — this investigation state was superseded by the verified activation benchmark, Hermes adapter/capture instrumentation, and fail-closed/partial corpus contracts. Real runtime evidence remains pending.


## Skill Activation / Invocation Evidence Benchmark — VERIFIED ON MAIN — 2026-10-06

Issue #357 was advanced from investigation to an executable evidence instrument without introducing a new routing authority. PR #359 merged this measurement boundary to `main` as `51f22be5d3935437e19561e8aa1fdbf2eb19daab`. It adds:

- `benchmarks/activation/skill-activation-v1.json` — four bounded natural-language cases covering expected activation, must-not-activate behavior, collision groups, and repeated runs.
- `tools/run_skill_activation_benchmark.py` — trace-based evaluator for explicit `skill_selection` and `skill_execution` events.
- `tests/test_skill_activation_benchmark.py` — deterministic parser/metric regression coverage using synthetic fixtures only.
- `benchmark/skill-activation-v1` — registered in the existing Benchmark runtime boundary.

The evaluator deliberately does not simulate model routing or infer activation from prompt text. `NO_OBSERVATIONS` is an explicit non-PASS state. Therefore the repository now has an activation/invocation measurement boundary, but **no empirical activation-rate claim is made yet** because real agent-runtime traces have not been supplied.

Metrics: expected activation rate, false activation rate, invocation-evidence rate, and repeated-run activation variance.

Next executable action: obtain real structured traces from a compatible agent runtime, run the benchmark, record the evidence, then decide whether failures justify skill-description, runtime, or evaluation changes.


## Activation Observation Contract — IMPLEMENTED — 2026-10-06

The activation benchmark now has an explicit machine-readable observation contract at `meta/skill-activation-observation.schema.json`. `tools/run_skill_activation_benchmark.py` validates external trace payloads against this schema before calculating activation, false-activation, variance, and invocation-evidence metrics. This closes the interoperability/contract gap between an external agent runtime and the benchmark without introducing a routing runtime or new authority.

Empirical activation reliability remains UNVERIFIED: no real runtime trace corpus has been recorded in the repository. Synthetic fixtures remain evaluator tests only.

Next executable action: capture repeated fresh-session traces from a compatible external agent runtime that emits `skill_selection` and `skill_execution` events conforming to the schema, then run `benchmark/skill-activation-v1` and record the resulting evidence.


## Hermes Activation Observation Adapter — IMPLEMENTED — 2026-10-06

The activation evidence boundary now includes a deterministic interoperability adapter at tools/convert_hermes_activation_observations.py. It consumes explicit Hermes observer-hook JSONL evidence and emits the existing meta/skill-activation-observation.schema.json shape.

The adapter maps only observed events:
- Hermes post_tool_call with tool_name=skill_view → skill_selection.
- Hermes on_skill_lifecycle with action=loaded → skill_execution.
- Both must share an explicit session/task correlation and the run must be mapped explicitly to an ACT-* case. Selection-only evidence is preserved as selection evidence; execution evidence is independently preserved when observed. Mismatched selection/execution is intentionally retained so false activation and invocation gaps remain measurable.

The adapter does not infer activation from prompts, aggregate .usage.json counters, or missing events. It does not add routing authority or change runtime behavior.

Status: IMPLEMENTED — empirical evidence remains UNVERIFIED until real Hermes traces are collected and the resulting 12-run corpus passes schema validation and benchmark execution.

## Hermes Real-Trace Capture Instrumentation — VERIFIED ON MAIN — 2026-10-06

PR #364 merged the real-trace capture boundary as `ebb150dfb0f0ad6ddb3d2426cb81d7d7c31579ac`. It adds `benchmarks/activation/hermes_skill_activation_observer.py` and `benchmarks/activation/HERMES-TRACE-CAPTURE.md`.

The observer records only explicit Hermes `post_tool_call` / `skill_view` and `on_skill_lifecycle(action=loaded)` evidence with session/task correlation. It intentionally excludes prompts, model output, tool results, and aggregate usage counters. This is capture instrumentation, not a benchmark result.

Current blocker: no real Hermes trace corpus has been captured in this repository. The next executable action is operational capture of 12 fresh-session observations (4 cases × 3 repetitions), explicit ACT-case mapping, conversion, schema validation, and benchmark execution. Do not claim empirical reliability before that evidence exists.
## Evaluation Harness Integrity — FAIL-CLOSED GAP — 2026-10-06

Fresh public evidence identified silent zero-run benchmark failure as a reusable evaluation-harness integrity risk. Internal audit confirmed `tools/run_skill_activation_benchmark.py` reported `NO_OBSERVATIONS` while returning exit code 0.

PR #365 applies the minimum remediation: zero observed cases now return exit code 2 while still writing the explicit `NO_OBSERVATIONS` result. Existing observed-trace metrics and partial-corpus reporting are unchanged.

Status: VERIFIED — PR #365 merged as `d39d899e23e8614eb11971953541cda9bd7dec9f` after exact-head applicable CI passed. This is not an activation-result claim.
Next executable action: continue real-runtime activation evidence collection and evidence-integrity hardening.
## Previous Full-Project Live Reconciliation — 2026-10-06 (historical)

Live main now contains the verified Model/Agent/Tool/Capability/Skill semantic boundary from PR #368, the Hermes activation adapter/capture instrumentation from PRs #363/#364, and the fail-closed zero-observation benchmark behavior from PR #365.

At the 2026-10-06 audit point, `meta/QUALITY-REPORT.md` reported 382 skill files (223 battle-tested, 158 enriched, 0 stubs, 0 invalid, 1 intentional fixture). The Agent Skills Distribution Audit on the PR #368 head verified 382 corpus entries and 302 existing packages. The graph projections at that point were byte-identical at 382 nodes / 250 edges, and the search projections were byte-identical.

Governance: GitHub branch protection is not a project completion gate under the current repository-local governance decision; obsolete Issue #159 is closed as not planned. The remaining material activation investigation is Issue #357, which still lacks a real Hermes trace corpus.

Activation evidence contract: zero observations are a process failure; partial traces are explicitly classified as PARTIAL; empirical completion is COMPLETE only when all 4 benchmark cases meet their declared 3 repetitions (12 observations total). PR #371 implements this contract.

Earlier point-in-time audit sections in this file remain historical and must not be read as current counts or current activation status.
Next executable action: collect real-runtime activation evidence for Issue #357, resolve the retrieval benchmark freshness/reproducibility gap in Issue #336, and maintain the 45-workflow inventory against live `main`. Issues #370 and #372 are completed.
## DevLens Writer Isolation — VERIFIED ON MAIN — 2026-10-06

Full-project audit identified `devlens.yml` as a manual README writer outside the repository-wide generated-main boundary. PR #377 merged as `5a25ef13751e4a43ce2a92226198c2b24232ecf3` with the workflow reduced to diagnostic-only: `contents: read`, `security-events: read`, and `update_readme: false`. The stale DevLens snapshot was removed from README.md.

Governance verification now fails if DevLens regains repository write permission or README mutation. This closes the direct DevLens writer risk; it does not make DevLens an authoritative health metric.
## Activation Observation Integrity — VERIFIED ON MAIN — 2026-10-06

The activation benchmark now fails closed before metric calculation when an observation case_id is outside the selected dataset or when run_id is duplicated. PR #379 merged as `290cb3495d1905615501471e4e1b3bec86301a7b`. Case-level status is aligned with completion_status so partial evidence cannot be represented as OBSERVED.

This is evidence-integrity hardening only. No routing, skill definition, or metric formula changed.
## Previous Full-Project Audit Reconciliation — 2026-10-06 (historical)

The live main audit has no open pull requests. PRs #368, #371, #374, #375, #376, #377, and #379 were verified through exact-head CI before merge. The final evidence hardening merges are #377 (DevLens writer isolation) and #379 (activation observation integrity).

At the 2026-10-06 audit point, the quality report contained 382 skill files including one intentional `00-sandbox` fixture; the public canonical production corpus contained 381 skills across 17 categories. The reconciliation report recorded 264 eligible canonical projections, 118 blocked entries, and 302 existing Agent Skills packages. Graph projections were byte-identical at 382 nodes / 250 edges; search projections were byte-identical.

Current remaining evidence gap: Issue #357 requires real external agent-runtime traces before activation/reliability claims. Issue #336 is resolved: the stale model-comparison benchmark is explicitly historical, canonical references and evaluation triggers were repaired, and a version-matched 12-case deterministic retrieval benchmark produced a reproducible artifact. No new skill, search engine, or routing authority is justified by the present evidence.

