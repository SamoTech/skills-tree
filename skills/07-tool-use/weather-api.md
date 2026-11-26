---
title: "Weather API"
category: 07-tool-use
level: intermediate
stability: stable
version: v2
description: "Retrieve weather observations or forecasts through a documented API with explicit location, time window, units, freshness, and provider-status handling."
added: "2026-09"
related: [tool-guardrails, function-calling, tool-output-validation]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-weather-api.json)

# Weather API

**Category:** `tool-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Retrieve weather observations or forecasts through a documented API with explicit location, time window, units, freshness, and provider-status handling. The invocation is contract-first: least-privilege credentials, bounded scope, validated inputs, and post-action verification instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | location | object | Explicit coordinates or verified place id, never a guessed name |
| Input | window | object | Time range, units (metric/imperial), and acceptable data age |
| Output | weather | object | Observations or forecast with units, timestamps, and provider metadata |
| Output | freshness | object | Data age disclosed; stale data labeled rather than passed as current |

### Procedure
1. Resolve the location explicitly (coordinates or verified place id) before querying.
2. State the time window and units in the request; never convert by assumption.
3. Authenticate with a least-privilege key from the authorized channel.
4. Validate the response schema and check the observation timestamp against the freshness bound.
5. Disclose data age and provider status; label stale or degraded results.
6. Cache raw responses with their fetch time for reproducibility.

### Example

```python
req = {'lat': 30.0444, 'lon': 31.2357, 'units': 'metric', 'window_h': 24, 'max_age_min': 60}
assert -90 <= req['lat'] <= 90 and -180 <= req['lon'] <= 180
assert req['units'] == 'metric'
print('explicit location, units, and freshness bound')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries and least privilege
- [Tool Output Validation](tool-output-validation.md) - validate provider responses before use
- [Tool Result Caching](tool-result-caching.md) - time-stamped response reuse

## Failure Modes

- Guessing locations from ambiguous names.
- Mixing unit systems or omitting them from results.
- Passing stale observations as current.
- Exposing the API key in code or logs.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails reference).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification
- https://openweathermap.org/api

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.
