---
name: sandbox-manifest-artifact-perception
description: Parse sandbox workspace manifests into explicit entry, mount, and permission contracts before an agent runs against sandboxed files.
metadata:
  source: skills/01-perception/sandbox-manifest-artifact-perception.md
  category: 01-perception
  version: "v1"
---

# Sandbox Manifest Artifact Perception

## Description
Parse sandbox workspace manifests into explicit entry, mount, and permission contracts before an agent runs against sandboxed files. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A sandboxed agent is about to inspect files or run commands and the workspace boundary must be understood first.
- The outcome would change if a manifest entry were misread and an out-of-scope path were treated as sandboxed.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The sandbox manifest document, the declared workspace entries, and the permission contract for each entry. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Extract each manifest entry with its source path, mount point, and declared access mode.
4. Cross-check every entry against the task scope and flag paths outside the declared boundary.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A manifest record naming each entry, its mount point, access mode, and any out-of-scope flags. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def parse_manifest(manifest):
    entries = []
    for name, spec in manifest["entries"].items():
        entries.append({"name": name, "src": spec["src"], "mode": spec.get("mode", "read")})
    return {"entries": entries, "count": len(entries)}
m = parse_manifest({"entries": {"data": {"src": "/tmp/dataroom", "mode": "read"}}})
assert m["count"] == 1 and m["entries"][0]["mode"] == "read"
```

## Failure Modes
- A manifest entry with no declared access mode is treated as read-only without flagging the ambiguity.
- Host paths outside the declared sandbox root are accepted as entries.
- The parsed record loses the source path, so later evidence cannot be traced to files.
- Mount points with the same name in different manifests are merged silently.
- The parser invents an entry for a default workspace that the manifest never declared.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The OpenAI Agents SDK introduced Manifest-based sandbox workspaces where agents inspect files inside controlled sandboxes (OpenAI, dated April 15, 2026) ([public signal](https://openai.com/index/the-next-evolution-of-the-agents-sdk/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Action Result Verification](../04-action-execution/action-result-verification.md)
- [Risk Assessment](../02-reasoning/risk-assessment.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
