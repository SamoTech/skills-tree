# AGENT EXECUTION PLAYBOOK

**Status:** ACTIVE  
**Authority:** `AI_CONSTITUTION.md`, `AGENTS.md`, `meta/AGENT_OPERATING_MODEL.md`, `meta/COO_MASTER_MISSION.md`  
**Scope:** the concrete, step-by-step procedure for executing a perpetual-development cycle in this repository. `meta/AGENT_OPERATING_MODEL.md` defines the bounded Core Agentic Execution Loop (`OBSERVE → ASSESS → PLAN → EXECUTE → VERIFY → RECORD → DECIDE`); this playbook defines how each phase is executed concretely against GitHub, CI, and the governance documents.

---

## 1. Select the next work item (PLAN input)

- Sources, in priority order: the execution sequence in `meta/CURRENT-STATE.md`, the current execution block in `meta/ROADMAP.md`, open issues, CI/audit failures, and verified documentation drift.
- Select only items that are **agent-executable within documented authority**. Items that require human-only input (e.g., human-labeled datasets), owner-only control-plane actions, or unavailable infrastructure are `BLOCKED`; keep them tracked with the blocker recorded and do not work around them.
- Prefer the smallest evidence-backed change that closes a documented gap. Do not invent work merely to keep the loop active.
- If no agent-executable item exists, record that finding and the blocking conditions, and select `BLOCKED` rather than fabricating work.

## 2. Branch and tracking discipline

- Verify the live `main` head SHA, then branch from it, named `fix|feat|docs|chore/<short-slug>`.
- If the item is not already tracked by an open issue, create a tracking issue first with: problem, concrete fix, and acceptance criteria. Close it via the PR body (`Closes #N`).
- Generated artifacts (`agent-skills/`, `docs/api/`, `data/`, search index, graph) are projections: never hand-edit them. Change the canonical source or the deterministic generator and regenerate.

## 3. Pre-push verification (mandatory for generated or transcribed content)

Any content derived from another file must be verified byte-exact against the repository **before** pushing:

- Validate any reimplementation of a generator against at least one known-good input/output pair already on `main` before trusting its output.
- Verify every modified file against its `main` counterpart; the delta must be exactly the intended change (e.g., only the inserted section) — no accidental reformatting, whitespace, or encoding drift.
- Run, before pushing, the same structural checks the CI validators will enforce: schema conformance, size limits, required sections, secret patterns, count expectations in tests.
- Push with conventional-commit messages per `.github/COMMIT_CONVENTION.md`.

## 4. PR and the exact-head CI gate

- Open the PR against `main` using `.github/pull_request_template.md`; check every applicable checklist item honestly and note explicitly what does not apply and why.
- Verify CI on the **exact head SHA of the final push**: every check run must be completed with `success`, or `skipped` for jobs documented as out of scope on PRs (e.g., main-only generation/quality jobs). A mergeable GitHub status alone is not sufficient.
- Distinguish infrastructure failures from code failures before reacting; never weaken a gate to make CI green.

## 5. Documentation synchronization (same cycle)

- The work commit and its documentation sync belong to the **same PR cycle**; do not leave documentation for a later PR.
- Update in this cycle: `meta/CURRENT-STATE.md` (state bullets and execution sequence), `meta/ROADMAP.md` when roadmap state changes, and a decision record appended to `meta/memory/DECISIONS.md` for significant decisions (Topic, Decision, Confidence, Evidence IDs, Status, Reopen Conditions).
- Documentation must separate what is **verified** from what is **pending**, cite PR/issue/run references, and state honest boundaries — what the change does *not* claim.

## 6. Merge

- Squash-merge with the expected head SHA of the PR branch; use a conventional-commit title carrying the PR number.
- Merge only when the exact-head gate and the repository's documented invariants are satisfied (see `AGENTS.md` — PR and Merge Discipline).

## 7. Post-merge verification and reporting

- Verify live `main` at the merge SHA (spot-check the merged files).
- Verify the tracking issue closed; post a summary comment recording what changed, what was verified (with the exact-head CI evidence), honest boundaries, and remaining blockers with their blocking conditions.
- Generated-projection automation runs on trusted `main` pushes and may open follow-up PRs; bot-created commits can produce `action_required` check results (the #447 caveat) — document the behavior rather than bypassing protections.

## 8. Reporting to the owner

- Report concisely in the owner's requested language: what changed, the evidence, the honest boundaries, what remains, and the next executable action.
- Never claim empirical results, adoption, or production readiness without evidence supporting that exact claim. Evidence must be proportional to the claim.

## Worked references

PR #459 (CAP-011 deterministic ground truth) and PR #461 (Agent Skills provenance hardening, closing #460) executed this playbook end-to-end: tracking issue → deterministic change with pre-push byte-exact verification → exact-head CI (30/30 green on the final head) → squash-merge with expected head SHA → post-merge verification → summary comment → same-cycle documentation sync.
