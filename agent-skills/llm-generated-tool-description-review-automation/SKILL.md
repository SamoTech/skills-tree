---
name: llm-generated-tool-description-review-automation
description: Automate the review of LLM-generated tool descriptions before they are published to a tool catalog or registry.
metadata:
  source: skills/05-code/llm-generated-tool-description-review-automation.md
  category: 05-code
  version: "v1"
---
# LLM Generated Tool Description Review Automation

## Description
Automate the review of LLM-generated tool descriptions before they are published to a tool catalog or registry. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A pipeline generates tool descriptions with an LLM and must review them before publishing.
- Descriptions that overstate capability or omit side effects must be caught automatically.
- Review findings must block publication rather than just warn.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The generated description, the source schema, and the review rule set. |
| Outputs | A review verdict naming blocking findings and the publish or reject decision. |
| Safety | Fail closed by rejecting descriptions with unverified capability claims. |

## Procedure
1. Read the generated description alongside the source schema it was derived from.
2. Check that every capability named in the description exists in the schema operations.
3. Flag side effects such as writes, payments, or deletions that the description omits.
4. Flag marketing language and unsupported claims against the rule set.
5. Reject the description when blocking findings remain, and record them.
6. Emit the verdict with findings and the corrected description request.

## Outputs
| Area | Contract |
|---|---|
| Primary | A review verdict with blocking findings and the publish or reject decision. |
| Verification | Recorded rule matches and schema checks that reproduce the verdict. |
| Failure | A fail-closed rejection naming the unverified claim and the withheld publication. |

## Runnable Example
```python
def review_description(desc, schema, rules):
    findings = []
    ops = set(schema.get("operations", []))
    for claim in desc.get("claims", []):
        if claim not in ops:
            findings.append({"blocking": True, "reason": "unsupported_claim", "claim": claim})
    if schema.get("side_effects") and not desc.get("mentions_side_effects"):
        findings.append({"blocking": True, "reason": "omitted_side_effects"})
    if any(w in desc.get("text", "").lower() for w in rules["marketing"]):
        findings.append({"blocking": False, "reason": "marketing_language"})
    if any(f["blocking"] for f in findings):
        return {"publish": False, "findings": findings}
    return {"publish": True, "findings": findings}

schema = {"operations": ["read"], "side_effects": ["write"]}
rules = {"marketing": ["revolutionary", "seamless"]}
no = review_description({"text": "revolutionary tool", "claims": ["read", "heal"], "mentions_side_effects": True}, schema, rules)
assert no["publish"] is False and any(f["reason"] == "unsupported_claim" for f in no["findings"])
ok = review_description({"text": "reads records", "claims": ["read"], "mentions_side_effects": True}, schema, rules)
assert ok["publish"] and ok["findings"] == []
```

## Failure Modes
- Descriptions publish without schema checks and unsupported claims reach agents.
- Omitted side effects pass review and agents invoke destructive tools unknowingly.
- Marketing language findings are dropped instead of being recorded for correction.
- The review warns but publishes anyway when blocking findings remain.
- Generated descriptions are overwritten by regeneration before review findings land.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Uber's AutoCrawler uses a large language model to produce tool descriptions for discovered tools, which remain disabled until their owning teams review and enable them (InfoQ, November 2, 2026, dated November 2, 2026) ([public signal](https://www.infoq.com/news/2026/11/uber-mcp-gateway-ai-agents/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Generated Code Auditing](agent-generated-code-auditing.md)
- [Documentation Example Testing](documentation-example-testing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
