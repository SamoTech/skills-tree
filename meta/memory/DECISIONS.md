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

**Status:** IN PROGRESS â Batches 01â06 merged; current generated quality report verified at 121 battle-tested, 16 enriched, 237 stubs, 0 invalid.

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

**Status:** IN PROGRESS â staged on branch coo/action-execution-batch-01-2026-09-30 pending PR CI.

**Reopen Conditions:** Reopen if validation reveals schema, security, projection, or evidence-contract incompatibility.


## DECISION-2026-09-30-ACTION-EXECUTION-BATCH-02

**Topic:** Complete the remaining 04-action-execution stub modernization.

**Decision:** Convert the remaining nine action-execution stubs into evidence-backed canonical skills with standards-compatible Agent Skills projections. Preserve explicit target verification, authorization, bounds, secret handling, and postcondition checks.

**Confidence:** High

**Status:** IN PROGRESS â staged on branch coo/action-execution-batch-02-2026-09-30 pending PR CI.

**Reopen Conditions:** Reopen if CI identifies schema, graph, security, projection, or evidence-contract incompatibility.


## DECISION-2026-09-30-CODE-BATCH-01

**Topic:** Begin 05-code stub modernization in controlled batches.

**Decision:** Modernize ten code skills at a time, preserving repository conventions, security gates, explicit acceptance criteria, and evidence requirements.

**Status:** IN PROGRESS â staged on branch coo/code-batch-01-2026-09-30 pending PR CI.


## DECISION-2026-09-30-CODE-BATCH-02

**Topic:** Continue controlled 05-code stub modernization.

**Decision:** Modernize the next ten code skills with repository-backed procedures and synchronized Agent Skills projections, without weakening validation, security, or evidence requirements.

**Status:** IN PROGRESS â staged on branch coo/code-batch-02-2026-09-30 pending PR CI.

**Reopen Conditions:** Reopen if CI identifies schema, graph, security, projection, or evidence-contract incompatibility.


## DECISION-2026-09-30-CODE-BATCH-03

**Topic:** Continue 05-code modernization after batch 02.

**Decision:** Modernize the next available code skills with explicit runnable guidance, synchronized projections where permitted, and unchanged repository quality gates. Blocked connector writes are not bypassed.

**Status:** IN PROGRESS â staged on branch coo/code-batch-03-2026-09-30 pending PR CI.

**Reopen Conditions:** Reopen if CI identifies schema, graph, projection, evidence, or documentation incompatibility.


## DECISION-2026-09-30-TOOL-USE-BATCH-01

**Topic:** Begin controlled 07-tool-use stub modernization.

**Decision:** Modernize ten tool-use skills with explicit contracts, runnable guidance, synchronized Agent Skills projections, and unchanged quality/security gates.

**Status:** IN PROGRESS â staged pending PR CI.


## DECISION-2026-09-30-TOOL-USE-BATCH-02

**Topic:** Continue controlled 07-tool-use stub modernization.

**Decision:** Modernize the next ten tool-use skills with explicit contracts, runnable examples, evidence references, synchronized Agent Skills projections, and unchanged repository quality/security gates.

**Scope:** image-gen-tool, jira-api, linear-api, maps-geolocation, mcp-tool, news-api, notion-api, pdf-tool, sendgrid-api, slack-api.

**Status:** IN PROGRESS â staged on branch coo/tool-use-batch-02-2026-09-30 pending PR CI.

**Reopen Conditions:** Reopen if CI identifies schema, graph, security, projection, evidence, or documentation incompatibility.


## DECISION-2026-09-30-TOOL-USE-BATCH-03

**Topic:** Continue controlled 07-tool-use stub modernization.

**Decision:** Modernize the next ten tool-use skills with explicit contracts, runnable examples, evidence references, synchronized Agent Skills projections, and unchanged repository quality/security gates.

**Scope:** github-api, google-workspace-api, huggingface-api, sql-tool, stripe-api, twilio-api, vector-db-tool, weather-api, web-search, wikipedia-api.

**Status:** IN PROGRESS â staged on branch coo/tool-use-batch-03-2026-09-30 pending PR CI.

**Reopen Conditions:** Reopen if CI identifies schema, graph, security, projection, evidence, or documentation incompatibility.


## DECISION-2026-10-01-DOMAIN-SPECIFIC-BATCH-01

**Decision:** Begin controlled modernization of the 16-domain-specific stub cluster.

**Scope:** First ten skills listed in the live category inventory.

**Status:** IN PROGRESS â staged on coo/domain-specific-batch-01-2026-10-01 pending CI.

**Constraint:** Domain-specific skills must preserve scope, evidence, uncertainty, and applicable professional-domain boundaries; no validator or security gate may be weakened.


## DECISION-2026-10-01-DOMAIN-SPECIFIC-BATCH-02

**Decision:** Continue controlled modernization of the remaining 16-domain-specific stub cluster.

**Scope:** flashcard-creation, hypothesis-generation, iac-generation, incident-response, invoice-processing, legal-research, lesson-plan, literature-review, log-analysis, and medical-literature-search.

**Status:** IN PROGRESS â staged on `coo/domain-specific-batch-02-2026-10-01` pending CI.

**Constraint:** Preserve source traceability, uncertainty, applicable professional-domain boundaries, and unchanged validation/security gates.


## DECISION-2026-10-01-DOMAIN-SPECIFIC-BATCH-03

**Decision:** Complete the 16-domain-specific stub modernization.

**Scope:** paper-summarization, portfolio-analysis, product-description, quiz-generation, review-analysis, seo-optimization, stock-lookup, and symptom-analysis.

**Status:** IN PROGRESS â staged on `coo/domain-specific-batch-03-2026-10-01` pending CI.

**Constraint:** Preserve source traceability, uncertainty, professional-domain boundaries, and unchanged validation/security gates.


## DECISION-2026-10-01-COMPUTER-USE-BATCH-01

**Decision:** Begin controlled modernization of the `10-computer-use` stub cluster.

**Scope:** accessibility-tree, app-launch, clipboard-read, clipboard-write, double-click, drag-drop, file-dialog, keyboard-shortcut, keyboard-type, and mouse-click.

**Status:** IN PROGRESS â staged on `coo/computer-use-batch-01-2026-10-01` pending CI.

**Constraint:** Computer-use skills must require target verification, authorization, bounded actions, sensitive-data protection, and postcondition checks; no validator or security gate may be weakened.


## DECISION-2026-10-01-COMPUTER-USE-BATCH-02

**Decision:** Complete the remaining `10-computer-use` stub modernization in a second controlled batch.

**Scope:** mouse-move, multi-monitor, right-click, screen-ocr, screenshot-capture, scroll, terminal-interaction, visual-element-detection, vm-interaction, and window-management.

**Status:** IN PROGRESS â staged on `coo/computer-use-batch-02-2026-10-01` pending CI.

**Constraint:** Require target/session verification, bounded actions, sensitive-data protection, authorization, and postcondition checks; no validator or security gate may be weakened.


## DECISION-2026-10-01-DATA-BATCH-01

**Decision:** Begin controlled modernization of the `12-data` stub cluster.

**Scope:** anomaly-detection, csv-processing, data-aggregation, data-cleaning, data-filtering, data-joining, data-summarization, data-visualization, etl-pipeline, and json-transformation.

**Status:** IN PROGRESS â staged on `coo/data-batch-01-2026-10-01` pending CI.

**Constraint:** Preserve source provenance, explicit schemas, validation, data-loss boundaries, and unchanged validation/security gates.


## DECISION-2026-10-01-DATA-BATCH-02

**Decision:** Complete the remaining `12-data` stub modernization while preserving the existing battle-tested embedding skill.

**Scope:** nosql-query, pandas-operations, schema-inference, similarity-search, sql-execution, statistical-analysis, and time-series.

**Status:** IN PROGRESS â staged on `coo/data-batch-02-2026-10-01` pending CI.

**Constraint:** Preserve explicit data contracts, validation, provenance, bounded execution, and unchanged validation/security gates.


## DECISION-2026-10-01-ORCHESTRATION-BATCH-01

**Decision:** Begin controlled modernization of the remaining `15-orchestration` stub cluster.

**Scope:** agent-communication, agent-handoff, budget-management, conditional-branching, consensus-voting, event-triggers, hierarchical-tree, logging-observability, parallel-execution, and retry-backoff.

**Status:** IN PROGRESS â staged on `coo/15-orchestration-batch-01-2026-10-01` pending CI.

**Constraint:** Preserve workflow state, ownership, authorization, idempotency, recovery, and evidence boundaries; no validator or security gate may be weakened.


## DECISION-2026-10-01-ORCHESTRATION-BATCH-02

**Decision:** Complete the remaining `15-orchestration` stub modernization while preserving existing battle-tested skills.

**Scope:** role-assignment, sequential-workflow, shared-memory, state-machine, subagent-spawning, and task-queue.

**Status:** IN PROGRESS â staged on `coo/15-orchestration-batch-02-2026-10-01` pending CI.

**Constraint:** Preserve workflow state, ownership, authority boundaries, recovery, idempotency, and evidence; no validator or security gate may be weakened.


## DECISION-2026-10-01-AGENTIC-PATTERNS-BATCH-01

**Decision:** Begin controlled modernization of the remaining stub-level agentic-pattern cluster.

**Scope:** tot, lats, mcts, rag-pipeline, reflection, critic-agent, self-play, constitutional-ai, debate-pattern, and mixture-of-agents.

**Status:** IN PROGRESS â staged on `coo/agentic-patterns-batch-01-2026-10-01` pending CI.

**Constraint:** Agentic patterns must state objective, evaluation criteria, budget, provenance, evidence boundary, uncertainty, and failure handling; no validator or security gate may be weakened.


## DECISION-2026-10-01-MULTIMODAL-BATCH-01

**Decision:** Begin controlled modernization of the remaining stub-level multimodal cluster.

**Scope:** 3d-scene-understanding, audio-classification, audio-transcription, chart-generation, document-layout-analysis, image-captioning, image-classification, image-editing, image-generation, object-detection, text-to-speech, video-description, video-frame-extraction, and vqa.

**Status:** IN PROGRESS â staged on `coo/multimodal-batch-01-2026-10-01` pending CI.

**Constraint:** Multimodal skills must define modality-specific inputs and outputs, bounded preprocessing/execution, provenance, uncertainty, failure handling, and safety boundaries; no validator or security gate may be weakened.


## DECISION-2026-10-01-AGENTIC-PATTERNS-BATCH-02

**Decision:** Complete the remaining stub-level agentic-patterns cluster.

**Scope:** bootstrapping, memory-augmented, subagent-delegation, and tool-use-loop.

**Status:** IN PROGRESS â staged on `coo/agentic-patterns-batch-02-2026-10-01` pending CI.

**Constraint:** Agentic patterns must state objective, evaluation criteria, budgets, provenance, evidence boundaries, uncertainty, and failure handling; no validator or security gate may be weakened.


## DECISION-2026-10-01-MEMORY-BATCH-01

**Decision:** Modernize the remaining placeholder-level memory skills with explicit state and verification contracts.

**Scope:** fact-verification-memory, fact-verification, procedural, user-profile, and working-memory.

**Status:** IN PROGRESS â staged on `coo/memory-batch-01-2026-10-01` pending CI.

**Constraint:** Memory must define scope, provenance, retention, freshness, conflict handling, uncertainty, and verification boundaries; no validator or security gate may be weakened.


## DECISION-2026-10-01-COMMUNICATION-BATCH-01

**Decision:** Begin controlled modernization of the remaining placeholder-level communication cluster.

**Scope:** argument-construction, citation-attribution, clarification-seeking, debate, email-drafting, instruction-following, multilingual-output, persona-adoption, question-answering, and report-writing.

**Status:** IN PROGRESS â staged on `coo/communication-batch-01-2026-10-01` pending CI.

**Constraint:** Communication skills must preserve evidence boundaries, user intent, explicit constraints, uncertainty, and safety/authority boundaries; no validator or security gate may be weakened.


## DECISION-2026-10-01-COMMUNICATION-BATCH-02

**Decision:** Complete the remaining placeholder-level communication cluster.

**Scope:** structured-output and tone-adjustment.

**Status:** IN PROGRESS â staged on `coo/communication-batch-02-2026-10-01` pending CI.

**Constraint:** Communication skills must preserve meaning, explicit constraints, evidence boundaries, and validation results; no validator or security gate may be weakened.


## DECISION-2026-10-01-WEB-BATCH-01

**Decision:** Begin controlled modernization of the first ten remaining placeholder-level web skills.

**Scope:** api-discovery, browser-navigation, captcha-solving, cookie-management, dom-inspection, form-filling, js-execution, link-extraction, rss-parsing, and sitemap-parsing.

**Status:** IN PROGRESS â staged on `coo/web-batch-01-2026-10-01` pending CI.

**Constraint:** Web automation must remain within authorization and must not bypass authentication, CAPTCHA/anti-bot controls, rate limits, robots restrictions, paywalls, or other access controls.


## DECISION-2026-10-01-WEB-BATCH-02

**Decision:** Complete the remaining placeholder-level web cluster.

**Scope:** url-fetching, url-screenshot, and web-login.

**Status:** IN PROGRESS â staged on `coo/web-batch-02-2026-10-01` pending CI.

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

**Status:** LOCKED â implementation merged as PR #213 at `42bc204a944cb27ee42f0b626592a48a1d4b92e1`.

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

**Alternatives:** Continue raw access â rejected because it leaks storage representation. Create another compatibility facade â rejected because the repository already has CompatibilityRuntime.

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

**Finding:** The canonical ontology defines the Goal â Capability â Skill traversal, and `GoalRuntime` already provides Goal resolution and Goal-to-Skill traversal, but consumers had no typed `capabilities_for_goal()` accessor and therefore could fall back to the raw Goal record structure for the immediate relationship.

**Decision:** Add deterministic read-only `GoalRuntime.capabilities_for_goal()`, expose `UniversalRegistry.capabilities_for_goal()`, and make `skills_for_goal()` reuse the validated Capability boundary. Preserve defensive snapshots, deterministic ordering, existing validation, and the no-new-claims boundary.

**Confidence:** HIGH

**Evidence IDs:** `meta/IMPLEMENTATION_ONTOLOGY.md`, `meta/DEVELOPMENT_KNOWLEDGE.md`, `registry/goal.py`, `tests/test_universal_registry_runtime.py`

