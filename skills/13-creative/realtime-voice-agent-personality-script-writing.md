---
title: "Realtime Voice Agent Personality Script Writing"
category: 13-creative
level: advanced
stability: experimental
description: "Write personality scripts for realtime voice agents with bounded tone, filler, and escalation rules."
added: "2026-10"
version: v1
related: [chatbot-persona-backstory-writing, dialogue-writing]
tags: [voice, personality, writing, scripts]
---
# Realtime Voice Agent Personality Script Writing

## Description
Write personality scripts for realtime voice agents with bounded tone, filler, and escalation rules. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A team must give a realtime voice agent a consistent personality without losing its escalation and safety rules.
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
3. Write the personality profile as a bounded script covering greeting, tone, filler-word policy, error responses, and escalation wording, and verify every rule survives the profile verbatim.
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
def validate_personality_script(profile, mandatory_rules):
    missing = [r for r in mandatory_rules if r not in profile["rules"]]
    if missing:
        raise ValueError("personality script dropped mandatory rules: " + ", ".join(missing))
    if len(profile["greeting"]) > 120:
        raise ValueError("greeting exceeds the attention budget")
    return {"name": profile["name"], "rules": sorted(profile["rules"])}
profile = {"name": "concierge", "greeting": "Hi, what can I book for you today?", "rules": {"tone_warm", "escalate_on_frustration", "no_medical_advice"}}
result = validate_personality_script(profile, ["escalate_on_frustration", "no_medical_advice"])
assert result["rules"] == ["escalate_on_frustration", "no_medical_advice"]
```

## Failure Modes
- The personality script rewrites escalation wording and safety phrases lose their literal meaning.
- Filler words are tuned for text and read aloud as robotic pauses.
- The greeting exceeds the attention budget and callers interrupt before the agent can act.
- Personality rules conflict and the agent oscillates between tones mid-call.
- The profile is written for one language and localization turns the persona inconsistent.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Azure Speech real-time voice-agent coverage documents lifelike realtime voice personas, which teams script as bounded personality profiles (techcommunity.microsoft.com, dated 2026) ([public signal](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/azure-speech-at-build-2026-powering-voice-agents-with-real-time-and-life-like-ex/4524638))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Chatbot Persona Backstory Writing](../13-creative/chatbot-persona-backstory-writing.md)
- [Dialogue Writing](../13-creative/dialogue-writing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
