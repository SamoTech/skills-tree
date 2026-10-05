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
Decision: Skill validation must be read-only. Dependency changes may merge through the repository CI-gated merge rule when the exact HEAD passes required validation, security, tests, and invariants; no separate maintainer approval is required unless a higher-priority control-plane rule applies.
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


## DECISION-2026-10-02-SKILL-RUNTIME-FACADE-INTEGRATION

**Decision-ID:** DECISION-2026-10-02-SKILL-RUNTIME-FACADE-INTEGRATION

**Topic:** Route canonical Skill access through the existing validated SkillRuntime facade.

**Decision:** Integrate the existing read-only `SkillRuntime` into `UniversalRegistry`. Expose `resolve_skill()` and `capabilities_for_skill()`, and delegate `implementations_for_skill()` to the runtime. Preserve canonicality enforcement, deterministic ordering, defensive snapshots, existing registry validation, and the no-new-claims boundary.

**Rationale:** The repository already had a dedicated, tested Skill runtime, but the UniversalRegistry facade still bypassed it with direct registry storage access. This was an abstraction-boundary inconsistency analogous to the previously corrected Evidence and Compatibility gaps.

**Evidence:** `meta/POST_P2_2_SKILL_RUNTIME_AUDIT_20260919.md`; PR #234; exact-head CI green; merge commit `37b2a529555db2e5db34713ffcb8e3b72083cfb5`.

**Status:** LOCKED

**Reopen Conditions:** Reopen if tests or repository evidence demonstrate a regression in canonicality, deterministic behavior, snapshot isolation, import architecture, or facade/runtime consistency, or if a replacement runtime architecture supersedes this boundary.


## DECISION-2026-10-02-CAPABILITY-RUNTIME-FACADE-INTEGRATION

**Decision-ID:** DECISION-2026-10-02-CAPABILITY-RUNTIME-FACADE-INTEGRATION

**Topic:** Route Capability access through the existing validated CapabilityRuntime facade.

**Decision:** Integrate the existing read-only `CapabilityRuntime` into `UniversalRegistry`. Expose `resolve_capability()`, `implementations_for_capability()`, and `adapters_for_capability()`. Preserve deterministic traversal, defensive snapshots, existing registry validation, and the no-new-claims boundary.

**Rationale:** The repository already had a dedicated, tested Capability runtime, but the UniversalRegistry facade lacked typed Capability access. This was the remaining counterpart to the corrected Skill, Evidence, and Compatibility facade boundaries.

**Evidence:** `meta/IMPLEMENTATION_ONTOLOGY.md`; PR #236; exact-head CI green; merge commit `8fc4dc8f6423b6b39ec2218f077a9d153b4560da`.

**Status:** LOCKED

**Reopen Conditions:** Reopen if tests or repository evidence demonstrate a regression in deterministic traversal, snapshot isolation, import architecture, or facade/runtime consistency, or if a replacement runtime architecture supersedes this boundary.


## DECISION-2026-10-02-GOAL-RUNTIME-FACADE-INTEGRATION

**Decision-ID:** DECISION-2026-10-02-GOAL-RUNTIME-FACADE-INTEGRATION

**Topic:** Establish a typed Goal runtime boundary for the UniversalRegistry facade.

**Decision:** Add a read-only deterministic `GoalRuntime` and route `UniversalRegistry.resolve_goal()` and `skills_for_goal()` through it. Reuse the validated Capability and Skill runtime boundaries for Goal traversal. Preserve defensive snapshots, deterministic ordering, existing registry validation, and the no-new-claims boundary.

**Rationale:** Goal was the remaining public UniversalRegistry access path implemented directly against registry storage after Skill, Capability, Evidence, and Compatibility facade boundaries had been normalized.

**Evidence:** `meta/IMPLEMENTATION_ONTOLOGY.md`; PR #238; exact-head CI green; merge commit `3290ebc88060fca07e944cd31ad31d392982ca3d`.

**Status:** LOCKED

**Reopen Conditions:** Reopen if tests or repository evidence demonstrate a regression in deterministic traversal, snapshot isolation, import architecture, or facade/runtime consistency, or if a replacement runtime architecture supersedes this boundary.


## DECISION-2026-10-02-UNIVERSAL-REGISTRY-DATA-SCHEMA-RUNTIME-VALIDATION

**Decision-ID:** DECISION-2026-10-02-UNIVERSAL-REGISTRY-DATA-SCHEMA-RUNTIME-VALIDATION

**Topic:** Validate the UniversalRegistry seed against a schema governing the actual serialized registry data.

**Finding:** The runtime previously validated semantic integrity and entity-specific contracts but lacked a first structural schema boundary for the loaded registry document. The existing `meta/universal-registry.schema.json` was initially considered for this purpose, but CI and contract tests demonstrated that it defines the registry ontology/contract vocabulary rather than the `registry/universal_registry.json` instance shape.

**Decision:** Introduce `meta/universal-registry-data.schema.json` as the normative schema for the serialized registry seed. Validate it immediately after JSON load. Resolve the dedicated Implementation and Adapter contracts through an explicit local JSON Schema resource registry. Preserve existing semantic validation after structural validation.

**Evidence:** PR #241; final implementation head `8ad05dfc995db49da847ea479e06e13bec80d2e1`; exact-head Security Scan, PR Checks, Test Suite, and Build & Verify Wheel passed; squash merge `93c50c3616a7c558b483f341f44a91509ed032ca`.

**Status:** LOCKED.

**Reopen Conditions:** Reopen if the serialized registry shape changes without corresponding schema evolution, schema/runtime drift is detected, cross-schema resolution becomes nondeterministic, or a replacement registry architecture supersedes this boundary.


