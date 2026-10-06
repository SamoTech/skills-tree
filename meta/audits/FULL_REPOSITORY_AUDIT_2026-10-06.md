# Full Repository Audit — 2026-10-06

> Scope: live `main`, open/merged PR state, executable workflows, schemas, registry/runtime, canonical skills, generated projections, governance/security controls, evaluation evidence, and authoritative documentation.

## Executive disposition

Repository core is operational and evidence-backed. The final verified main after PR #379 is `290cb3495d1905615501471e4e1b3bec86301a7b` before subsequent generated-only maintenance commits. There are currently no open pull requests.

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

Issue #372 was resolved by PR #379. The benchmark now rejects unknown case IDs and duplicate `run_id` values before metric calculation.

## Governance / writer audit

Issue #159 was closed as `not_planned` because branch protection is not part of the current project-local completion model.

Issue #370 was resolved by PR #377. `.github/workflows/devlens.yml` is now a read-only diagnostic with `contents: read` and `update_readme: false`; the stale DevLens README block was removed.

Issue #373 is addressed by PR #374. The obsolete `docs/index.html` write path was removed and README counting was unified under `tools/update_readme_counts.py`.

## Release / deployment / security

After PR #368, GitHub Pages deployment and Zero-Touch Release both succeeded. Main Security Scan, Build & Verify Wheel, Test Suite, Validate Skills Graph, and Governance Gate succeeded on the PR #374 merge cycle.

Zero-Touch Release semantic-release stage completed successfully after PR #374; build/publish asset stages were skipped because no semantic version change was required.

CodeQL on the #374 merge head was still running at the last snapshot; no failure evidence was observed.

## Documentation health

Current reconciliation and distribution documents were refreshed to the 2026-10-06 baseline. Historical sections are retained as historical evidence.

Documentation risk from the DevLens block is resolved. The live workflow inventory is now explicitly reconciled to 45 files; historical 40/42 counts remain only in dated records.

## Final decision

Do not add new skills merely to increase corpus size. The current implementation/security/governance gaps from this audit are resolved. The next highest-value work is evidence collection:

1. Collect real Hermes traces for Issue #357 and run the 12-observation activation corpus.
2. Resolve the retrieval freshness/reproducibility boundary in Issue #336 without manufacturing current scores.
3. Keep the 45-workflow inventory, generated projections, and project-brain documentation synchronized with live main.

## Final Reconciliation — 2026-10-06

### Current verified baseline
- 45 workflow files in `.github/workflows/`; inventory reconciled in `meta/WORKFLOW_INVENTORY.md`.
- 382 quality-corpus skill files, including one intentional `00-sandbox` fixture; 381 production/public canonical skills across 17 categories.
- 264 eligible Agent Skills projections, 118 blocked canonical entries, and 302 existing Agent Skills packages; current reconciliation reports no missing eligible projections, drift, stale entries, unexpected packages, ambiguous provenance, or unresolved collisions.
- Graph projections are byte-identical at 382 nodes / 250 edges; search projections are byte-identical.

### Resolved audit findings
- PR #374 repaired the README skill-count writer and removed the obsolete `docs/index.html` path.
- PR #377 isolated DevLens as read-only and removed its stale public snapshot.
- PR #379 made activation observation integrity fail-closed for unknown cases and duplicate run IDs.
- PRs #368 and #371 established the Model/Agent/Tool/Capability/Skill boundary and explicit NO_OBSERVATIONS / PARTIAL / COMPLETE benchmark status.

### Remaining evidence gaps
- Issue #357: real runtime activation traces are still absent, so activation/reliability/effectiveness claims remain unverified.
- Issue #336: historical retrieval benchmark results remain explicitly historical and need a reproducible current run or explicit qualification/retirement.

### Final audit verdict
No current P0 implementation or security blocker was found in the verified repository state. No new routing authority, search implementation, or bulk skill creation is justified by the evidence reviewed. The project should continue through the evidence-first loop rather than optimize for raw skill count.