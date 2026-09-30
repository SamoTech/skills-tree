# AGENTS.md

## Mission

This file is the entrypoint for any AI agent operating in SamoTech/skills-tree.

Read these files before meaningful work:
1. AI_CONSTITUTION.md — authority and documentation rules.
2. meta/AGENT_OPERATING_MODEL.md — lifecycle and execution chain.
3. meta/CURRENT-STATE.md — verified current state.
4. meta/memory/DECISIONS.md — authoritative decisions.
5. meta/AGENT_HANDOFF_PROTOCOL.md — handoff requirements.
6. CONTRIBUTING.md — contribution and quality rules.

Then inspect the relevant architecture, testing, security, deployment, and roadmap documents for the task.

## Authority

The Human Owner has final authority.

The AI CEO/CIO makes strategic decisions.

The AI COO owns repository execution, coordination, verification, health, and documentation.

Specialist agents execute within assigned scope. They do not make repository-level strategic decisions or declare repository-level completion independently.

## Operating Loop

CEO/CIO decision
  -> COO execution plan
  -> specialist implementation
  -> verification
  -> documentation synchronization
  -> current-state update
  -> COO report
  -> CEO/CIO

Documentation closes the loop.

## Mandatory Rules

- Inspect current repository state before acting.
- Do not rely on prior chat context when repository documentation can establish the state.
- Do not silently override strategic decisions.
- Do not declare meaningful work complete while required documentation is missing.
- Record significant decisions in meta/memory/DECISIONS.md.
- Update meta/CURRENT-STATE.md when verified repository state changes materially.
- Update meta/ROADMAP.md when roadmap state changes.
- Update architecture/testing/security/deployment documentation when those areas change.
- Preserve evidence: tests, CI results, commit/PR references, and known blockers.
- Resolve documentation drift rather than working around it.
- Escalate strategic ambiguity instead of guessing.

## PR and Merge Discipline

Before merging a meaningful PR:
1. Confirm it targets current main.
2. Inspect the actual changed files.
3. Check overlap and duplicate work.
4. Verify required CI and tests.
5. Separate infrastructure failures from code failures.
6. Confirm documentation requirements.
7. Record significant decisions and the resulting state.
8. Merge only when the repository's stated gates are satisfied.

A mergeable GitHub status alone is not proof of semantic correctness.

## Completion Status

Use precise status labels:
- IN PROGRESS
- BLOCKED
- PARTIALLY COMPLETE
- IMPLEMENTED — NOT VERIFIED
- VERIFIED — DOCUMENTATION PENDING
- COMPLETE

COMPLETE requires both implementation and documentation verification.

## Handoff

Before leaving:
- State objective and decision source.
- List changed files.
- Record tests and verification evidence.
- Record failures and risks.
- State remaining work.
- Identify the next action.
