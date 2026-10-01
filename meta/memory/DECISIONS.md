# DECISIONS.md

# Each decision should follow this format:

DECISION-ID:
Topic:

Decision:

Confidence:
HIGH
MEDIUM
LOW

Evidence IDs:
[List of EVIDENCE-ID references]

Status:
LOCKED

Reopen Conditions:
[Contradictory evidence must include file, line numbers, and exact quote]

# Example:
# DECISION-001:
# Topic: Naming convention for skill modules
# Decision: Use kebab-case for skill directory names.
#
# Confidence:
# HIGH
#
# Evidence IDs:
# EVIDENCE-002
#
# Status:
# LOCKED
#
# Reopen Conditions:
# If contrary evidence is found showing a different convention is used consistently, including file path and exact quote.

# DECISION-002
DECISION-ID: DECISION-002
Topic: AI repository governance and COO documentation gate
Decision: Adopt AI_CONSTITUTION.md as the authoritative repository governance model. AI CEO/CIO retains strategic decision authority; AI COO owns execution, repository health, verification, and documentation. No meaningful task may be reported COMPLETE while required documentation is missing.
Confidence: HIGH
Evidence IDs: GOV-001, GOV-002
Status: LOCKED
Reopen Conditions: Reopen only if the Human Owner changes the governance model or an authoritative repository decision supersedes it.

# DECISION-003
DECISION-ID: DECISION-003
Topic: PR audit disposition on 2026-09-30
Decision: Merge focused PR #141 after verification; close duplicate PR #150; close stale PRs #142, #146, #155, and #156 after current-main revalidation; keep #145 separately closed after its supply-chain review. Vercel deployment-rate-limit failures are treated as infrastructure conditions, not code-quality evidence.
Confidence: HIGH
Evidence IDs: PR-141, PR-142, PR-145, PR-146, PR-150, PR-155, PR-156, MAIN-20260930
Status: LOCKED
Reopen Conditions: Reopen if current-main revalidation, CI evidence, or contributor changes materially alter the technical assessment.


# DECISION-006
DECISION-ID: DECISION-006
Topic: Project source of truth and deployment surface
Decision: GitHub is the authoritative source for repository content, operational evidence, releases, issues, pull requests, and machine-readable skill distribution. README.md is the public source guide. Remove Vercel configuration and project-health/launch dashboard artifacts; they are not authoritative project surfaces. GitHub-controlled files and GitHub-native evidence replace those surfaces.
Confidence: HIGH
Evidence IDs: SRC-001, SRC-002, SRC-003
Status: LOCKED
Reopen Conditions: Reopen only if the Human Owner explicitly adopts a different source-of-truth architecture.


# DECISION-004
DECISION-ID: DECISION-004
Topic: Skills Tree as a public AI skill source
Decision: Keep `skills/` as the canonical registry source, expose `docs/api/skills.json` as the machine-readable registry projection, and add a separate standards-compatible Agent Skills distribution layer. Do not treat the legacy flat Markdown corpus as already compliant with the `SKILL.md` standard. Web discovery via `/.well-known/agent-skills/index.json` must be generated with reproducible SHA-256 digests before being declared live.
Confidence: HIGH
Evidence IDs: DIST-001, DIST-002, DIST-003
Status: LOCKED
Reopen Conditions: Reopen if the Agent Skills discovery specification materially changes or the Human Owner chooses a different canonical distribution architecture.

# DECISION-005
DECISION-ID: DECISION-005
Topic: CI and dependency automation security hardening
Decision: Skill validation must be read-only, and Dependabot must not auto-approve or auto-merge dependency updates. Automated jobs may propose changes, but the exact green HEAD requires maintainer review before merge.
Confidence: HIGH
Evidence IDs: SEC-001, SEC-002
Status: LOCKED
Reopen Conditions: Reopen only after a documented replacement governance model provides equal or stronger review and supply-chain controls.


## DECISION-2026-09-30-STUB-MIGRATION

**Topic:** Convert the remaining legacy skill stubs into evidence-backed, standards-compatible Agent Skills.

