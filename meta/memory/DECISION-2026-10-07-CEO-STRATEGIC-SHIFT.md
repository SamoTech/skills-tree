# DECISION-2026-10-07-CEO-STRATEGIC-SHIFT

**DECISION-ID:** DECISION-2026-10-07-CEO-STRATEGIC-SHIFT  
**Date:** 2026-10-07  
**Authority:** AI CEO / CIO under Human Owner final authority  
**Status:** LOCKED

## Topic

Strategic product priority shift for Skills Tree after full project audit.

## Decision

Skills Tree has completed the phase of building a rigorous, evidence-oriented, governance-heavy internal registry. The next phase must optimize for **measured external usefulness**: real agent activation, reliable skill selection/invocation, public activation evidence, and organic adoption.

### Priority order (effective immediately)

**P0 — Control plane**
1. Enable branch protection on `main` with required status checks, **or** document compensating controls and Human Owner acknowledgement if the connector cannot perform the change.

**P1 — Prove real-world value**
1. Collect real agent-runtime activation/invocation traces for the gap recorded in Issue #357 (minimum 4 cases × 3 fresh sessions).
2. Harden the top 20–30 high-demand / high-utility skills for clearer activation (description, examples, failure modes) using demand signals — not directory-order bulk migration.
3. Publish a public, evidence-backed activation surface (leaderboard or equivalent) that distinguishes structural quality from real runtime evidence. No fabricated scores.

**P2 — Distribution & adoption**
1. Prefer integrations and usage references in real agent platforms over additional internal schema work.
2. Seed external references only with evidence-backed claims.

**P3 — Process discipline**
1. Keep documentation-as-brain and fail-closed gates.
2. Do not invent new search engines, routing authorities, or bulk skill additions without measured need.
3. Freeze further large-scale stub migration until activation data exists.

### Explicit non-goals
- Fabricating adoption, popularity, or activation rates.
- Weakening validation, security, or evidence gates for velocity.
- Treating classifier “battle-tested” labels as runtime proof.

## Confidence

HIGH for the strategic diagnosis and priority order.  
MEDIUM for exact timing of external trace collection (depends on available runtimes).

## Evidence IDs

- Live repository audit 2026-10-06 / 2026-10-07 (CURRENT-STATE, ROADMAP, QUALITY-REPORT, Issue #357)
- Product mission (`meta/PRODUCT_MISSION.md`)
- COO master mission (`meta/COO_MASTER_MISSION.md`)
- External activation signals cited in #357 and MOST-WANTED-SKILLS (Hermes, agent-skills routing reports)

## Status

LOCKED

## Reopen Conditions

Reopen only if:
1. Human Owner overrides the priority order, or
2. New measured evidence shows that activation reliability is already solved at scale and a different bottleneck is dominant, or
3. A security incident requires temporary suspension of external-facing work.

## Execution implications

- `meta/ROADMAP.md` current execution queue is updated to match this decision.
- `meta/CURRENT-STATE.md` next-action section is updated.
- Issue #357 remains the primary activation evidence tracker.
- New tracking issues for top-20 hardening and public activation surface may be opened when the issue-creation path is available.
- Branch protection remains a documented control-plane gap (connector cannot set it automatically).
