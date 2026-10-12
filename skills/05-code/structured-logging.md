---
title: "Structured Logging"
category: 05-code
level: intermediate
stability: experimental
description: "Emit logs as structured events — timestamp, level, ids, and measured fields — with stable schemas, correlation ids, and redaction rules instead of free-text lines."
added: "2026-10"
version: v1
related: ["debugging", "performance-profiling"]
---

# Structured Logging

Category: Code | Level: intermediate | Stability: experimental | Version: v1

## Description

A log line that only a human can parse is a cost center: it cannot be filtered, alerted on, or audited at scale. Structured logging emits events — a stable name, a level, a timestamp, and measured fields — with correlation ids that tie each event to the request or agent step that produced it, and redaction rules that keep sensitive values out of records by design.

## When to Use

Use whenever more than one system or more than one day separates writing from reading — services, pipelines, agent frameworks — where logs must be filtered by field rather than grepped by hope.

Do not log raw payloads as fields; structure exists partly to make redaction enforceable.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `events` | `list` | Yes | The operations to instrument |
| `schema` | `map` | Yes | Field names and types per event |
| `redaction` | `map` | No | Fields to drop or mask at emit time |

## Procedure

1. Define the event vocabulary first — a stable event name per operation, with a documented field schema per event.
2. Include correlation ids in every event: request id, run id, step id, so a chain is reconstructable across systems.
3. Emit at the level that matches the reader: debug for development detail, info for operations, warning for degraded-but-serving, error for failures with an owner.
4. Redact by schema rather than by review: sensitive fields are masked or dropped at emit time, before any sink sees them.
5. Measure rather than narrate: durations, counts, and statuses as typed fields, with free text as a supplement rather than the record.
6. Log an error once with full context at the handling site, not re-logged at every layer of propagation.

## Outputs

| Output | Type | Description |
|---|---|---|
| `events` | `list` | Structured records with schema-conformant fields |
| `schemas` | `map` | Event-to-field contracts |
| `pipeline` | `map` | Sink routing and retention per level |

## Runnable Example

```python
import json
import time

def log_event(event, level, run_id, fields):
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": level,
        "event": event,
        "run_id": run_id,
        **fields,
    }
    sensitive = {"user_email"}
    redacted = {k: ("***" if k in sensitive else v) for k, v in record.items()}
    return json.dumps(redacted, sort_keys=True)

print(log_event("tool_call", "info", "run-42", {"tool": "search", "duration_ms": 130}))
print(log_event("tool_call", "info", "run-42", {"tool": "search", "user_email": "sam@example.org"}))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Free-text only | Records cannot be filtered or alerted on | Emit schema-conformant fields |
| Context stripping | Events lack the ids to reassemble a chain | Correlate every event to request and run |
| Redaction by review | Sensitive values reach sinks before anyone looks | Mask or drop by schema at emit time |
| Level inflation | Everything is an error and nothing is actionable | Map levels to reader decisions |
| Duplicate error logging | The same failure is logged at every layer | Log once with full context at the handling site |

## Security and Authority Boundary

Logs are among the most commonly exfiltrated artifacts: they outlive sessions, replicate to multiple sinks, and reach wide audiences. Enforce schema-level redaction, treat log systems as production data stores, and audit what event fields can carry before adding them.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of log files and their role in operational systems (https://en.wikipedia.org/wiki/Log_file).
2. The JSON Lines format documentation for newline-delimited structured records (https://jsonlines.org/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Debugging](debugging.md) — the investigation layer these records serve.
- [Performance Profiling](performance-profiling.md) — the measurement layer whose fields often share this pipeline.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