**Decision:** Migrate the 293 stubs incrementally. Preserve `skills/` as canonical source, generate `agent-skills/<skill-name>/SKILL.md` as the compatibility projection, require evidence references and explicit failure/security boundaries, and prohibit performance/battle-tested claims without reproducible benchmark evidence.

**Confidence:** High

**Evidence IDs:** `meta/QUALITY-REPORT.md`, `docs/AGENT_SKILLS_DISTRIBUTION.md`, Agent Skills specification, batch-01 validation workflow.

**Status:** IN PROGRESS — Batches 01–06 merged; current generated quality report verified at 121 battle-tested, 16 enriched, 237 stubs, 0 invalid.

**Reopen Conditions:** Change only if the canonical Agent Skills specification, repository quality contract, or security findings materially change.

**Execution record:** Batch 01 merged as PR #164 (`424fb43bee42545ac09f4683adb1127dfa97bcda`). Batch 02 merged as PR #168 (`2c123af09fe6eb506eab543e2eea96efb0124273`). Batch 03 merged as PR #169 (`a86b05aa55dab80d4180d8cae19356f7b35c314f`). Batch 04 merged as PR #170 (`ff4a774d33f81282508a3fb7879b5fed0238c223`). Batch 03 required removal of unsupported legacy frontmatter properties before schema validation passed. Batch 04 passed the full repository quality/security gate. Batch 05 merged 8 additional reasoning skills and Batch 06 completed the 02-reasoning category with 0 reasoning stubs. PR #179 subsequently added the reusable project-operating skills used for repository execution. Remaining stubs are intentionally not mass-promoted without evidence.


## DECISION-2026-09-30-CI-AUTOMATION

**Topic:** Serialize generated-main automation and repair OSV/README drift.

**Decision:** Generated writers that commit to `main` share the `auto-commit-main` concurrency group with cancellation disabled. OSV Watch installs its required `httpx` dependency. README category counting excludes the `00-sandbox` fixture so the public taxonomy remains 17 categories.

**Confidence:** High

**Evidence IDs:** CI-20260930-OSV, CI-20260930-README, CI-20260930-GRAPH, PR-172

**Status:** LOCKED

**Reopen Conditions:** Reopen if a generated-main writer requires an incompatible serialization model or the public taxonomy intentionally expands to include `00-sandbox`.


## DECISION-2026-09-30-REASONING-MIGRATION

**Topic:** Complete the 02-reasoning stub migration.

**Decision:** Migrate the remaining reasoning stubs incrementally under the evidence-backed v2 contract. Batch 06 completes the 02-reasoning category; the generated quality report now shows 46 reasoning skills with 0 stubs and repository-wide totals of 369 skills, 113 classifier battle-tested, 14 enriched, 242 stubs, and 0 invalid.

**Confidence:** High

**Evidence IDs:** PR-174, QUALITY-20260930, MAIN-20260930

**Status:** LOCKED

**Reopen Conditions:** Reopen if the canonical skill schema, evidence contract, or quality classification changes materially.


# DECISION-2026-09-30-PROJECT-OPERATING-SKILLS
DECISION-ID: DECISION-2026-09-30-PROJECT-OPERATING-SKILLS
Topic: Reusable AI operating skills for repository execution
Decision: Encode the repository's established state-loading, documentation-drift, evidence-verification, automation-review, and execution-handoff procedures as reusable skills under the canonical orchestration taxonomy. Agent Skills projections are created only through the repository's existing skills-to-agent-skills contract; governance documents remain authoritative.
Confidence: HIGH
Evidence IDs: GOV-001, PROJECT-SKILLS-20260930
Status: LOCKED
Reopen Conditions: Reopen if the repository governance model, canonical skill projection contract, or agent operating lifecycle materially changes.


## DECISION-2026-09-30-ACTION-EXECUTION-MIGRATION

**Topic:** Modernize action-execution skill stubs incrementally.

**Decision:** Convert the first ten 04-action-execution stubs into evidence-backed canonical skills with standards-compatible Agent Skills projections. Preserve explicit destructive-action, secret-handling, validation, and failure boundaries. Do not claim benchmark or battle-tested status without reproducible evidence.

**Confidence:** High

**Evidence IDs:** QUALITY-20260930, ACTION-EXECUTION-BATCH-01, AI-CONSTITUTION, AGENTS

