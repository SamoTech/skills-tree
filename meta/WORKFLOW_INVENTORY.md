# GitHub Actions Workflow Inventory

**Snapshot:** 2026-10-07  
**Live workflow files:** 46

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
