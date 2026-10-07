# P0 Branch Protection — VERIFIED

**Date:** 2026-10-07  
**Authority:** Human Owner confirmation + public API check  
**Decision link:** DECISION-2026-10-07-CEO-STRATEGIC-SHIFT

## Verified facts

- GitHub API reports `branches/main.protected = true`
- Human Owner confirmed settings:
  - Require a pull request before merging: **on**
  - Do not allow bypassing the above settings: **on**
  - Allow force pushes: **off**
  - Required status checks: `gitleaks`, `Test Python 3.13`

## Status

**P0 CLOSED.**

Optional follow-ups (non-blocking):
- Add more required checks (e.g. Test Python 3.12, build wheel, governance contracts)
- Require conversation resolution
- Require branches up to date (if not already on)

## Next mandatory product action

Issue #357 — collect real activation traces (4 cases × 3 fresh sessions).