**Status:** IN PROGRESS — staged on branch coo/action-execution-batch-01-2026-09-30 pending PR CI.

**Reopen Conditions:** Reopen if validation reveals schema, security, projection, or evidence-contract incompatibility.


## DECISION-2026-09-30-ACTION-EXECUTION-BATCH-02

**Topic:** Complete the remaining 04-action-execution stub modernization.

**Decision:** Convert the remaining nine action-execution stubs into evidence-backed canonical skills with standards-compatible Agent Skills projections. Preserve explicit target verification, authorization, bounds, secret handling, and postcondition checks.

**Confidence:** High

**Status:** IN PROGRESS — staged on branch coo/action-execution-batch-02-2026-09-30 pending PR CI.

**Reopen Conditions:** Reopen if CI identifies schema, graph, security, projection, or evidence-contract incompatibility.


## DECISION-2026-09-30-CODE-BATCH-01

**Topic:** Begin 05-code stub modernization in controlled batches.

**Decision:** Modernize ten code skills at a time, preserving repository conventions, security gates, explicit acceptance criteria, and evidence requirements.

**Status:** IN PROGRESS — staged on branch coo/code-batch-01-2026-09-30 pending PR CI.


## DECISION-2026-09-30-CODE-BATCH-02

**Topic:** Continue controlled 05-code stub modernization.

**Decision:** Modernize the next ten code skills with repository-backed procedures and synchronized Agent Skills projections, without weakening validation, security, or evidence requirements.

**Status:** IN PROGRESS — staged on branch coo/code-batch-02-2026-09-30 pending PR CI.

**Reopen Conditions:** Reopen if CI identifies schema, graph, security, projection, or evidence-contract incompatibility.


## DECISION-2026-09-30-CODE-BATCH-03

**Topic:** Continue 05-code modernization after batch 02.

**Decision:** Modernize the next available code skills with explicit runnable guidance, synchronized projections where permitted, and unchanged repository quality gates. Blocked connector writes are not bypassed.

**Status:** IN PROGRESS — staged on branch coo/code-batch-03-2026-09-30 pending PR CI.

**Reopen Conditions:** Reopen if CI identifies schema, graph, projection, evidence, or documentation incompatibility.


## DECISION-2026-09-30-TOOL-USE-BATCH-01

**Topic:** Begin controlled 07-tool-use stub modernization.

**Decision:** Modernize ten tool-use skills with explicit contracts, runnable guidance, synchronized Agent Skills projections, and unchanged quality/security gates.

**Status:** IN PROGRESS — staged pending PR CI.


## DECISION-2026-09-30-TOOL-USE-BATCH-02

**Topic:** Continue controlled 07-tool-use stub modernization.

**Decision:** Modernize the next ten tool-use skills with explicit contracts, runnable examples, evidence references, synchronized Agent Skills projections, and unchanged repository quality/security gates.

**Scope:** image-gen-tool, jira-api, linear-api, maps-geolocation, mcp-tool, news-api, notion-api, pdf-tool, sendgrid-api, slack-api.

**Status:** IN PROGRESS — staged on branch coo/tool-use-batch-02-2026-09-30 pending PR CI.

**Reopen Conditions:** Reopen if CI identifies schema, graph, security, projection, evidence, or documentation incompatibility.


## DECISION-2026-09-30-TOOL-USE-BATCH-03

**Topic:** Continue controlled 07-tool-use stub modernization.

**Decision:** Modernize the next ten tool-use skills with explicit contracts, runnable examples, evidence references, synchronized Agent Skills projections, and unchanged repository quality/security gates.

**Scope:** github-api, google-workspace-api, huggingface-api, sql-tool, stripe-api, twilio-api, vector-db-tool, weather-api, web-search, wikipedia-api.

**Status:** IN PROGRESS — staged on branch coo/tool-use-batch-03-2026-09-30 pending PR CI.

**Reopen Conditions:** Reopen if CI identifies schema, graph, security, projection, evidence, or documentation incompatibility.


## DECISION-2026-10-01-DOMAIN-SPECIFIC-BATCH-01

**Decision:** Begin controlled modernization of the 16-domain-specific stub cluster.

**Scope:** First ten skills listed in the live category inventory.

