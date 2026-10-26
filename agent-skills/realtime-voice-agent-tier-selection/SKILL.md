---
name: realtime-voice-agent-tier-selection
description: Select realtime voice agent serving tiers using measured turn latency, concurrency, and cost under the declared conversation workload.
metadata:
  source: skills/08-multimodal/realtime-voice-agent-tier-selection.md
  category: 08-multimodal
  version: "v1"
---

# Realtime Voice Agent Tier Selection

## Description
Select realtime voice agent serving tiers using measured turn latency, concurrency, and cost under the declared conversation workload. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An operator needs this capability to proceed safely and verifiably.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Load-test each realtime tier at the declared concurrency, record turn latency and cost per conversation minute, and select the cheapest tier meeting the latency gate at target concurrency.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def select_realtime_tier(tiers, target_ccu, p95_gate):
    ok = [t for t in tiers if t["max_ccu"] >= target_ccu and t["p95_turn_ms"] <= p95_gate]
    if not ok:
        raise ValueError("no tier meets the latency gate at target concurrency")
    return min(ok, key=lambda t: t["cost_per_hour"])

tiers = [{"name":"mini","max_ccu":100,"p95_turn_ms":900,"cost_per_hour":0.30},
         {"name":"max","max_ccu":500,"p95_turn_ms":400,"cost_per_hour":1.20}]
assert select_realtime_tier(tiers, 200, 800) == tiers[1]
```

## Failure Modes
- Tiers are compared at single-session latency and the gate fails at production concurrency.
- Cost per hour is compared without concurrency and a cheap tier is picked that needs four times the sessions.
- Reasoning-enabled tiers are compared against non-reasoning tiers on the same latency gate.
- Load tests run on synthetic silence and barge-in traffic behaves differently.
- The selection is never revisited after the provider changes tier limits mid-contract.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- ElevenLabs shipped Eleven Realtime v1 Mini and v1 Max with a reasoning tier on October 20 (llmreference.com, dated October 2026) ([public signal](https://www.llmreference.com/changelog/2026-10))
- The same week shipped Voxtral Mini Transcribe Realtime 3, making realtime voice tier selection a multi-vendor recorded decision (llmreference.com, dated October 2026) ([public signal](https://www.llmreference.com/changelog/2026-10))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [08 Multimodal/speech Agent Turn Latency.md](../08-multimodal/speech-agent-turn-latency.md.md)
- [08 Multimodal/realtime Voice Provider Protocol Interchange.md](../08-multimodal/realtime-voice-provider-protocol-interchange.md.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
