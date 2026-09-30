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
Decision: Merge focused PR #141 after verification; close duplicate PR #150; keep #145, #146, #155, #156, and #142 open pending current-main revalidation and reconciliation where changes overlap. Vercel deployment-rate-limit failures are treated as infrastructure conditions, not code-quality evidence.
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

**Status:** IN PROGRESS — Batch 01 merged; post-merge generated quality report refresh pending.

**Reopen Conditions:** Change only if the canonical Agent Skills specification, repository quality contract, or security findings materially change.

**Execution record:** Batch 01 covers 10 perception skills and adds `tools/validate_agent_skills.py` plus `.github/workflows/validate-agent-skills.yml`. Remaining stubs are intentionally not mass-promoted without evidence. The generated quality report must be refreshed before reporting the new corpus counts.
