# Full Repository Audit — 2026-10-12

> Scope: live `main`, PR/CI state, code review of `tools/` and generated-writer workflows, generated projections versus the canonical corpus, governance/security controls, public documentation claims, branch hygiene, and the owner-approved next-decision priority. Recorded by the auditing agent session; the parallel wave-2 expansion track's merges are reported, not re-verified.

## Executive disposition

Repository core is operational and evidence-backed. No P0 implementation or security blocker was found. Verified `main` at audit close is `2666ccf665f5a99c2e911ad6efe9c455f7479745` (the PR #525 README claim-alignment squash merge).

A parallel expansion track (wave 2) is active in the same period: pilot PR #506 (+10, corpus 383→393→493 public baseline after the 2026-10-12 owner-directed batches) and batch-2 PR #514 (+45) are merged. Generated projections on `main` still publish at the 493 baseline pending the open generated-writer PRs #518–#524.

`skills/` remains canonical. The generated-writer loop is now deterministic (PR #479) and atomic for the index/export pair (PR #477); the perpetual-churn defect is dead and post-merge rebuilds of an unchanged corpus publish nothing.

## Corpus and generated state

- Canonical corpus on `main`: 538 public skills plus the one intentional `00-sandbox` fixture = 539 quality-corpus files across 17 categories. Basis: the auto-synced 493-public README count anchors, plus exactly 45 `skills/**/*.md` additions verified in PR #514's changed-file list (distributed 6–7 per category across `11-web` through `17-infrastructure`).
- PR #514 also carried 46 `agent-skills/*/SKILL.md` projections plus support files; its generated-artifact republications are queued, not yet published (see below).
- Projections on `main` at audit close: `docs/api/skills.json` reports `count: 493`, generated `2026-10-12T10:48:09Z`. Open generated-writer PRs #518–#524 (graph, quality report, README counts, search index, skills API, badges, changelog) are the republication queue for the 538-skill corpus.
- Wave-2 additions follow the experimental `v1` / `added: 2026-10` format with the full section structure (Description, When to Use, Inputs, Procedure, Outputs, Runnable Example, Failure Modes, Security and Authority Boundary, Evidence, Related Skills, Changelog), verified in the API export entries and the PR #514 file list.
- Failure-modes coverage, measured 2026-10-12 at the 493-skill baseline: 453 of 493 skill files carry a `## Failure Modes` section (GitHub code search, `incomplete_results: false`; 0 matches in category README files). Runnable-example coverage is CI-gated, not merely conventional: the quality gate reports 0 stubs / 0 invalid.
- Note: this audit's measurement pass hit GitHub's unauthenticated REST rate limit (60/hr) partway through a directory count; measurements were switched to the authenticated connector (PR file lists, code search). No repository state was affected.

## Code review findings

### P2 — fix recommended

1. **Branch hygiene.** 423 branches measured; only `main` and the 8 `automation/*` generated-writer branches are live. Approximately 414 stale squash-merged working branches remain: `fix/*` 98, `coo/*` 87, `docs/*` 48, `feat/*` 45, `p1/*` 33, `phase2/*` 22, `chore/*` 14, `ceo/*` 6, and smaller sets. The agent connector exposes no branch-deletion tool, so cleanup is owner-side.
2. **Projection-republication inconsistency window.** Between a corpus merge and the merge of its generated-writer PRs, `main` serves stale projections while the canonical corpus has moved. Live instance at audit close: canonical 538 public skills versus projections at 493 while PRs #518–#524 are open. PR #477 removed the related cross-projection pairing failure (index and export counts move atomically), but the window itself is structural under the PR-publication model. Mitigation: prompt owner merging of the queued writer PRs; a fail-closed gate comparing the canonical count against projection counts would close it detectably (candidate future work — not implemented, not claimed).
3. **Issue #447 (generated-writer PR creation and checks).** New evidence recorded 2026-10-12: bot PRs #509 and #512 were successfully created by generated writers after the permission fixes, so the historical `gh pr create` failure mode is not reproducing. Run-log confirmation of the original failures remains owner-side. The issue is left open for the owner's close/hold decision; no agent action beyond the posted evidence.

### P3 — quality of life

1. `tools/build_search_index.py` applies silent frontmatter defaults: a skill with missing or malformed frontmatter indexes with invented default values instead of failing or warning. A warn-or-fail on missing fields would keep index entries honest.
2. The coverage gate measures only `cli/`, `api/`, and `mcp/` at a 50% threshold; `tools/` and `tests/` sit outside the gate.
3. README comparison-table overclaims — **resolved this cycle** by PR #525 (see Documentation health).
4. `skill-activation-runtime.yml` is a ~43 KB monolith workflow; decomposition into composable/reusable jobs is on the owner-approved backlog.
5. `meta/` layering: `meta/audits/` now holds 27 dated audit documents and `meta/CURRENT-STATE.md` is ~104 KB with historical sections retained as evidence. The evidence-first convention is sound, but a periodic roll-up index would improve navigability.

### Verified strengths

- `tools/export_skills.py` is deterministic (git-derived timestamps, sorted keywords — PR #479); rebuilds of an unchanged corpus publish nothing, ending the bot-PR churn loop.
- The cross-projection consistency test enforces index/export atomicity (PR #477), so no projection can merge alone without reddening `main`.
- Protected-writer and authoritative-path governance contract phrases survived the permission restoration (PR #472) and the later CI-permission hardening (PR #501) intact.

## PR and CI audit

- PR #525 (this cycle): README comparison-claims alignment. Exact-head CI: 16/16 check runs completed, 14 success / 2 skipped, zero failures; squash-merged as `2666ccf6` with verified post-merge content.
- PRs #477 / #479 / #478 (earlier 2026-10-12, same session track): atomic index+export republication, export determinism, converging canonical rebuild — all merged after green exact-head CI; superseded PRs #471/#473/#474 closed with explanations.
- CI on `main` at `176744bf6` (pre-#525 snapshot): 19/19 check runs completed, success/skipped only.
- Wave-2 merges #506 and #514 landed through the parallel expansion track; their merge-head CI is that track's responsibility and was not re-verified here (no cross-session interference).
- Skipped conclusions (Dependabot/labeler, where applicable) were not treated as failures, consistent with prior audits.

## Evaluation / activation boundary

Unchanged from the 2026-10-06 audit and still binding:

- Issue #357 activation evidence remains infrastructure-blocked (`INFRASTRUCTURE_INELIGIBLE` runner classification); the 12-observation activation corpus does not exist.
- CAP-007, CAP-011, and CAP-014 empirical contracts remain NOT RUN. Deterministic ground-truth tooling exists (CAP-011's 100-case dataset with mechanical re-derivation), but no candidate run exists.
- Therefore no activation-rate, reliability, invocation, or general efficacy claim is valid. Do not fabricate labels or empirical success.

## Documentation health

- The README comparison table now carries measured claims with a claim-basis footnote (PR #525): CI-gated coverage cells are distinguished from template-convention cells; the unsupported "production-ready" phrasing is gone; auto-synced count anchors (owned by `tools/update_readme_counts.py`) are untouched.
- `meta/CURRENT-STATE.md` top summary bullets were re-verified current at the recorded reconciliation (484 files / 483 public at that layer, with wave-2 sections layered beneath); the stale pilot-era bullets flagged in an earlier pass had already been corrected. Historical narrative retained as evidence is intentional.
- The claim-basis footnote's measured figure (453/493) is dated; it should be re-measured (or promoted to a CI gate) when the corpus next moves.

## Branch hygiene (measured 2026-10-12)

- Total: 423 branches. Keep: `main` and `automation/*` (8). Stale: ~414.
- Prefix tally: `fix/*` 98, `coo/*` 87, `docs/*` 48, `feat/*` 45, `p1/*` 33, `phase2/*` 22, `chore/*` 14, `ceo/*` 6, `governance/*` 6, `evaluation/*` 5, `evidence/*` 5, `improve/*` 5, `quality/*` 5, `devin/*` 4, `audit/*` 3, `diag/*` 3, `platform/*` 3, `runtime/*` 3, `skills/*` 7, `ci/*` 2, plus singles (`agent/*`, `demand/*`, `maint/*`, `maintenance/*`, `provenance/*`, `security/*`, `badge-data`).
- Owner-side action: delete the stale set. The agent connector has no branch-deletion tool.

## Next decision — owner-approved corpus priority

1. **Evidence & quality pass** over the expanded corpus; highest-leverage item is promoting the failure-modes section from template convention (453/493) to a CI gate.
2. **CAP-011 empirical contracts** — ground truth exists; candidate runs do not.
3. **Continue expansion to the 593-skill target** (wave 2 in flight: 538/593 public after PR #514, pending its projection republications).
4. **Decompose `skill-activation-runtime.yml`** (the ~43 KB monolith).

Owner-side operational items: merge the queued generated-writer PRs #518–#524 promptly to close the live republication window; delete the ~414 stale branches; decide on issue #447 closure.

## Final audit verdict

No P0 blocker. The evidence-first loop is functioning end to end: generated writers are deterministic, republication is atomic, public claims are now measured rather than aspirational, and corpus expansion proceeds under the documented owner-directed governance override. The residual risks are operational — the republication window and branch sprawl — not correctness or security.
