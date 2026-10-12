---
name: social-engineering-detection
description: Detect social engineering attempts across messages and support channels by recognizing pretexting, urgency, authority impersonation, and credential harvesting patterns.
metadata:
  source: skills/14-security/social-engineering-detection.md
  category: 14-security
  version: "v1"
---

# Social Engineering Detection

Category: Security | Level: intermediate | Stability: experimental | Version: v1

## Description

Social engineering attacks people, not code, so detection works on message patterns and process anomalies. The skill covers screening inbound communications for the classic patterns: manufactured urgency, unverifiable authority, pretext setup, and redirection to off-channel or credential capture. It flags for review rather than silently blocking, because false positives on legitimate urgent mail are costly, and it never auto-responds to a suspected attacker.

## When to Use

Use when inbound email, chat, or support requests must be screened for phishing, pretexting, executive impersonation, and credential or payment redirection.

Do not auto-reply to suspected attacks or reveal the detection. Acknowledgment teaches the attacker what worked and marks the target as monitored.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `messages` | `table` | Yes | Inbound communications with headers, sender, and content |
| `identity_directory` | `object` | Yes | Known internal identities and their verified channels |
| `threshold` | `object` | No | Scores that route to review, warn, or block |

## Procedure

1. Verify sender identity against the directory, including display-name spoofing and lookalike domains.
2. Scan content for the core patterns: urgency, authority, secrecy pressure, and redirection.
3. Inspect links and attachments for credential capture and off-channel redirection.
4. Score the message from matched patterns and route by threshold: review, warn, or block.
5. Escalate with the evidence: matched patterns, sender analysis, and links.
6. Never auto-respond; suspected messages are silently routed to review.

## Outputs

| Output | Type | Description |
|---|---|---|
| `verdicts` | `table` | Per-message classification with matched patterns and score |
| `escalations` | `list` | Messages routed to security review with evidence attached |
| `campaign_view` | `object` | Grouped view when several messages share a sender or template |

## Runnable Example

```python
def score_message(msg, patterns):
    """msg: dict with sender, subject, body; patterns: {name: [keywords]}"""
    hits = []
    text = (msg.get("subject", "") + " " + msg.get("body", "")).lower()
    for name, keywords in patterns.items():
        if any(k in text for k in keywords):
            hits.append(name)
    score = min(1.0, len(hits) / 4.0)
    return {"hits": hits, "score": score, "route": "review" if score >= 0.5 else "warn"}

print(score_message(
    {"subject": "URGENT: payroll update needed", "body": "the ceo asked me to keep this quiet; confirm your login here"},
    {"urgency": ["urgent", "immediately"], "authority": ["ceo", "executive"],
     "secrecy": ["keep this quiet", "confidential"], "harvest": ["login", "password"]},
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| False confidence in blocking | Novel pretexts evade keyword patterns | Route on pattern plus identity anomalies, and staff a review path |
| Legitimate urgent mail flagged | Real urgency reads as manufactured | Warn rather than block borderline messages |
| Display-name spoof missed | Only reply-to checked | Compare full sender identity, not display names |
| Attacker tipped off | Auto-replies reveal the detection | Silently route; never acknowledge |
| Isolated alerts | Campaign messages triaged one by one | Group by sender and template to see campaigns |

## Security and Authority Boundary

This skill processes private communications. Screen only on metadata and content necessary for detection, keep suspected-message archives access-controlled, and be aware the sender may be a compromised legitimate account rather than an outsider.

## Evidence

This skill is grounded in dated public implementation references:

1. The MITRE ATT&CK phishing technique reference (https://attack.mitre.org/techniques/T1566/).
2. The SANS Institute awareness resources on social engineering (https://www.sans.org/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Input Guardrails](input-guardrails.md) — the inbound screening layer these detections extend to agents.
- [Harm Detection](harm-detection.md) — the pattern-matching approach shared with abuse screening.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
