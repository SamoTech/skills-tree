# CEO Execution Queue — 2026-10-07

> Authoritative short-term queue under DECISION-2026-10-07-CEO-STRATEGIC-SHIFT.

## Active queue

1. **P0 — Branch protection on `main`** — **VERIFIED 2026-10-07**
   - `main` protected = true
   - Require PR before merging: on
   - Do not allow bypassing: on
   - Allow force pushes: off
   - Required checks: `gitleaks`, `Test Python 3.13`
   - Optional hardening still available (more required checks, conversation resolution)

2. **P1 — Real activation traces (#357)** — **NEXT**
   Minimum 4 cases × 3 fresh-session runs from a compatible agent runtime (Hermes preferred).
   - Dataset: `benchmarks/activation/skill-activation-v1.json`
   - Capture guide: `benchmarks/activation/HERMES-TRACE-CAPTURE.md`
   - Observer: `benchmarks/activation/hermes_skill_activation_observer.py`
   - Schema: `meta/skill-activation-observation.schema.json`
   - Runner: `tools/run_skill_activation_benchmark.py`
   - No fabricated scores. Missing corpus = not PASS.

3. **P1 — Top-20 skill activation hardening**
   After (or in parallel with) traces: select from demand signals; improve descriptions / examples / failure modes.

4. **P1 — Public activation evidence surface**
   Transparent table of measured activation / false-activation rates with sample size and date.

5. **Ongoing**
   Keep workflow inventory, generated projections, and project-brain docs synchronized. No new search/routing authority or bulk migration without measured need.

## Success metrics (90 days)

| Metric | Target |
|--------|--------|
| Branch protection on main | Done |
| Real activation traces published | ≥ 1 complete dataset |
| Skills with measured activation data | ≥ 15 |
| External projects referencing Skills Tree | ≥ 5 (evidence-backed) |
| New skills | Demand + evidence driven only |

## Status

P0 CLOSED. P1 activation traces are the active product gate.
