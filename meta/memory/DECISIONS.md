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