## DECISION-2026-10-02-SECURITY-SKILL-MIGRATION-BATCH-01

**Decision-ID:** DECISION-2026-10-02-SECURITY-SKILL-MIGRATION-BATCH-01

**Topic:** Upgrade the remaining security-category stubs as the first corpus-quality migration batch.

**Decision:** Migrate all nine category-14 security stubs under the existing evidence-backed gate. Require explicit descriptions, I/O contracts, runnable examples, failure modes, related metadata, and authoritative references. Do not add unsupported benchmark or compliance claims.

**Evidence:** PR #243; final head `a76f44379b1fba4a6667e9efce04a5db6c912d97`; final validation matrix green; squash merge `40fb35aa6c54438f08062c89c118815262b6fe98`.

**Status:** LOCKED.

## DECISION-2026-10-02-QUALITY-REPORT-POST-MERGE-TRIGGER

**Decision-ID:** DECISION-2026-10-02-QUALITY-REPORT-POST-MERGE-TRIGGER

**Topic:** Ensure generated skill-quality state is regenerated after merged PRs.

**Finding:** The live `quality-report.yml` declared a `push: main` publication trigger, but no post-merge quality run was observable after the API-driven security batch merge. The generated report therefore remained at the pre-merge 374/170/159/45/0 classification even though the nine security skill bodies had passed the quality-report workflow before the metadata correction.

**Decision:** Add a trusted `pull_request_target: closed` trigger limited to `main`, and execute the existing publish job only when `github.event.pull_request.merged == true`. The workflow checks out the default branch and never checks out or executes PR head code.

**Security basis:** GitHub documents that `pull_request_target` runs workflow code from the default branch and can safely perform trusted post-merge automation when untrusted PR code is not executed. The trigger is constrained to closed PRs and a merged condition.

**Evidence:** GitHub Actions regenerated `meta/QUALITY-REPORT.md` as commit `ac8aacb5982018d2ee57a2953924dd74a9013e20` after merged PR #244. The generated report verifies 374 skills: 202 battle-tested, 159 enriched, 13 stubs, 0 invalid.

**Status:** LOCKED.


## DECISION-2026-10-02-GOAL-CAPABILITY-RUNTIME-ACCESS

**Decision-ID:** DECISION-2026-10-02-GOAL-CAPABILITY-RUNTIME-ACCESS

**Topic:** Expose typed Goal-to-Capability traversal through the UniversalRegistry runtime.

**Finding:** The canonical ontology defines the Goal → Capability → Skill traversal, and `GoalRuntime` already provides Goal resolution and Goal-to-Skill traversal, but consumers had no typed `capabilities_for_goal()` accessor and therefore could fall back to the raw Goal record structure for the immediate relationship.

**Decision:** Add deterministic read-only `GoalRuntime.capabilities_for_goal()`, expose `UniversalRegistry.capabilities_for_goal()`, and make `skills_for_goal()` reuse the validated Capability boundary. Preserve defensive snapshots, deterministic ordering, existing validation, and the no-new-claims boundary.

**Confidence:** HIGH

**Evidence IDs:** `meta/IMPLEMENTATION_ONTOLOGY.md`, `meta/DEVELOPMENT_KNOWLEDGE.md`, `registry/goal.py`, `tests/test_universal_registry_runtime.py`

**Status:** IN VERIFICATION — implementation merged to the development branch; exact-head CI pending.

**Reopen Conditions:** Reopen if repository tests or architecture evidence show that Goal-to-Capability is intentionally excluded from typed runtime traversal, or if the runtime boundary introduces non-deterministic, mutable, or duplicated relationship behavior.


# DECISION-2026-10-02-AI-SOURCE-DISCOVERY

DECISION-ID: DECISION-2026-10-02-AI-SOURCE-DISCOVERY
Topic: Make Skills Tree directly discoverable as a public AI skill source

Decision: Add a root `llms.txt`, an AI discovery guide, and explicit README/AGENTS retrieval instructions that point agents to the generated `docs/api/skills.json` registry, canonical `skills/` source, and compatible `agent-skills/` projections. Keep `skills/` canonical and do not declare the future `/.well-known/agent-skills/index.json` live until its deterministic generation, validation, provenance, reproducibility, and SHA-256 integrity gates exist.

Confidence: HIGH

Evidence IDs: DECISION-004, docs/AGENT_SKILLS_DISTRIBUTION.md, meta/COO_MASTER_MISSION.md, meta/ROADMAP.md, agent-skills/skills-tree-registry/SKILL.md

Status: LOCKED

Reopen Conditions: Reopen if the Agent Skills distribution contract or canonical source-of-truth architecture changes.


# DECISION-2026-10-02-PRODUCT-MISSION

**Decision-ID:** DECISION-2026-10-02-PRODUCT-MISSION

**Topic:** Establish the governing product mission for Skills Tree.

**Decision:** The primary product mission is:

> **Skills Tree is a public, trusted, machine-discoverable source of AI skills. AI agents should be able to find the right skill here, and humans should be able to discover, understand, use, share, and contribute skills easily.**

All active product, architecture, roadmap, documentation, distribution, and automation work must align with this mission.

**Product outcomes:** AI discovery; human discovery and use; reliable consumption; sharing and contribution; organic GitHub discovery and adoption through genuine utility.

**Source-of-truth rule:** `skills/` remains canonical. `docs/api/skills.json` and `agent-skills/` remain projections. No generated artifact may become a competing catalog.

**Trust rule:** Public discoverability must not be represented as proof of safety, production readiness, popularity, adoption, or universal applicability. Claims require evidence.

**Growth rule:** “Viral on GitHub” is treated as a product objective to build the conditions for organic discovery, reuse, sharing, and contribution. It is not a claim or guaranteed outcome, and the repository must not fabricate engagement signals.

