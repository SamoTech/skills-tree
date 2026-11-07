---
title: "Mobile Agent Session Event Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Parse live mobile agent-session events that stream tool calls, approvals, steering requests, and remote stops from a managed agent platform."
added: "2026-11"
version: v1
related: [agent-runtime-action-event-parsing, agent-screen-event-stream-parsing]
tags: [parsing, agents, supervision, auditing]
---

# Mobile Agent Session Event Parsing

## Description
Parse live mobile agent-session events that stream tool calls, approvals, steering requests, and remote stops from a managed agent platform. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A live supervised agent session must be followed from a mobile device before an approval is granted.
- Tool-call approval requests must be distinguished from steering requests and remote stops.
- Session events must be audited after the run to verify who approved what and when.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The raw mobile session event stream, the agent task registry, and the approval vocabulary. |
| Outputs | A parsed session timeline naming each tool call, its approval outcome, and any steering or stop events. |
| Safety | Fail closed by withholding approval when the event actor or the referenced tool cannot be resolved. |

## Procedure
1. Read the session event stream and locate the tool-call identifier, actor, and timestamp.
2. Resolve the referenced tool against the task registry before any approval is judged.
3. Map each event to the approval vocabulary such as request, grant, deny, steer, and stop.
4. Attach the responding human actor to every grant and deny event.
5. Verify that steering events point at a live execution segment in the timeline.
6. Emit the parsed session timeline with approval outcomes and unresolved events flagged.

## Outputs
| Area | Contract |
|---|---|
| Primary | A parsed session timeline naming each tool call, its approval outcome, and any steering or stop events. |
| Verification | Recorded event fields and actor-resolution checks that reproduce the approval audit. |
| Failure | A fail-closed error report naming the unresolved tool or actor and the withheld approval. |

## Runnable Example
```python
def parse_session(events, tools, vocab):
    timeline = []
    for e in events:
        if e["kind"] not in vocab:
            return {"ok": False, "reason": "unknown_event", "event": e["kind"]}
        if e["kind"] == "tool_call" and e["tool"] not in tools:
            return {"ok": False, "reason": "unknown_tool", "tool": e["tool"]}
        if e["kind"] in ("grant", "deny") and not e.get("actor"):
            return {"ok": False, "reason": "missing_actor"}
        timeline.append((e["ts"], e["kind"], e.get("tool", ""), e.get("actor", "")))
    return {"ok": True, "timeline": timeline}

events = [{"ts": 1, "kind": "tool_call", "tool": "read_doc"}, {"ts": 2, "kind": "grant", "actor": "dana"}]
r = parse_session(events, {"read_doc"}, {"tool_call", "grant", "deny", "steer", "stop"})
assert r["ok"] and r["timeline"][1][2] == "" 
assert parse_session([{"ts": 3, "kind": "reboot"}], set(), set())["ok"] is False
```

## Failure Modes
- Approval outcomes are recorded without the responding human actor.
- Unknown tool references are passed through instead of withholding the approval.
- Steering events are attached to the wrong execution segment.
- Remote stops are logged as routine completions rather than operator interventions.
- The parsed timeline is emitted without unresolved-event flags.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- DigitalOcean's Cuttlefish iPhone app lets customers follow live agent sessions, approve or deny tool calls, steer an execution, or stop it remotely on the Managed Agents platform (AI Agent News Today, November 6, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/daily/2026-11-06))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Runtime Action Event Parsing](agent-runtime-action-event-parsing.md)
- [Agent Screen Event Stream Parsing](agent-screen-event-stream-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

