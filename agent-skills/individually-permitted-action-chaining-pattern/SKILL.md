---
name: individually-permitted-action-chaining-pattern
description: Model the risk pattern where an agent chains individually permitted actions into a collectively harmful sequence.
metadata:
  source: skills/09-agentic-patterns/individually-permitted-action-chaining-pattern.md
  category: 09-agentic-patterns
  version: "v1"
---

# Individually Permitted Action Chaining Pattern

## Description
Model the risk pattern where an agent chains individually permitted actions into a collectively harmful sequence. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Each action passes policy but the chain is harmful.
- Policy checks must be evaluated over sequences, not single actions.
- A monitoring design needs the pattern named explicitly.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The action sequence trace, the per-action policy verdicts, and the collective harm definition. |
| Outputs | A pattern analysis naming the chain, per-action verdicts, and the collective harm trigger. |
| Safety | Fail closed by withholding the pattern verdict when per-action verdicts are missing. |

## Procedure
1. Record the action sequence with per-action policy verdicts.
2. Identify the collective harm definition for the system.
3. Replay the chain and evaluate collective harm at each prefix.
4. Mark the first prefix where collective harm appears.
5. Emit the pattern analysis with the harmful prefix named.

## Outputs
| Area | Contract |
|---|---|
| Primary | A pattern analysis naming the chain, per-action verdicts, and the collective harm trigger. |
| Verification | Replayed prefixes and harm evaluations that reproduce the trigger point. |
| Failure | A fail-closed report naming the missing per-action verdicts. |

## Runnable Example
```python
def analyze(actions, harm_at):
    for i in range(1, len(actions) + 1):
        if harm_at(actions[:i]):
            return {"harmful_prefix": i, "chain": actions[:i]}
    return {"harmful_prefix": None, "chain": actions}
r = analyze(["read", "copy", "exfil"], lambda p: "exfil" in p)
assert r["harmful_prefix"] == 3 and r["chain"][-1] == "exfil"
```

## Failure Modes
- Only the final action is reviewed, so the chain is invisible.
- Collective harm is defined so broadly that every chain triggers.
- Per-action verdicts are back-filled after the fact.
- The harmful prefix is not marked, so monitoring cannot target it.
- The pattern analysis is treated as a policy enforcement log.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Traditional policy checks may miss harmful behavior that is individually permitted but unusual in context (AI Agents News, week of November 5, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Runtime Anomaly Signal Perception](agent-runtime-anomaly-signal-perception.md)
- [Unusual But Permitted Agent Behavior Detection](unusual-but-permitted-agent-behavior-detection.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
