# GitHub Actions Workflow Inventory

**Snapshot:** 2026-10-07  
**Live workflow files:** 47

This is the Phase 0 workflow classification baseline. It classifies every workflow by operational role and records the remaining security/control-plane boundary. YAML does not prove GitHub repository settings such as branch protection, required checks, environment approvals, or Actions execution policies.

| Workflow | Classification | Purpose / disposition |
|---|---|---|
| `agent-skills-distribution.yml` | Authoritative validation | Agent Skills distribution audit; PR/push/manual reconciliation gate |
| `ast-sweep.yml` | Scheduled maintenance | AST/repository hygiene |
| `auto-label.yml` | Supporting automation | Issue/PR labeling |
| `build-and-verify.yml` | Authoritative validation | Package build and wheel verification |
| `check-links.yml` | Supporting validation | Link validation |
| `clean-install-test.yml` | Supporting validation | Clean-install regression |
| `dependabot-auto-merge.yml` | Supporting automation | Dependabot PR handling |
| `demand-signals.yml` | Scheduled/manual evidence collection | Public demand signal collection; read-only artifact |
| `dependency-auditor.yml` | Maintenance automation | Dependency/security audit with repository side effects |
| `deploy-pages.yml` | Authoritative Pages deployment | Single repository-controlled Pages deployment |
| `devlens.yml` | Manual read-only diagnostic | Repository health assessment; no repository writes |
| `export-skills.yml` | Generated-main writer | Published skill export + JSON-LD projection through protected-main PR; redundant triggers (self-path push, merged-PR `pull_request_target` with merged-only guard, explicit `main` checkout) and `pull-requests: write` mirror `quality-report.yml` and close the #447 stranding class |
| `generate-blueprint.yml` | Supporting artifact generation | Blueprint generation |
| `generate-changelog.yml` | Generated-main writer | Generated changelog |
| `governance-gate.yml` | Authoritative validation | Repository governance contract verification |
| `generate-search-index.yml` | Generated-main writer | Search index through protected-main PR; redundant triggers (self-path push, merged-PR `pull_request_target` with merged-only guard, weekly self-heal) mirror `quality-report.yml` and close the #447 stranding class; `pull-requests: write` and no-skip-ci automation commits restored 2026-10-12 so the bot PR-creation step and its required checks can run |
| `issue-welcome.yml` | Supporting automation | Issue onboarding |
| `leaderboard.yml` | Generated-main writer | Leaderboard projection |
| `osv-watch.yml` | Generated-main writer | OSV/advisory state |
| `pr-checks.yml` | Authoritative PR gate | Pull-request checks |
| `quality-report.yml` | Generated-main writer | Quality report through protected-main PR; requires `pull-requests: write` and valid PR checks; bot-triggered check behavior tracked in #447 |
| `release.yml` | Manual recovery | Existing-tag PyPI republish |
| `retrieval-benchmark.yml` | Evidence benchmark | Deterministic retrieval evidence; PR/push/manual run with workflow self-validation |
| `revoke-phantom-badges.yml` | Generated-main writer | Badge reconciliation |
| `schema-enforce.yml` | Authoritative validation | Schema enforcement |
| `security-scan.yml` | Authoritative security gate | Security scanning |
| `skill-selection-benchmark.yml` | Evidence benchmark | Capability-to-skill selection evidence; PR/push/manual run with workflow self-validation |
| `skill-upgrade-comment.yml` | Supporting PR automation | Upgrade/review comments |
| `skill-activation-runtime.yml` | Evidence benchmark | Real Hermes runtime activation/invocation evidence for Issue #357 |
| `skill-version-badge.yml` | Supporting PR automation | Version/badge labeling |
| `stale-skills.yml` | Supporting issue maintenance | Skill freshness issues |
| `stale.yml` | Supporting issue maintenance | Generic stale issues/PRs |
| `sync-badges.yml` | Generated-main writer | Badge reconciliation |
| `test.yml` | Authoritative test execution | Repository tests |
| `update-skill-count.yml` | Generated-main writer | Skill-count projection through protected-main PR; README stat anchors (hero strip, comparison row, What's-Inside line, heading, category table) are patched loudly and fail on drift |
| `uptime-monitor.yml` | Scheduled maintenance | Availability monitoring |
| `used-in-tracker.yml` | Generated-main writer | Usage tracker |
| `validate-agent-skills.yml` | Authoritative validation | Agent Skills distribution validation |
| `validate-corpus.yml` | Authoritative validation | Structured corpus validation |
| `validate-evaluations.yml` | Authoritative validation | Evaluation ontology integrity, scenario-specific corpus contract scope/reference validation, P0 coverage, and freshness warnings |
| `validate-graph.yml` | Authoritative validation + generated writer | Graph validation plus protected-main generated-branch PR; normalized semantic comparison suppresses timestamp/format-only churn; bot-triggered PR checks tracked in #447 |
| `validate-skills.yml` | Authoritative validation | Skill metadata validation |
| `verify-taxonomy.yml` | Authoritative validation | Taxonomy verification |
| `version-stats.yml` | Generated-main writer | Version statistics |
| `weekly-highlights.yml` | Generated-main writer | Weekly highlights |
| `zero-touch-release.yml` | Authoritative release | Production release pipeline |
| `temp-regen.yml` | Temporary steward tooling (delete before merge) | Branch-restricted projection regen + audit verification for PR #652 only; deleted before merge; live count returns to 46 |

## Reconciliation findings

1. `deploy-pages.yml` is the single repository-controlled Pages deployment.
2. `zero-touch-release.yml` is the production release authority.
3. `release.yml` is manual recovery only.
4. Catalog release packaging is now executed inside `zero-touch-release.yml`; there is no second release-package writer.
5. `stale.yml` and `stale-skills.yml` have different scopes and are not duplicates.
6. JSON-LD is generated by `tools/export_skills.py` under the `export-skills.yml` writer; there is no separate `jsonld-export.yml` workflow.
7. Generated-main writers are a high-risk class and must remain least-privileged, deterministic, serialized, bounded, and observable.
8. `validate-graph.yml` is now permission-isolated and protected-main compatible: graph validation is `contents: read`; generated graph materialization uses `contents: write` only to publish the deterministic projection to `automation/generated-graph`; no direct `main` mutation is attempted; the quality job is read-only.
9. GitHub control-plane state remains a separate verification boundary: the live branch inspection reports `main` as unprotected with required-status-check enforcement off. Other repository settings not exposed by the connector remain unverified rather than inferred.

## Known generated-main write paths

`export-skills.yml`, `generate-changelog.yml`, `generate-search-index.yml`, `leaderboard.yml`, `osv-watch.yml`, `quality-report.yml`, `revoke-phantom-badges.yml`, `sync-badges.yml`, `update-skill-count.yml`, `used-in-tracker.yml`, `version-stats.yml`, `weekly-highlights.yml`, and `dependency-auditor.yml`. `validate-graph.yml` no longer writes directly to `main`.

The repository-wide `auto-commit-main` semaphore remains the required serialization boundary for any remaining direct generated-main writers; protected `main` writers must not bypass the PR boundary.

## Completion gate

Workflow classification is materially reconciled at the file/role level and the identified `validate-graph.yml` permission boundary is hardened and CI-verified. Phase 0 remains open only for control-plane reconciliation/limitations and any other material security finding discovered by inspection.

Any new or modified workflow must be classified in this file in the same change.

## Live inventory refresh — 2026-10-06

A full git-tree audit of `main` found 46 workflow files. The five workflows newly reconciled into this inventory are `agent-skills-distribution.yml`, `demand-signals.yml`, `governance-gate.yml`, `retrieval-benchmark.yml`, and `skill-selection-benchmark.yml`. The prior `jsonld-export.yml` entry was stale and has been removed from the live inventory.

The inventory is descriptive only; CI and `tools/verify_governance.py` remain the enforcement boundaries.

## Disposition update — 2026-10-11

`generate-search-index.yml` was hardened with `quality-report.yml`'s proven redundant trigger set (self-path push trigger, merged-PR `pull_request_target` with a merged-only job guard and explicit `main` checkout, weekly self-heal schedule) to close the #447 stranding class observed after PR #467. The workflow count and classification are unchanged; the trusted-generator provenance, `auto-commit-main` serialization, and protected-main PR publication path are preserved (PR #470).

## Disposition update — 2026-10-12

The #447 stranding class was root-caused (step-level evidence; run logs remain owner-side) to the generated-main writers lacking `pull-requests: write` for the `gh pr create` step and carrying `[skip ci]` in their automation commits, which leaves bot PRs without runnable required checks. `quality-report.yml` had both fixed on 2026-10-11 (`7a9cc9e92d` granted the permission; `4057d03db7` removed `[skip ci]`) and both were reverted when `e6620488ec` landed minutes later; `generate-search-index.yml` and `export-skills.yml` never carried them. This change restores `pull-requests: write` and no-skip-ci automation commits across the three writers (mirroring `validate-graph.yml`, whose bot PRs are created successfully, e.g. PR #468) and hardens `export-skills.yml` with the proven redundant trigger set. Workflow count and classifications are unchanged; the trusted-generator provenance, `auto-commit-main` serialization, and protected-main PR publication path are preserved.

## Disposition update - 2026-10-12 (second)

The nine remaining generated-main writers (`generate-changelog.yml`, `leaderboard.yml`, `osv-watch.yml`, `revoke-phantom-badges.yml`, `sync-badges.yml`, `update-skill-count.yml`, `used-in-tracker.yml`, `version-stats.yml`, `weekly-highlights.yml`) still lacked `pull-requests: write` for their `gh pr create` step and carried `[skip ci]` in their automation commits, so their generated branches never produced bot PRs and required checks never ran (#447 stranding class). Live evidence: `automation/generated-skill-count` was force-pushed at `f36e120fd4` with a failed check run on `main` and no PR, and `automation/generated-weekly-highlights` did not exist. This change restores `pull-requests: write` (upgrading the existing `pull-requests: read` in `generate-changelog.yml` in place rather than adding a duplicate key) and removes `[skip ci]` from the automation commits across all nine writers, mirroring PR #472 and `validate-graph.yml`. `tools/update_readme_counts.py` was also rewritten to patch the current README stat anchors loudly (hero stat strip with the graph-edge count from `data/SKILLS_GRAPH.json`, comparison-table row, What's-Inside line, category heading, category table) and to fail on drift instead of silently no-oping on obsolete formats. Workflow count and classifications are unchanged; the trusted-generator provenance, `auto-commit-main` serialization, and protected-main PR publication path are preserved.

## Disposition update — 2026-10-12 (failure-modes ratchet)

`validate-skills.yml` now requires a `## Failure Modes` section on every changed skill file, promoting the section from template convention to a CI gate. Because the workflow validates only files changed in the PR, the requirement is a ratchet: legacy corpus files without the section (445 of 538 public skills carried it at the 2026-10-12 API-export measurement) are grandfathered until next touched, while any new or modified skill must document failure modes. Workflow count, classification (`Authoritative validation`), triggers, and permissions are unchanged; no validation or security gate is weakened. Measured coverage and the claim-basis wording in `README.md` are synchronized in the same change.

## Disposition update — 2026-10-12 (#447 closure)

Issue #447 is closed by recorded decision: the atomic-republication path — cross-coupled generated projections publishing together through agent-assembled, fully checked PRs built by branch-level merges of the trusted automation branches (the validated PR #477 / #490 / #499 / #517 pattern) — is adopted as the standard publication path, so `main` is never merged on an unchecked `GITHUB_TOKEN` bot commit. The historical `gh pr create` 403 class is fixed and verified live (bot PRs #509, #512); the residual platform behavior (required checks not running on `GITHUB_TOKEN`-authored bot PR commits; latest evidence: merged bot PR #521 ran only CodeQL ×4 + GitGuardian) is accepted as a documented GitHub same-actor limitation. No workflow file, trigger, or permission changes in this update; workflow count and classifications are unchanged, and the table cells referencing #447 remain accurate as historical tracking references. The decision is recorded in `meta/memory/DECISIONS.md`.

## Disposition update — 2026-10-12 (skill-activation-runtime decomposition)

`skill-activation-runtime.yml` (Evidence benchmark, issue #357) is decomposed behavior-preserving: the eleven inline Python heredocs are extracted verbatim into `tools/activation/*.py` and the workflow now orchestrates the scripts. The `tools/activation/**` path is added to the push and pull_request triggers so script edits still run the benchmark. Nothing else changes: classification (Evidence benchmark), the 46-workflow count, permissions, step order, the pinned Hermes commit, the `qwen3.5:4b` model, the 65536 context window, the 12-observation acceptance contract, and the `INFRASTRUCTURE_INELIGIBLE`/`RUNTIME_PREFLIGHT_FAILED` NOT-RUN semantics are preserved verbatim, and no validation or security gate is weakened. The pre-existing `tools/convert_hermes_activation_observations.py` adapter (single-file, case-map-keyed correlation, `hermes-###` run IDs) is intentionally not reused for the runtime trace conversion because the benchmark converter contract (glob of `ACT-*.jsonl`, filename-derived case IDs, `unmapped/...` preservation of out-of-scope selections, trace-ID run IDs) differs; forcing reuse would change observation identity semantics. The benchmark itself remains NOT RUN pending a supported accelerator runner; this refactor makes no runtime or efficacy claim.

## Disposition update — 2026-10-12 (release-pipeline orphaned-version recovery)

`zero-touch-release.yml` (Authoritative release) is repaired behavior-preserving: a mid-flight writer failure on 2026-10-05 pushed the `chore(release): v1.80.0 [skip ci]` version bump to `main` (`1a8f2cd58b`) without its tag, and the workflow's pre-comparison gate then classified every later run as "no releasable commits" (NEXT == CURRENT == 1.80.0 with tag `v1.80.0` absent), freezing all GitHub and PyPI releases at v1.79.0 while 212 commits — including the owner-directed corpus expansions — merged. The gate now skips only when the declared version's tag already exists; when `pyproject.toml` declares a version whose tag is missing, the workflow completes that orphaned release by creating and pushing tag `v<version>` at the live `main` tip so the existing build → PyPI → release-assets jobs publish it. Classification (Authoritative release), the 46-workflow count, triggers, the `auto-commit-main` serialization, permissions, and all `tools/verify_governance.py` pinned phrases are unchanged; no validation or security gate is weakened.

## Disposition update — 2026-10-14 (Pages deploy self-heal and Node-24 action bump)

`deploy-pages.yml` (Authoritative Pages deployment) gains two changes. First, a `staleness-gate` job runs before every build: it compares the latest `github-pages` deployment SHA and state with the main tip via the deployments API and outputs `needs_deploy`; a new six-hourly schedule (`23 */6 * * *`) uses it to skip build+deploy when the live deployment already serves main and to re-deploy otherwise, closing the gap where a transiently failed deploy left the public site silently stale (observed on `265f6026`). Second, the deploy step is pinned from `actions/deploy-pages@v4` to `actions/deploy-pages@v5.0.1`: the v4 major tag resolves to the 2024 `node20` build, which the runner-side forced Node 24 breaks systematically, while v5.0.1 is the upstream Node-24 release (node24 + dependency updates, no input changes). Classification (Authoritative Pages deployment), the 46-workflow count, triggers, permissions, the `pages` concurrency group, every build/deploy verification step, and all `tools/verify_governance.py` pinned phrases are unchanged; no validation or security gate is weakened.


## Disposition update — 2026-10-14 (post-deploy served-bytes verification retries)

`deploy-pages.yml` (Authoritative Pages deployment) modifies exactly one step: the post-deploy "Verify served discovery bytes" step now invokes `tools/verify_agent_skills_discovery.py` with `--max-attempts 5 --retry-delay 30`. The served mode previously performed a single immediate pass (fetch the served index plus every artifact, compare each SHA-256 digest), and the deploy run on `c01d1dff` demonstrated the race: the `actions/deploy-pages@v5.0.1` step published successfully and the live site served the new build, but the immediate single pass observed stale CDN bytes, failed the job, and marked the environment deployment failure. The retry is whole-pass and fail-closed — the final attempt's error propagates unchanged and the local verification mode used by the build job is unchanged — so the guarantee that every served byte must match its committed digest is unchanged and no validation or security gate is weakened. Classification (Authoritative Pages deployment), the 46-workflow count, triggers, permissions, the `pages` concurrency group, the staleness gate, and all `tools/verify_governance.py` pinned phrases are unchanged.

## Disposition update — 2026-10-14 (deploy-verification command-line repair)

`deploy-pages.yml` (Authoritative Pages deployment) repairs exactly one shell line in the post-deploy "Verify served discovery bytes" step: the `--max-attempts 5 --retry-delay 30` flags added earlier had been appended on a separate line of the `run:` block, so they never reached `tools/verify_agent_skills_discovery.py` (the step silently ran single-pass), and once a single pass succeeded on `60b7308c` the orphaned flag line executed as a command and failed the step with exit 127 ("command not found"). The step is now one properly backslash-continued command, so the whole-pass retrying verification actually executes in CI; no verification requirement, retry count, trigger, permission, or governance-pinned phrase changes. Classification (Authoritative Pages deployment), the 46-workflow count, triggers, permissions, the `pages` concurrency group, and the staleness gate are unchanged; no validation or security gate is weakened.

## Disposition update — 2026-10-15 (post-expansion projection republication wave)

No workflow file, trigger, permission, or classification changes in this wave. The six generated-writer bot PRs republishing the post-expansion projections (#591 quality report, #592 graph, #593 README counts, #594 Skills API, #595 badges, #597 search index) required App-authored identical-content recommits on their automation branches to obtain the full runnable check suite (the documented #447 same-actor workaround: bot `GITHUB_TOKEN` pushes leave required checks at `action_required`); each was squash-merged at its exact head after every non-staleness check passed, and duplicate bot PR #596 was verified byte-identical to `main` and closed as already applied. The wave's only test change (#598) realigns the hard-coded discovery-index count in `tests/test_agent_skills_discovery.py` (861 → 912) with the reconciled corpus; parallel fix PR #599 was closed as superseded by the fully-green #598. The 46-workflow count, all classifications, and all governance-pinned phrases are unchanged, and no CI, quality, security, or governance gate is weakened.


## Disposition update — 2026-10-16 (Counsel agent onboarding)

The tenth permanent specialist agent (Counsel) is hired with a worker +
advisory-challenger mandate (`meta/COUNSEL_CHARTER.md`,
DECISION-2026-10-16-COUNSEL-AGENT-HIRE in `meta/memory/DECISIONS.md`). No
workflow is added, removed, or modified in this cycle: the hire is a
governance-documentation change, and Counsel executes work through the
existing branch → PR → CI → exact-head merge protocol with no new
automation. The workflow count, all classifications, and all
governance-pinned phrases are unchanged, and no CI, quality, security, or
governance gate is weakened.

## Disposition update — 2026-10-16 (Counsel slice 1: search-index freshness contract)

No workflow is added, removed, or modified in this cycle. The new `tests/test_search_index_freshness.py` extends the authoritative test execution in `test.yml`'s pytest suite (no workflow file change): it re-derives the search projection in-memory from the canonical corpus and requires equality plus byte-identity with the committed `docs/search-index.json` / `data/search-index.json`, closing the CI-blindness behind the 2026-10-15 batch-2 encoding defect. The generate-search-index writer itself is unchanged and remains the only search-index producer; the new contract only verifies its committed output. The workflow count, all classifications, and all governance-pinned phrases are unchanged, and no CI, quality, security, or governance gate is weakened (a gate is added, never removed).

## Disposition update — 2026-10-20 (temporary regen + link-report tooling for PR #643)

`temp-regen.yml` is temporary steward tooling on the `skills/expansion-2026-10-20-b1` branch only: it runs the repository's own generators (`tools/build_graph.py`, `tools/build_search_index.py`, `tools/export_skills.py`, `tools/check_skill_quality.py`, `tools/update_readme_counts.py`) at the branch head and records a lychee markdown report so failing Evidence URLs can be identified without run-log access. It publishes nothing to `main`, does not alter any existing workflow, and is deleted before merge so the live count returns to 46. No CI, quality, security, or governance gate is weakened; the normal PR checks continue to gate PR #643 independently.
Repair note (2026-10-20): the report step originally installed the lychee binary directly and failed with exit 127 on the runner; it now uses the same pinned `lycheeverse/lychee-action@v2` path as `check-links.yml`, with `fail: false` so the report is always recorded for diagnosis while the authoritative gate keeps failing independently.
Second repair note (2026-10-20): the report step now uses the action's documented `format`/`output` inputs with `continue-on-error` so a link-check failure still records the report and the projections are committed regardless.
Closure note (2026-10-20): `temp-regen.yml` and `meta/LYCHEE-REPORT.md` were deleted on the branch before merge as planned (net zero on `main`); the live workflow count returns to 46 and this row is removed from the live table, with the disposition sections retained as the historical record.

## Disposition update — 2026-10-20 (temporary regen + link-report tooling for PR #647)

`temp-regen.yml` is temporary steward tooling on the `skills/expansion-2026-10-20-b2` branch only: it runs the repository's own generators (`tools/build_graph.py`, `tools/build_search_index.py`, `tools/export_skills.py`, `tools/check_skill_quality.py`, `tools/update_readme_counts.py`) at the branch head and records a lychee markdown report so failing Evidence URLs can be identified without run-log access. It publishes nothing to `main`, does not alter any existing workflow, and is deleted before merge so the live count returns to 46. No CI, quality, security, or governance gate is weakened; the normal PR checks continue to gate PR #647 independently.
Closure note (2026-10-20): `temp-regen.yml` and `meta/LYCHEE-REPORT.md` were deleted on the `skills/expansion-2026-10-20-b2` branch before merge as planned (net zero on `main`); the live workflow count returns to 46 and this row is removed from the live table, with the disposition sections retained as the historical record.

## Disposition update — 2026-10-20 (temp-regen re-add for PR #647 evidence-URL fix)

`temp-regen.yml` is re-added on the `skills/expansion-2026-10-20-b2` branch only, to regenerate the repo's own projections after six skill Evidence URLs were replaced with live primary sources (CI-unreachable VentureBeat 429 / safeguard.sh 502). It publishes nothing to `main`, alters no existing workflow, and is deleted before merge so the live count returns to 46. No CI, quality, security, or governance gate is weakened.

Closure note (2026-10-20): the re-added `temp-regen.yml` completed the post-fix projection regen (bot commit 94dae1e6, lychee 2993/2993 with 0 errors) and was deleted on the branch together with `meta/LYCHEE-REPORT.md` before merge (net zero on `main`); the live workflow count returns to 46 and the temporary table row is removed.


## Disposition update — 2026-10-21 (temporary regen + link-report tooling for PR #649)

`temp-regen.yml` is temporary steward tooling on the `skills/expansion-2026-10-21-b1` branch only: it runs the repository's own generators (`tools/build_graph.py`, `tools/build_search_index.py`, `tools/export_skills.py`, `tools/check_skill_quality.py`, `tools/update_readme_counts.py`) at the branch head and records a lychee markdown report so failing Evidence URLs can be identified without run-log access. It publishes nothing to `main`, does not alter any existing workflow, and is deleted before merge so the live count returns to 46. No CI, quality, security, or governance gate is weakened; the normal PR checks continue to gate PR #649 independently.

Closure note (2026-10-21): `temp-regen.yml` completed the post-fix projection regen after the Evidence-URL swap (bot commits `a637d368` and `563a9ee6`) and was deleted on the branch together with `meta/LYCHEE-REPORT.md` before merge (net zero on `main`); the live workflow count returns to 46 and the temporary table row is removed.


## Disposition update — 2026-10-21 (temporary regen + link-report tooling for PR #651)

`temp-regen.yml` is temporary steward tooling on the `skills/expansion-2026-10-21-b2` branch only: it runs the repository's own generators (`tools/build_graph.py`, `tools/build_search_index.py`, `tools/export_skills.py`, `tools/check_skill_quality.py`, `tools/update_readme_counts.py`) at the branch head and records a lychee markdown report so failing Evidence URLs can be identified without run-log access. It publishes nothing to `main`, does not alter any existing workflow, and is deleted before merge so the live count returns to 46. No CI, quality, security, or governance gate is weakened; the normal PR checks continue to gate PR #651 independently.

Closure note (2026-10-21): `temp-regen.yml` completed the on-branch projection regen for PR #651 (bot commit `1fccb82a`, lychee 3293/3293 with 0 errors) and was deleted on the branch together with `meta/LYCHEE-REPORT.md` before merge (net zero on `main`); the live workflow count returns to 46 and the temporary table row is removed.


## Disposition update - 2026-10-22 (temp-regen re-add for PR #652 audit diagnosis)

`temp-regen.yml` is re-added on the `skills/expansion-2026-10-22-b1` branch only, this time to capture the Agent Skills distribution audit outputs (`generate_agent_skills.py --audit`, `validate_agent_skills.py`, `reconcile_agent_skills.py --check`) into `meta/AUDIT-REPORT.md` for diagnosis, because the `audit` CI check failed with only a generic exit-code annotation and job logs are not readable through the available tooling. It publishes nothing to `main`, alters no existing workflow, and is deleted before merge so the live count returns to 46. No CI, quality, security, or governance gate is weakened.
