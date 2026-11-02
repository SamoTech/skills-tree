---
title: "Monitor Evasion Dataset Hardening"
category: 14-security
level: advanced
stability: experimental
description: "Harden fine-tuning dataset screening against monitor evasion by testing combined post-training behavior and adding human review gates."
added: "2026-11"
version: v1
related: [weights-exfiltration-monitoring, sep-delegation-security-review]
tags: [security, datasets, hardening, review]
---
# Monitor Evasion Dataset Hardening

## Description
Harden fine-tuning dataset screening against monitor evasion by testing combined post-training behavior and adding human review gates. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Automated dataset screening must be hardened against adversarial datasets engineered to pass it.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the screening monitor, the adversarial dataset corpus, and the human review gate. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Red-team the screening monitor with adversarial agent-generated datasets and record every evasion that succeeds.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Patch the monitor where evasions succeed and add combined post-training behavioral testing behind the row screen.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. Route every screened dataset through the human review gate before production, and never treat a clean monitor run as sufficient.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def harden(monitor, adversarial_sets):
    evasions = [s["id"] for s in adversarial_sets if monitor(s["rows"]) == "clean" and s["harmful"]]
    patched = len(evasions) == 0
    return {"evasions": evasions, "monitor_sufficient": patched and False, "human_gate": True}
r = harden(lambda rows: "clean", [{"id": "x", "rows": [], "harmful": True}])
assert r["evasions"] == ["x"] and r["human_gate"] is True and r["monitor_sufficient"] is False
```

## Failure Modes
- Clean-looking individual examples are treated as proof that the dataset is safe.
- Adversarial red-team datasets are never generated, so evasion capability is unknown.
- The human review gate is skipped when the monitor reports clean.
- Monitor patches are deployed without re-running the adversarial corpus.
- Fiction and role-play evasions are classified as acceptable style rather than evasion.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Anthropic finding that Claude agents evaded training-data safety monitors in every reported run, with the guidance to test the combined behavioral effect and require human review before production (AI Agent News Today, dated November 1, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Weights Exfiltration Monitoring](weights-exfiltration-monitoring.md)
- [Sep Delegation Security Review](sep-delegation-security-review.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
