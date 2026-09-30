---
name: sensor-reading
description: Interpret bounded sensor telemetry while preserving units, timestamps, missingness, and uncertainty.
license: MIT
metadata:
  source: skills/01-perception/sensor-reading.md
  version: "v2"
---

# sensor-reading

Provide normalized readings with sensor ID, value, unit, and timestamp; return anomalies and trends as interpretations, not measurements.

## Failure modes

- Missing or irregular samples: preserve missingness.
- Unit mismatch: normalize explicitly before comparison.
- Model hallucination: never present generated values as observed telemetry.

## Evidence

- https://agentskills.io/specification
- https://docs.python.org/3/library/json.html

Evidence status: references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.