**Canonical document:** `meta/PRODUCT_MISSION.md`.

**Confidence:** HIGH

**Status:** LOCKED

**Reopen Conditions:** Reopen only if the Human Owner changes the product direction or repository evidence demonstrates that this mission no longer produces the intended product outcome.


## DECISION-2026-10-02-DETERMINISTIC-AGENT-SKILLS-PROJECTION

**Decision-ID:** DECISION-2026-10-02-DETERMINISTIC-AGENT-SKILLS-PROJECTION

**Topic:** Establish the executable canonical-to-Agent-Skills projection contract.

**Decision:** Keep `skills/` as the sole canonical source and introduce a deterministic projection tool that derives standards-compatible `agent-skills/<name>/SKILL.md` packages only from canonical entries that pass explicit evidence, description, naming, collision, and size gates. CI performs a read-only corpus audit; generation requires an explicit write mode and refuses blocked entries. Do not publish `/.well-known/agent-skills/index.json` until generated artifacts, provenance, validation, reproducibility, and SHA-256 integrity are verified together.

**Evidence:** PR #251; merge commit `f1d169c3fd9388cf4244d9d4bfc4c64df382a1bb`; exact-head CI matrix; `tools/generate_agent_skills.py`; `tools/generate_agent_skills.py`; `tests/test_generate_agent_skills.py`; `docs/AGENT_SKILLS_DISTRIBUTION.md`; `SECURITY.md`; `meta/PRODUCT_MISSION.md`.

**Status:** LOCKED — executable contract verified and merged as PR #251; full-corpus projection is not yet claimed.

**Reopen Conditions:** Reopen if the Agent Skills specification changes materially, canonical skill metadata becomes structurally incompatible, generated projections cannot remain deterministic, or security evidence requires a stronger publication boundary.


## DECISION-2026-10-02-AGENT-SKILLS-CORPUS-RECONCILIATION

**Decision-ID:** DECISION-2026-10-02-AGENT-SKILLS-CORPUS-RECONCILIATION

**Topic:** Reconcile the existing Agent Skills packages against the canonical registry before deterministic generation.

**Decision:** Treat `skills/` as the sole canonical source. Reconcile existing `agent-skills/` packages by canonical provenance first, explicit legacy aliases second, and package-name inference only when provenance is absent. Resolve canonical name collisions deterministically with category-qualified projection names. Preserve blocked existing packages and the intentional `skills-tree-registry` auxiliary package rather than silently deleting them.

**Evidence:** Reconciliation tooling and CI; PR #253 control-plane merge; final corpus PR #264; verified final `main` state contains 288 packages with 250 eligible projections, 37 retained blocked existing packages, and one intentional auxiliary package.

**Status:** LOCKED

**Reopen Conditions:** Reopen if the canonical source-of-truth model changes, the Agent Skills specification changes materially, or provenance evidence demonstrates an incorrect mapping.

## DECISION-2026-10-02-AGENT-SKILLS-PROJECTION-SAFETY-GATES

**Decision-ID:** DECISION-2026-10-02-AGENT-SKILLS-PROJECTION-SAFETY-GATES

**Topic:** Make deterministic Agent Skills generation compatible with validation and repository hygiene gates.

**Decision:** Generated projections must use collision-safe package names, rewrite renamed package frontmatter to match directory names, remove secret-shaped credential literals from canonical examples, normalize trailing whitespace in projections, pass Agent Skills validation, and pass `git diff --check`. Canonical source files remain authoritative; normalization is projection-only except for canonical examples that violate repository security validation.

**Evidence:** PR #260 fixed collision-safe projection naming; PR #261 fixed rename frontmatter and a secret-shaped canonical example; PR #263 normalized projection whitespace. All three exact-head CI matrices passed before merge.

**Status:** LOCKED

**Reopen Conditions:** Reopen if the Agent Skills specification, repository validator, or canonical content contract changes and requires a stronger or different projection boundary.

## DECISION-2026-10-02-AGENT-SKILLS-CORPUS-COMPLETION

**Decision-ID:** DECISION-2026-10-02-AGENT-SKILLS-CORPUS-COMPLETION

**Topic:** Establish the verified deterministic Agent Skills corpus baseline.

**Decision:** The current eligible Agent Skills corpus is the deterministic projection of all canonical skills that pass the repository projection gates. The verified baseline is 374 canonical entries scanned, 250 eligible projections generated, 124 canonical entries blocked, and 288 total Agent Skills packages retained on `main` including blocked legacy packages and the intentional registry helper.

**Evidence:** Generation run for PR #264 reported exactly 250 generated eligible canonical packages; the generation job passed reconciliation, Agent Skills validation, and `git diff --check`; final PR checks passed Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, PR Checks, Agent Skills Distribution Audit, and graph validation. Merge commit: `892a4d747e588cf2876e45ba3effcdd031fd9592`.

**Status:** LOCKED

**Reopen Conditions:** Reopen if canonical eligibility rules change, Agent Skills specification changes materially, or a later reproducible audit finds corpus drift.


## DECISION-2026-10-03-ANTI-SLOP-QUALITY-GATE

**Decision-ID:** DECISION-2026-10-03-ANTI-SLOP-QUALITY-GATE

**Topic:** Enforce deterministic anti-slop quality rules on changed canonical skills.

**Finding:** Existing schema, quality, evidence, provenance, and security gates did not explicitly reject selected low-information placeholder and marketing filler in newly changed skill prose.

**Decision:** Add a deterministic changed-skill anti-slop gate. Block selected placeholder and marketing-filler patterns; warn on unsupported absolute and generic value claims; ignore fenced code and frontmatter; include renamed skills in changed-file detection; and keep placeholder matching case-sensitive so legitimate lowercase lifecycle states such as `todo` are not rejected.