**Status:** IN VERIFICATION â implementation merged to the development branch; exact-head CI pending.

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

**Growth rule:** âViral on GitHubâ is treated as a product objective to build the conditions for organic discovery, reuse, sharing, and contribution. It is not a claim or guaranteed outcome, and the repository must not fabricate engagement signals.

**Canonical document:** `meta/PRODUCT_MISSION.md`.

**Confidence:** HIGH

**Status:** LOCKED

**Reopen Conditions:** Reopen only if the Human Owner changes the product direction or repository evidence demonstrates that this mission no longer produces the intended product outcome.


## DECISION-2026-10-02-DETERMINISTIC-AGENT-SKILLS-PROJECTION

**Decision-ID:** DECISION-2026-10-02-DETERMINISTIC-AGENT-SKILLS-PROJECTION

**Topic:** Establish the executable canonical-to-Agent-Skills projection contract.

**Decision:** Keep `skills/` as the sole canonical source and introduce a deterministic projection tool that derives standards-compatible `agent-skills/<name>/SKILL.md` packages only from canonical entries that pass explicit evidence, description, naming, collision, and size gates. CI performs a read-only corpus audit; generation requires an explicit write mode and refuses blocked entries. Do not publish `/.well-known/agent-skills/index.json` until generated artifacts, provenance, validation, reproducibility, and SHA-256 integrity are verified together.

**Evidence:** PR #251; merge commit `f1d169c3fd9388cf4244d9d4bfc4c64df382a1bb`; exact-head CI matrix; `tools/generate_agent_skills.py`; `tools/generate_agent_skills.py`; `tests/test_generate_agent_skills.py`; `docs/AGENT_SKILLS_DISTRIBUTION.md`; `SECURITY.md`; `meta/PRODUCT_MISSION.md`.

**Status:** LOCKED â executable contract verified and merged as PR #251; full-corpus projection is not yet claimed.

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

**Status:** LOCKED â merged and exact-head CI verified.

**Reopen Conditions:** Reopen if repository evidence shows Benchmark is intentionally excluded from typed runtime consumption, if the benchmark contract conflicts with an authoritative existing contract, or if tests reveal non-deterministic or mutable runtime behavior.


# DECISION-2026-10-03-REGISTRY-FRESHNESS-BOUNDARY

**Decision-ID:** DECISION-2026-10-03-REGISTRY-FRESHNESS-BOUNDARY

**Topic:** Expose existing freshness semantics through the universal registry without forcing a corpus-wide migration.

**Finding:** The evidence model defines last reviewed, review due, freshness basis, and known stale conditions, but the universal registry generic entity contract and runtime had no normalized freshness boundary.

**Decision:** Add an optional schema-validated freshness object to universal registry entities and expose deterministic read-only `freshness_for_entity()` access. Preserve legacy entities without freshness declarations and reject internally inconsistent freshness timestamps. Do not calculate a trust/freshness score or infer currentness from wall-clock time.

**Evidence:** `meta/EVIDENCE_MODEL.md`, `meta/ROADMAP.md`, `meta/POST_20261003_FRESHNESS_RUNTIME_AUDIT.md`, `meta/universal-registry-data.schema.json`, `registry/runtime.py`, and focused regression tests.

**Status:** VERIFIED â PR #281 merged as `a26a1dabac28da3cc598ad85ddf655b8b1b5b108`; exact-head validation passed before merge.

**Reopen Conditions:** Reopen if repository evidence shows freshness is intentionally excluded from universal registry consumption, if the evidence model changes, or if a stronger versioned freshness contract supersedes this boundary.


## DECISION-2026-10-03-UNIVERSAL-GRAPH-RELATIONSHIP-BOUNDARY

**Decision-ID:** DECISION-2026-10-03-UNIVERSAL-GRAPH-RELATIONSHIP-BOUNDARY

**Topic:** Fail closed on Universal Graph relationship types that are declared by schema but not yet semantically implemented by runtime.

**Finding:** The Universal Graph schema intentionally declares a broader relationship vocabulary than the current graph data uses. Repository architecture documentation says deferred relationships require deterministic generation and validation rules before introduction. The runtime previously accepted unsupported schema-valid relationship types through a silent fallback path.

**Decision:** Keep the declared schema vocabulary unchanged as the forward-compatible contract, but make the runtime-supported relationship set explicit and reject every schema-valid relationship without an implemented semantic validator. Do not invent semantics for deferred relationships.

**Evidence:** `meta/POST_20261003_GRAPH_RELATIONSHIP_RUNTIME_AUDIT.md`, `meta/universal-graph.schema.json`, `docs/architecture/UNIVERSAL_REGISTRY_AUDIT.md`, `registry/runtime.py`, and `tests/test_graph_relationship_integrity.py`.

**Status:** VERIFIED ON BRANCH â implementation and focused regression coverage are present; exact-head CI and merge remain pending.

**Reopen Conditions:** Reopen when repository evidence justifies introducing a deferred relationship and provides explicit endpoint semantics, deterministic generation rules, provenance requirements, and behavioral tests.


## DECISION-2026-10-03-AUTOMATED-CI-MERGE-AUTHORIZATION

**Decision-ID:** DECISION-2026-10-03-AUTOMATED-CI-MERGE-AUTHORIZATION

**Topic:** Pull-request merge authorization

**Decision:** For normal repository pull requests, a verified exact HEAD that passes the required CI/test/security gates and satisfies the documented engineering invariants is sufficient authorization for merge. A separate human approval is not required unless an explicit repository control-plane rule or higher-priority decision requires it.

**Evidence:** User/CEO-CIO decision recorded 2026-10-03; PR #283 exact-head CI passed and was merged without human review as c8e1c536f8abfd860ddf41cefeff15b88518d095; AI_CONSTITUTION.md; AGENTS.md.

**Status:** VERIFIED â operating policy adopted and documentation update prepared.

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
Status: VERIFIED â PR #298 merged as `8c5de33d2f3fb6054b122c9f52f381257066993f`; exact-head Test Suite, Security Scan, Build & Verify Wheel, PR Checks, Validate Skills Graph, and Auto Label passed.
Reopen Conditions: Reopen if packaging cannot reliably deliver the projection, if source/package bytes diverge, or if a different authoritative search data contract supersedes this boundary.



# DECISION-2026-10-03-CLI-SEARCH-RANKING-CONTRACT

DECISION-ID: DECISION-2026-10-03-CLI-SEARCH-RANKING-CONTRACT
Topic: Deterministic CLI search behavior over the canonical generated search projection

Finding: The repository contains a validated generated search corpus and an installable runtime loader, but no existing Python ranking implementation or verified web ranking semantics that can be reused. Issue #86 requires ranked keyword search without specifying ranking behavior.

Decision: Implement one deterministic lexical consumer over the canonical generated documents. Tokenize Unicode words with case-folding; use OR matching across title, tags, category, description, and body; weight fields 8/6/4/3/1 respectively; count each distinct query token at most once per field; sort by descending score, case-folded title, then canonical ID; default to 20 results with a 1â100 limit; return stable result fields and existing CLI output formats. Do not add a second index, parser, embedding layer, fuzzy matching, trust score, or undocumented filters.

Evidence: meta/SEARCH_CLI_CONTRACT.md, cli/search_engine.py, cli/search_runtime.py, tests/test_search_engine.py, tests/test_search_cli.py, tools/build_search_index.py, and Issue #86.

Status: VERIFIED â PR #299 merged as `7302d0780b2857bdd2f54363a2e6158eafc45292`. Exact-head Test Suite, Security Scan, Build & Verify Wheel, PR Checks, and Auto Label passed. The wheel gate also executed `skills-tree search` from the installed wheel successfully.

Reopen Conditions: Reopen if verified canonical search behavior appears elsewhere, the generated search projection changes shape, or evidence shows this lexical contract does not satisfy the authoritative CLI requirement.


# DECISION-2026-10-03-DISCOVERY-REGISTRY-CONTEXT

DECISION-ID: DECISION-2026-10-03-DISCOVERY-REGISTRY-CONTEXT
Topic: Optional UniversalRegistry context in the generated machine-readable skill discovery projection

Finding: docs/api/skills.json is generated directly from canonical skills/ and did not expose the already-verified UniversalRegistry context. The UniversalRegistry currently covers only three canonical skills, so projecting context for the full corpus would require inventing unsupported registry membership or evidence.

Decision: Add optional registry_context only when a canonical skill has an exact registry skill record. Project canonical ID/version, canonical flag, capability IDs, implementation IDs, evidence IDs derived from explicit Evidence.supports, declared provenance, and declared freshness when present. Leave unregistered skills without synthetic context. Keep docs/search-index.json a search corpus rather than a second registry catalog.

Evidence: tools/export_skills.py, registry/universal_registry.json, registry/runtime.py, docs/api/skills.json, docs/api/skills-schema.json, tests/test_export_registry_context.py, docs/DISCOVERY_REGISTRY_CONTEXT.md.

Status: VERIFIED â PR #300 merged as `4ff041511f2291e826b2a32c2cc72f36f8f023cb`. Final head `52ae305ad504416114d7efdd8313eff8f931f57d` passed Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, PR Checks, Validate Skills Graph, and Auto Label. The wheel gate also executed installed CLI search successfully.

Reopen Conditions: Reopen if UniversalRegistry coverage becomes corpus-wide, the discovery projection becomes a runtime registry consumer, or an authoritative machine-readable discovery contract supersedes this projection boundary.


# DECISION-2026-10-03-DISCOVERY-DATE-PROJECTION-RECONCILIATION

DECISION-ID: DECISION-2026-10-03-DISCOVERY-DATE-PROJECTION-RECONCILIATION
Topic: Correct canonical date metadata and reconcile generated API projections

Finding: `skills/15-orchestration/kanban-task-management.md` had correct YAML frontmatter but malformed legacy body metadata combining Added and Last Updated on one line. The exporter consumed that body value and produced an invalid `added` value in docs/api/skills.json and docs/api/skills.yaml.

Decision: Correct the canonical source metadata, add a regression test, then reconcile the affected generated JSON/YAML projections. Do not weaken the schema to accept malformed source metadata. Keep generated artifacts subordinate to the canonical source and existing export workflow.

Evidence: PR #301 merged as `ff3943efeb49e40466b3bc408c87b4de820c1728`; PR #302 merged as `32cee4e430dc5c8ebf495e84048fd15e1e5404d2`. PR #301 exact-head CI passed the full applicable validation matrix; PR #302 passed Test Suite on Python 3.11/3.12/3.13, Security Scan, Build & Verify Wheel, and PR Checks. Main artifacts now report `added: 2026-10` and `last_updated: 2026-10` for the affected skill.

Status: VERIFIED â MAIN

Reopen Conditions: Reopen if the export workflow regenerates a divergent value, if the exporter changes its source precedence, or if another canonical skill exhibits the same cross-field metadata contamination pattern.


# DECISION-2026-10-04-AGENT-SKILLS-RECONCILIATION-GATE

DECISION-ID: DECISION-2026-10-04-AGENT-SKILLS-RECONCILIATION-GATE
Topic: Make canonical-to-Agent-Skills reconciliation a hard CI invariant

Finding: The existing reconciler classified eligible missing projections but its default command returned success regardless of those findings. This allowed a newly eligible canonical skill to be absent from the deterministic Agent Skills projection without failing the distribution workflow.

Decision: Preserve the existing canonical projection and collision-resolution architecture and enforce it through a read-only `--check` mode. The check fails for eligible missing projections, deterministic projection drift, stale or ambiguous provenance, unexpected packages outside the explicit auxiliary boundary, and duplicate target names after deterministic collision resolution. `rename_needed` remains compatibility metadata and is not a standalone failure; an eligible canonical source with only a legacy package still fails until its deterministic projection exists. Resolved source-name collisions remain valid when category-qualified target names are unique. No second generator, index, or semantic search system is introduced.

Confidence: HIGH

Evidence IDs: PR-305, TOOLS-RECONCILE-AGENT-SKILLS, TESTS-AGENT-SKILLS-RECONCILIATION, WORKFLOW-AGENT-SKILLS-DISTRIBUTION

Status: VERIFIED â PR #305 exact head `1c1d70a337f9952cd2c24d555ee9d67bab9cbe30` passed the applicable CI checks and merged to main as `a9a649481c68bf0dd33447a2238174ebd8b79a4b`.

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
Decision: AI agents operating on Skills Tree must execute meaningful work as a bounded evidence-driven loop: OBSERVE â ASSESS â PLAN â EXECUTE â VERIFY â RECORD â DECIDE. Verification failures, regressions, CI failures, and documentation drift become inputs to subsequent cycles. Agents continue autonomously when a safe evidence-backed next action exists, stop as BLOCKED when it does not, and select DONE only after the goal, invariants, tests/CI, generated artifacts, documentation, and final audit are verified. The loop has a default 12-iteration ceiling and must not expose private chain-of-thought. This augments the existing lifecycle and does not create a competing orchestration system.
Confidence: HIGH
Evidence IDs: AI_CONSTITUTION.md, AGENTS.md, meta/AGENT_OPERATING_MODEL.md, tools/verify_governance.py
Status: VERIFIED â PR #324 merged to main as `6fa92dd42768395102215a26e22999d6de81c013`; exact-head governance, graph, test, security, build, and PR validation passed.
Reopen Conditions: Reopen if a stronger repository-native agent orchestration contract supersedes this loop, if bounded execution proves insufficient for real repository work, or if the authority/escalation model changes.


