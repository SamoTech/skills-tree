---
name: jira-api
description: Use Jira REST APIs for bounded issue retrieval and project operations. Validate fields and permissions, minimize query scope, and re-read important mutations.
---

# Jira API

## Description
Use Jira REST APIs for bounded issue retrieval and project operations. Validate fields and permissions, minimize query scope, and re-read important mutations.

## When to Use
Use this capability when the workflow explicitly requires jira api and the target interface is documented and authorized.

## Inputs / Outputs
- Inputs: validated task data, documented tool parameters, and authorization context.
- Outputs: structured provider result plus evidence needed to verify the outcome.

## Failure Modes
- Invalid or ambiguous inputs.
- Missing permissions, unavailable provider, rate limits, or transport failures.
- Credential exposure or excessive tool scope.
- Treating an acknowledgement as proof of a completed side effect.

## Runnable Example

```python
request = {"capability": "jira-api", "validated": True}
assert request["validated"]
print("invoke only after validating the tool contract")
```

## Evidence
Repository-backed guidance; see the canonical skill under skills/07-tool-use/jira-api.md and its cited provider documentation.

## Related
- 07-tool-use
- tool-guardrails
