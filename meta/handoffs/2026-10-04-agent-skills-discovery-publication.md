# Agent Skills Discovery Publication Handoff

Date: 2026-10-04
Branch: feat/agent-skills-discovery-publication

## Scope

This slice closes the discovery-publication architecture gap without introducing a second source of truth.

Canonical source remains `skills/`.
Deterministic Agent Skills projection remains `agent-skills/`.
Existing reconciliation remains the enforcement boundary.
Existing GitHub Pages deployment remains the only Pages deployment authority.

## Verified baseline entering this slice

- 375 canonical skill entries.
- 258 eligible deterministic projections.
- 117 blocked canonical entries.
- 296 Agent Skills packages.
- Reconciliation enforced by `python tools/reconcile_agent_skills.py --check`.

## Implementation

Added `meta/agent-skills-discovery-index.schema.json`.

Added `tools/build_agent_skills_discovery.py`. It:

1. executes the existing reconciliation contract;
2. reuses canonical projection naming and eligibility logic;
3. refuses reconciliation failures;
4. verifies every eligible published `SKILL.md` against the deterministic projection;
5. computes SHA-256 over the exact published bytes;
6. emits a stable name-sorted discovery index;
7. validates the index against the dedicated schema.

Added `tools/verify_agent_skills_discovery.py`.

It verifies either:
- a local Pages artifact, or
- the deployed HTTP index and every advertised skill artifact.

## Pages integration

`.github/workflows/deploy-pages.yml` now:

- runs reconciliation and Agent Skills validation;
- builds the existing MkDocs site;
- stages deterministic Agent Skills packages into the Pages artifact;
- generates `.well-known/agent-skills/index.json` in the same artifact;
- verifies local artifact bytes before upload;
- deploys using the existing Pages workflow;
- verifies served index and served `.SKILL.md` bytes against SHA-256 digests after deployment.

No second deployment workflow was introduced.

## Hosting boundary

The repository currently uses the GitHub Pages project URL `https://samotech.github.io/skills-tree` and has no repository `CNAME`.

GitHub Pages project sites are served below the repository-name path. Therefore this implementation deliberately verifies:

`https://samotech.github.io/skills-tree/.well-known/agent-skills/index.json`

It does not claim that `/.well-known/agent-skills/index.json` is live at the domain root.

Root-level discovery requires a root-capable user/organization Pages site or verified custom domain. That hosting change is an independent control-plane decision and must be verified before changing published URLs.

## Tests

Added `tests/test_agent_skills_discovery.py` covering:

- SHA-256 digest format;
- deterministic index generation;
- exact expected eligible count of 258;
- schema validation;
- stable ordering;
- duplicate-name rejection.

The branch must pass the repository CI matrix before merge. No local test result is claimed because the execution environment cannot clone GitHub repositories directly.

## Non-goals

This slice does not:

- create another skill generator;
- create another reconciler;
- change canonical skill eligibility;
- publish blocked or legacy-only packages;
- add trust or ranking semantics;
- alter search behavior;
- activate the root discovery endpoint prematurely.

## Completion gate

The implementation is COMPLETE only after exact-head CI passes, Pages build/deployment succeeds, and served-byte verification succeeds for the published project-site endpoint. Documentation/current-state synchronization must be merged with the implementation.
