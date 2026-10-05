---
name: agent-observability-tracing
description: Instrument agent runs so model calls, skill versions, tool calls, latency, failures, and costs can be reconstructed from correlated telemetry.
---

# Agent Observability Tracing

Propagate a stable run/trace identifier through skill selection, skill execution, model calls, and tool calls. Record versioned skill identity, timestamps, outcomes, latency, and observed token/cost data when available. Redact secrets and sensitive payloads. Verify that an induced failure can be reconstructed from telemetry alone; telemetry is evidence, not authorization.

## Evidence
Public 2026 OpenClaw and Hermes ecosystem issues request OpenTelemetry/observability for agent, skill-version, model-call, and tool-call attribution. The canonical skill is authoritative.
