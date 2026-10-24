---
name: notification-content-egress-protection
description: Prevent notification content captured by an agent from leaving the declared boundary, with egress rules checked per channel.
metadata:
  source: skills/14-security/notification-content-egress-protection.md
  category: 14-security
  version: "v1"
---

# Notification Content Egress Protection

## Description
Prevent notification content captured by an agent from leaving the declared boundary, with egress rules checked per channel. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent stores notification captures and their content must not egress through logs, telemetry, or model calls.
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
3. Classify stored notification content as boundary-limited, attach the egress rule to each storage record, and reject outbound channels that do not check the rule.
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
def egress_check(record, channel, rules):
    rule = rules.get(record["class"])
    if rule is None:
        return {"allowed": False, "reason": "no_rule"}
    if channel in rule["deny"]:
        return {"allowed": False, "reason": "channel_denied", "channel": channel}
    return {"allowed": True, "channel": channel}

rules = {"notification_body": {"deny": {"telemetry", "third_party_llm"}}}
rec = {"class": "notification_body"}
assert egress_check(rec, "telemetry", rules)["reason"] == "channel_denied"
assert egress_check(rec, "local_index", rules)["allowed"] is True
assert egress_check({"class": "unknown"}, "telemetry", rules)["reason"] == "no_rule"
```

## Failure Modes
- Notification content is sent to third-party models for summarization without a rule check.
- Telemetry payloads embed raw notification bodies as context fields.
- The rule is attached to the storage record but not read at the egress point.
- New channels are allowed until a rule is written for them.
- Logs are exempted from the check because they are internal.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Associated Press reporting records notification and message content reaching parties who never agreed, making notification-content egress protection a dated live control (apnews.com, dated October 19, 2026) ([public signal](https://apnews.com/article/meta-muse-openai-dot-ai-privacy-449734d41d3750aad7038b761faa49c9))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Plaintext Credential Egress Hardening](../14-security/plaintext-credential-egress-hardening.md)
- [Data Exfiltration Detection](../14-security/data-exfiltration-detection.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
