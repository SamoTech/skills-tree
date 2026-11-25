---
title: "Llms Txt Mcp Server Discovery Usage"
category: 07-tool-use
level: advanced
stability: experimental
description: "Use llms.txt, MCP server discovery, and OAuth metadata endpoints to enumerate candidate tool servers with recorded verification."
added: "2026-11"
version: v1
related: [browser-tool, a2a-tool]
tags: [tools, discovery, mcp]
---

# Llms Txt Mcp Server Discovery Usage

## Description
Use llms.txt, MCP server discovery, and OAuth metadata endpoints to enumerate candidate tool servers with recorded verification. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A task needs candidate tool servers from public discovery.
- Server identity and auth modes must be verified before use.
- A discovery record must list exclusions with reasons.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The task capability description, the discovery endpoints, and the verification checks. |
| Outputs | A discovery record naming each candidate server, its identity proof, and its auth mode. |
| Safety | Fail closed by excluding servers whose identity or auth metadata cannot be verified. |

## Procedure
1. Fetch the llms.txt and discovery metadata for candidate servers.
2. Parse advertised capabilities against the task description.
3. Verify server identity through its recorded proof material.
4. Read the OAuth metadata and record the supported auth modes.
5. Exclude servers failing identity or auth verification.
6. Emit the discovery record with candidates and exclusions.

## Outputs
| Area | Contract |
|---|---|
| Primary | A discovery record naming each candidate server, its identity proof, and its auth mode. |
| Verification | The recorded inputs and intermediate values that reproduce the primary output from the runnable example. |
| Failure | A fail-closed hold naming the unmet precondition and the withheld primary output. |

## Runnable Example
```python
def discover(endpoints, checks):
    record = []
    for e in endpoints:
        ok = e["identity_proof"] and e["oauth_metadata"]
        record.append({"server": e["server"], "verified": ok, "excluded": not ok or not checks.get(e["server"], False)})
    return record

eps = [{"server": "a", "identity_proof": True, "oauth_metadata": True},
       {"server": "b", "identity_proof": False, "oauth_metadata": True}]
r = discover(eps, {"a": True, "b": True})
assert r[0]["excluded"] is False and r[1]["excluded"] is True
```

## Failure Modes
- Candidate servers are used before identity verification..
- OAuth metadata is skipped when the server is popular..
- Exclusions are not recorded with reasons..
- Discovery results are cached past their verification date..
- The task description is matched to servers by keyword only..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- dailyai.report publishes developer resources including MCP server discovery, OAuth metadata, and llms.txt alongside its public feed API (DailyAI Report, November 8, 2026) ([public signal](https://dailyai.report/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Browser Tool](browser-tool.md)
- [A2a Tool](a2a-tool.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
