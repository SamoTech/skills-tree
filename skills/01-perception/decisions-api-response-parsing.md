---
title: "Decisions API Response Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Parse OpenAI Decisions API responses that classify content or route requests against a finite set of user-defined answers."
added: "2026-11"
version: v1
related: [intent-classification, json-schema-validation]
tags: [parsing, api, classification, routing]
---
# Decisions API Response Parsing

## Description
Parse OpenAI Decisions API responses that classify content or route requests against a finite set of user-defined answers. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A Decisions API call returns a decision that must gate a downstream branch.
- The finite answer set and the returned answer must be checked for agreement.
- The decision must be recorded with its question context before acting.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The raw Decisions API response, the declared finite answer set, and the question context. |
| Outputs | A parsed decision naming the returned answer, its set membership, and the mapped branch. |
| Safety | Fail closed by withholding the branch decision when the answer is outside the declared set. |

## Procedure
1. Read the response envelope and locate the returned answer and any confidence or metadata.
2. Load the declared finite answer set defined for the question.
3. Check that the returned answer is a member of the declared set.
4. Map the answer to the consuming branch, such as classify, route, or next action.
5. Record the question context, answer, and branch decision together.
6. Emit the parsed decision with its branch mapping and the recorded evidence.

## Outputs
| Area | Contract |
|---|---|
| Primary | A parsed decision naming the returned answer, its set membership, and the mapped branch. |
| Verification | Recorded envelope fields and set-membership checks that reproduce the decision. |
| Failure | A fail-closed error report naming the out-of-set answer and the withheld branch decision. |

## Runnable Example
```python
def parse_decision(resp, allowed):
    ans = resp.get("answer")
    if ans not in allowed:
        return {"ok": False, "answer": ans, "branch": None}
    branch = {"classify": "moderate", "route": "dispatch", "next_action": "plan"}[ans]
    return {"ok": True, "answer": ans, "branch": branch}
r = parse_decision({"answer": "route"}, {"classify", "route", "next_action"})
assert r["ok"] and r["branch"] == "dispatch"
bad = parse_decision({"answer": "maybe"}, {"classify", "route", "next_action"})
assert bad["ok"] is False and bad["branch"] is None
```

## Failure Modes
- The returned answer is outside the declared set and the closest match is silently substituted.
- The question context is dropped, so the answer cannot be audited against what was asked.
- Confidence or metadata fields are treated as authoritative instructions to act.
- An empty answer is coerced to a default branch without halting.
- The decision is emitted without recording the set-membership check.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 introduced the Decisions API, which returns real-time answers from a finite set of user-defined questions to classify content, route requests, or choose an agent next action (OpenAI DevDay 2026 Recap, dated November 5, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Intent Classification](intent-classification.md)
- [JSON Schema Validation](json-schema-validation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