**Evidence:** PR #273 with targeted review-fix PR #275; final #273 head `4477d33d846c68d71b666e6c283c8787312e023f`; required CI matrix passed before merge as `90f9422954936e054adc630ad723e6165074492c`.

**Scope boundary:** The gate is changed-skill enforcement. Historical corpus findings require a separate evidence-driven migration and are not silently reclassified by this decision.

**Status:** LOCKED

**Reopen Conditions:** Reopen if deterministic false positives/negatives materially undermine the gate, the canonical skill contract changes, or a replacement content-quality architecture is adopted.

# DECISION-2026-10-03-BEHAVIORAL-EVALUATION-RUNTIME

**Decision-ID:** DECISION-2026-10-03-BEHAVIORAL-EVALUATION-RUNTIME

**Topic:** Establish the smallest universal-registry boundary for reproducible behavioral evaluation.

**Finding:** Provenance, Evidence, registry integrity, memory-safety skills, and action-governance skills are already represented and validated at their existing boundaries. Benchmarks are already a first-class registry collection, but they were covered only by the generic entity schema and had no dedicated typed runtime facade.

**Decision:** Add a dedicated Benchmark contract and read-only runtime boundary without adding benchmark records or external claims. Require task, inputs, expected behavior, evaluation criteria, test data, methodology, historical results, and provenance; optionally scope a benchmark to explicit entity subjects. Expose deterministic resolve_benchmark() and benchmarks_for_entity() access through UniversalRegistry.

**Confidence:** HIGH

**Evidence IDs:** meta/POST_20261003_BEHAVIORAL_EVALUATION_AUDIT.md, meta/ROADMAP.md, meta/EVIDENCE_MODEL.md, registry/runtime.py, meta/universal-registry-data.schema.json

**Status:** LOCKED — merged and exact-head CI verified.

**Reopen Conditions:** Reopen if repository evidence shows Benchmark is intentionally excluded from typed runtime consumption, if the benchmark contract conflicts with an authoritative existing contract, or if tests reveal non-deterministic or mutable runtime behavior.


# DECISION-2026-10-03-REGISTRY-FRESHNESS-BOUNDARY

**Decision-ID:** DECISION-2026-10-03-REGISTRY-FRESHNESS-BOUNDARY

**Topic:** Expose existing freshness semantics through the universal registry without forcing a corpus-wide migration.

**Finding:** The evidence model defines last reviewed, review due, freshness basis, and known stale conditions, but the universal registry generic entity contract and runtime had no normalized freshness boundary.

**Decision:** Add an optional schema-validated freshness object to universal registry entities and expose deterministic read-only `freshness_for_entity()` access. Preserve legacy entities without freshness declarations and reject internally inconsistent freshness timestamps. Do not calculate a trust/freshness score or infer currentness from wall-clock time.

**Evidence:** `meta/EVIDENCE_MODEL.md`, `meta/ROADMAP.md`, `meta/POST_20261003_FRESHNESS_RUNTIME_AUDIT.md`, `meta/universal-registry-data.schema.json`, `registry/runtime.py`, and focused regression tests.

**Status:** VERIFIED — PR #281 merged as `a26a1dabac28da3cc598ad85ddf655b8b1b5b108`; exact-head validation passed before merge.

**Reopen Conditions:** Reopen if repository evidence shows freshness is intentionally excluded from universal registry consumption, if the evidence model changes, or if a stronger versioned freshness contract supersedes this boundary.


## DECISION-2026-10-03-UNIVERSAL-GRAPH-RELATIONSHIP-BOUNDARY

**Decision-ID:** DECISION-2026-10-03-UNIVERSAL-GRAPH-RELATIONSHIP-BOUNDARY

**Topic:** Fail closed on Universal Graph relationship types that are declared by schema but not yet semantically implemented by runtime.

**Finding:** The Universal Graph schema intentionally declares a broader relationship vocabulary than the current graph data uses. Repository architecture documentation says deferred relationships require deterministic generation and validation rules before introduction. The runtime previously accepted unsupported schema-valid relationship types through a silent fallback path.

**Decision:** Keep the declared schema vocabulary unchanged as the forward-compatible contract, but make the runtime-supported relationship set explicit and reject every schema-valid relationship without an implemented semantic validator. Do not invent semantics for deferred relationships.

**Evidence:** `meta/POST_20261003_GRAPH_RELATIONSHIP_RUNTIME_AUDIT.md`, `meta/universal-graph.schema.json`, `docs/architecture/UNIVERSAL_REGISTRY_AUDIT.md`, `registry/runtime.py`, and `tests/test_graph_relationship_integrity.py`.

**Status:** VERIFIED ON BRANCH — implementation and focused regression coverage are present; exact-head CI and merge remain pending.

**Reopen Conditions:** Reopen when repository evidence justifies introducing a deferred relationship and provides explicit endpoint semantics, deterministic generation rules, provenance requirements, and behavioral tests.


## DECISION-2026-10-03-AUTOMATED-CI-MERGE-AUTHORIZATION

**Decision-ID:** DECISION-2026-10-03-AUTOMATED-CI-MERGE-AUTHORIZATION

**Topic:** Pull-request merge authorization

**Decision:** For normal repository pull requests, a verified exact HEAD that passes the required CI/test/security gates and satisfies the documented engineering invariants is sufficient authorization for merge. A separate human approval is not required unless an explicit repository control-plane rule or higher-priority decision requires it.

**Evidence:** User/CEO-CIO decision recorded 2026-10-03; PR #283 exact-head CI passed and was merged without human review as c8e1c536f8abfd860ddf41cefeff15b88518d095; AI_CONSTITUTION.md; AGENTS.md.

