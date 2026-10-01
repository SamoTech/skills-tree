# Skills Tree — Live Repository State

> Maintained as a point-in-time operational snapshot. This file records verified state used for engineering and governance decisions.

## Verified snapshot

- Snapshot date: 2026-10-01
- Main HEAD: `7d83d43a3c953d7ce66c7d52f13ea8c3545d2a8d` — current main after domain-specific modernization batch 01
- Quality report: generated counts pending the post-merge quality writer; last verified report remains 135 battle-tested, 59 enriched, 180 stubs, 0 invalid
- Invalid: 0
- Stub migration: batch 01 merged as PR #164 at `424fb43bee42545ac09f4683adb1127dfa97bcda` (10 perception skills)
- Stub migration: batch 02 merged as PR #168 at `2c123af09fe6eb506eab543e2eea96efb0124273` (10 additional perception skills)
- Stub migration: batch 03 merged as PR #169 at `a86b05aa55dab80d4180d8cae19356f7b35c314f` (4 additional perception skills)
- Stub migration: batch 04 merged as PR #170 at `ff4a774d33f81282508a3fb7879b5fed0238c223` (10 reasoning skills)
- Stub migration: batch 05 merged as PR #171 at `ca90ca58f04661580e00f0dc59df780d2a4f90fb` (8 reasoning skills)
- Stub migration: batch 06 merged as PR #174 at `0f0ec52895d825c70eaf06297441443782bd301c` (10 reasoning skills)
- DevLens health: 87/100 (README badge, updated 2026-09-30)
- PR #141: merged on 2026-09-30 as commit `e34d71e6cf7e980871bf71fb084b46c0f5617127`
- PR #150: closed as duplicate of PR #155
- Stale substantive PRs remain open only where GitHub safety controls prevented bulk disposition; they are not merge candidates until reconciled against current `main`.
- Governance implementation: `AI_CONSTITUTION.md` and `AGENTS.md` are merged to `main` via PR #158 at `ee427de8705dba318a32d8c7be82bbdac53f80f8`.
- Source-of-truth cleanup: PR #162 merged on 2026-09-30 as `33b36dfa02b5acb87d517a5669f1a9eca3b50626`.
- Security/distribution consolidation: PR #163 merged on 2026-09-30 as `2a6d2dfe50006746d7866df6890691f154840dfb`.

## Validation and CI state

The generated `meta/QUALITY-REPORT.md` is refreshed on `main` and reports 374 skills, 121 classifier battle-tested, 16 enriched, 237 stubs, and 0 invalid. The quality classifier is intentionally stricter than the migration gate, so a rewritten evidence-backed skill is not automatically counted as enriched or battle-tested.

Batch 02 exposed two CI gates and both were reconciled before completion: the Agent Skills packages required an explicit evidence-status statement, and the spreadsheet-reading skill referenced an ODFPy documentation URL returning 404; it now points to the authoritative `eea/odfpy` repository.

PR #141 added and enforced the machine-readable Evidence contract at registry initialization and added regression coverage. It was merged after review because it was focused and GitHub reported it mergeable.

The repository no longer depends on Vercel or an external project dashboard. GitHub is the authoritative operational source; `README.md` is the public source guide. CI, issues, pull requests, releases, generated reports, and repository files are the evidence surfaces.

## Corpus modernization priority

The current quality distribution makes the remaining 237 stubs the dominant modernization target. Migration is incremental and evidence-driven. Batches 01 and 02 each covered 10 perception skills. Batch 03 covered 4 additional perception skills. Batch 04 covered 10 reasoning skills, Batch 05 covered 8 additional reasoning skills, and Batch 06 covered the final 10 reasoning stubs; both batches added standards-compatible `SKILL.md` projections plus the automated evidence/security validation gate. No skill is promoted to battle-tested solely because it has been rewritten; reproducible benchmark evidence is required for that claim.

## Governance state

The repository now has an explicit AI governance entrypoint:

- `AI_CONSTITUTION.md` — authority, escalation, documentation gate, decision record, handoff, and completion rules.
- `AGENTS.md` — AI-agent entrypoint and mandatory operating rules.
- `meta/AGENT_OPERATING_MODEL.md` — existing lifecycle and execution-chain specification.
- `meta/memory/DECISIONS.md` — authoritative decision record.
- `meta/CURRENT-STATE.md` — current verified state.

The authoritative-document map intentionally reuses existing repository documents instead of creating duplicate status, roadmap, architecture, testing, deployment, or security files.

## Operational rule

Do not treat historical snapshots in `PROJECT_MEMORY.md` or older audit documents as current truth when they conflict with current main SHA, current PR metadata, current CI results, or generated quality reports.

A meaningful task is not COMPLETE until implementation and required documentation are both verified.

