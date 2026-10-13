---
name: browser-fingerprint-management
description: Manage browser fingerprint consistency across automation runs with recorded profiles and detection-site checks instead of random spoofing.
metadata:
  source: skills/11-web/browser-fingerprint-management.md
  category: 11-web
  version: "v1"
---

# Browser Fingerprint Management

## Description
Manage browser fingerprint consistency across automation runs with recorded profiles and detection-site checks instead of random spoofing. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- automation must maintain a consistent browser identity across sessions.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for browser fingerprint management work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the browser fingerprint management steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def profile_consistent(profile, observed):
    keys = ('viewport', 'timezone', 'language')
    return all(profile.get(k) == observed.get(k) for k in keys)

p = {'viewport': '1280x800', 'timezone': 'UTC', 'language': 'en'}
assert profile_consistent(p, {'viewport': '1280x800', 'timezone': 'UTC', 'language': 'en'})
assert not profile_consistent(p, {'viewport': '1280x800', 'timezone': 'UTC', 'language': 'fr'})
```

## Failure Modes
- Randomizing fingerprints per request into obvious inconsistency.
- Mixing profile attributes that never co-occur in real browsers.
- Never checking consistency against detection sites.
- Losing fingerprint state between runs in the same session.
- Treating fingerprint changes as harmless without re-login checks.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Fingerprint consistency and detection checks recur in 2026 web-automation requests; this is a dated signal, not an adoption metric.

## Related
- browser-profile-management.md
- browser-session-isolation.md
- headless-browser-configuration.md
