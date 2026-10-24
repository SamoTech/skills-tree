---
name: voice-control-command-parsing
description: Parse voice-control utterances from a coding agent transcript into bounded command intents with argument slots and confidence, without executing anything.
metadata:
  source: skills/01-perception/voice-control-command-parsing.md
  category: 01-perception
  version: "v1"
---
# Voice Control Command Parsing

## Description
Parse voice-control utterances from a coding agent transcript into bounded command intents with argument slots and confidence, without executing anything. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A voice-driven coding agent session must turn spoken commands into structured intents before any tool is invoked.
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
3. Tokenize the transcript, match each utterance against the declared command grammar, extract argument slots, and drop utterances whose confidence is below the declared threshold.
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
def parse_voice_command(utterance, grammar):
    text = utterance.strip().lower()
    for intent, patterns in grammar.items():
        for pat in patterns:
            if text.startswith(pat):
                arg = text[len(pat):].strip()
                return {"intent": intent, "arg": arg, "confidence": 0.9 if arg else 0.6}
    return {"intent": "unmatched", "arg": text, "confidence": 0.0}

grammar = {"run_tests": ["run the tests", "run tests"], "open_file": ["open file"]}
assert parse_voice_command("run the tests now", grammar)["intent"] == "run_tests"
assert parse_voice_command("maybe run the tests", grammar)["intent"] == "unmatched"
```

## Failure Modes
- Partial words in the transcript are matched as complete command intents.
- Homophone commands such as test and text map to the wrong intent.
- Utterances below the confidence threshold are executed anyway.
- Argument slots capture trailing words that are not part of any argument.
- A multi-command utterance is parsed as one intent and the rest is dropped.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The OpenAI Codex CLI 0.163 release adds voice control to a terminal coding agent, making spoken-command parsing a live agent input path (trendintech.com, dated October 2026) ([public signal](https://trendintech.com/openai-codex-cli-0-163-voice-control-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Voice Activity Detection](../01-perception/voice-activity-detection.md)
- [Streaming Asr Partial Parsing](../01-perception/streaming-asr-partial-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