# DECISION-2026-10-04-MAIN-WRITER-SERIALIZATION
DECISION-ID: DECISION-2026-10-04-MAIN-WRITER-SERIALIZATION
Topic: Prevent stale-SHA races among automated main writers
Finding: Post-merge verification of PR #324 exposed a real race: the graph writer advanced main while the quality projection and zero-touch release workflows still operated from the original triggering SHA. Graph generation succeeded, but quality failed on a stale upstream SHA and zero-touch release failed when upstream main changed.
Decision: Treat direct-main generated/release automation as one serialized writer class. Use the shared `auto-commit-main` concurrency group with `cancel-in-progress: false`; synchronize stale event checkouts to live `origin/main` before generation or release mutation; keep `skills/` canonical and generated outputs subordinate projections. The graph writer remains the sole graph projection writer. Do not solve the defect with branch protection or human approval.
Confidence: HIGH
Evidence IDs: PR-324, workflow run 37223742787, workflow run 37223742707, meta/GOVERNANCE_MODEL.md, .github/workflows/validate-graph.yml, .github/workflows/zero-touch-release.yml
Status: VERIFIED â PR #325 merged to main as `0892cfe20130368ad12655a8ec71616ae97027fd`; exact-head Governance Gate, Graph, Tests, Security, Build, and PR validation passed. Post-merge writer execution completed without the prior stale-SHA failure.
Reopen Conditions: Reopen if a post-merge writer race, stale-SHA mutation, generated-projection divergence, or release concurrency defect remains after the new contract is merged and verified.


# DECISION-2026-10-04-MAIN-WRITER-QUEUE
DECISION-ID: DECISION-2026-10-04-MAIN-WRITER-QUEUE
Topic: Preserve pending automated main-writer runs
Finding: After the writer-race fix was merged, the zero-touch release run was cancelled while waiting on the shared writer concurrency boundary. GitHub Actions concurrency permits only one pending run by default; a newer pending run can replace an older one.
Decision: The repository-wide `auto-commit-main` writer group must use `queue: max` with `cancel-in-progress: false`, so pending generated/release writers are retained and processed sequentially. Writers still synchronize to live `origin/main` before mutation because queue ordering alone does not make an event SHA current.
Confidence: HIGH
Evidence IDs: post-merge main commit `0892cfe20130368ad12655a8ec71616ae97027fd`, workflow run 37223991086, GitHub Actions concurrency documentation.
Status: VERIFIED â PR #326 merged to main; exact-head Governance Gate, Graph, Tests, Security, Build, and PR validation passed. Post-merge Zero-Touch Release completed successfully and pending writer runs were retained by the lossless queue.
Reopen Conditions: Reopen if pending writer runs are still lost, if queue pressure exceeds the repository's acceptable automation latency, or if a stronger repository-native writer scheduler replaces this mechanism.


# DECISION-2026-10-04-DEMAND-SIGNAL-REVIEW
DECISION-ID: DECISION-2026-10-04-DEMAND-SIGNAL-REVIEW
Topic: First controlled demand-intelligence evidence cohort
Finding: The first configured public GitHub issue-search collection returned raw result counts of 64, 63, and 54 across three overlapping query groups. Review of the returned issues identified capability signals for search/discovery, memory, code/IDE integration, reasoning, and action execution. The result sets also contain operational/security issues, demonstrating why raw query volume cannot be used as a demand score.
Decision: Treat these as an unranked evidence cohort. Reconcile each capability against canonical coverage, evidence tier, freshness, dependencies, and implementation gaps before selecting migration priorities. Search/discovery is already implemented and verified and must not be reimplemented merely because issue #86 is a historical demand signal.
Confidence: MEDIUM-HIGH
Evidence IDs: meta/demand-sources.json, tools/collect_demand_signals.py, .github/workflows/demand-signals.yml, issues #86, #87, #88, #90, #91, controlled GitHub issue-search run 2026-10-04.
Status: VERIFIED OBSERVATION â prioritization intentionally deferred until coverage/evidence reconciliation.
Reopen Conditions: Reopen if a stronger public-signal source invalidates the cohort, if the collector proves non-reproducible, or if current canonical coverage materially changes.


# DECISION-2026-10-04-IDE-INTEGRATION-MIGRATION
DECISION-ID: DECISION-2026-10-04-IDE-INTEGRATION-MIGRATION
Topic: First demand/evidence-driven Phase 3 migration
Finding: The controlled demand review surfaced issue #88 requesting IDE integration patterns, pair-programming protocols, and polyglot-agent support. Coverage reconciliation found no dedicated canonical IDE integration skill under `05-code`, while the repository already has adjacent code-generation, code-review, execution, Git, API, and debugging skills. Current public documentation and implementations also demonstrate a real agentâIDE capability boundary via MCP and IDE-native APIs.
Decision: Implement one canonical `05-code/ide-integration.md` skill as the first Phase 3 slice. Keep it protocol-neutral, least-privilege, workspace-scoped, and independently verifiable. Do not create separate vendor-specific skills until evidence demonstrates distinct reusable contracts.
Confidence: HIGH
Evidence IDs: issue #88, skills/05-code directory audit, GitHub Copilot MCP documentation, public AgentBridge implementation, current Skills Tree governance and evidence model.
Status: IMPLEMENTED â exact-head CI and projection verification required before merge.
Reopen Conditions: Reopen if CI finds an existing canonical duplicate, evidence quality proves insufficient, the capability cannot be expressed as a reusable contract, or vendor-specific semantics require a distinct skill.

# DECISION-2026-10-05-EVALUATION-EVIDENCE-GATE-RECONCILIATION
DECISION-ID: DECISION-2026-10-05-EVALUATION-EVIDENCE-GATE-RECONCILIATION
Topic: Reconcile evaluation validation with canonical corpus and historical retrieval evidence
Finding: The evaluation validator was checking the obsolete `data/corpus/` location while authoritative corpus entries live under `intelligence/corpus/entries/`. The evaluation ontology contains seven mappings, while P0 capabilities CAP-007, CAP-011, and CAP-014 remain unmapped. The retrieval benchmark `benchmarks/memory/retrieval-accuracy.md` has historical results without a current version-matched run artifact.
Decision: Keep `intelligence/ontology/evaluation_ontology.json` and the existing Benchmark contract/runtime as authoritative evaluation boundaries. Correct `validate-evaluations.yml` to inspect the canonical corpus path, surface missing P0 mappings, and validate declared freshness metadata without rewriting review dates. Qualify the stale retrieval benchmark as historical and do not claim current retrieval quality until reproducible evidence is recorded. Do not create a second evaluation framework or search implementation.
Evidence IDs: pre-merge main `a61af71fc4e47593bd430039a9362d4ae31756ce`; merged main `4b1c1b9ffc28bcbecc3b899da8cbb58af7de65ec`; `meta/EVIDENCE_MODEL.md`; `intelligence/ontology/evaluation_ontology.json`; `intelligence/corpus/entries/`; Issue #335; Issue #336; `benchmarks/memory/retrieval-accuracy.md`.
Status: IMPLEMENTED AND MERGED â PR #337 exact-head CI passed; post-merge Governance Gate passed. The evaluation workflow's self-trigger path was then identified as missing and is addressed by the follow-up change.
Reopen Conditions: Reopen if the canonical corpus/evaluation paths change, the Benchmark contract is superseded, current reproducible benchmark evidence becomes available, or a concrete retrieval-ranking failure case is measured.


# DECISION-2026-10-05-P0-EVALUATION-CONTRACTS
DECISION-ID: DECISION-2026-10-05-P0-EVALUATION-CONTRACTS
Topic: Add canonical evaluation mappings for the remaining P0 capabilities
Finding: CAP-007 semantic_retrieval, CAP-014 tool_execution, and CAP-011 self_evaluation are P0 requirements in the canonical corpus but had no capability evaluation mappings in the canonical evaluation ontology. Existing corpus entries already define concrete acceptance requirements for these capabilities.
Decision: Add exactly one evaluation mapping per missing P0 capability to the existing evaluation ontology. Reuse existing ET-001/002/003/005/007/008/009/010/012 metrics and the existing benchmark/evidence boundary. Keep retrieval currentness explicitly unclaimed until a reproducible run artifact exists. Treat confidence calibration/ECE as diagnostic evidence for CAP-011 rather than creating a new ontology metric. Keep structured quality-gate state authoritative for tool execution and deployment decisions.
Evidence IDs: intelligence/ontology/evaluation_ontology.json; intelligence/corpus/entries/support/CORPUS-001.json; intelligence/corpus/entries/engineering/CORPUS-002.json; Issue #335; Issue #336.
Status: IMPLEMENTED ON BRANCH â exact-head CI verification pending.
Reopen Conditions: Reopen if the canonical corpus acceptance requirements change, an existing evaluation type supersedes these mappings, or reproducible evidence demonstrates that a mapping is materially incorrect or insufficient.


# DECISION-2026-10-05-P0-EVALUATION-CONTRACTS
DECISION-ID: DECISION-2026-10-05-P0-EVALUATION-CONTRACTS
Topic: Add canonical evaluation mappings for the remaining P0 capabilities
Finding: CAP-007 semantic_retrieval, CAP-014 tool_execution, and CAP-011 self_evaluation were P0 requirements in the canonical corpus but had no capability evaluation mappings. The existing validation gate also contained a field-name mismatch and two stale capability names that were exposed when the new mappings were added.
Decision: Add exactly one evaluation mapping per missing P0 capability, reuse the existing evaluation types and benchmark boundary, correct the validator to recognize the canonical minimum_required_score field, and reconcile CAP-023/CAP-025 names with the capability ontology. Keep retrieval currentness explicitly unclaimed until a reproducible run artifact exists. Treat confidence calibration/ECE as diagnostics for CAP-011 rather than creating a new ontology metric. Keep structured quality-gate state authoritative for tool execution and deployment decisions.
Evidence IDs: PR #339; merged main c88672e1d19e381aad8137796d4283678e3fc9e1; Validate Evaluations run 37300715147; intelligence/ontology/evaluation_ontology.json; .github/workflows/validate-evaluations.yml; CORPUS-001; CORPUS-002.
Status: VERIFIED â merged and exact-head CI passed.
Reopen Conditions: Reopen if corpus acceptance requirements change, evaluation types are superseded, or reproducible evidence demonstrates the mappings are materially incorrect or insufficient.


# DECISION-2026-10-05-RETRIEVAL-EVIDENCE-BENCHMARK
DECISION-ID: DECISION-2026-10-05-RETRIEVAL-EVIDENCE-BENCHMARK
Topic: Establish current reproducible evidence for canonical CLI retrieval quality
Finding: The canonical deterministic search implementation had no current version-matched retrieval run artifact. Existing recommendation and retrieval benchmark results were historical and could not justify current ranking claims.
Decision: Reuse the existing Benchmark contract/runtime and canonical CLI search implementation. Add one registered `benchmark/retrieval-cli-v1`, one versioned 12-case repository-authored dataset derived from canonical skill titles/descriptions, one deterministic runner, and one observational CI workflow that uploads the exact result artifact. Do not add embeddings, LLM ranking, a second search implementation, or a new evaluation framework.
Evidence IDs: PR #340; merged main `8ae02bd08841a496d19f49cd1092ec5f011c6c6b`; Retrieval Evidence Benchmark run `37301951280`; artifact `retrieval-benchmark-95839c52567c32cad38c0a0038edc01dc0a298f4`; result commit `95839c52567c32cad38c0a0038edc01dc0a298f4`; search-index SHA-256 `cca13a4edb3f7b725992d90f7c63b988cd7d303c63150667dfe4e3c64c634e9a`; dataset SHA-256 `c2eca9737387fc75ee0bd2674550022b2aa67aee36924d6593571f0bcaa9e6c0`.
Result: Recall@5 1.0000; MRR 0.9583; deterministic replay true. RAG case ranked at position 2 behind `09-agentic-patterns/rag`; all other cases ranked first.
Status: VERIFIED â PR #340 merged after exact-head CI passed.
Reopen Conditions: Reopen when a broader representative query set is available, when the search projection/ranking contract changes, or when a measured failure case justifies a ranking intervention.


# DECISION-2026-10-05-CAPABILITY-BASED-SKILL-SELECTION

DECISION-ID: DECISION-2026-10-05-CAPABILITY-BASED-SKILL-SELECTION
Topic: Add the missing canonical skill-selection contract identified by demand/evidence reconciliation
Finding: Public demand signals include automated task breakdown, agent assignment based on skills/performance, dependency-aware orchestration, and runtime action decisioning. Skills Tree already covers search, specialist routing, role assignment, task decomposition, delegation, dependencies, eligibility, and orchestration primitives, but it lacked a dedicated skill-level contract for competing-skill discrimination, prerequisite resolution, invocation verification, and next-skill selection.
Decision: Add one experimental canonical skill, `15-orchestration/capability-based-skill-selection`, without creating a second search engine, registry, or orchestration authority. The contract must select the smallest sufficient skill set, reject ineligible/competing candidates with reasons, resolve prerequisites, verify outcomes, and choose the next action from observed results. Register the demand signal in `meta/MOST-WANTED-SKILLS.md` and extend the reproducible demand collector with selection/routing/orchestration/task-breakdown queries.
Evidence IDs: PR #341; merged main `af892ebf9aafd90dedb9d6039974d51c2bf02726`; public GitHub issue `BrianTruong23/kanban-coding-agents#8`; public OWASP Agentic Top 10 discussion `www-project-top-10-for-large-language-model-applications#802`; `meta/MOST-WANTED-SKILLS.md`; exact-head Retrieval Evidence Benchmark run on PR #341.
Status: VERIFIED â merged after exact-head CI passed. The skill remains experimental pending behavioral evaluation evidence.
Reopen Conditions: Reopen if behavioral evaluation shows the contract is redundant, insufficiently discriminating, missing required dependencies, or better represented as an existing orchestration skill.


# DECISION-2026-10-05-BEHAVIORAL-SKILL-SELECTION

DECISION-ID: DECISION-2026-10-05-BEHAVIORAL-SKILL-SELECTION
Topic: Establish the first executable behavioral boundary for capability-based skill selection
Finding: The existing recommendation path operates at Goal/Taxonomy level and does not itself provide a canonical skill-level selection contract with explicit candidate rejection, registry eligibility, terminal failure behavior, and next-action output. A new bounded runtime boundary was therefore justified.
Decision: Add `registry/skill_selection.py` using the existing UniversalRegistry and EligibilityEngine, plus a versioned deterministic benchmark and CI evidence workflow. Do not create a second registry, search engine, or orchestration authority.
Evidence IDs: PR #343; merged main `203d4b12e576cbeb5eaa83249cc97d96905b01fc`; Skill Selection Evidence Benchmark run `37310654422`; benchmark dataset `benchmarks/selection/capability-selection-v1.json`.
Result: 6/6 benchmark cases passed with deterministic replay. The verified slice covers registered capability matching, candidate discrimination, fail-closed unknown candidates, insufficient-capability blocking, and no-recovery failure termination.
Limitation: The Universal Registry currently contains only three skill records. Prerequisite routing is implemented against the canonical REQUIRES graph API but is not behaviorally verified through a prerequisite-bearing registered skill pair. Full task-to-dependency-to-invocation sequencing remains UNVERIFIED.
Status: VERIFIED BOUNDED SLICE
Reopen Conditions: Reopen if benchmark results fail, registry eligibility semantics change, or prerequisite-bearing skill coverage is added and produces contradictory evidence.