**Status:** IN PROGRESS — staged on coo/domain-specific-batch-01-2026-10-01 pending CI.

**Constraint:** Domain-specific skills must preserve scope, evidence, uncertainty, and applicable professional-domain boundaries; no validator or security gate may be weakened.


## DECISION-2026-10-01-DOMAIN-SPECIFIC-BATCH-02

**Decision:** Continue controlled modernization of the remaining 16-domain-specific stub cluster.

**Scope:** flashcard-creation, hypothesis-generation, iac-generation, incident-response, invoice-processing, legal-research, lesson-plan, literature-review, log-analysis, and medical-literature-search.

**Status:** IN PROGRESS — staged on `coo/domain-specific-batch-02-2026-10-01` pending CI.

**Constraint:** Preserve source traceability, uncertainty, applicable professional-domain boundaries, and unchanged validation/security gates.


## DECISION-2026-10-01-DOMAIN-SPECIFIC-BATCH-03

**Decision:** Complete the 16-domain-specific stub modernization.

**Scope:** paper-summarization, portfolio-analysis, product-description, quiz-generation, review-analysis, seo-optimization, stock-lookup, and symptom-analysis.

**Status:** IN PROGRESS — staged on `coo/domain-specific-batch-03-2026-10-01` pending CI.

**Constraint:** Preserve source traceability, uncertainty, professional-domain boundaries, and unchanged validation/security gates.


## DECISION-2026-10-01-COMPUTER-USE-BATCH-01

**Decision:** Begin controlled modernization of the `10-computer-use` stub cluster.

**Scope:** accessibility-tree, app-launch, clipboard-read, clipboard-write, double-click, drag-drop, file-dialog, keyboard-shortcut, keyboard-type, and mouse-click.

**Status:** IN PROGRESS — staged on `coo/computer-use-batch-01-2026-10-01` pending CI.

**Constraint:** Computer-use skills must require target verification, authorization, bounded actions, sensitive-data protection, and postcondition checks; no validator or security gate may be weakened.


## DECISION-2026-10-01-COMPUTER-USE-BATCH-02

**Decision:** Complete the remaining `10-computer-use` stub modernization in a second controlled batch.

**Scope:** mouse-move, multi-monitor, right-click, screen-ocr, screenshot-capture, scroll, terminal-interaction, visual-element-detection, vm-interaction, and window-management.

**Status:** IN PROGRESS — staged on `coo/computer-use-batch-02-2026-10-01` pending CI.

**Constraint:** Require target/session verification, bounded actions, sensitive-data protection, authorization, and postcondition checks; no validator or security gate may be weakened.


## DECISION-2026-10-01-DATA-BATCH-01

**Decision:** Begin controlled modernization of the `12-data` stub cluster.

**Scope:** anomaly-detection, csv-processing, data-aggregation, data-cleaning, data-filtering, data-joining, data-summarization, data-visualization, etl-pipeline, and json-transformation.

**Status:** IN PROGRESS — staged on `coo/data-batch-01-2026-10-01` pending CI.

**Constraint:** Preserve source provenance, explicit schemas, validation, data-loss boundaries, and unchanged validation/security gates.


## DECISION-2026-10-01-DATA-BATCH-02

**Decision:** Complete the remaining `12-data` stub modernization while preserving the existing battle-tested embedding skill.

**Scope:** nosql-query, pandas-operations, schema-inference, similarity-search, sql-execution, statistical-analysis, and time-series.

**Status:** IN PROGRESS — staged on `coo/data-batch-02-2026-10-01` pending CI.

**Constraint:** Preserve explicit data contracts, validation, provenance, bounded execution, and unchanged validation/security gates.


## DECISION-2026-10-01-ORCHESTRATION-BATCH-01

**Decision:** Begin controlled modernization of the remaining `15-orchestration` stub cluster.

**Scope:** agent-communication, agent-handoff, budget-management, conditional-branching, consensus-voting, event-triggers, hierarchical-tree, logging-observability, parallel-execution, and retry-backoff.

**Status:** IN PROGRESS — staged on `coo/15-orchestration-batch-01-2026-10-01` pending CI.

