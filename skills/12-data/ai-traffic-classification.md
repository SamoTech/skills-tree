---
title: "AI Traffic Classification"
category: 12-data
level: advanced
stability: experimental
description: "Classify API and web traffic into AI-agent, bot, and human categories from recorded signals with confidence thresholds and auditable rules."
added: "2026-10"
version: v1
related: [anomaly-detection, data-profiling, stream-processing]
tags: [traffic, classification, rate-limits]
---

# AI Traffic Classification

## Description
Classify API and web traffic into AI-agent, bot, and human categories from recorded signals with confidence thresholds and auditable rules. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- access decisions or analytics need traffic separated by caller type.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for ai traffic classification work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the ai traffic classification steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def classify(signature):
    if signature.get('user_agent_contains') and 'llm' in signature['user_agent_contains']:
        return ('ai-agent', 'high')
    if signature.get('requests_per_minute', 0) > 600:
        return ('bot', 'medium')
    return ('human', 'low')

assert classify({'user_agent_contains': ['llm-bot']})[0] == 'ai-agent'
assert classify({'requests_per_minute': 900})[0] == 'bot'
assert classify({'requests_per_minute': 5})[0] == 'human'
```

## Failure Modes
- Classifying on a single spoofable header.
- Rules that nobody can audit or reproduce.
- Forgetting confidence bands so weak signals block traffic.
- Never validating labels against ground truth samples.
- Treating classification as proof of intent rather than signal.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Sites asking how to distinguish AI-agent traffic grew through 2026; this is a dated signal, not an adoption metric.

## Related
- anomaly-detection.md
- data-profiling.md
- stream-processing.md