## Source of truth

- Canonical source: GitHub repository `SamoTech/skills-tree`.
- Public source guide: `README.md`.
- Operational state: `meta/CURRENT-STATE.md` and GitHub CI/PR state.
- Strategic decisions: `meta/memory/DECISIONS.md`.
- Quality evidence: generated repository reports.
- External dashboards and Vercel deployments are not authoritative and are not part of the project architecture.

## Distribution readiness

- Canonical skill source: `skills/` in GitHub.
- Machine-readable projection: `docs/api/skills.json`, generated from canonical skill content.
- Standards-compatible seed: `agent-skills/skills-tree-registry/SKILL.md`.
- Distribution contract: `docs/AGENT_SKILLS_DISTRIBUTION.md`.
- GitHub raw content is the repository-native machine-readable distribution surface; no external dashboard is authoritative.
- Full `/.well-known/agent-skills/index.json` publication remains a release-engineering task until reproducible artifact generation and SHA-256 verification are implemented.

## Security hardening

- Skill validation is read-only and does not mutate contributor branches.
- Dependabot automation does not auto-approve or auto-merge dependency updates.
- Agent-facing skill instructions are explicitly treated as a supply-chain/security surface.


## Project-operating skills

- Added reusable repository-operation skills under skills/15-orchestration/ for state loading, documentation-drift resolution, evidence verification, automation review, and execution handoff.
- Added Agent Skills projections where the repository projection path was successfully created.
- These skills encode the existing AI_CONSTITUTION.md, AGENTS.md, and agent operating model rather than creating a competing governance system.
- Validation status: PR #179 merged as `b0e47cf9ebbfa97377fb881caeb3a00e65209d40`; PR #181 merged as `8280d7ba4a8d7f6038d79900fc64a00a6a17ccb9`; both passed their substantive CI gates.


## Automation review — 2026-09-30

- Live workflow inventory contains multiple automated writers to `main`, including exports, changelog generation, search-index generation, leaderboard updates, OSV Watch, quality reports, badge synchronization, skill-count updates, used-in tracking, and release packaging.
- Several writers use the shared `auto-commit-main` concurrency group, but not every writer is serialized through that group. In particular, `generate-changelog.yml` and `quality-report.yml` currently have no workflow-level concurrency block while retaining `contents: write` capability.
- This is a documented automation-risk finding, not a demonstrated failure. No automation was changed during this audit because altering generated-main coordination is a significant infrastructure change and requires the established governance escalation path.
- Open pull requests: 0 at the time of the previous snapshot; the action-execution modernization batch is now staged on a dedicated branch for CI verification.


## Action-execution modernization — batch 01

- Ten canonical 04-action-execution stubs were rewritten with explicit inputs/outputs, runnable examples, failure modes, related skills, and repository evidence.
- Ten corresponding Agent Skills projections were added under agent-skills/.
- No benchmark or battle-tested performance claim is made by this batch.
- Verification gate: PR CI must pass the canonical skill validator, Agent Skills validator, schema checks, security scans, and new-stub quality gate before merge.


## Action-execution modernization — batch 02

- Nine remaining 04-action-execution stubs were rewritten: form-submission, keyboard-input, mouse-input, notification-sending, process-management, screenshot-capture, scroll, shell-command, and wait-sleep.
- Nine corresponding Agent Skills projections were added under agent-skills/.
- No benchmark or battle-tested performance claim is made by this batch.
- PR CI must verify canonical schema, Agent Skills evidence, graph integrity, security scans, and the no-new-stub quality gate before merge.


## Code modernization — batch 01

- Ten 05-code stubs were rewritten with explicit procedures, runnable examples, failure modes, related references, and evidence statements.
- Ten corresponding Agent Skills projections were added.
- No benchmark or battle-tested claim is introduced.
- PR CI must pass canonical validation, Agent Skills validation, graph checks, security scans, and the no-new-stub quality gate before merge.


## Code modernization — batch 02

- Ten additional 05-code stubs were modernized: code-translation, db-schema-design, debugging, dependency-auditor, dependency-management, dockerfile-generation, documentation-generation, git-operations, github-api, and integration-test-writing.
- Corresponding Agent Skills projections were added or synchronized.
- No benchmark or battle-tested claim is introduced.
- PR CI must pass canonical validation, Agent Skills validation, graph checks, security scans, and the no-new-stub quality gate before merge.


## Code modernization — batch 03

- Seven additional 05-code stubs were modernized: linting-formatting, performance-profiling, refactoring, regex-generation, repl-interaction, sql-query-generation, and unit-test-generation.
- Agent Skills projections were added for the completed skills except where the repository connector safety layer blocked a projection path; no validator was weakened.
- security-scanning was intentionally not modified because the connector safety layer blocked the repository write; it remains subject to a later safe execution path.
- No benchmark or battle-tested claim is introduced.