**Constraint:** Preserve workflow state, ownership, authorization, idempotency, recovery, and evidence boundaries; no validator or security gate may be weakened.


## DECISION-2026-10-01-ORCHESTRATION-BATCH-02

**Decision:** Complete the remaining `15-orchestration` stub modernization while preserving existing battle-tested skills.

**Scope:** role-assignment, sequential-workflow, shared-memory, state-machine, subagent-spawning, and task-queue.

**Status:** IN PROGRESS — staged on `coo/15-orchestration-batch-02-2026-10-01` pending CI.

**Constraint:** Preserve workflow state, ownership, authority boundaries, recovery, idempotency, and evidence; no validator or security gate may be weakened.


## DECISION-2026-10-01-AGENTIC-PATTERNS-BATCH-01

**Decision:** Begin controlled modernization of the remaining stub-level agentic-pattern cluster.

**Scope:** tot, lats, mcts, rag-pipeline, reflection, critic-agent, self-play, constitutional-ai, debate-pattern, and mixture-of-agents.

**Status:** IN PROGRESS — staged on `coo/agentic-patterns-batch-01-2026-10-01` pending CI.

**Constraint:** Agentic patterns must state objective, evaluation criteria, budget, provenance, evidence boundary, uncertainty, and failure handling; no validator or security gate may be weakened.


## DECISION-2026-10-01-MULTIMODAL-BATCH-01

**Decision:** Begin controlled modernization of the remaining stub-level multimodal cluster.

**Scope:** 3d-scene-understanding, audio-classification, audio-transcription, chart-generation, document-layout-analysis, image-captioning, image-classification, image-editing, image-generation, object-detection, text-to-speech, video-description, video-frame-extraction, and vqa.

**Status:** IN PROGRESS — staged on `coo/multimodal-batch-01-2026-10-01` pending CI.

**Constraint:** Multimodal skills must define modality-specific inputs and outputs, bounded preprocessing/execution, provenance, uncertainty, failure handling, and safety boundaries; no validator or security gate may be weakened.


## DECISION-2026-10-01-AGENTIC-PATTERNS-BATCH-02

**Decision:** Complete the remaining stub-level agentic-patterns cluster.

**Scope:** bootstrapping, memory-augmented, subagent-delegation, and tool-use-loop.

**Status:** IN PROGRESS — staged on `coo/agentic-patterns-batch-02-2026-10-01` pending CI.

**Constraint:** Agentic patterns must state objective, evaluation criteria, budgets, provenance, evidence boundaries, uncertainty, and failure handling; no validator or security gate may be weakened.


## DECISION-2026-10-01-MEMORY-BATCH-01

**Decision:** Modernize the remaining placeholder-level memory skills with explicit state and verification contracts.

**Scope:** fact-verification-memory, fact-verification, procedural, user-profile, and working-memory.

**Status:** IN PROGRESS — staged on `coo/memory-batch-01-2026-10-01` pending CI.

**Constraint:** Memory must define scope, provenance, retention, freshness, conflict handling, uncertainty, and verification boundaries; no validator or security gate may be weakened.


## DECISION-2026-10-01-COMMUNICATION-BATCH-01

**Decision:** Begin controlled modernization of the remaining placeholder-level communication cluster.

**Scope:** argument-construction, citation-attribution, clarification-seeking, debate, email-drafting, instruction-following, multilingual-output, persona-adoption, question-answering, and report-writing.

**Status:** IN PROGRESS — staged on `coo/communication-batch-01-2026-10-01` pending CI.

**Constraint:** Communication skills must preserve evidence boundaries, user intent, explicit constraints, uncertainty, and safety/authority boundaries; no validator or security gate may be weakened.


## DECISION-2026-10-01-COMMUNICATION-BATCH-02

**Decision:** Complete the remaining placeholder-level communication cluster.

**Scope:** structured-output and tone-adjustment.

**Status:** IN PROGRESS — staged on `coo/communication-batch-02-2026-10-01` pending CI.

**Constraint:** Communication skills must preserve meaning, explicit constraints, evidence boundaries, and validation results; no validator or security gate may be weakened.


## DECISION-2026-10-01-WEB-BATCH-01

**Decision:** Begin controlled modernization of the first ten remaining placeholder-level web skills.

