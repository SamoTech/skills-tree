---
name: maps-geolocation
description: Use mapping APIs for geocoding, place search, distance, and routing with validated coordinates, explicit scope, privacy minimization, and result verification.
---

# Maps & Geolocation

## Description
Use mapping APIs for geocoding, place search, distance, and routing with validated coordinates, explicit scope, privacy minimization, and result verification.

## When to Use
Use this capability when the workflow explicitly requires maps & geolocation and the target interface is documented and authorized.

## Inputs / Outputs
- Inputs: validated task data, documented tool parameters, and authorization context.
- Outputs: structured provider result plus evidence needed to verify the outcome.

## Failure Modes
- Invalid or ambiguous inputs.
- Missing permissions, unavailable provider, rate limits, or transport failures.
- Credential exposure or excessive tool scope.
- Treating an acknowledgement as proof of a completed side effect.

## Runnable Example

```python
request = {"capability": "maps-geolocation", "validated": True}
assert request["validated"]
print("invoke only after validating the tool contract")
```

## Evidence
Repository-backed guidance; see the canonical skill under skills/07-tool-use/maps-geolocation.md and its cited provider documentation.

## Related
- 07-tool-use
- tool-guardrails