# DECISION-2026-10-05-PREREQUISITE-ROUTING

DECISION-ID: DECISION-2026-10-05-PREREQUISITE-ROUTING
Topic: Verify dependency-aware skill selection against registered prerequisite-bearing skills
Finding: The initial behavioral selection slice proved capability matching and fail-closed selection but could not verify prerequisite routing because the Universal Registry lacked a prerequisite-bearing registered skill pair. Adding Agentic RAG, CoT, and ReAct exposed an ontology collision when Agentic RAG inherited the general knowledge-retrieval capability; that would have made selection ambiguous and altered baseline registry resolution.
Decision: Represent Agentic RAG under a distinct `capability/agentic-knowledge-retrieval` capability, retain general knowledge-retrieval for baseline RAG, register the prerequisite-bearing skills needed by the canonical graph, and implement deterministic transitive `REQUIRES` traversal with cycle/unregistered-prerequisite fail-closed behavior. Extend the existing selection benchmark rather than creating another orchestration authority.
Evidence IDs: PR #345; exact-head `8200b0f359e35293121189cdf2dd263ce96252db`; merged main `f15c729adf76794fc914f954f74a4964d7dbdd76`; Skill Selection Evidence Benchmark run `37317066498`; Test Suite run `37317066396`; Security Scan run `37317066520`; Build & Verify Wheel run `37317066342`; Retrieval Evidence Benchmark run `37317066571`.
Result: Exact-head CI passed. The bounded benchmark now verifies target selection, ordered transitive prerequisites, partial-completion resume, and terminal invocation after prerequisites.
Status: VERIFIED BOUNDED RUNTIME
Limitation: This is evidence for the registered Agentic RAG dependency scenario, not general autonomous planning or arbitrary dependency-graph correctness.
Reopen Conditions: Reopen if prerequisite routing fails under a new registered dependency pattern, registry capability semantics change, or a concrete measured failure demonstrates that the selection/recovery contract is insufficient.


## DECISION-2026-10-05-RECOVERY-FAILURE-HISTORY

**Status:** VERIFIED BOUNDED SLICE

**Evidence:** PR #347; exact head `40cff5782307469b9d9e62733d04841c667b9870`; merge `adbbb55c58a853e843883b2cbc14997f315226b7`; Skill Selection Evidence Benchmark run 37320381751; Test Suite run 37320382230; Security Scan run 37320381979; Build & Verify Wheel run 37320382114.

**Decision:** Preserve the existing SkillSelectionEngine and extend recovery with explicit failed-skill history. Recovery must never blindly retry a previously failed candidate. If remaining candidates are ineligible or do not cover the required capability, the selector remains BLOCKED and escalates.

**Boundary:** Current registry coverage is insufficient for a genuine multi-step A â failure â B â failure â C behavioral benchmark. Do not create synthetic skills or a parallel registry merely to manufacture this evidence. Reopen this boundary when real canonical registry coverage provides multiple independently eligible alternatives for the same capability.


# DECISION-2026-10-06-AGENT-SKILL-SECURITY-AUDIT

DECISION-ID: DECISION-2026-10-06-AGENT-SKILL-SECURITY-AUDIT
Topic: Add the missing pre-installation/pre-execution security-audit contract for agent skills
Finding: Demand/evidence reconciliation identified direct ecosystem concern around auditing agent skills before installation, including declared-vs-observed behavior, credential access, exfiltration, obfuscation, bundled scripts/hooks, and permission declarations. Skills Tree already had sandboxing, secret scanning, permission checking, input sanitization, audit logging, and human approval, but no dedicated canonical contract for auditing a complete skill package before execution.
Decision: Add experimental `skills/14-security/agent-skill-security-audit.md` and record the demand signal in `meta/MOST-WANTED-SKILLS.md`. Reuse existing security controls and preserve the boundary between evidence and authorization; do not create a second scanner, registry, ontology, or authorization authority.
Evidence IDs: PR #350; merged main `436c15c745e1747e3ec1e931dccacea1ca013c7c`; exact-head CI runs 37422390762, 37422390882, 37422390775, 37422390740, 37422390824, 37422390793, 37422390811, 37422390802, 37422390790, 37422390739, 37422390769, 37422390800, 37422390773, and 37422390805; OWASP Secure Agent Playbook issue #21; 2026 malicious-agent-skill detection research.
Result: Exact-head applicable CI passed. The new skill is a bounded contract, not a claim of complete malware detection or universal safety.
Status: VERIFIED BOUNDED SECURITY CONTRACT
Reopen Conditions: Reopen if security evaluation exposes missing audit dimensions, if the ecosystem contract changes materially, or if a measured implementation gap requires executable audit tooling rather than guidance.


# DECISION-2026-10-06-EVALUATION-ONTOLOGY-FRESHNESS

DECISION-ID: DECISION-2026-10-06-EVALUATION-ONTOLOGY-FRESHNESS
Topic: Re-qualify evaluation ontology freshness without expanding the evaluation architecture
Finding: The canonical evaluation ontology review date had expired (`2026-10-03`), while live integrity checks showed all 12 evaluation types are internally resolvable, mapping IDs are unique, mapping names resolve to the canonical capability ontology, and all eight P0 capabilities have explicit mappings.
Decision: Preserve the existing evaluation ontology and Benchmark boundary. Refresh only the verified freshness metadata after the integrity audit, using the existing 90-day review cadence. Do not add evaluation types, registries, benchmark frameworks, or skills as part of this maintenance slice.
Evidence IDs: live `intelligence/ontology/evaluation_ontology.json`; `intelligence/ontology/capability_ontology.json`; `CORPUS-001`; `CORPUS-002`; main baseline `537c30944bdf2163f0ac3350ff4661a66ba85f8e`.
Result: Initial audit confirmed 12/12 evaluation references, 0 duplicate mapping IDs, and 0 unknown mapping IDs, but exact-head CI then exposed two corpus P0 capabilities absent from the mapping set: CAP-018 `multi_turn_dialogue_management` and CAP-027 `compliance_logging`. Existing ET metrics were sufficient, so the ontology was extended with exactly two mappings. Freshness metadata remains reviewed `2026-10-06`, due `2027-01-04`.
Status: VERIFIED ON MAIN â PR #354 merged as `15c455bbef43d5f88c17c0cbdbac1af09c8e2d04` after the exact-head repair matrix passed
Reopen Conditions: Reopen if evaluation ontology structure, capability mappings, metric semantics, corpus requirements, or reproducibility evidence changes materially.


# DECISION-2026-10-06-P0-EVALUATION-COVERAGE-REPAIR

DECISION-ID: DECISION-2026-10-06-P0-EVALUATION-COVERAGE-REPAIR
Topic: Add the two P0 evaluation mappings exposed by exact-head validation
Finding: Validate Evaluations on PR #354 found CORPUS-001 P0 capabilities CAP-018 `multi_turn_dialogue_management` and CAP-027 `compliance_logging` had no evaluation mappings. This is a genuine canonical coverage gap, not a validator defect.
Decision: Add exactly two mappings to the existing evaluation ontology. CAP-018 uses ET-012 with ET-007 as secondary evidence for multi-turn coherence and continuity. CAP-027 uses ET-001 with ET-005 and ET-007 for log completeness, audit-query latency, and logging reliability. Do not add new metric types, registries, or benchmark frameworks.
Evidence IDs: PR #354; Validate Evaluations run 37441839608; job 112197207764; CORPUS-001; intelligence/ontology/evaluation_ontology.json; intelligence/ontology/capability_ontology.json.
Result: Exact-head CI passed after the JSON repair; all 10 corpus P0 capabilities now have mappings. Merge verified on main as `15c455bbef43d5f88c17c0cbdbac1af09c8e2d04`.
Status: VERIFIED ON MAIN.
Reopen Conditions: Reopen if the corpus acceptance requirements or evaluation semantics require a metric not expressible through the existing ontology, or if exact-head validation rejects the mappings for a substantive contract reason.


# DECISION-2026-10-06-P0-EVALUATION-COVERAGE-VERIFIED

DECISION-ID: DECISION-2026-10-06-P0-EVALUATION-COVERAGE-VERIFIED
Topic: Close the P0 evaluation coverage repair
Evidence IDs: PR #354; merged main `15c455bbef43d5f88c17c0cbdbac1af09c8e2d04`; Validate Evaluations 37442131150; Governance Gate 37442131224; Test Suite 37442131102; Security Scan 37442131109; Build & Verify Wheel 37442131230; PR Checks 37442131292; Auto Label 37442131333.
Result: All 10 P0 capabilities required by the canonical corpus now have evaluation mappings. The existing 12 evaluation types and Benchmark boundary were preserved; exactly two mappings were added for CAP-018 and CAP-027.
Status: VERIFIED ON MAIN
Reopen Conditions: Reopen if a corpus P0 capability becomes unmapped, evaluation semantics change, or new evidence shows either mapping is materially insufficient.


# DECISION-2026-10-06-SKILL-ACTIVATION-EVIDENCE

DECISION-ID: DECISION-2026-10-06-SKILL-ACTIVATION-EVIDENCE
Topic: Prioritize activation/invocation evidence over adding another skill
Finding: Current Skills Tree behaviorally verifies explicit capability-based selection, prerequisite routing, and failure recovery, but lacks a benchmark for natural-language skill activation, false activation, collision handling, repeated fresh-session variance, and direct invocation evidence.
External Evidence: addyosmani/agent-skills #620; NousResearch/hermes-agent #82253; NousResearch/hermes-agent #96704; Google skill-reach; all reviewed 2026-10-06.
Decision: Treat this as an evaluation/invocation evidence gap. Build a bounded benchmark on existing discovery/selection/observability surfaces before changing skill descriptions or runtime routing. Do not create a new skill, search engine, or routing authority unless measured failures establish a concrete implementation gap.
Repository Evidence: `registry/skill_selection.py`; `benchmarks/selection/capability-selection-v1.json`; `tools/run_skill_selection_benchmark.py`; existing agent observability tracing skills.
Status: VERIFIED BOUNDED BENCHMARK + OBSERVATION CONTRACT â Issue #357; empirical evidence pending.
Reopen Conditions: Reopen if real traces expose a semantic limitation in the benchmark or require a new canonical boundary.


# DECISION-2026-10-06-SKILL-ACTIVATION-BENCHMARK

DECISION-ID: DECISION-2026-10-06-SKILL-ACTIVATION-BENCHMARK
Topic: Implement activation/invocation measurement without inventing a routing runtime
Finding: The repository has deterministic capability selection and an observability contract for skill selection/execution, but no canonical benchmark consumes actual agent trace evidence for natural-language activation.
Decision: Add a bounded trace-based activation benchmark using the existing Benchmark runtime and observability event contract. The benchmark definition covers expected activation, forbidden activation, collision cases, repeated-run variance, and explicit invocation evidence.
Implementation: `benchmarks/activation/skill-activation-v1.json`, `tools/run_skill_activation_benchmark.py`, `tests/test_skill_activation_benchmark.py`, and registry entry `benchmark/skill-activation-v1`.
Evidence boundary: The runner accepts externally captured `skill_selection` and `skill_execution` events. It never simulates model routing, infers activation from prompt text, or treats an empty observation set as PASS. Synthetic fixtures are test coverage only, not empirical evidence.
Result: Measurement infrastructure is implemented; empirical activation reliability remains UNVERIFIED pending real agent-runtime traces.
Status: VERIFIED ON MAIN â PR #359 merged as `51f22be5d3935437e19561e8aa1fdbf2eb19daab`; EMPIRICAL EVIDENCE PENDING.
Reopen Conditions: Reopen if real traces cannot be represented by the existing event contract, or if measured failures demonstrate a concrete runtime/description gap requiring architectural change.


# DECISION-2026-10-06-ACTIVATION-OBSERVATION-CONTRACT

DECISION-ID: DECISION-2026-10-06-ACTIVATION-OBSERVATION-CONTRACT
Topic: Formalize the input contract for real skill activation evidence
Finding: The activation benchmark runner required structured `skill_selection` and `skill_execution` observations, but the accepted payload shape was previously implicit in code/tests.
Decision: Add `meta/skill-activation-observation.schema.json` and validate all benchmark observations against it before metric calculation. Reuse the existing Agent Observability Tracing event concepts; do not add a routing runtime, inference mechanism, or second telemetry authority.
Evidence boundary: The schema accepts observed selection/execution events only. It explicitly rejects inferred activation event kinds. Synthetic fixtures validate schema mechanics, not empirical routing behavior.
Result: External agent runtimes now have a machine-readable input contract for `benchmark/skill-activation-v1`. Empirical activation reliability remains unverified pending real traces.
Status: VERIFIED ON MAIN after merge; EMPIRICAL EVIDENCE PENDING.
Reopen Conditions: Reopen if a compatible runtime cannot express its observed selection/execution events through this contract, or if measured evidence requires materially different semantics.


# DECISION-2026-10-06-HERMES-ACTIVATION-ADAPTER

DECISION-ID: DECISION-2026-10-06-HERMES-ACTIVATION-ADAPTER
Topic: Establish a deterministic interoperability path from Hermes observer evidence to the existing activation benchmark
Finding: Hermes exposes authoritative post_tool_call evidence for skill_view and on_skill_lifecycle evidence for action=loaded, with session/task correlation. The existing Skills Tree benchmark requires explicit skill_selection and skill_execution observations.
Decision: Add one deterministic converter, tools/convert_hermes_activation_observations.py, that maps only these observed events into the existing observation contract. Require explicit correlation and explicit ACT-case mapping; discard only runs with no observed selection or execution events. Preserve mismatched selection/execution evidence so false activation and invocation gaps remain measurable. Do not infer activation, use aggregate counters as execution evidence, or add a routing/runtime authority.
Evidence IDs: Hermes Event Hooks documentation; Hermes tools/skill_usage.py; Skills Tree meta/skill-activation-observation.schema.json; Issue #357.
Status: IMPLEMENTED â empirical traces still pending.
Reopen Conditions: Reopen if Hermes changes the authoritative hook semantics, the observation contract changes, or real traces demonstrate that the mapping is insufficient.
# DECISION-2026-10-06-BENCHMARK-FAIL-CLOSED

