---
title: "Transaction Data Provenance Recording"
category: 12-data
level: advanced
stability: experimental
description: "Record the source, time, and verification state of every external data element an agent uses in a transaction so outcomes can be traced back to their inputs."
added: "2026-11"
version: v1
related: [agent-data-launch-partner-integration, agent-task-success-rate-measurement]
tags: [provenance, transactions, data, audit]
---
# Transaction Data Provenance Recording

## Description
Record the source, time, and verification state of every external data element an agent uses in a transaction so outcomes can be traced back to their inputs. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent decision is disputed later and no one can show which data source produced the outcome.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the external data calls, the per-element provenance schema, and the transaction outcome record. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Attach a provenance record to every external data element at fetch time.
2. Store the provenance records alongside the transaction they fed, indexed by element.
3. Verify the stored records resolve to their sources on a sampled basis.
4. On an unresolvable provenance record, flag the transaction for review rather than silently keeping it.
5. Expire provenance records only together with their transaction records, never before.
6. Emit a structured result with the provenance set, sampling results, and flags.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def record_provenance(fetches):
    records = {}
    for source, key, value, ts in fetches:
        records[key] = {"source": source, "value": value, "ts": ts}
    return records
f = [("dataline", "price", 12.4, 1730000000), ("openweather", "temp", 21, 1730000001)]
rec = record_provenance(f)
assert rec["price"]["source"] == "dataline" and rec["temp"]["value"] == 21
```

## Failure Modes
- Data elements enter transactions with no record of which source produced them.
- Provenance is stored in a separate system that expires out of sync with transactions.
- Sampled verification never runs, so broken source links go unnoticed.
- Disputed outcomes are re-derived from current data instead of the recorded inputs.
- Provenance records are stripped on archive to save space.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Dataline reporting 19.4 million on-chain transactions through its cross-verified data network for agents (AI Agent News Today, dated November 1, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Data Launch Partner Integration](agent-data-launch-partner-integration.md)
- [Agent Task Success Rate Measurement](agent-task-success-rate-measurement.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