**Status:** VERIFIED — operating policy adopted and documentation update prepared.

**Reopen Conditions:** Reopen if the Human Owner changes this policy, repository control-plane rules require approval, or evidence shows automated gates are insufficient for a specific change class.


# DECISION-2026-10-03-DOCUMENTATION-SYNCHRONIZATION-GATE

**Decision-ID:** DECISION-2026-10-03-DOCUMENTATION-SYNCHRONIZATION-GATE

**Topic:** Make authoritative documentation synchronization a mandatory agent execution gate.

**Finding:** The live implementation and generated quality report had advanced beyond stale operational snapshots and roadmap queue entries. Existing governance already required documentation, but the pre-execution behavior was not explicit enough to force agents to verify and reconcile documentation before unrelated work.

**Decision:** Require every agent performing meaningful repository work to complete a live Documentation Preflight: read the authoritative governance/state documents, verify current-state and roadmap claims against live main, implementation, generated artifacts, and recent CI/PR evidence, synchronize drift before unrelated feature work, re-read the affected documents, and only then execute. Unresolved documentation drift prevents a task from being reported COMPLETE.

**Evidence:** AI_CONSTITUTION.md, AGENTS.md, meta/CURRENT-STATE.md, meta/ROADMAP.md, meta/QUALITY-REPORT.md, and live main commit af176a061abfa84401176043cd04ad2704736f47.

**Status:** LOCKED.

**Reopen Conditions:** Reopen only if the repository adopts a stronger equivalent documentation-control mechanism or the authoritative source-of-truth architecture changes.


# DECISION-2026-10-03-PYPI-RELEASE-CONTRACT
DECISION-ID: DECISION-2026-10-03-PYPI-RELEASE-CONTRACT
Topic: PyPI release documentation follows the executable zero-touch pipeline
Decision: Treat `.github/workflows/zero-touch-release.yml` and `pyproject.toml` as the authoritative release implementation. `meta/PYPI_RELEASE_PLAN.md` must describe semantic-release, tag/version verification, wheel verification, GitHub OIDC Trusted Publishing, and the `pypi` environment. Historical API-token/manual-publish instructions must not be presented as current procedure.
Confidence: HIGH
Evidence IDs: PYPI-RELEASE-WORKFLOW-20261003, PYPROJECT-20261003
Status: LOCKED
Reopen Conditions: Reopen only if the executable release workflow or versioning architecture changes.


# DECISION-2026-10-03-OPERATIONAL-STATE-RECONCILIATION

DECISION-ID: DECISION-2026-10-03-OPERATIONAL-STATE-RECONCILIATION
Topic: Current operational documentation follows merged runtime and consumer state
Decision: Treat merged PR state and live implementation as the current execution source. PR #283's Universal Graph fail-closed boundary is merged; PR #292's recommendation registry context and PR #293's blueprint registry context are merged; PR #294 reconciled the PyPI release contract. Historical records that describe these slices as pending remain historical and must not determine current execution state. The next engineering slice is a fresh audit of remaining machine-readable discovery projections and the canonical search pipeline before implementing Issue #86.
Confidence: HIGH
Evidence: live `main` ref verified at the cycle start; PR #283, PR #292, PR #293, and PR #294; `docs/AI_DISCOVERY.md`; `docs/api.md`; `docs/cli.md`
Status: LOCKED
Reopen Conditions: Reopen if live implementation, merged PR state, or authoritative architecture changes.

# DECISION-2026-10-03-GRAPH-STATUS-RECONCILIATION

DECISION-ID: DECISION-2026-10-03-GRAPH-STATUS-RECONCILIATION
Topic: Universal Graph relationship runtime decision status
Decision: The Universal Graph fail-closed relationship boundary is a merged implementation, not a pending branch-only change. The historical branch status remains historical; current status is verified on main at merge commit c8e1c536f8abfd860ddf41cefeff15b88518d095.
Confidence: HIGH
Evidence IDs: PR-283, tests/test_graph_relationship_integrity.py, registry/runtime.py
Status: LOCKED
Reopen Conditions: Reopen if a later graph architecture change supersedes or modifies the supported relationship set.


# DECISION-2026-10-03-SEARCH-PROJECTION-CONTRACT

DECISION-ID: DECISION-2026-10-03-SEARCH-PROJECTION-CONTRACT
Topic: Search projection integrity before CLI search
Decision: Establish `docs/search-index.json` as a validated generated projection, not an independent catalog. The projection is governed by `meta/search-index.schema.json`; tests require unique IDs, canonical file resolution, and exact path parity with `docs/api/skills.json`. A stale projection entry was detected for `skills/15-orchestration/kanban-task-management.md` and reconciled before merge. CLI search remains deferred until the installed-wheel/source-checkout runtime data boundary is audited.
Confidence: HIGH
Evidence: PR #296 merged as `c66def14c5c21f348275978042e8c9d07ad43086`; exact-head Test Suite, Security Scan, Build & Verify Wheel, PR Checks, and Auto Label passed.
Status: LOCKED
Reopen Conditions: Reopen if search projection format, canonical source, packaging contract, or runtime consumer architecture changes.

# DECISION-2026-10-03-SEARCH-PACKAGING-BOUNDARY

