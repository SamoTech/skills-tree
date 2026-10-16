---
name: agent-registry-poisoning-defense
description: Defend against poisoned agent and skill registry entries by verifying publisher identity, checking entry provenance and signature, and quarantining entries that change behavior or metadata without a new signed release.
metadata:
  source: skills/14-security/agent-registry-poisoning-defense.md
  category: 14-security
  version: "v1"
---

# Agent Registry Poisoning Defense

## Description
Defend against poisoned agent and skill registry entries by verifying publisher identity, checking entry provenance and signature, and quarantining entries that change behavior or metadata without a new signed release. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A team consumes skills or plugins from a registry that could host malicious or swapped entries.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the registry entry, its signature and provenance data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent registry poisoning defense steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A verification record with publisher, signature, and provenance checks, plus quarantine decisions. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def verify_entry(entry):
    checks = {"signed": entry.get("sig") is not None, "publisher": entry.get("publisher") is not None}
    failed = [k for k, ok in checks.items() if not ok]
    return {"allow": not failed, "failed": failed}
v = verify_entry({"sig": "s", "publisher": "p"})
assert v["allow"] is True
```

## Failure Modes
- Trusting entry popularity as proof of integrity.
- Accepting metadata updates without a new signed release.
- Skipping provenance checks for first-party-looking publishers.
- Letting quarantined entries stay active while under review.
- Verifying only on install and never on update.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Skill and plugin registry poisoning patterns are part of dated agent supply-chain security coverage. ([public signal](https://www.shakudo.io/blog/top-9-ai-agent-frameworks))
- Plugin management security is named in dated ecosystem digests covering OpenClaw plugin practice. ([public signal](https://github.com/jinming1345/agents-radar/issues/274))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [mcp tool poisoning detection](../14-security/mcp-tool-poisoning-detection.md)
- [mcp registry curation](../07-tool-use/mcp-registry-curation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
