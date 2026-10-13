---
name: ip-geolocation-parsing
description: Resolve IP addresses to coarse location fields from offline databases or API responses, record precision limits, and never present coarse geolocation as an exact position.
metadata:
  source: skills/01-perception/ip-geolocation-parsing.md
  category: 01-perception
  version: "v1"
---

# IP Geolocation Parsing

## Description
Resolve IP addresses to coarse location fields from offline databases or API responses, record precision limits, and never present coarse geolocation as an exact position. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a decision needs a coarse location estimate with honest precision bounds before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for ip geolocation parsing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the ip geolocation parsing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def lookup(prefix_db, ip):
    octets = [int(o) for o in ip.split(".")]
    if len(octets) != 4 or any(o > 255 for o in octets):
        raise ValueError("invalid ipv4 %r" % ip)
    prefix = ".".join(str(o) for o in octets[:2])
    return prefix_db.get(prefix, "unknown")

db = {"203.0": "test-region"}
assert lookup(db, "203.0.113.5") == "test-region"
assert lookup(db, "198.51.100.1") == "unknown"
try:
    lookup(db, "999.1.1.1")
    raise AssertionError("should have raised")
except ValueError:
    print("ip guard held")
```

## Failure Modes
- Treating city-level guesses as verified addresses.
- Using stale geolocation databases.
- Ignoring VPN and proxy indicators.
- Inferring personal identity from coarse location.
- Skipping validation of malformed addresses.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Compliance-aware agents that handle location context are a recurring 2026 enterprise request signal in public coverage; this is a dated signal, not an adoption metric.

## Related
- network-traffic-reading.md
- geospatial-reading.md
- url-normalization.md
