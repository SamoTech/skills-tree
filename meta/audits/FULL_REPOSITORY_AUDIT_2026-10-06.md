# Full Repository Audit — 2026-10-06

> Scope: live `main`, open/merged PR state, executable workflows, schemas, registry/runtime, canonical skills, generated projections, governance/security controls, evaluation evidence, and authoritative documentation.

## Executive disposition

Repository core is operational and evidence-backed. The latest verified main is `50e2c2a6797a471cbc0c678cc403e56ee3c9f875` (PR #374 merge commit). There are currently no open pull requests.

Canonical source remains `skills/`. The semantic boundary is now explicit and enforced:

`Capability = What`
`Skill = How`
`Model = Inference Engine`
`Tool = Action/Data Surface`
`Agent = Coordinator`

## Corpus and generated state

- 382 canonical skill files in the quality corpus.
- 223 battle-tested, 158 enriched, 0 stubs, 0 invalid, 1 intentional fixture.
- 264 eligible canonical Agent Skills projections and 118 blocked.
- 302 existing Agent Skills packages.
- Latest Agent Skills reconciliation audit: no eligible missing projections, no deterministic projection drift, no stale entries, no unexpected packages, no ambiguous provenance, and no unresolved collisions.
- Graph projections: 382 nodes / 250 edges; `data/SKILLS_GRAPH.json` and `docs/api/graph.json` are byte-identical.
- Search projections: `data/search-index.json` and `docs/search-index.json` are byte-identical.
- `docs/api/skills.json` was regenerated after PR #368 and reports 382 skills.

Note: the public README count intentionally excludes `skills/00-sandbox/pipeline-test.md`; the quality corpus count includes it as the intentional fixture. This distinction must remain explicit.

## PR and CI audit

- PR #368 merged after exact-head CI passed. It formalized the Model/Agent/Tool/Capability/Skill boundary and corrected the affected corpus/projections.
- PR #371 merged after exact-head Governance, Security, Build, Test, Graph, and PR checks passed. It introduced NO_OBSERVATIONS / PARTIAL / COMPLETE benchmark status.
- PR #374 merged after exact-head Governance, Security, Build, Test, Graph, and PR checks passed. It repaired the README skill-count writer.
- Dependabot gates were consistently `skipped` where no Dependabot-triggered condition applied; skipped was not treated as a failure.
- One older Gitleaks failure was diagnosed as a runner/scan invocation error (`stderr is not empty`, no leak finding) and was superseded by a later successful exact-head Security Scan.

## Evaluation / activation boundary

Issue #357 remains the main empirical investigation. The repository now has:
- bounded activation benchmark `benchmark/skill-activation-v1` (4 cases × 3 repetitions);
- observation schema with explicit `skill_selection` and `skill_execution` events;
- Hermes adapter and capture instrumentation;
- zero-observation fail-closed process behavior;
- explicit PARTIAL versus COMPLETE corpus status.

No real Hermes runtime trace corpus exists yet. Therefore no empirical activation-rate, false-activation, invocation-reliability, or general efficacy claim is valid.

Issue #372 is a newly identified evidence-integrity hardening gap: unknown case IDs and duplicate `run_id` values can currently contaminate or inflate the benchmark corpus and should be rejected before metric calculation.

## Governance / writer audit

Issue #159 was closed as `not_planned` because branch protection is not part of the current project-local completion model.

Issue #370 remains open: `.github/workflows/devlens.yml` can write README with `contents: write` and `update_readme: true` outside the serialized generated-main writer contract, and the current README DevLens block is stale (2026-09-30).

Issue #373 is addressed by PR #374. The obsolete `docs/index.html` write path was removed and README counting was unified under `tools/update_readme_counts.py`.

## Release / deployment / security

After PR #368, GitHub Pages deployment and Zero-Touch Release both succeeded. Main Security Scan, Build & Verify Wheel, Test Suite, Validate Skills Graph, and Governance Gate succeeded on the PR #374 merge cycle.

Zero-Touch Release semantic-release stage completed successfully after PR #374; build/publish asset stages were skipped because no semantic version change was required.

CodeQL on the #374 merge head was still running at the last snapshot; no failure evidence was observed.

## Documentation health

Current reconciliation and distribution documents were refreshed to the 2026-10-06 baseline. Historical sections are retained as historical evidence.

Remaining documentation risk is the stale DevLens block and any generated README count refresh that depends on the next applicable writer trigger. These are tracked, not hidden.

## Decision

Do not add new skills merely to increase corpus size. The next highest-value work is:

1. Resolve Issue #370 (DevLens writer isolation).
2. Resolve Issue #372 (unknown/duplicate activation observation rejection).
3. Collect real Hermes traces for Issue #357.
4. Only then use measured failures to justify skill-description, routing, evaluation, or new capability work.
