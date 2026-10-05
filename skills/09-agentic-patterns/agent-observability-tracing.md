---
title: "Agent Observability Tracing"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Instrument agent runs so model calls, skill versions, tool calls, latency, failures, and costs can be reconstructed from correlated telemetry."
added: "2026-10"
version: v1
tags: [observability, tracing, telemetry, agents, opentelemetry]
---

# Agent Observability Tracing

## Description
Create correlated telemetry for agent execution so a complete run can be reconstructed without relying on model self-report. Capture agent/session identity, skill version, model invocation, tool invocation, latency, outcome, and relevant cost/token metadata while excluding secrets and unnecessary sensitive content.

## When to Use
- Debugging multi-step agent execution.
- Measuring skill invocation and failure behavior.
- Attributing latency, tokens, or cost across agent/tool chains.
- Verifying which skill version actually ran.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Agent run, correlation/trace ID, skill identity/version, model/tool calls, timestamps, outcome metadata, and telemetry policy. |
| Outputs | Structured logs/metrics/traces with correlated spans and explicit outcome/error fields. |
| Evidence | Telemetry must identify the executed component/version and distinguish observed data from inferred conclusions. |

## Procedure
1. Define the operational questions the telemetry must answer.
2. Establish a stable run/trace identifier and propagate it through model, skill, and tool calls.
3. Emit structured spans for skill selection, skill execution, model calls, and tool calls.
4. Record versioned skill identity and execution outcome.
5. Record latency and token/cost data only when actually available.
6. Redact secrets and sensitive payloads before export.
7. Verify that an induced failure can be reconstructed from telemetry alone.

## Failure Modes
- Missing correlation IDs break call-chain reconstruction.
- Skill/version attribution is absent or inferred incorrectly.
- Cost is reported from guessed pricing rather than observed instrumentation.
- Logs contain credentials or raw sensitive prompts.
- Metrics use unbounded labels and create cardinality explosions.
- A successful span is mistaken for proof of a successful side effect.

## Security Boundary
Telemetry is an evidence surface, not an authorization surface. Never expand permissions to improve observability.

## Evidence
Public 2026 ecosystem requests explicitly seek OpenTelemetry/observability hooks for MCP and agent skill evaluation, including attribution of agent, skill version, model calls, tool calls, latency, and cost.

## Related
- audit-logging.md
- mcp-tool.md
- agent-evaluation.md
- tool-execution.md