## Tool-use modernization — batch 01

- Modernized ten 07-tool-use skills with repository-backed procedures and runnable examples: a2a-tool, browser-tool, calculator, code-exec-tool, custom-api-wrapper, file-system-tool, function-calling, github-api, google-workspace-api, and huggingface-api.
- Agent Skills projections were synchronized for the batch.
- No validation or security gate was weakened.


## Tool-use modernization — batch 02

- Modernized ten additional 07-tool-use skills: image-gen-tool, jira-api, linear-api, maps-geolocation, mcp-tool, news-api, notion-api, pdf-tool, sendgrid-api, and slack-api.
- Added corresponding Agent Skills projections under agent-skills/.
- Provider-specific claims are grounded in cited provider documentation; no benchmark or battle-tested performance claim is introduced.
- No validator, security gate, or repository governance rule was weakened.
- PR CI is the required verification gate before merge.


## Tool-use modernization — batch 03

- Modernized ten additional 07-tool-use skills: github-api, google-workspace-api, huggingface-api, sql-tool, stripe-api, twilio-api, vector-db-tool, weather-api, web-search, and wikipedia-api.
- Added or synchronized corresponding Agent Skills projections under agent-skills/.
- Provider-specific behavior is referenced to official provider documentation; no benchmark or battle-tested claim is introduced.
- No validator, security gate, or repository governance rule was weakened.
- PR CI is the required verification gate before merge.


## Domain-specific modernization — batch 01

- Modernized ten 16-domain-specific skills: ad-copy, alert-triage, clinical-note-summarization, compliance-checking, compliance-review-workflows, contract-review, data-labeling, drug-interaction, essay-grading, and financial-statement.
- Added corresponding Agent Skills projections.
- Added explicit scope, validation, uncertainty, and failure handling; no unsupported domain certainty was introduced.
- No validator, security gate, or repository governance rule was weakened.


## Domain-specific modernization — batch 02

- Staged ten additional 16-domain-specific skills: flashcard-creation, hypothesis-generation, iac-generation, incident-response, invoice-processing, legal-research, lesson-plan, literature-review, log-analysis, and medical-literature-search.
- Added or synchronized corresponding Agent Skills projections under `agent-skills/`.
- Preserved explicit scope, evidence boundaries, uncertainty handling, and professional-domain limitations.
- No validator, security gate, or repository governance rule was weakened.
- PR CI is the required verification gate before merge.


## Domain-specific modernization — batch 03

- Modernized the final eight 16-domain-specific stubs: paper-summarization, portfolio-analysis, product-description, quiz-generation, review-analysis, seo-optimization, stock-lookup, and symptom-analysis.
- Added or synchronized corresponding Agent Skills projections.
- The 16-domain-specific category is now fully modernized; no domain-specific stub remains in the planned migration queue.
- No validator, security gate, or repository governance rule was weakened.


## Computer-use modernization — batch 01

- Modernized ten `10-computer-use` skills: accessibility-tree, app-launch, clipboard-read, clipboard-write, double-click, drag-drop, file-dialog, keyboard-shortcut, keyboard-type, and mouse-click.
- Added or synchronized corresponding Agent Skills projections.
- Added explicit target verification, authorization, postcondition, sensitive-data, and destructive-action boundaries.
- No validator, security gate, or repository governance rule was weakened.


## Computer-use modernization — batch 02

- Modernized the remaining ten `10-computer-use` skills: mouse-move, multi-monitor, right-click, screen-ocr, screenshot-capture, scroll, terminal-interaction, visual-element-detection, vm-interaction, and window-management.
- Added or synchronized corresponding Agent Skills projections.
- The `10-computer-use` category is now fully modernized; target verification, bounded interaction, sensitive-data protection, and postcondition checks remain mandatory.
- No validator, security gate, or repository governance rule was weakened.


## Data modernization — batch 01

- Modernized ten `12-data` stubs: anomaly-detection, csv-processing, data-aggregation, data-cleaning, data-filtering, data-joining, data-summarization, data-visualization, etl-pipeline, and json-transformation.
- Added or synchronized corresponding Agent Skills projections.
- Added explicit schema, provenance, validation, cardinality, null-handling, and data-loss boundaries.
- No validator, security gate, or repository governance rule was weakened.


## Data modernization — batch 02

- Modernized the remaining seven `12-data` stubs: nosql-query, pandas-operations, schema-inference, similarity-search, sql-execution, statistical-analysis, and time-series.
- Added or synchronized corresponding Agent Skills projections.
- The `12-data` category is now fully modernized; the existing embedding-generation skill was preserved as the category's already battle-tested implementation.
- No validator, security gate, or repository governance rule was weakened.