DECISION-ID: DECISION-2026-10-06-BENCHMARK-FAIL-CLOSED
Topic: Prevent silent success when the activation benchmark receives no observations
Finding: The activation runner emitted a NO_OBSERVATIONS result but returned process exit code 0, so a caller could treat missing evidence as a successful benchmark execution.
External Evidence: anthropics/skills#1383 documents silent benchmark failure modes caused by zero discovered runs and recommends loud failure instead of writing misleading empty results.
Decision: Return exit code 2 when zero benchmark cases have observations. Preserve the machine-readable NO_OBSERVATIONS result so the evidence state remains explicit. Do not change routing, activation metrics for observed traces, or partial-corpus reporting.
Status: VERIFIED ON MAIN â PR #365 merged as `d39d899e23e8614eb11971953541cda9bd7dec9f` after exact-head applicable CI passed.
Reopen Conditions: Reopen if a downstream benchmark contract requires a different process-level status model or if zero-observation invocations must remain successful for a documented orchestration reason.

# DECISION-2026-10-06-MODEL-AGENT-TOOL-SKILL-BOUNDARY

DECISION-ID: DECISION-2026-10-06-MODEL-AGENT-TOOL-SKILL-BOUNDARY
Topic: Establish a shared conceptual boundary for Model, Agent, Tool, Capability, and Skill
Finding: Existing architecture already separates these entities in the universal registry, but human-readable schema/glossary definitions could still make Skill sound equivalent to Capability.
Source insight: The project article on AI Skills emphasizes a reusable Skill as procedural guidance and distinguishes it from the inference Model, the executing Agent, and the Tool action surface.
Decision: Treat Capability as the outcome-level "what"; Skill as reusable procedural "how"; Model as inference engine; Tool as callable action/data surface; Agent as the coordinating system. Skills may guide an agent but do not grant authorization. Selection, invocation/load, and downstream task efficacy remain separate evidence boundaries.
Scope: Update semantic schema descriptions, glossary definitions, and current architecture documentation without changing runtime routing, permissions, or entity IDs.
Status: VERIFIED ON MAIN â PR #365 merged as `d39d899e23e8614eb11971953541cda9bd7dec9f` after exact-head applicable CI passed.
Reopen Conditions: Reopen if executable registry/runtime evidence requires a different entity relationship or if a schema consumer cannot preserve this distinction.
DECISION-ID: DECISION-2026-10-06-LIVE-RECONCILIATION-382
Topic: Current main corpus and governance reconciliation
Decision: Treat 382 canonical skill files, 302 Agent Skills packages, byte-identical 382-node/250-edge graph projections, and byte-identical search projections as the current generated baseline verified by CI on 2026-10-06. Preserve older count snapshots only as historical records.
Status: SUPERSEDED BY CURRENT MAIN RECONCILIATION â the verified current baseline remains 382 total quality-corpus files including the intentional fixture, 381 production/public canonical skills, 264 eligible projections, 118 blocked entries, and 302 Agent Skills packages.
Reopen Conditions: Reopen if a later exact-head CI audit shows corpus/projection drift.

DECISION-ID: DECISION-2026-10-06-ACTIVATION-CORPUS-COMPLETENESS
Topic: Distinguish partial activation evidence from a complete empirical corpus
Decision: Make benchmark result status first-class: NO_OBSERVATIONS when no case has evidence, PARTIAL when observed evidence does not satisfy every case repetition contract, and COMPLETE only when every case meets its declared repetitions. Current complete corpus requirement is 4 cases Ã 3 repetitions = 12 observations.
Status: VERIFIED ON MAIN â PR #371 merged as `3dd21558d4ad6b223908a2cd05c431f678ce6036` after exact-head applicable CI passed.
Reopen Conditions: Reopen if a future benchmark contract intentionally changes case weighting or repetition policy.
DECISION-ID: DECISION-2026-10-06-DEVLENS-READONLY
Topic: Isolate DevLens from authoritative repository writes
Decision: DevLens remains a manual diagnostic only. It must not write README.md or any repository projection, and its workflow must retain read-only permissions. The public README must not carry stale externally generated health snapshots.
Evidence IDs: Issue #370; .github/workflows/devlens.yml; tools/verify_governance.py; meta/WORKFLOW_INVENTORY.md.
Status: VERIFIED ON MAIN â PR #377 merged as `5a25ef13751e4a43ce2a92226198c2b24232ecf3` after exact-head applicable CI passed.
Reopen Conditions: Reopen only if DevLens is intentionally integrated into a documented authoritative projection boundary with the same writer serialization and governance controls.
DECISION-ID: DECISION-2026-10-06-ACTIVATION-OBSERVATION-INTEGRITY
Topic: Prevent invalid or duplicated runtime observations from contaminating activation evidence
Decision: Reject observations whose case_id is not present in the selected benchmark dataset and reject duplicate run_id values before metric calculation. Preserve existing metric formulas and benchmark case semantics.
Evidence IDs: Issue #372; meta/skill-activation-observation.schema.json; tools/run_skill_activation_benchmark.py; tests/test_skill_activation_benchmark.py.
Status: VERIFIED ON MAIN â PR #379 merged as `290cb3495d1905615501471e4e1b3bec86301a7b` after exact-head applicable CI passed.
Reopen Conditions: Reopen if the observation contract intentionally permits cross-dataset observations or multi-record run identities.
DECISION-ID: DECISION-2026-10-06-FINAL-AUDIT-RECONCILIATION
Topic: Final live repository audit baseline and remaining work
Decision: Treat live main as the sole current execution authority. Current verified baseline is 45 workflow files, 382 quality-corpus skill files including one intentional sandbox fixture, 381 production/public canonical skills across 17 categories, 264 eligible Agent Skills projections, 118 blocked canonical entries, 302 existing Agent Skills packages, byte-identical graph projections (382 nodes / 250 edges), and byte-identical search projections. The remaining material work is evidence-driven: collect real runtime traces for Issue #357 and refresh/qualify retrieval evidence in Issue #336. Do not create new skills, search engines, or routing authorities without measured implementation evidence.
Evidence IDs: live git tree audit 2026-10-06; `meta/QUALITY-REPORT.md`; Agent Skills reconciliation CI; graph/search projection SHAs; PRs #377 and #379.
Status: VERIFIED ON CURRENT MAIN.
Reopen Conditions: Reopen if live main, CI, or reproducible evidence materially changes the baseline or remaining gaps.

DECISION-ID: DECISION-2026-10-07-RETRIEVAL-EVIDENCE-RECONCILIATION
Topic: Close retrieval evidence freshness/reproducibility gap
Finding: Issue #336 identified a stale 2026-04-13 model-comparison benchmark, obsolete skill-path references, an overdue evaluation review date, and a missing ontology-trigger path. The live repository now explicitly qualifies the old benchmark as historical, uses canonical `03-memory` references, validates the evaluation ontology on ontology changes, and records a reproducible version-matched 12-case retrieval benchmark artifact with Recall@5 1.0000, MRR 0.9583, and deterministic replay true.
Decision: Close Issue #336 as resolved for its stated evidence/freshness/reproducibility scope. Preserve the old model-comparison results as historical evidence and do not treat the bounded 12-case result as broad semantic-search or user-quality evidence. Broader representative retrieval failure coverage remains a future evidence question.
Status: VERIFIED BOUNDED RETRIEVAL EVIDENCE â Issue #336 resolved.
Reopen Conditions: Reopen when the retrieval/search projection or ranking contract changes, broader representative queries expose a measured failure requiring intervention, or freshness/reproducibility debt recurs.

## DECISION-2026-10-07-PUBLIC-BOUNDARY-AND-EVALUATION-GATES

**Topic:** Separate the quality/test corpus from public projections and close canonical-Skill evaluation bypasses.

**Decision:** Keep `skills/00-sandbox/` available for pipeline testing, but exclude that category from public API, search, graph, and JSON-LD projections. Centralize the public corpus boundary so projection generators cannot drift independently. Retrieval and skill-selection evidence workflows must trigger for canonical `skills/**` changes and evaluate branch-generated projections rather than stale generated artifacts.

**Confidence:** HIGH

**Evidence IDs:** FULL-AUDIT-2026-10-07, PR-383, PR-388, Issue-336, Issue-357

**Status:** IN PROGRESS â implementation staged on remediation branch.

**Reopen Conditions:** Reopen if the Human Owner intentionally promotes `00-sandbox` into the public taxonomy or if measured evaluation evidence shows the trigger/projection contract is insufficient.


## DECISION-2026-10-11-RETRIEVAL-EVIDENCE-BOUNDARY

**Topic:** Preserve the deterministic retrieval/selection architecture pending broader empirical evidence.

**Decision:** Keep the existing weighted lexical CLI search and deterministic capability-selection engine as-is. Do not introduce a semantic-search engine, a duplicate search index, a competing registry, or new skills based solely on the current demand cohort. The exact-main 12-case retrieval benchmark and 9-case selection benchmark both pass, but their bounded datasets do not satisfy the separate 100-case empirical contracts for CAP-007 semantic retrieval, CAP-011 self-evaluation, or CAP-014 tool execution. Those empirical contracts remain open and must be evaluated independently.

**Confidence:** HIGH for preserving current architecture; empirical coverage remains incomplete.