**Scope:** api-discovery, browser-navigation, captcha-solving, cookie-management, dom-inspection, form-filling, js-execution, link-extraction, rss-parsing, and sitemap-parsing.

**Status:** IN PROGRESS — staged on `coo/web-batch-01-2026-10-01` pending CI.

**Constraint:** Web automation must remain within authorization and must not bypass authentication, CAPTCHA/anti-bot controls, rate limits, robots restrictions, paywalls, or other access controls.


## DECISION-2026-10-01-WEB-BATCH-02

**Decision:** Complete the remaining placeholder-level web cluster.

**Scope:** url-fetching, url-screenshot, and web-login.

**Status:** IN PROGRESS — staged on `coo/web-batch-02-2026-10-01` pending CI.

**Constraint:** Web operations must stay within authorized origin/session boundaries and must not expose or bypass credentials, authentication, anti-bot controls, rate limits, robots restrictions, paywalls, or other access controls.


## DECISION-2026-10-01-COO-MISSION

**Decision-ID:** DECISION-2026-10-01-COO-MISSION

**Topic:** Adopt the AI COO master mission as the repository's strategic product-execution model.

**Decision:** Evolve Skills Tree from a raw AI skill registry toward trusted capability infrastructure optimized for utility, evidence, freshness, interoperability, provenance, reproducibility, security, machine discovery, and transparent public demand signals. Raw skill count and raw stub count are secondary engineering measurements, not product objectives.

**Evidence IDs:** LIVE-MAIN-20261001, AI-CONSTITUTION, AGENTS, COO-MASTER-MISSION, ROADMAP, EVIDENCE-MODEL

**Confidence:** HIGH

**Status:** LOCKED

**Reopen Conditions:** Reopen only if the Human Owner/CEO changes the strategic product direction or repository evidence demonstrates that the objective is producing the wrong product outcome.

**Implementation:** `meta/COO_MASTER_MISSION.md`, `meta/ROADMAP.md`, `meta/EVIDENCE_MODEL.md`, and `meta/MOST-WANTED-SKILLS.md` establish the authoritative execution surfaces. Existing migration decisions remain historical execution records unless explicitly superseded by a later decision.

## DECISION-2026-10-01-GENERATED-MAIN-SERIALIZATION

**Decision-ID:** DECISION-2026-10-01-GENERATED-MAIN-SERIALIZATION

**Topic:** Unify generated-main writer concurrency.

**Decision:** All verified repository workflows that directly commit generated projections or maintenance output to `main` must use the shared `auto-commit-main` concurrency group with `cancel-in-progress: false`. Workflow-specific serialization groups are not sufficient for cross-workflow writers.

**Evidence:** Live workflow inventory on 2026-10-01 identified six direct-main writers with workflow-specific groups: `generate-search-index.yml`, `leaderboard.yml`, `used-in-tracker.yml`, `version-stats.yml`, `weekly-highlights.yml`, and `revoke-phantom-badges.yml`. PR #213 changed only those concurrency controls and passed Test Suite, PR Checks, Security Scan, Build & Verify Wheel, and Auto Label.

**Status:** LOCKED — implementation merged as PR #213 at `42bc204a944cb27ee42f0b626592a48a1d4b92e1`.

**Reopen Conditions:** Reopen if a new generated-main writer cannot safely share the semaphore, or if the repository adopts a different serialized generation architecture with equal or stronger guarantees.


## DECISION-2026-10-01-EVIDENCE-RUNTIME-INTEGRATION

**Decision-ID:** DECISION-2026-10-01-EVIDENCE-RUNTIME-INTEGRATION

**Topic:** Integrate typed Evidence access into the UniversalRegistry facade.

**Context:** Evidence was already a first-class, contract-validated registry entity with a dedicated `EvidenceRuntime`, but consumers of `UniversalRegistry` still had to depend on the internal registry JSON layout to resolve or enumerate Evidence.

**Decision:** Integrate the existing `EvidenceRuntime` into `UniversalRegistry` and expose deterministic `resolve_evidence()` and `evidence_for_entity()` access. Preserve existing validation, provenance semantics, read-only behavior, and registry claims.

