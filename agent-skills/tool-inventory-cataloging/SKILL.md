---
name: tool-inventory-cataloging
description: Maintain a catalog of available tools with declared capabilities, permissions, owners, and deprecation status, and check it before adding duplicates.
metadata:
  source: skills/07-tool-use/tool-inventory-cataloging.md
  category: 07-tool-use
  version: "v1"
---

# Tool Inventory Cataloging

## Description
Maintain a catalog of available tools with declared capabilities, permissions, owners, and deprecation status, and check it before adding duplicates. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires tool inventory cataloging before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for tool inventory cataloging. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the tool inventory cataloging procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Tool Inventory Cataloging: deterministic check
def validate(record, required):
    missing = [k for k in required if k not in record]
    return (True, []) if not missing else (False, missing)

ok, missing = validate({"id": "x", "source": "y"}, ["id", "source"])
assert ok and not missing
print("validated")
```

## Failure Modes
- Proceeding with tool inventory cataloging without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Tool governance is a named 2026 enterprise requirement; published governance guidance requests tool inventories. These are dated public signals, not adoption metrics.

## Related
- tool-schema-design.md
- capability-based-skill-selection.md
- permission-checking.md