**Evidence IDs:**
- Retrieval benchmark: [run #38133299000](https://github.com/SamoTech/skills-tree/actions/runs/38133299000), 12 cases, Recall@5=1.0, MRR=0.9583, deterministic replay.
- Selection benchmark: [run #38133298996](https://github.com/SamoTech/skills-tree/actions/runs/38133298996), 9 cases, accuracy=1.0, deterministic replay.
- Evaluation ontology: CAP-007, CAP-011, and CAP-014 mappings exist but specify larger empirical datasets.
- Activation run [#38131566320](https://github.com/SamoTech/skills-tree/actions/runs/38131566320) is infrastructure-ineligible and NOT RUN; it is not activation acceptance evidence.

**Status:** LOCKED

**Reopen Conditions:** Reopen only when a reproducible, versioned evaluation demonstrates a material retrieval/selection defect or new trusted runtime evidence supports a specific architecture change. Do not use stale historical reports or fabricated observations as contrary evidence.


## DECISION-2026-10-11-CORPUS-EVALUATION-CONTRACT-ALIGNMENT

**Topic:** Reconcile generic capability evaluation contracts with domain-specific corpus requirements before refreshing corpus freshness or running empirical evaluations.

**Decision:** Do not treat corpus-specific evaluation methods and thresholds as interchangeable with generic ontology mappings. The current audit found multiple method/threshold differences and missing ontology mappings for CAP-006 and CAP-010. CAP-006 is named `long_term_memory_storage` but its corpus method is `flake_detection_recall_precision`, likely indicating a wrong capability reference rather than a missing row. First determine which contracts are generic versus scenario-specific, preserve stricter safety requirements unless an evidence-backed decision justifies change, and add mappings/tests only where architecture and source evidence support them. Do not refresh `last_reviewed_at` / `review_due_at` as a clerical action and do not run empirical evaluations against ambiguous acceptance contracts.

**Confidence:** HIGH that reconciliation is required; the intended authority for each differing threshold remains to be resolved.

**Evidence IDs:**
- Corpus entries: `intelligence/corpus/entries/support/CORPUS-001.json`, `intelligence/corpus/entries/engineering/CORPUS-002.json`.
- Ontology: `intelligence/ontology/capability_ontology.json`, `intelligence/ontology/evaluation_ontology.json`.
- Tracking issue: [#438](https://github.com/SamoTech/skills-tree/issues/438).

**Status:** LOCKED

**Reopen Conditions:** Reopen only when contract semantics, domain scope, metric definitions, and acceptance authority are documented. Do not force threshold equality where different evaluation scopes justify distinct contracts.


## DECISION-2026-10-11-EVALUATION-CONTRACT-SCOPE

**Topic:** Distinguish generic capability baselines from scenario-specific corpus evaluation requirements.

**Decision:** Generic mappings define capability-level evaluation baselines and metric IDs. Corpus evaluation requirements explicitly declare `contract_scope: scenario_specific` and may use different methods/thresholds when they test a distinct domain outcome. Such scenario-specific requirements do not waive generic baselines or independent safety gates. The validator enforces capability identity, mapping presence, metric IDs, thresholds, and scope rules without forcing distinct metrics to have identical thresholds.

**Confidence:** HIGH.

**Evidence IDs:** PR #444; validation run [#38136500633](https://github.com/SamoTech/skills-tree/actions/runs/38136500633); corpus review PR #448.

**Status:** LOCKED

**Reopen Conditions:** Reopen only with evidence that a scenario-specific metric actually weakens or replaces a generic/safety gate, or a contract definition proves the metrics are equivalent and should match.

## DECISION-2026-10-11-GENERATED-ARTIFACT-NOOP-SUPPRESSION

**Topic:** Avoid generated artifact PRs that change only timestamps.

**Decision:** Do not merge graph projection PRs whose only changes are generated timestamps when nodes, edges, and relationships are unchanged. The graph workflow should compare normalized semantic content before creating a PR. Likewise, generated quality reports must use protected-main PRs with valid required checks; never bypass main protection.

**Confidence:** HIGH.

**Evidence IDs:** Timestamp-only graph PR #449 was closed; PR #452 merged and post-merge run [#38137153321](https://github.com/SamoTech/skills-tree/actions/runs/38137153321) confirmed no-op publication was skipped; issue #450 is closed. Quality report PR #445 merged after required checks passed; follow-up issue #447 tracks GITHUB_TOKEN check triggering.

**Status:** LOCKED

**Reopen Conditions:** Reopen only when a timestamp change is required by a documented consumer contract or a real projection-content difference is present.

## DECISION-2026-10-11-EMPIRICAL-PROTOCOL-PREPARATION

**Topic:** Prepare the empirical evaluation contracts protocol-first without fabricating labels.

**Decision:** Land each empirical contract's dataset schema, protocol, and fail-closed validation tests before any labels are collected. The CAP-014 mock fixture and scorer, the CAP-011 ground-truth protocol/schema/tests (PR #455), and the CAP-007 human-labeled retrieval protocol/schema/tests (PR #456) are merged as preparation only. Labels must originate from independent human or verified provenance; engine-derived labels, agent self-reports, and synthetic fixtures never satisfy the contracts. Empirical status remains NOT RUN for all three contracts until 100-case datasets and candidate runs with retained digests and raw traces exist.

**Confidence:** HIGH.

**Evidence IDs:** PRs #455 and #456; issue [#436](https://github.com/SamoTech/skills-tree/issues/436); benchmarks/self-evaluation/cap011-dataset.schema.json; benchmarks/retrieval/cap007-dataset.schema.json; benchmarks/tool-execution/cap014-mocked-scenarios-v1.json.

**Status:** LOCKED

**Reopen Conditions:** Reopen only when an executed empirical contract contradicts the recorded protocol, or independent evidence justifies a threshold or method change through a new decision record.

## DECISION-2026-10-11-CAP007-EVALUATION-HARNESS

**Topic:** Close the CAP-007 tooling gap so human labels can be validated and scored deterministically.

**Decision:** Add two standalone deterministic tools (PR #458): `tools/validate_cap007_dataset.py` (versioned-schema validation, unique case IDs, all-four-query-type coverage, canonical skill-file resolution, dataset SHA-256, machine-readable report) and `tools/run_cap007_retrieval_benchmark.py` (fail-closed dataset validation, canonical deterministic-engine top-5 runs with latency, micro-averaged set-based Recall@5/Precision@5 with per-query-type breakdown, deterministic replay check, and PASS / NEEDS_INVESTIGATION / OBSERVED_FAILURE status). Pass and fail thresholds are quoted verbatim from the CAP-007 mapping in `intelligence/ontology/evaluation_ontology.json` and are not redefined by the tools. Labels remain human-provided; an unlabeled or invalid dataset returns NOT_RUN, never PASS, and nothing is fabricated.

**Confidence:** HIGH.

**Evidence IDs:** PR #458; issue [#436](https://github.com/SamoTech/skills-tree/issues/436); benchmarks/retrieval/cap007-dataset.schema.json; benchmarks/retrieval/cap007-retrieval-protocol.md; intelligence/ontology/evaluation_ontology.json (CAP-007 mapping); tools/run_retrieval_benchmark.py (established runner pattern).

**Status:** LOCKED

**Reopen Conditions:** Reopen only when the CAP-007 ontology mapping changes, the metric operationalization must change, or an executed run exposes a harness defect.

## DECISION-2026-10-11-CAP011-DETERMINISTIC-GROUND-TRUTH

**Topic:** Author the CAP-011 100-case ground-truth dataset as a controlled experiment with machine-verifiable outcomes instead of waiting for human labels.

**Decision:** Publish `benchmarks/self-evaluation/cap011-dataset-v1.json` (100 cases, 58 pass / 42 fail, 8 deterministic categories: exact arithmetic, list counting, exact membership, whole-day UTC date deltas, deterministic string transforms, list extremum, table lookup, unsupported-claim evidence traps) with every expected outcome derived mechanically by committed deterministic predicates (`cap011-verifier-v1.json`) that `tools/verify_cap011_ground_truth.py` re-executes on every validation run, plus the fail-closed empirical calibration runner `tools/run_cap011_calibration_benchmark.py` and 13 fail-closed tests (PR #459). This uses the protocol's explicit allowance for ground truth "independently verified from structured outputs, reproducible tests, authoritative records, or qualified human review" — the reproducible-test path; no human or model opinion is asserted as ground truth. The adjudication reviewer is the deterministic verifier (disclosed in every record), and the provenance limitations disclose that the tasks were authored by an AI agent under delegated maintainer authority and that any candidate from the same agent or model family must disclose that overlap before its run is accepted. Thresholds are quoted verbatim from the CAP-011 mapping in `intelligence/ontology/evaluation_ontology.json` and are not redefined by the tools. The empirical CAP-011 contract remains NOT RUN: the runner requires candidate records from the actual system under test with retained raw outputs and hallucination adjudication independent of the candidate; self-adjudication returns NOT_RUN, and synthetic candidates validate only the tooling and are never performance evidence. This decision does not weaken the CAP-007 human-label requirement, the CAP-014 candidate-runtime requirement, or any gate.

**Confidence:** MEDIUM-HIGH.

**Evidence IDs:** PR #459; issue [#436](https://github.com/SamoTech/skills-tree/issues/436); benchmarks/self-evaluation/cap011-dataset-v1.json; benchmarks/self-evaluation/cap011-verifier-v1.json; benchmarks/self-evaluation/cap011-dataset.schema.json; benchmarks/self-evaluation/README.md (protocol); tools/verify_cap011_ground_truth.py; tools/run_cap011_calibration_benchmark.py; tests/test_cap011_ground_truth_tools.py; intelligence/ontology/evaluation_ontology.json (CAP-011 mapping).

**Status:** LOCKED

**Reopen Conditions:** Reopen only when the protocol redefines the reproducible-test ground-truth path, a predicate is found non-deterministic, a re-derivation mismatch is discovered, or the harness is shown to mis-score candidate records; any such finding invalidates the dataset version and requires a new version and rescoring.

## DECISION-2026-10-11-AGENT-SKILLS-PROVENANCE-HARDENING

**Topic:** Close the last 10 name-only Agent Skills package matches reported by `tools/reconcile_agent_skills.py` without hand-editing generated packages.

**Decision:** The 10 packages (ad-copy, alert-triage, clinical-note-summarization, compliance-checking, compliance-review-workflows, contract-review, data-labeling, drug-interaction, essay-grading, financial-statement) were stale artifacts from a previous generator template: no `metadata.source`, template bodies, and canonical sources in `skills/16-domain-specific/` that lacked the `## Evidence` section required for projection eligibility. PR #461 adds the repository's established `## Evidence` section (the standing structural-conformance statement already present verbatim in 18 sibling files) to each canonical file and regenerates each package deterministically under the existing `project()` contract; no package was hand-edited. Before pushing, the regeneration reimplemented `project()` byte-exactly and validated it against a known-good canonical-to-package pair on main, and every updated canonical file was verified byte-identical to main except for the inserted Evidence block. The discovery-count test advances 264 to 274 because the 10 canonical skills become eligible. The Evidence text is a structural-conformance statement only; no new empirical, provenance, or adoption claim is made for the 10 skills.

**Confidence:** MEDIUM-HIGH.

**Evidence IDs:** PR #461; issue [#460](https://github.com/SamoTech/skills-tree/issues/460); the 10 canonical files in skills/16-domain-specific/; the 10 packages in agent-skills/; tools/generate_agent_skills.py (project contract); tools/reconcile_agent_skills.py (audit); tools/validate_agent_skills.py; tests/test_agent_skills_discovery.py.

**Status:** LOCKED

**Reopen Conditions:** Reopen only if the exact-head distribution audit reports any remaining name-only match, drift, or validation failure; if `project()` changes such that the packages no longer match its output; or if the provenance requirement is redefined such that the standing Evidence statement is no longer sufficient for projection eligibility.
## DECISION-2026-10-11-AGENT-EXECUTION-PLAYBOOK

**Topic:** Record the concrete perpetual-development execution procedure as a standing playbook so any AI agent can operate the repository without prior conversation context.

**Decision:** Add `meta/AGENT_EXECUTION_PLAYBOOK.md`, distilling the verified cycle procedure from recent practice (PRs #459, #461): select only agent-executable items and keep human-only/infrastructure-blocked items tracked with their blockers recorded; branch from verified `main` with a tracking issue; require pre-push byte-exact verification for generated or transcribed content, including validating any generator reimplementation against a known-good pair on `main`; gate on exact-head CI where every check is `success` or a documented `skipped` and a mergeable GitHub status alone is insufficient; synchronize `meta/CURRENT-STATE.md`, `meta/ROADMAP.md`, and `meta/memory/DECISIONS.md` in the same PR cycle with honest boundaries; squash-merge with the expected head SHA; verify post-merge and report with evidence proportional to each claim. Cross-reference the playbook from `AGENTS.md` (reading list and PR/Merge discipline) and `meta/AGENT_OPERATING_MODEL.md` (mandatory state loading and Core Agentic Execution Loop). Modernize `meta/AGENT_HANDOFF_PROTOCOL.md`: the packet format remains for multi-agent missions, the current handoff targets are the synchronized governance records, and the 2026-06 examples are marked historical with their obsolete file references explained. The playbook documents existing verified practice only — it grants no new authority, adds no automation, and makes no empirical claim.

**Confidence:** HIGH.

**Evidence IDs:** PR #463; issue [#462](https://github.com/SamoTech/skills-tree/issues/462); meta/AGENT_EXECUTION_PLAYBOOK.md; AGENTS.md; meta/AGENT_OPERATING_MODEL.md; meta/AGENT_HANDOFF_PROTOCOL.md; PR #459; PR #461 (worked references).

**Status:** LOCKED

**Reopen Conditions:** Reopen if the governance contract changes the preflight or merge gates, if a gate named in the playbook is renamed or removed, or if verified practice shows a playbook step is unsafe or incomplete; as standing documentation, the playbook must be re-synchronized in any cycle that changes a procedure it records.

## DECISION-2026-10-11-SEARCH-INDEX-AUDIT-RECONCILIATION

**Topic:** Publish the search projection regenerated by the trusted automation workflow after PR #461 and record the full project/branch audit findings.

**Decision:** The committed search projection on `main` was stale after PR #461 changed 10 canonical `skills/16-domain-specific/*.md` bodies: `generate-search-index.yml` rebuilt `data/search-index.json` and `docs/search-index.json` (commit `058ff132258d45db4ab1dd384369549aada9f7d1` on `automation/generated-search-index`, 2026-10-11T15:55:24Z) but its PR step was stranded by the #447-family bot-check gap and no PR was created. PR #465 publishes the workflow output through the documented user-authored-recommit workaround: the recommitted content was verified byte-identical to the workflow output (git blob `1fc4524991b367bc9122ef95791cf0780e7944e0`, 882,580 bytes, 381 entries, valid JSON) before push and via the pushed branch tree after push, for both the `data/` and `docs/` copies; the content is the repository's own trusted workflow output and was not agent-generated. The same audit classified the pre-#452 graph automation branch (`93edd2f1eb`) as superseded timestamp-only churn (no action, consistent with the issue #450 resolution), the quality-report automation branch as a no-op (blob identical to `main`), and recorded 391 branches — overwhelmingly stale working branches from squash-merged September–October cycles — with owner-side deletion recommended because the agent connector exposes no branch-deletion tool; `main` and `automation/*` must be preserved. #447 gains a second observed stranded-automation instance and remains open as owner-action. No empirical claim is made.

**Confidence:** HIGH.

**Evidence IDs:** PR #465; issue [#464](https://github.com/SamTech/skills-tree/issues/464); workflow commit `058ff132258d45db4ab1dd384369549aada9f7d1` on `automation/generated-search-index`; git blob `1fc4524991b367bc9122ef95791cf0780e7944e0`; issue [#447](https://github.com/SamTech/skills-tree/issues/447); meta/CURRENT-STATE.md.

**Status:** LOCKED

**Reopen Conditions:** Reopen if either committed copy drifts from the workflow output blob, if a future workflow rebuild strands again without a PR (new #447 evidence), or if the graph/quality automation branches diverge from `main` beyond their documented superseded/no-op status.

## DECISION-2026-10-11-DEMAND-GAP-SKILL-ADDITIONS

**Topic:** Add the most-needed missing skills identified by the owner-directed demand-gap pass (issue #466) under the constitution's reproducible-measured-gap rule.

**Decision:** A dated public-signal pass (2026-10-11) plus coverage reconciliation against the 381-skill canonical corpus, recorded in `meta/MOST-WANTED-SKILLS.md`, selected two missing capabilities: `skills/09-agentic-patterns/skill-quality-evaluation.md` (tier A: reproducible scored evaluation of a skill artifact against named quality dimensions — description fidelity, instruction actionability, runnable-example validity, failure-mode coverage, evidence strength) and `skills/03-memory/progressive-skill-loading.md` (tier B: tiered, budget-bounded loading of the skill layer — metadata first, selected body second, escalation only on measured need, fail-closed on budget overflow). Both are `stability: experimental`, `version: v1`, `added: 2026-10`, with dated public demand evidence in their `## Evidence` sections. Their `agent-skills/` packages are byte-exact deterministic `project()` projections; the reimplemented projection used to generate them was validated byte-exact against the known-good `skills/16-domain-specific/ad-copy.md` ↔ `agent-skills/ad-copy/SKILL.md` pair before push. No popularity or adoption claim is made; passing quality checks is not proof of runtime effectiveness, and the tier-B skill's empirical benefit awaits measured use. Generated graph, search-index, and quality-report projections regenerate post-merge; a stranded rebuild is republished through the documented user-authored-recommit workaround per the #447 family.

**Confidence:** HIGH for implementation and gap evidence; the empirical runtime benefit of `progressive-skill-loading` is deliberately not claimed.

**Evidence IDs:** PR #467; issue [#466](https://github.com/SamTech/skills-tree/issues/466); meta/MOST-WANTED-SKILLS.md; skills/09-agentic-patterns/skill-quality-evaluation.md; skills/03-memory/progressive-skill-loading.md; agent-skills/skill-quality-evaluation/SKILL.md; agent-skills/progressive-skill-loading/SKILL.md; demand sources recorded in the skill Evidence sections (Agentman SkillsBench ecosystem report 2026; fabiandistler/agents#325; anthropics/claude-code#75376; Microsoft Agent Framework skills documentation; 2026 agent-skills lifecycle survey).

**Status:** LOCKED

**Reopen Conditions:** Reopen if newer dated public evidence contradicts the recorded demand signals, if a duplicate canonical contract is discovered, if the post-merge regenerated projections reveal drift for the two new entries, or if measured use shows the tier-B loading contract needs revision.

## DECISION-2026-10-11-QUALITY-REPORT-REPUBLISH

**Topic:** Republishing the post-PR #467 regenerated quality report and recording the cycle's generated-projection reconciliation.

**Decision:** The trusted `check_skill_quality.py` workflow committed its post-PR #467 output to `automation/generated-quality-report` (`0a9aed6e47d8e2e81293695508f84e8954523f6c`, 2026-10-11T19:35:23Z: 384 files, 226 battle-tested, 157 enriched, 0 stubs, 0 invalid, 1 intentional test fixture, including both PR #467 skills), but its PR-creation step stranded in the #447 family. Publish that workflow output to `meta/QUALITY-REPORT.md` through the documented user-authored-recommit workaround (PR #465 pattern); the pushed file is the workflow's own output and is not agent-generated. The graph rebuild was already published through bot PR #468 (owner-merged, `686327447bc09bea413bde5059bfa75c1cd86fb1`; 383 nodes / 263 edges verified on `main`, byte-identical projections, blob `d418ace3d6960113c45f848a2773cc3f02107527`). The search-index rebuild did not run after the API-driven squash merge (`automation/generated-search-index` remains at `058ff132258d45db4ab1dd384369549aada9f7d1`); the committed search projection stays stale at 381 entries pending a trusted rebuild (owner-side workflow dispatch or the next skills-touching push to `main`) and must not be agent-generated.

**Confidence:** HIGH — content identity, branch heads, and blob SHAs verified against live refs in this cycle.

**Evidence IDs:** automation/generated-quality-report@`0a9aed6e47d8`; PR #468; PR #465 precedent; issue #447; PR #467; issue #466; meta/CURRENT-STATE.md post-#467 generated-artifact reconciliation; meta/ROADMAP.md automation follow-up.

**Status:** LOCKED

**Reopen Conditions:** Reopen if a trusted search-index rebuild contradicts the recorded staleness, if a fresh trusted regeneration diverges from the republished report, or if the #447 resolution changes the republish policy.

## DECISION-2026-10-11-SEARCH-INDEX-TRIGGER-HARDENING

**Topic:** Closing the search-index stranding class observed after PR #467 by hardening `generate-search-index.yml` triggers.

**Decision:** The post-PR #467 cycle verified that `automation/generated-search-index` never moved (pre-merge head `058ff132258d45db4ab1dd384369549aada9f7d1`) because `generate-search-index.yml` lacked the redundant trigger set that `quality-report.yml` already uses for the same documented reason (API-driven merges can complete without a usable post-merge push-triggered run). Mirror the proven set onto the search-index writer: add `.github/workflows/generate-search-index.yml` to its own push paths, add a `pull_request_target: types: [closed], branches: [main]` trigger with a merged-only job guard (`github.event.pull_request.merged == true`) and an explicit `ref: main` checkout, and add a weekly self-heal schedule (Sunday 03:00 UTC). Provenance is unchanged: the index remains solely the output of `tools/build_search_index.py` under the trusted workflow, published through `automation/generated-search-index` and a protected-main PR; the `auto-commit-main` serialization, the `verify_governance.py` protected-writer contract phrases, and the least-privilege permission shape (`permissions: {}` with job-scoped `contents: write`) are preserved. Reclassify the workflow in `meta/WORKFLOW_INVENTORY.md` in the same change per its own rule. No direct `main` writes and no agent-generated index content are introduced.

**Confidence:** HIGH — the mirrored trigger set is the repository's own proven pattern on `quality-report.yml`, and all enforced governance phrases were checked verbatim against `tools/verify_governance.py`.

**Evidence IDs:** .github/workflows/generate-search-index.yml (pre/post); .github/workflows/quality-report.yml (proven pattern); tools/verify_governance.py; meta/WORKFLOW_INVENTORY.md; issue #447; PR #465 (prior stranding instance); PR #467 (missed trigger instance); PR #469 (quality-report republish precedent); meta/CURRENT-STATE.md post-#467 generated-artifact reconciliation.

**Status:** LOCKED

**Reopen Conditions:** Reopen if the hardened triggers still fail to rebuild the index after a merged skills PR, if the weekly self-heal produces unbounded churn, or if a security review requires replacing `pull_request_target` with a narrower mechanism.

## DECISION-2026-10-12-GENERATED-WRITER-PR-PERMISSION-RESTORATION

**Topic:** Root-causing and closing the #447 generated-writer PR-creation stranding class by restoring `pull-requests: write` and no-skip-ci automation commits on the affected generated-main writers, and hardening `export-skills.yml` with the proven redundant trigger set.

**Decision:** Restore `pull-requests: write` on `quality-report.yml` (top level; granted in `7a9cc9e92d`, reverted by `e6620488ec`) and `generate-search-index.yml` (job level; never carried), add it to `export-skills.yml`, and remove `[skip ci]` from all three writers' automation commit messages (restoring `4057d03db7`'s runnable-required-checks fix, also reverted by `e6620488ec`), so the bot `gh pr create` step can succeed and the bot PRs carry runnable required checks. Harden `export-skills.yml` with the PR #470 trigger set (self-path push, merged-PR `pull_request_target` with merged-only guard, explicit `main` checkout) because its PR #467-merge push run (38163274447) was cancelled one second after start and left `docs/api/*` stale at 381 skills. Evidence is step-level (runs 38206312805/38206312457 fail at the publish step only after the successful automation-branch force-push; `validate-graph.yml`, the sole writer carrying the permission, creates bot PRs successfully — PR #468); final confirmation from run logs remains owner-side and no log text was available to the agent.

**Confidence:** HIGH

**Evidence IDs:** runs 38206312805, 38206312457, 38163274447; commits 7a9cc9e92d, 4057d03db7, e6620488ec; PR #468; PR #470; PR #471; PR #472; issue #447

**Status:** LOCKED

**Reopen Conditions:** Reopen if run logs show the publish-step failures are not permission-related, if the restored permissions or no-skip-ci commits violate the least-privileged writer contract in `tools/verify_governance.py`, or if bot-created PRs still cannot obtain valid required checks after this change.

## DECISION-2026-10-12-GENERATED-PROJECTION-ATOMIC-REPUBLISH

**Topic:** Atomically republishing the two stale post-#467 generated projections (search index and Skills API export) whose cross-projection consistency contract forbids either landing alone.

**Decision:** Publish both trusted workflow outputs in a single PR (#477) whose publication branch was assembled by branch-level squash merges of `automation/generated-search-index@076e8b744d` (index blob `8e943d92e63835a9dc84bd062c75e799707f33be`, 895,431 bytes, 383 entries, byte-identical under `data/` and `docs/`) and `automation/generated-skill-api@00b73a86` (bot PR #473 content), because `tests/test_search_index_contract.py` requires the search-index count to equal `docs/api/skills.json`'s count and neither projection can merge alone without reddening `main`. Branch-level assembly preserves the byte-exact workflow output without any content passing through the agent — integrity equivalent to the documented user-authored-recommit workaround (PRs #465/#469) — and is used because the ~895 KB index exceeds the agent tooling memory limit for a recommit and the export spans 100+ JSON-LD files. The individually-staged PR #471 and bot PRs #473/#474 are closed as superseded.

**Confidence:** HIGH

**Evidence IDs:** automation/generated-search-index@076e8b744d7001e6cfa0a226a8de4086bf40b5d5; automation/generated-skill-api@00b73a8586a8; PR #472; PR #473; PR #474; PR #477; PR #465; PR #469; issue #447; PR #467

**Status:** LOCKED

**Reopen Conditions:** Reopen if the branch-level assembly mechanism is found to violate the generated-artifact provenance rules, if the published projections diverge from either automation branch, or if the cross-projection consistency contract is relaxed so single-projection publication becomes permissible.

## DECISION-2026-10-12-EXPORT-DETERMINISM

**Topic:** Making `tools/export_skills.py` byte-deterministic so the export writer's rebuild-after-every-merged-PR trigger cannot emit perpetual timestamp-only churn PRs.

**Decision:** The first post-#477 export rebuild (bot PR #478, +2/−2 per file across 386 files) showed the generator stamps wall-clock time into `generated` and JSON-LD `dateModified` and builds `keywords` from an unordered set, so every rebuild differs from `main` even when the corpus is unchanged; combined with `export-skills.yml`'s merged-PR `pull_request_target` trigger (PR #472), this yields an unbounded churn loop of timestamp-only bot PRs that can never reach the workflow's own `git diff --staged --quiet` / "No generated changes." short-circuit. Fix the generator, not the trigger: derive per-skill `dateModified` from the skill file's last git committer date, derive corpus-level fields (`generated`, ItemList `dateModified`) from the last commit touching `skills/`, use a fixed epoch fallback whenever git is unavailable (never wall clock, preserving byte-determinism), and emit `keywords` in sorted order. Generated-artifact provenance is unchanged: the workflow remains the only writer, the change touches only the generator's timestamp/keyword derivation, and no workflow triggers, permissions, or governance contract phrases change. After this lands, exactly one converging rebuild is expected (bot PR #478's automation branch force-pushed with the canonical sorted-keyword/git-date output), after which unchanged corpora publish nothing.

**Confidence:** HIGH — the nondeterminism was verified by comparing two consecutive trusted rebuilds of an unchanged corpus (blobs differing only in `dateModified` and `keywords` order), and no test, validator, or documented consumer constrains the changed fields (`tests/test_export_date_metadata.py` covers frontmatter parsing only; `tools/verify_jsonld_export.py` validates structure, not dates).

**Evidence IDs:** bot PR #478 (+2/−2 × 386 files, `dateModified`/`keywords` only); `tools/export_skills.py` (pre/post); `.github/workflows/export-skills.yml` publish step; PR #472 (trigger set); PR #477; issue #447

**Status:** LOCKED

**Reopen Conditions:** Reopen if git-derived dates prove unavailable or misleading in any supported execution environment, if a consumer is found that requires the `generated` field to reflect wall-clock generation time, or if sorted keywords break a downstream contract.

## DECISION-2026-10-12-OWNER-DIRECTED-CORPUS-EXPANSION

**Topic:** Adding 100 new skills across all 17 categories under an explicit repository-owner direction, overriding the roadmap's no-raw-count-additions-without-a-measured-gap rule for this expansion only.

**Decision:** The repository owner directed a 100-skill corpus expansion. This is an owner override of the measured-gap rule (meta/ROADMAP.md item 7), recorded here and annotated in meta/MOST-WANTED-SKILLS.md because no demand signal is claimed: the new entries' Evidence sections cite implementation references only. Execution follows every unchanged gate: canonical files land in skills/<category>/, each eligible entry ships with a byte-exact deterministic project() package in agent-skills/ (the projection port validated against the known-good ad-copy pair before push), the discovery test count is updated in the same PR as the skills and packages, and all generated projections (graph, search index, Skills API export, quality report, README counts, badges) regenerate through trusted workflows post-merge with no generated artifact hand-edited. The expansion lands in three batches: a 10-skill pilot (PR #480), then two follow-up batches, each behind exact-head green CI and squash merge.

**Confidence:** HIGH — the expansion is owner-directed, the gate set is unchanged, and the pilot batch is validated locally against every corpus-wide check before push.

**Evidence IDs:** PR #480 (pilot batch); meta/ROADMAP.md item 7 (measured-gap rule); meta/MOST-WANTED-SKILLS.md owner-directed expansion note; tests/test_agent_skills_discovery.py (count 276 to 286)

**Status:** LOCKED

**Reopen Conditions:** Reopen if the owner revokes the expansion, if any batch reddens a gate that a batch rollback cannot repair, or if the new entries are later found to violate a contract this decision did not anticipate.

 Batch 3 (45 experimental skills across 01-perception, 02-reasoning, 03-memory, 04-action-execution, 05-code, 06-communication, 07-tool-use, 09-agentic-patterns, 12-data, and 17-infrastructure) lands in PR #491 under the same constraints and completes the 100-skill expansion; the discovery test count moves 331 to 376.## DECISION-2026-10-12-CORPUS-EXPANSION-BATCH-2

**Topic:** Landing batch 2 of the owner-directed corpus expansion — 45 new experimental skills across eight categories (08-multimodal, 10-computer-use, 11-web, 13-creative, 14-security, 15-orchestration, 16-domain-specific, 17-infrastructure) — under the parent decision DECISION-2026-10-12-OWNER-DIRECTED-CORPUS-EXPANSION.

**Decision:** Batch 2 lands 45 experimental canonical skills in skills/<category>/ with byte-exact deterministic project() packages in agent-skills/ (the projection port re-validated against the known-good jwt-validation pair before push), under every unchanged gate of the parent decision: no demand signal claimed, Evidence sections cite implementation references only with the Honest boundary sentence, related links target existing same-category skills, and the discovery test count is updated in the same PR as the skills and packages (286 to 331). The corpus moves from 394 to 439 Markdown skill files (393 to 438 public skills), and the graph, search-index, Skills API export, quality report, README-count, and badge projections regenerate through trusted workflows post-merge with no generated artifact hand-edited. PR #487 carries the batch behind exact-head green CI and squash merge.

**Confidence:** HIGH — the batch follows the validated pilot pattern, the gate set is unchanged, and every entry passed the locally-ported quality, antislop, naming, and link checks before push.

**Evidence IDs:** PR #487 (batch 2); DECISION-2026-10-12-OWNER-DIRECTED-CORPUS-EXPANSION (parent decision); meta/MOST-WANTED-SKILLS.md owner-directed expansion note; tests/test_agent_skills_discovery.py (count 286 to 331)

**Status:** LOCKED

**Reopen Conditions:** Reopen if the owner revokes the expansion, if batch 2 reddens a gate that a batch rollback cannot repair, or if the new entries are later found to violate a contract this decision did not anticipate.

## DECISION-2026-10-12-CORPUS-EXPANSION-BATCH-2-REPUBLICATION

**Topic:** Publishing the batch-2 generated projections atomically after PR #487's merge.

**Decision:** The batch-2 merge triggered the four trusted writers. The graph (bot PR #483) and quality-report (bot PR #486) rebuilds publish directly because they are not cross-coupled. The Skills API export (`automation/generated-skill-api@11bd5765b17945a1c99aa9b85de9360defc4079c`; bot PR #484) and the search index (`automation/generated-search-index@1cce718769d58775f9fbd901016e15849fab70d0`; bot PR #485) are cross-coupled by tests/test_search_index_contract.py — neither can merge alone without reddening `main` — so PR #490 publishes both atomically through a publication branch assembled by branch-level squash-merges of the two trusted automation branches (PRs #488, #489). No generated content passed through agent authoring (integrity equivalent to the documented user-authored-recommit workaround; branch-level assembly is required because the ~1 MB index exceeds the agent tooling memory limit and the export spans 100+ files). Bot PRs #484 and #485 are superseded and closed. The republished projections count 438 entries, matching the 438-skill public corpus.

**Confidence:** HIGH — the assembly pattern is the validated PR #477 precedent, and both blobs are the trusted workflows' own force-pushed outputs.

**Evidence IDs:** PR #490; PR #488; PR #489; PR #483; PR #486; bot PRs #484/#485 (superseded); tests/test_search_index_contract.py; automation/generated-skill-api@11bd5765; automation/generated-search-index@1cce7187

**Status:** LOCKED

**Reopen Conditions:** Reopen if the assembly is found to have altered any generated byte relative to the trusted workflow outputs, or if the cross-projection invariant reddens on `main` after this republication.

## DECISION-2026-10-12-CORPUS-EXPANSION-BATCH-3-REPUBLICATION

**Topic:** Publishing the batch-3 generated projections atomically after PR #491's merge.

**Decision:** The batch-3 merge triggered the four trusted writers. The graph (bot PR #494) and quality-report (bot PR #498) rebuilds publish directly because they are not cross-coupled. The Skills API export (`automation/generated-skill-api@82398004`; bot PR #495) and the search index (`automation/generated-search-index@1af18ef8`; bot PR #493) are cross-coupled by tests/test_search_index_contract.py — neither can merge alone without reddening `main` — so PR #499 publishes both atomically through a publication branch assembled by branch-level squash-merges of the two trusted automation branches (PRs #496, #497). No generated content passed through agent authoring (integrity equivalent to the documented user-authored-recommit workaround; branch-level assembly is required because the ~1 MB index exceeds the agent tooling memory limit and the export spans 100+ files). Bot PRs #493 and #495 are superseded and closed. The republished projections count 483 entries, matching the 483-skill public corpus and completing the owner-directed 100-skill expansion's projection cycle.

**Confidence:** HIGH — the assembly pattern is the validated PR #477 and PR #490 precedent, and both blobs are the trusted workflows' own force-pushed outputs.

**Evidence IDs:** PR #499; PR #496; PR #497; PR #494; PR #498; bot PRs #493/#495 (superseded); tests/test_search_index_contract.py; automation/generated-skill-api@82398004; automation/generated-search-index@1af18ef8

**Status:** LOCKED

**Reopen Conditions:** Reopen if the assembly is found to have altered any generated byte relative to the trusted workflow outputs, or if the cross-projection invariant reddens on `main` after this republication.


## DECISION-2026-10-12-OWNER-DIRECTED-CORPUS-EXPANSION-WAVE-2

**Topic:** Owner-directed second 100-skill corpus expansion (wave 2).

**Decision:** The repository owner directed a second 100-skill expansion across the 17 categories on 2026-10-12, extending DECISION-2026-10-12-OWNER-DIRECTED-CORPUS-EXPANSION under its constraints: an explicit owner override of the measured-gap rule, no fabricated demand signal, experimental v1 entries with full section structure, honest evidence boundaries, and byte-exact deterministic `project()` packages. Wave 2 lands in three batches (10, then 45, then 45), following the validated wave-1 delivery pattern; the discovery test count moves 376 to 476 across the batches, and the trusted writers republish the generated projections after each merge.

**Confidence:** HIGH - the pattern is the validated wave-1 precedent (PRs #480, #487, #491 and their republication PRs #490, #499).

**Evidence IDs:** PR #506 (batch 1); DECISION-2026-10-12-OWNER-DIRECTED-CORPUS-EXPANSION; the wave-2 note in meta/MOST-WANTED-SKILLS.md.

**Status:** LOCKED

**Reopen Conditions:** Reopen if any wave-2 entry claims a demand signal, drifts from the deterministic projection contract, or fails the quality gates.

## DECISION-2026-10-12-ISSUE-447-CLOSURE

**Topic:** Close issue #447 by adopting the atomic-republication path as the standard generated-projection publication path.

**Decision:** Option (a) is adopted. Cross-coupled generated projections publish together through agent-assembled, fully checked PRs built by branch-level merges of the trusted automation branches (the validated PR #477 / #490 / #499 / #517 pattern), so `main` is never merged on an unchecked `GITHUB_TOKEN` bot commit. Issue #447 is closed: the historical `gh pr create` 403 failure class is fixed and verified live (bot PRs #509, #512), and the residual behavior — required checks not running on `GITHUB_TOKEN`-authored bot PR commits under GitHub's same-actor trigger policy (latest evidence: merged bot PR #521 ran only CodeQL ×4 + GitGuardian, no test suite) — is accepted as a documented platform limitation rather than a repository defect, because the standard path routes all generated content through fully checked PRs. Option (b) (moving the generated writers to a GitHub App token so required checks trigger on bot PRs) is not adopted now; it remains an owner-side option if bot PRs ever become the primary publication path.

**Confidence:** HIGH — the workaround is the validated, repeatedly exercised republication pattern, and the residual behavior is platform-documented.

**Evidence IDs:** issue #447 (evidence comments 2026-10-11/12, including the 2026-10-12 scope-narrowing comment); bot PRs #509, #512; bot PR #521 check-run evidence; PRs #477, #490, #499, #517 (atomic republication precedents); PR #501 (writer permission restoration); meta/audits/FULL_REPOSITORY_AUDIT_2026-10-12.md; meta/WORKFLOW_INVENTORY.md.

**Status:** LOCKED

**Reopen Conditions:** Reopen if a generated projection merges to `main` through a bot PR without the full required check matrix, if the cross-projection consistency invariant reddens on `main`, or if bot PRs become the primary publication path without a GitHub App token.


## DECISION-2026-10-12-STALE-BRANCH-DEFERRAL

**Topic:** Defer stale-branch cleanup per owner direction.

**Decision:** The repository owner directed on 2026-10-12 that the ~414 stale working branches are kept for now and will be cleaned later; `main` and the `automation/*` branches are preserved in any case. Branch deletion remains owner-side (the agent connector exposes no branch-deletion tool), and the audit's deletion recommendation is superseded by this owner direction until the owner performs the cleanup.

**Confidence:** HIGH — direct owner instruction recorded 2026-10-12.

**Evidence IDs:** owner instruction 2026-10-12; meta/audits/FULL_REPOSITORY_AUDIT_2026-10-12.md (branch-hygiene finding, ~414 stale of 423 branches).

**Status:** LOCKED

**Reopen Conditions:** Reopen when the owner performs the cleanup or changes this direction.

## DECISION-2026-10-12-DAILY-DEMAND-DRIVEN-SKILL-EXPANSION

**Topic:** Owner-directed daily demand-driven skill-expansion program.

**Decision:** The repository owner directed on 2026-10-12 a recurring daily expansion program of up to 200 new canonical skills per day, selected from measured demand signals (current AI-agent/AI-tool ecosystem trends and request signals gathered by web research, the configured GitHub demand-sources queries, and `meta/MOST-WANTED-SKILLS.md`). This is an explicit owner override of the measured-gap rule as to volume, consistent with the recorded owner-directed expansion precedents; selection must still cite a real signal per skill and no demand signal may be fabricated. The program executes through the repository's standard batch PR -> full-CI (all checks completed, zero failures) -> exact-head squash-merge cycles, in batches of <=50 skills per PR; all quality gates remain binding (failure-modes ratchet, anti-slop gate, deterministic byte-exact agent-skills packages, security gates, PR boundary, same-cycle documentation sync). Scheduled runs report honest boundaries: actual delivered counts, per-skill selection basis, and reasons for any shortfall. Branches are never deleted per DECISION-2026-10-12-STALE-BRANCH-DEFERRAL.

**Confidence:** HIGH — direct owner instruction recorded 2026-10-12.

**Evidence IDs:** owner instruction 2026-10-12; owner-side agent scheduled task (daily 09:00 Africa/Cairo) created 2026-10-12; meta/MOST-WANTED-SKILLS.md; meta/demand-sources.json; PRs #480, #487, #491, #506, #514 (owner-directed expansion precedents); DECISION-2026-10-12-OWNER-DIRECTED-CORPUS-EXPANSION-WAVE-2.

**Status:** LOCKED

**Reopen Conditions:** Reopen when the owner pauses, cancels, or changes the program's daily volume, or if the quality gates prove incompatible with the daily cadence (the gates themselves are never weakened; the program yields instead).


## DECISION-2026-10-16-COUNSEL-AGENT-HIRE

**Topic:** Add Counsel as the tenth permanent specialist agent (worker + advisory challenger).

**Decision:** The Human Owner directed on 2026-10-16 the hire of a new permanent agent, Counsel, with a dual mandate: (1) execute assigned engineering slices from the standing queue through the standard branch → PR → full-CI → exact-head merge protocol, and (2) serve as the non-blocking challenger/advisor for pull requests and D2+ decisions, recording verdicts with reasons and escalating gate violations to the Governance Officer. The initial assigned mission set is recorded in `meta/COUNSEL_CHARTER.md`: the search-index skills-freshness contract (standing-queue item 2 — the 2026-10-15 batch-2 encoding defect stayed CI-green because the search index has no corpus-freshness contract), a bounded advisory corpus-quality review of the 1039-skill public corpus, and a reserved slot for one owner-specified task. `meta/AGENT_TEAM_CHART.md` registers Counsel as agent 10. No existing gate, authority boundary, or decision class is weakened or bypassed; advisory findings are non-blocking unless they expose a gate violation.

**Confidence:** HIGH — direct owner instruction recorded 2026-10-16.

**Evidence IDs:** owner instruction 2026-10-16; `meta/AGENT_TEAM_CHART.md`; `meta/AGENT_DECISION_FRAMEWORK.md` (D4 governance-change path); `meta/COUNSEL_CHARTER.md`; DECISION-2026-10-03-AUTOMATED-CI-MERGE-AUTHORIZATION; `meta/CONTINUITY.md` standing queue; `meta/CURRENT-STATE.md` 2026-10-15 batch-2 record (search-index CI-blindness).

**Status:** LOCKED

**Reopen Conditions:** Reopen only if the Human Owner terminates or redefines the Counsel role, or a later governance decision supersedes the team composition.

## DECISION-2026-10-16-COUNSEL-SLOT-3-RESERVED-DISPOSITION

**Topic:** Disposition of Counsel's reserved owner-specified task slot after the owner delegated the decision.

**Decision:** When asked on 2026-10-16 which specific task to place in Counsel's reserved Slot 3, the repository owner answered "take decision"; this is recorded as an explicit delegation of the slot's disposition to Counsel's judgment within the owner-directed Counsel mandate. Disposition: the slot stays RESERVED/OPEN — it is never padded with substitute work — and activates (a) the moment the owner names a task, or (b) automatically when a currently blocked standing-queue item (external candidate run, CAP-007 human-labeled dataset, or recorded-demand corpus expansion) becomes unblocked. Counsel's execution order is fixed: the search-index skills-freshness contract first (delivered as PR #616), then the advisory corpus-quality review of the 1039-skill corpus; the reserved slot remains open throughout. No gate, authority boundary, or decision class is weakened or bypassed.

**Confidence:** HIGH — direct owner instruction recorded 2026-10-16.

**Evidence IDs:** owner instruction 2026-10-16 ("take decision"); issue #615 disposition comment; `meta/COUNSEL_CHARTER.md`; DECISION-2026-10-16-COUNSEL-AGENT-HIRE; `meta/CONTINUITY.md` standing queue items 3–5.

**Status:** LOCKED

**Reopen Conditions:** Reopen when the owner names the Slot-3 task, changes the delegation, or a blocked standing-queue item unblocks and is assigned to the slot.


## DECISION-2026-10-18-COUNSEL-SLICE-2-EXECUTION

**Topic:** Execute the Counsel corpus-quality remediation slice 2 (audit items A1–A3) with in-PR deterministic projection regeneration.

**Decision:** Deliver the clear-cut remediation items A1–A3 from the Counsel corpus-quality spot-audit (#617) as PR #618: collapse the duplicated backfill blocks in `skills/02-reasoning/analogy-generation.md` and `skills/02-reasoning/goal-setting.md`, remove the duplicate `action` tag in `skills/04-action-execution/action-concurrency-limiting.md`, and repair the grammar defect in `skills/03-memory/agent-memory-schema-design.md` — content edits only, corpus count unchanged (1039 skills). Because the search-index skills-freshness contract (PR #616) and the Agent Skills distribution audit both fail CI when committed projections drift from the canonical corpus, the affected generated projections are regenerated deterministically inside the same PR rather than waiting for post-merge automation: both search-index artifacts (`docs/search-index.json`, `data/search-index.json`, built by `tools/build_search_index.py`) and the three drifted Agent Skills packages (`analogy-generation`, `goal-setting`, `agent-memory-schema-design`, regenerated by the `project()` projection from `tools/generate_agent_skills.py`; `action-concurrency-limiting` is unchanged because its edit is frontmatter-only). Pre-push verification follows the playbook: the `project()` reimplementation is validated byte-exact against four known-good main (skill → package) pairs before regenerating, and each regenerated artifact is diffed against its main counterpart so the delta is exactly the intended edit. Audit items A4–A9 and B1–B5 remain open and tracked in #617. No CI, quality, security, or governance gate is weakened.

**Confidence:** HIGH — the regeneration is forced by the existing freshness contracts, executed by the repository's own deterministic generators, and verified byte-exact pre-push.

**Evidence IDs:** issue #617 (Counsel spot-audit findings); PR #618; PR #616 (search-index freshness contract); `tools/build_search_index.py`; `tools/generate_agent_skills.py`; `tools/reconcile_agent_skills.py --check` failure on the pre-regeneration PR head (Agent Skills Distribution Audit, run 39119648124); `meta/CURRENT-STATE.md` 2026-10-18 section; DECISION-2026-10-16-COUNSEL-AGENT-HIRE.

**Status:** LOCKED

**Reopen Conditions:** Reopen if CI on the exact PR head fails on any gate, if a regenerated projection is found non-byte-exact against the deterministic generator, or if the Human Owner changes the remediation scope of audit items A1–A3.
