---
name: browser-profile-management
description: Create, persist, and isolate browser profiles and contexts for automation runs, managing cookies, storage state, and settings across sessions without cross-contamination.
metadata:
  source: skills/11-web/browser-profile-management.md
  category: 11-web
  version: "v1"
---

# Browser Profile Management

Category: Web | Level: intermediate | Stability: experimental | Version: v1

## Description

A browser profile is a bag of authenticated identity and accumulated state. The skill covers defining a profile blueprint, creating isolated contexts from it rather than mutating a shared session, restoring saved storage state when persistence is required, exporting state after authenticated runs, and proving teardown left the base profile untouched. Isolation is the default because concurrent writes to one profile corrupt state and make runs order-dependent.

## When to Use

Use when automation needs persistent login state, parallel isolated sessions, or reproducible browser environments with consistent locale, timezone, and viewport settings.

Do not share a single logged-in profile across parallel runs. Concurrent sessions on one profile corrupt storage state and produce flaky, order-dependent results.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `blueprint` | `object` | Yes | Profile definition: base settings, storage state source, isolation requirements |
| `persist_path` | `string` | No | Where storage state is saved to and restored from |
| `isolation` | `enum` | No | `context-per-run` (default), `shared`, or `fresh` |

## Procedure

1. Define the profile blueprint: base settings, storage state source, and the required isolation level.
2. Create a fresh context from the blueprint rather than mutating a shared browser session.
3. Restore saved storage state where persistence is required and record exactly what was restored.
4. Apply consistent locale, timezone, viewport, and permission settings for reproducibility.
5. Export storage state at the end of authenticated runs for reuse, without logging any secrets.
6. Tear down the context and confirm no state leaked into the base profile.

## Outputs

| Output | Type | Description |
|---|---|---|
| `profile_id` | `string` | Identifier of the context created for this run |
| `storage_state` | `object` | Exported cookies and local state after the run |
| `isolation_report` | `object` | What was shared, restored, and persisted |

## Runnable Example

```python
def plan_profiles(runs, isolation):
    """runs: list of run ids that need authenticated state"""
    if isolation == "context-per-run":
        return {r: "context:" + r for r in runs}
    if isolation == "fresh":
        return {r: "ephemeral" for r in runs}
    return {"shared": runs}

print(plan_profiles(["checkout-flow", "profile-edit"], "context-per-run"))
print(plan_profiles(["checkout-flow", "profile-edit"], "shared"))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Storage corruption | Parallel runs mutated one profile | Enforce context-per-run isolation |
| Login state lost | Storage not exported after authentication | Export state at run end and version the exports |
| Credential leakage | Secrets embedded in exported state files | Restrict permissions and never log exports |
| Fingerprint drift | Device settings differ between runs | Pin viewport, locale, and timezone in the blueprint |
| Cookie expiry mid-run | Restored state older than the session lifetime | Validate session age before starting |

## Security and Authority Boundary

A profile is a credential by another name. Treat exported storage state as a secret: restrict file permissions, scope each profile to the narrowest account the task needs, and never share profiles across operators or environments.

## Evidence

This skill is grounded in dated public implementation references:

1. The Playwright browser contexts documentation (https://playwright.dev/python/docs/browser-contexts).
2. The Playwright authentication and storage state documentation (https://playwright.dev/python/docs/auth).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Cookie Management](cookie-management.md) — the per-site state that profiles persist and restore.
- [Web Login](web-login.md) — the authentication flow that produces the state a profile stores.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