DECISION-ID: DECISION-2026-10-03-SEARCH-PACKAGING-BOUNDARY
Topic: Make the canonical generated search projection consumable by the installable CLI
Decision: Keep the generated search corpus single-source in content and format. The existing builder produces identical bytes for the static web projection at docs/search-index.json and the package runtime projection at data/search-index.json. cli/search_runtime.py owns only deterministic artifact discovery/loading, resolving the source checkout asset or the installed wheel data directory. It does not define a second index, parser, or ranking algorithm.
Confidence: HIGH
Evidence: tools/build_search_index.py, pyproject.toml data-files, .github/workflows/generate-search-index.yml, .github/workflows/build-and-verify.yml, tests/test_search_index_contract.py, cli/search_runtime.py.
Status: VERIFIED — PR #298 merged as `8c5de33d2f3fb6054b122c9f52f381257066993f`; exact-head Test Suite, Security Scan, Build & Verify Wheel, PR Checks, Validate Skills Graph, and Auto Label passed.
Reopen Conditions: Reopen if packaging cannot reliably deliver the projection, if source/package bytes diverge, or if a different authoritative search data contract supersedes this boundary.



# DECISION-2026-10-03-CLI-SEARCH-RANKING-CONTRACT

DECISION-ID: DECISION-2026-10-03-CLI-SEARCH-RANKING-CONTRACT
Topic: Deterministic CLI search behavior over the canonical generated search projection

Finding: The repository contains a validated generated search corpus and an installable runtime loader, but no existing Python ranking implementation or verified web ranking semantics that can be reused. Issue #86 requires ranked keyword search without specifying ranking behavior.

Decision: Implement one deterministic lexical consumer over the canonical generated documents. Tokenize Unicode words with case-folding; use OR matching across title, tags, category, description, and body; weight fields 8/6/4/3/1 respectively; count each distinct query token at most once per field; sort by descending score, case-folded title, then canonical ID; default to 20 results with a 1–100 limit; return stable result fields and existing CLI output formats. Do not add a second index, parser, embedding layer, fuzzy matching, trust score, or undocumented filters.

Evidence: meta/SEARCH_CLI_CONTRACT.md, cli/search_engine.py, cli/search_runtime.py, tests/test_search_engine.py, tests/test_search_cli.py, tools/build_search_index.py, and Issue #86.

Status: VERIFIED — PR #299 merged as `7302d0780b2857bdd2f54363a2e6158eafc45292`. Exact-head Test Suite, Security Scan, Build & Verify Wheel, PR Checks, and Auto Label passed. The wheel gate also executed `skills-tree search` from the installed wheel successfully.

Reopen Conditions: Reopen if verified canonical search behavior appears elsewhere, the generated search projection changes shape, or evidence shows this lexical contract does not satisfy the authoritative CLI requirement.


# DECISION-2026-10-03-DISCOVERY-REGISTRY-CONTEXT

DECISION-ID: DECISION-2026-10-03-DISCOVERY-REGISTRY-CONTEXT
Topic: Optional UniversalRegistry context in the generated machine-readable skill discovery projection

Finding: docs/api/skills.json is generated directly from canonical skills/ and did not expose the already-verified UniversalRegistry context. The UniversalRegistry currently covers only three canonical skills, so projecting context for the full corpus would require inventing unsupported registry membership or evidence.

Decision: Add optional registry_context only when a canonical skill has an exact registry skill record. Project canonical ID/version, canonical flag, capability IDs, implementation IDs, evidence IDs derived from explicit Evidence.supports, declared provenance, and declared freshness when present. Leave unregistered skills without synthetic context. Keep docs/search-index.json a search corpus rather than a second registry catalog.

Evidence: tools/export_skills.py, registry/universal_registry.json, registry/runtime.py, docs/api/skills.json, docs/api/skills-schema.json, tests/test_export_registry_context.py, docs/DISCOVERY_REGISTRY_CONTEXT.md.

Status: VERIFIED — PR #300 merged as `4ff041511f2291e826b2a32c2cc72f36f8f023cb`. Final head `52ae305ad504416114d7efdd8313eff8f931f57d` passed Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, PR Checks, Validate Skills Graph, and Auto Label. The wheel gate also executed installed CLI search successfully.

Reopen Conditions: Reopen if UniversalRegistry coverage becomes corpus-wide, the discovery projection becomes a runtime registry consumer, or an authoritative machine-readable discovery contract supersedes this projection boundary.


# DECISION-2026-10-03-DISCOVERY-DATE-PROJECTION-RECONCILIATION

DECISION-ID: DECISION-2026-10-03-DISCOVERY-DATE-PROJECTION-RECONCILIATION
Topic: Correct canonical date metadata and reconcile generated API projections

Finding: `skills/15-orchestration/kanban-task-management.md` had correct YAML frontmatter but malformed legacy body metadata combining Added and Last Updated on one line. The exporter consumed that body value and produced an invalid `added` value in docs/api/skills.json and docs/api/skills.yaml.

Decision: Correct the canonical source metadata, add a regression test, then reconcile the affected generated JSON/YAML projections. Do not weaken the schema to accept malformed source metadata. Keep generated artifacts subordinate to the canonical source and existing export workflow.

Evidence: PR #301 merged as `ff3943efeb49e40466b3bc408c87b4de820c1728`; PR #302 merged as `32cee4e430dc5c8ebf495e84048fd15e1e5404d2`. PR #301 exact-head CI passed the full applicable validation matrix; PR #302 passed Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, and PR Checks. Main artifacts now report `added: 2026-10` and `last_updated: 2026-10` for the affected skill.

Status: VERIFIED — MAIN

Reopen Conditions: Reopen if the export workflow regenerates a divergent value, if the exporter changes its source precedence, or if another canonical skill exhibits the same cross-field metadata contamination pattern.


# DECISION-2026-10-04-AGENT-SKILLS-RECONCILIATION-GATE

DECISION-ID: DECISION-2026-10-04-AGENT-SKILLS-RECONCILIATION-GATE
Topic: Make canonical-to-Agent-Skills reconciliation a hard CI invariant