**Evidence:** `meta/POST_P2_2_EVIDENCE_RUNTIME_AUDIT.md`; PR #223; exact-head CI green; merge commit `642e968879e9b6bfc8e7f9b2a44d12544585fc18`.

**Alternatives:** Continue exposing raw registry data; rejected because it leaks storage representation and weakens the runtime abstraction boundary. Create a second Evidence runtime facade; rejected because the repository already has `EvidenceRuntime`.

**Status:** LOCKED

**Reopen Conditions:** Reopen only if a replacement runtime architecture supersedes the current facade or tests demonstrate an abstraction/integrity regression.

## DECISION-2026-10-01-COMPATIBILITY-RUNTIME-INTEGRATION

**Decision-ID:** DECISION-2026-10-01-COMPATIBILITY-RUNTIME-INTEGRATION

**Topic:** Integrate typed Compatibility access into the UniversalRegistry facade.

**Context:** Compatibility was already a contract-validated registry entity with a dedicated CompatibilityRuntime, but UniversalRegistry.compatibility_for() directly traversed raw registry JSON. Consumers therefore had to depend on storage representation or construct the runtime independently.

**Decision:** Integrate the existing CompatibilityRuntime into UniversalRegistry, expose deterministic typed resolve_compatibility(), and route compatibility_for() through the validated runtime.

**Alternatives:** Continue raw access — rejected because it leaks storage representation. Create another compatibility facade — rejected because the repository already has CompatibilityRuntime.

**Evidence:** PR #227; exact-head CI green; merge commit `ba9682b26ea59b18f21eb017b6f239f735c4dec3`.

**Status:** LOCKED

**Reopen Conditions:** Reopen if verification exposes an abstraction or integrity regression, or if a replacement runtime architecture supersedes the current facade.


## DECISION-2026-10-01-WORKFLOW-GOVERNANCE-INVENTORY

**Decision-ID:** DECISION-2026-10-01-WORKFLOW-GOVERNANCE-INVENTORY

**Decision:** Treat the 42 workflows present on live `main` on 2026-10-01 as the authoritative Phase 0 workflow inventory. Preserve one Pages authority and one production release authority. Treat generated-main writers as a high-risk automation class requiring least privilege, deterministic output, serialization, bounded retry/rebase, and failure visibility.

**Key findings:** `zero-touch-release.yml` is the production release authority; `release.yml` is manual recovery; `deploy-pages.yml` is the single repository-controlled Pages deployment; `release-package.yml` is supporting catalog packaging. `validate-graph.yml` is the next concrete permission-boundary hardening candidate because its combined PR/main job grants write permissions not required by the PR validation path.

**Evidence:** live workflow inventory and source inspection on 2026-10-01; existing generated-main serialization decision; GitHub Actions permission documentation.

**Status:** LOCKED baseline; permission hardening remains OPEN.


## DECISION-2026-10-02-VALIDATE-GRAPH-PERMISSION-ISOLATION

**Decision-ID:** DECISION-2026-10-02-VALIDATE-GRAPH-PERMISSION-ISOLATION

**Topic:** Isolate validate-graph read-only validation from trusted-main generated writes.

**Decision:** Keep the graph validation job strictly read-only with `contents: read`. Isolate generated graph materialization to a dedicated `generate-main-graph` job with `contents: write`, restricted to pushes of trusted `main` and dependent on successful validation. Keep the quality projection writer dependent on graph generation to prevent same-workflow writer races. Preserve the repository-wide `auto-commit-main` serialization group and existing deterministic graph generation semantics.

**Security rationale:** The previous combined workflow job granted write permissions to the PR validation path, including `pull-requests: write`, although validation does not require them. The new boundary follows least privilege and limits write capability to the trusted-main projection jobs.

**Evidence:** PR #232; merged commit `d89bb26bfd3e55f513b3c07e6ebb5ee2f84ba85b`; Security Scan, PR Checks, Test Suite, Build & Verify Wheel, and Auto Label passed on the PR head; live `.github/workflows/validate-graph.yml` inspection after merge.

**Status:** LOCKED

**Reopen Conditions:** Reopen if deterministic generation, validation ordering, writer serialization, or least-privilege assumptions are contradicted by repository evidence or a replacement generation architecture is adopted.
