---
name: voice-agent-sdk-action-wiring
description: Wire spoken user requests to bounded tool actions through a voice agent SDK with typed schemas and confirmation gates.
metadata:
  source: skills/04-action-execution/voice-agent-sdk-action-wiring.md
  category: 04-action-execution
  version: "v1"
---

# Voice Agent SDK Action Wiring

## Description
Wire spoken user requests to bounded tool actions through a voice agent SDK with typed schemas and confirmation gates. Execution is bounded by typed action schemas and recorded confirmations rather than free-text tool invocation.

## When to Use
- A voice agent must call backend tools from spoken requests.
- Action schemas must be typed and validated before execution.
- Destructive actions require a spoken confirmation round.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The action schema registry, the transcribed request, and the confirmation policy. |
| Outputs | An executed action with its validated arguments and confirmation record. |
| Safety | Fail closed by refusing actions whose arguments fail schema validation. |

## Procedure
1. Register each backend action with a typed argument schema.
2. Map the transcribed request to a candidate action.
3. Validate extracted arguments against the schema.
4. Require a confirmation round for any destructive action.
5. Execute the action and record the call with arguments and result.
6. Emit the execution record with schema version and confirmation state.

## Outputs
| Area | Contract |
|---|---|
| Primary | An executed action with validated arguments and recorded result. |
| Verification | Schema versions and transcripts that reproduce the wiring. |
| Failure | A refusal record with the validation failure when arguments do not match. |

## Runnable Example
```python
def wire(request, schemas, confirmations):
    name = request["action"]
    if name not in schemas:
        return {"ok": False, "refuse": "unknown_action"}
    missing = [k for k in schemas[name]["required"] if k not in request["args"]]
    if missing:
        return {"ok": False, "refuse": "invalid_args", "missing": missing}
    if schemas[name]["destructive"] and not confirmations.get(name):
        return {"ok": False, "refuse": "needs_confirmation"}
    return {"ok": True, "executed": name, "args": request["args"]}

sch = {"book": {"required": ["date"], "destructive": True},
       "lookup": {"required": ["query"], "destructive": False}}
assert wire({"action": "lookup", "args": {"query": "x"}}, sch, {})["executed"] == "lookup"
assert wire({"action": "book", "args": {"date": "mon"}}, sch, {})["refuse"] == "needs_confirmation"
assert wire({"action": "book", "args": {}}, sch, {"book": True})["refuse"] == "invalid_args"
```

## Failure Modes
- Destructive actions execute on the first transcription without confirmation.
- Arguments bypass schema validation when extraction is confident.
- Unknown actions fall through to a default handler.
- Confirmation rounds are not recorded with the execution log.
- Schema changes are deployed without versioning executed actions.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Mistral released Voxtral 3 speech models together with a voice agent SDK (AIBriefs, November 7, 2026) ([public signal](https://aibriefs.news/ai-news-today))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Voice Agent Turn Taking Interruption Perception](voice-agent-turn-taking-interruption-perception.md)
- [Voice Agent Pipeline Orchestration](voice-agent-pipeline-orchestration.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