## Orchestration modernization — batch 01

- Modernized ten `15-orchestration` stubs: agent-communication, agent-handoff, budget-management, conditional-branching, consensus-voting, event-triggers, hierarchical-tree, logging-observability, parallel-execution, and retry-backoff.
- Added or synchronized corresponding Agent Skills projections where the repository projection path permitted creation.
- Added explicit ownership, state, idempotency, authorization, recovery, and evidence boundaries.
- No validator, security gate, or repository governance rule was weakened.


## Orchestration modernization — batch 02

- Modernized the final six `15-orchestration` stubs: role-assignment, sequential-workflow, shared-memory, state-machine, subagent-spawning, and task-queue.
- Added or synchronized corresponding Agent Skills projections.
- The `15-orchestration` category is now fully modernized; existing battle-tested orchestration skills were preserved.
- No validator, security gate, or repository governance rule was weakened.


## Agentic patterns modernization — batch 01

- Modernized ten `09-agentic-patterns` skills: tot, lats, mcts, rag-pipeline, reflection, critic-agent, self-play, constitutional-ai, debate-pattern, and mixture-of-agents.
- Added corresponding Agent Skills projections.
- Added explicit objectives, evaluation criteria, budgets, provenance, evidence boundaries, uncertainty handling, and failure modes.
- Preserved existing substantial ReAct, CoT, RAG, Agentic RAG, and Plan-and-Execute implementations.
- No validator, security gate, or repository governance rule was weakened.


## Multimodal modernization — batch 01

- Modernized fourteen `08-multimodal` skills: 3d-scene-understanding, audio-classification, audio-transcription, chart-generation, document-layout-analysis, image-captioning, image-classification, image-editing, image-generation, object-detection, text-to-speech, video-description, video-frame-extraction, and vqa.
- Added or synchronized corresponding Agent Skills projections.
- Added explicit modality contracts, bounded preprocessing/execution, provenance, uncertainty handling, failure modes, safety boundaries, and runnable examples.
- Preserved verified dependency metadata where present.
- No validator, security gate, or repository governance rule was weakened.


## Agentic patterns modernization — batch 02

- Modernized the remaining four stub-level `09-agentic-patterns` skills: bootstrapping, memory-augmented, subagent-delegation, and tool-use-loop.
- Added corresponding Agent Skills projections.
- Added explicit objectives, acceptance criteria, bounded execution, provenance, uncertainty handling, failure modes, and runnable examples.
- No validator, security gate, or repository governance rule was weakened.


## Memory modernization — batch 01

- Modernized five `03-memory` skills: fact-verification-memory, fact-verification, procedural, user-profile, and working-memory.
- Added corresponding Agent Skills projections.
- Added explicit memory scope, provenance, retention, freshness, conflict handling, uncertainty, bounded operations, and verification requirements.
- Removed unsupported legacy dependency/code-block metadata from the canonical procedural skill while preserving its operational intent.
- No validator, security gate, or repository governance rule was weakened.


## Communication modernization — batch 01

- Modernized ten `06-communication` skills: argument-construction, citation-attribution, clarification-seeking, debate, email-drafting, instruction-following, multilingual-output, persona-adoption, question-answering, and report-writing.
- Added corresponding Agent Skills projections.
- Added explicit communication contracts, evidence boundaries, uncertainty handling, constraint checking, failure modes, and runnable examples.
- Preserved existing enriched paraphrasing, summarization, and translation skills.
- No validator, security gate, or repository governance rule was weakened.


## Communication modernization — batch 02

- Modernized the remaining two `06-communication` placeholder skills: structured-output and tone-adjustment.
- Added corresponding Agent Skills projections.
- The `06-communication` placeholder cluster is now fully addressed; existing enriched skills were preserved.
- No validator, security gate, or repository governance rule was weakened.


## Web modernization — batch 01

- Modernized ten `11-web` skills: api-discovery, browser-navigation, captcha-solving, cookie-management, dom-inspection, form-filling, js-execution, link-extraction, rss-parsing, and sitemap-parsing.
- Added corresponding Agent Skills projections.
- Added explicit authorization boundaries, bounded requests/actions, provenance, postcondition checks, and anti-automation/access-control safety boundaries.
- No validator, security gate, or repository governance rule was weakened.


## Web modernization — batch 02

- Modernized the remaining three `11-web` skills: url-fetching, url-screenshot, and web-login.
- Added corresponding Agent Skills projections.
- `11-web` placeholder modernization is now complete; existing enriched web-search, web-scraping, and web-crawling skills were preserved.
- Added explicit origin/session boundaries, resource limits, provenance, and credential/access-control safety rules.