Finding: The existing reconciler classified eligible missing projections but its default command returned success regardless of those findings. This allowed a newly eligible canonical skill to be absent from the deterministic Agent Skills projection without failing the distribution workflow.

Decision: Preserve the existing canonical projection and collision-resolution architecture and enforce it through a read-only `--check` mode. The check fails for eligible missing projections, deterministic projection drift, stale or ambiguous provenance, unexpected packages outside the explicit auxiliary boundary, and duplicate target names after deterministic collision resolution. `rename_needed` remains compatibility metadata and is not a standalone failure; an eligible canonical source with only a legacy package still fails until its deterministic projection exists. Resolved source-name collisions remain valid when category-qualified target names are unique. No second generator, index, or semantic search system is introduced.

Confidence: HIGH

Evidence IDs: PR-305, TOOLS-RECONCILE-AGENT-SKILLS, TESTS-AGENT-SKILLS-RECONCILIATION, WORKFLOW-AGENT-SKILLS-DISTRIBUTION

Status: VERIFIED — PR #305 exact head `1c1d70a337f9952cd2c24d555ee9d67bab9cbe30` passed the applicable CI checks and merged to main as `a9a649481c68bf0dd33447a2238174ebd8b79a4b`.

Reopen Conditions: Reopen only if the canonical eligibility model, Agent Skills naming/provenance contract, reconciliation semantics, or publication architecture changes materially, or if reproducible evidence demonstrates a false positive or false negative in the gate.


## 2026-10-04 Release Workflow Reconciliation

The previous `release-package.yml` catalog-package publisher is no longer active. Catalog packaging is now part of the authoritative `zero-touch-release.yml` release job. `release.yml` remains manual recovery only. Historical audit references to the deleted workflow are retained as historical evidence and must not be treated as current executable architecture.

# DECISION-2026-10-04-SELF-ENFORCED-GOVERNANCE
DECISION-ID: DECISION-2026-10-04-SELF-ENFORCED-GOVERNANCE
Topic: Repository governance without GitHub branch protection
Decision: Do not require GitHub branch protection, required human approvals, or GitHub rulesets as a prerequisite for repository correctness or completion. The authoritative merge gate is exact-head automated validation plus documented architectural invariants, security checks, and documentation synchronization. Enforce these requirements from repository-local agent instructions and CI so the governance model remains reproducible from a clean checkout.
Confidence: HIGH
Evidence IDs: AI_CONSTITUTION.md, AGENTS.md, meta/GOVERNANCE_MODEL.md, tools/verify_governance.py, .github/workflows/governance-gate.yml
Status: LOCKED
Reopen Conditions: Reopen only if the owner explicitly chooses a control-plane governance model or repository-local automation proves insufficient for a concrete safety/correctness requirement.


# DECISION-2026-10-04-CORE-AGENTIC-EXECUTION-LOOP
DECISION-ID: DECISION-2026-10-04-CORE-AGENTIC-EXECUTION-LOOP
Topic: Make bounded agentic execution the repository's core operational behavior
Decision: AI agents operating on Skills Tree must execute meaningful work as a bounded evidence-driven loop: OBSERVE → ASSESS → PLAN → EXECUTE → VERIFY → RECORD → DECIDE. Verification failures, regressions, CI failures, and documentation drift become inputs to subsequent cycles. Agents continue autonomously when a safe evidence-backed next action exists, stop as BLOCKED when it does not, and select DONE only after the goal, invariants, tests/CI, generated artifacts, documentation, and final audit are verified. The loop has a default 12-iteration ceiling and must not expose private chain-of-thought. This augments the existing lifecycle and does not create a competing orchestration system.
Confidence: HIGH
Evidence IDs: AI_CONSTITUTION.md, AGENTS.md, meta/AGENT_OPERATING_MODEL.md, tools/verify_governance.py
Status: VERIFIED — PR #324 merged to main as `6fa92dd42768395102215a26e22999d6de81c013`; exact-head governance, graph, test, security, build, and PR validation passed.
Reopen Conditions: Reopen if a stronger repository-native agent orchestration contract supersedes this loop, if bounded execution proves insufficient for real repository work, or if the authority/escalation model changes.


# DECISION-2026-10-04-MAIN-WRITER-SERIALIZATION
DECISION-ID: DECISION-2026-10-04-MAIN-WRITER-SERIALIZATION
Topic: Prevent stale-SHA races among automated main writers
Finding: Post-merge verification of PR #324 exposed a real race: the graph writer advanced main while the quality projection and zero-touch release workflows still operated from the original triggering SHA. Graph generation succeeded, but quality failed on a stale upstream SHA and zero-touch release failed when upstream main changed.
Decision: Treat direct-main generated/release automation as one serialized writer class. Use the shared `auto-commit-main` concurrency group with `cancel-in-progress: false`; synchronize stale event checkouts to live `origin/main` before generation or release mutation; keep `skills/` canonical and generated outputs subordinate projections. The graph writer remains the sole graph projection writer. Do not solve the defect with branch protection or human approval.
Confidence: HIGH
Evidence IDs: PR-324, workflow run 37223742787, workflow run 37223742707, meta/GOVERNANCE_MODEL.md, .github/workflows/validate-graph.yml, .github/workflows/zero-touch-release.yml
Status: VERIFIED — PR #325 merged to main as `0892cfe20130368ad12655a8ec71616ae97027fd`; exact-head Governance Gate, Graph, Tests, Security, Build, and PR validation passed. Post-merge writer execution completed without the prior stale-SHA failure.
Reopen Conditions: Reopen if a post-merge writer race, stale-SHA mutation, generated-projection divergence, or release concurrency defect remains after the new contract is merged and verified.


