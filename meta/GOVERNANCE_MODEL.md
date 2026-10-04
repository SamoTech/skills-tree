# Skills Tree — Repository Governance Model

Effective: 2026-10-04
Scope: repository-enforced governance only

## Purpose
This document defines governance controls enforced by the repository itself. It deliberately does not require GitHub branch protection, required human approvals, or a GitHub ruleset for repository completion.

## Merge gate
1. The exact PR HEAD passes applicable automated validation, test, build, and security checks.
2. The change preserves documented architectural invariants and canonical-source boundaries.
3. Required documentation is synchronized and the documentation preflight is satisfied.
4. No unresolved blocking CI or security failure remains.
5. The COO may merge without a human approval requirement.

A GitHub UI state of mergeable is not semantic evidence. Absence of branch protection does not waive repository-local validation.

## Mandatory repository controls
- skills/ is the canonical skill source; generated indexes and distributions are projections.
- Agent preflight and completion rules are authoritative in AI_CONSTITUTION.md and AGENTS.md.
- New stubs and anti-slop violations are blocking PR checks.
- Security scanning includes Gitleaks, blocking Bandit SAST, and strict dependency auditing.
- Search, graph, JSON-LD, Agent Skills, and release boundaries each have an authoritative implementation/workflow.
- Zero-touch release uses semantic-release calculated next version and skips build/publish when no release is due.
- Documentation synchronization is a completion gate and is additionally protected by the repository governance contract checker.
- This model is testable from a clean checkout without private chat history.

## Control-plane independence
GitHub branch protection is not a project completion gate. It is intentionally outside this project's required completion model. If enabled later, it is an additional control-plane safeguard, not a prerequisite for repository-level correctness or completion.

Issue #159 is therefore not an engineering blocker under this governance model. Any future control-plane decision must be recorded as a new decision rather than silently changing this contract.
