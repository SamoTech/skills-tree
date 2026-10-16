---
name: maf-tool-wrapper-migration
description: Migrate tool wrappers to Microsoft Agent Framework conventions by mapping tool schemas, preserving argument validation and error contracts, and recording behavior differences found during migration testing.
metadata:
  source: skills/07-tool-use/maf-tool-wrapper-migration.md
  category: 07-tool-use
  version: "v1"
---

# MAF Tool Wrapper Migration

## Description
Migrate tool wrappers to Microsoft Agent Framework conventions by mapping tool schemas, preserving argument validation and error contracts, and recording behavior differences found during migration testing. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Existing tool wrappers must run under Microsoft Agent Framework without changing tool semantics.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the existing wrapper set, the MAF tool contract, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the MAF tool wrapper migration steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A migrated wrapper set with schema mappings, validation parity checks, and a recorded behavior-difference list. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def map_tool(tool, naming):
    return {"name": naming(tool["name"]), "params": sorted(tool["params"]), "validated": tool.get("validated", False)}
m = map_tool({"name": "get_user", "params": ["id"]}, lambda n: n.replace("_", "-"))
assert m["name"] == "get-user" and m["params"] == ["id"]
```

## Failure Modes
- Renaming tools and arguments without recording the old names for callers.
- Dropping argument validation during migration because the framework revalidates.
- Assuming framework error types map one-to-one to previous wrapper errors.
- Migrating all wrappers in one pass with no per-tool parity test.
- Leaving deprecated wrappers active alongside migrated ones with no cutover plan.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Microsoft Agent Framework 1.0 GA and migration guidance are dated 2026 coverage. ([public signal](https://atlan.com/know/ai-agent/microsoft/agent-framework/))
- Typed tool composition across agent frameworks is a named fall-2026 theme. ([public signal](https://vdf.ai/blog/best-ai-agent-frameworks/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [api pagination](../07-tool-use/api-pagination.md)
- [tool description writing](../06-communication/tool-description-writing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