# DECISION-2026-10-04-MAIN-WRITER-QUEUE
DECISION-ID: DECISION-2026-10-04-MAIN-WRITER-QUEUE
Topic: Preserve pending automated main-writer runs
Finding: After the writer-race fix was merged, the zero-touch release run was cancelled while waiting on the shared writer concurrency boundary. GitHub Actions concurrency permits only one pending run by default; a newer pending run can replace an older one.
Decision: The repository-wide `auto-commit-main` writer group must use `queue: max` with `cancel-in-progress: false`, so pending generated/release writers are retained and processed sequentially. Writers still synchronize to live `origin/main` before mutation because queue ordering alone does not make an event SHA current.
Confidence: HIGH
Evidence IDs: post-merge main commit `0892cfe20130368ad12655a8ec71616ae97027fd`, workflow run 37223991086, GitHub Actions concurrency documentation.
Status: VERIFIED — PR #326 merged to main; exact-head Governance Gate, Graph, Tests, Security, Build, and PR validation passed. Post-merge Zero-Touch Release completed successfully and pending writer runs were retained by the lossless queue.
Reopen Conditions: Reopen if pending writer runs are still lost, if queue pressure exceeds the repository's acceptable automation latency, or if a stronger repository-native writer scheduler replaces this mechanism.


# DECISION-2026-10-04-DEMAND-SIGNAL-REVIEW
DECISION-ID: DECISION-2026-10-04-DEMAND-SIGNAL-REVIEW
Topic: First controlled demand-intelligence evidence cohort
Finding: The first configured public GitHub issue-search collection returned raw result counts of 64, 63, and 54 across three overlapping query groups. Review of the returned issues identified capability signals for search/discovery, memory, code/IDE integration, reasoning, and action execution. The result sets also contain operational/security issues, demonstrating why raw query volume cannot be used as a demand score.
Decision: Treat these as an unranked evidence cohort. Reconcile each capability against canonical coverage, evidence tier, freshness, dependencies, and implementation gaps before selecting migration priorities. Search/discovery is already implemented and verified and must not be reimplemented merely because issue #86 is a historical demand signal.
Confidence: MEDIUM-HIGH
Evidence IDs: meta/demand-sources.json, tools/collect_demand_signals.py, .github/workflows/demand-signals.yml, issues #86, #87, #88, #90, #91, controlled GitHub issue-search run 2026-10-04.
Status: VERIFIED OBSERVATION — prioritization intentionally deferred until coverage/evidence reconciliation.
Reopen Conditions: Reopen if a stronger public-signal source invalidates the cohort, if the collector proves non-reproducible, or if current canonical coverage materially changes.


# DECISION-2026-10-04-IDE-INTEGRATION-MIGRATION
DECISION-ID: DECISION-2026-10-04-IDE-INTEGRATION-MIGRATION
Topic: First demand/evidence-driven Phase 3 migration
Finding: The controlled demand review surfaced issue #88 requesting IDE integration patterns, pair-programming protocols, and polyglot-agent support. Coverage reconciliation found no dedicated canonical IDE integration skill under `05-code`, while the repository already has adjacent code-generation, code-review, execution, Git, API, and debugging skills. Current public documentation and implementations also demonstrate a real agent↔IDE capability boundary via MCP and IDE-native APIs.
Decision: Implement one canonical `05-code/ide-integration.md` skill as the first Phase 3 slice. Keep it protocol-neutral, least-privilege, workspace-scoped, and independently verifiable. Do not create separate vendor-specific skills until evidence demonstrates distinct reusable contracts.
Confidence: HIGH
Evidence IDs: issue #88, skills/05-code directory audit, GitHub Copilot MCP documentation, public AgentBridge implementation, current Skills Tree governance and evidence model.
Status: IMPLEMENTED — exact-head CI and projection verification required before merge.
Reopen Conditions: Reopen if CI finds an existing canonical duplicate, evidence quality proves insufficient, the capability cannot be expressed as a reusable contract, or vendor-specific semantics require a distinct skill.

# DECISION-2026-10-05-EVALUATION-EVIDENCE-GATE-RECONCILIATION
DECISION-ID: DECISION-2026-10-05-EVALUATION-EVIDENCE-GATE-RECONCILIATION
Topic: Reconcile evaluation validation with canonical corpus and historical retrieval evidence
Finding: The evaluation validator was checking the obsolete `data/corpus/` location while authoritative corpus entries live under `intelligence/corpus/entries/`. The evaluation ontology contains seven mappings, while P0 capabilities CAP-007, CAP-011, and CAP-014 remain unmapped. The retrieval benchmark `benchmarks/memory/retrieval-accuracy.md` has historical results without a current version-matched run artifact.
Decision: Keep `intelligence/ontology/evaluation_ontology.json` and the existing Benchmark contract/runtime as authoritative evaluation boundaries. Correct `validate-evaluations.yml` to inspect the canonical corpus path, surface missing P0 mappings, and validate declared freshness metadata without rewriting review dates. Qualify the stale retrieval benchmark as historical and do not claim current retrieval quality until reproducible evidence is recorded. Do not create a second evaluation framework or search implementation.
Evidence IDs: live main `a61af71fc4e47593bd430039a9362d4ae31756ce`; `meta/EVIDENCE_MODEL.md`; `intelligence/ontology/evaluation_ontology.json`; `intelligence/corpus/entries/`; Issue #335; Issue #336; `benchmarks/memory/retrieval-accuracy.md`.
Status: IMPLEMENTED ON BRANCH — exact-head CI verification pending.
Reopen Conditions: Reopen if the canonical corpus/evaluation paths change, the Benchmark contract is superseded, current reproducible benchmark evidence becomes available, or a concrete retrieval-ranking failure case is measured.
