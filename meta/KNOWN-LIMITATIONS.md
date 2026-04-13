# Known Limitations — v1.0

This document is part of the Dependency Watchdog operational contract.
It lists runtime behaviours that were consciously accepted rather than patched,
with the precise reasoning and the conditions under which each limitation activates.

---

## 1. GitHub Pages Deployment Throttling (Accepted — v1.0)

**Risk level:** Low-Medium  
**SLA impact:** Pages render latency only. Does NOT affect the 15-minute CVE detection SLA.

### What happens

Every push to the `badge-data` branch triggers `deploy-badge-data.yml`,
which rebuilds and deploys to GitHub Pages. During high-velocity periods
(e.g., a Verification Day sprint with 20-30 PRs merging in an hour),
GitHub Pages may queue deployments. Users may see stale badge states for
5–15 minutes during those windows.

### Why it was not patched in v1.0

- GitHub Pages queues deployments; it does **not lose them**. Every push
  eventually deploys. The window is latency, not data loss.
- The 15-minute SLA in `meta/badge-states.md` refers to **CVE detection
  latency** (OSV polling → badge JSON written to `badge-data` branch).
  Pages render speed is a separate concern and is not contractual.
- Implementing a debounce/batch mechanism (e.g., a `staging-badge-data`
  branch that aggregates changes and pushes to `badge-data` every 5 minutes)
  adds significant workflow complexity for a problem that only manifests
  during sprint events.

### When it will be patched

If Pages throttling causes deployments to **fail** (not just queue)
during a Verification Day sprint, the following mechanism will be implemented:

**Proposed v1.1 fix — Staging Branch Debounce:**
1. `sync-badges.yml` writes to a `staging-badge-data` branch instead of `badge-data`.
2. A new `deploy-debounce.yml` workflow runs on a 5-minute cron, squashes all
   changes from `staging-badge-data` into a single `badge-data` push.
3. This reduces Pages deployments from N (one per PR) to max 12/hour.
4. `osv-watch.yml` continues to push directly to `badge-data` (bypasses staging)
   to preserve the CVE detection SLA.

**Trigger condition:** 3 or more Pages deployment failures in a single day.

---

## 2. Phantom Badge Visibility Window (Accepted with Mitigation — v1.0)

**Risk level:** Low (mitigated)  
**SLA impact:** None (user-trust cosmetic only)

### What happens

`ast-sweep.yml` pushes Yellow (machine-inferred) badge JSONs to `badge-data`
**before** the draft PR to `main` is created. This gives users immediate
visibility during the review window. If the draft PR is later closed without
merging, `revoke-phantom-badges.yml` automatically resets affected badges
to `unscanned` (grey) within ~60 seconds of the PR close event.

### Residual exposure

The window between the pre-merge badge push and the phantom revocation
(if the PR is closed) is the duration of the PR review — typically minutes
to hours. During that window, users see Yellow for a skill that may not
proceed. This is **accepted** because:

- Yellow means "machine-inferred, not human-verified" — this is already
  a provisional, low-trust state. It does not claim safety.
- The alternative (never pushing until merge) means Grey badges for the
  entire review window, which provides zero information to users.
- Revocation is automatic and deterministic — no manual cleanup required.

### What is NOT acceptable

A phantom badge remaining Yellow **after** PR close. `revoke-phantom-badges.yml`
prevents this. If that workflow fails (network, permissions), the next run of
`sync-badges.yml` or `osv-watch.yml` will also correct it via the rehydration pass.

---

## 3. Retry Exhaustion Under Extreme Concurrency (Accepted — v1.0)

**Risk level:** Very Low  
**SLA impact:** Delayed by at most one 15-minute cron cycle.

### What happens

All push steps use a 3-attempt retry-rebase loop to handle concurrent pushes
to `badge-data`. In the extreme case where all 3 attempts fail (>3 concurrent
workflows pushing simultaneously), the workflow exits with code 1 (marked as
failed in GitHub Actions) and logs a recovery note.

### Why this is safe

- The failed workflow logs clearly state which badges were not updated.
- `osv-watch.yml` runs every 15 minutes and will recover any missed badge states.
- 3 concurrent pushes is extremely unlikely outside of deliberate stress testing.
- The rebase conflict resolution policy is deterministic:
  - In `osv-watch.yml`: advisory badges win (OSV data takes precedence).
  - In `sync-badges.yml`: SBOM-derived Yellow/Green badges win.
  - In `revoke-phantom-badges.yml`: unscanned (grey) wins for non-protected badges.

### When it will be patched

If monitoring shows retry exhaustion occurring in normal operation (not stress tests),
the push steps will be replaced with a job-level mutex using
[`peaceiris/actions-gh-pages`](https://github.com/peaceiris/actions-gh-pages)
or a Redis-backed lock via a GitHub App.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| v1.0 | April 2026 | Initial known limitations document — 3 accepted behaviours |

*This document is updated whenever a known limitation is patched or a new one is identified.*
