---
name: linear-api
description: Use Linear's GraphQL API from agents for bounded issue and project operations with typed queries and verified mutations.
metadata:
  source: skills/07-tool-use/linear-api.md
  category: 07-tool-use
---

# Linear API

## Description
Use Linear's GraphQL API as a controlled agent tool for querying and mutating issues, projects, teams, and cycles. Prefer narrow queries, explicit variables, and post-mutation verification.

## When to Use
- Retrieve issues, projects, teams, or cycles for an agent task.
- Create or update issues with validated team and state identifiers.
- Integrate project-management state into an agent workflow.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Endpoint | Use the documented Linear GraphQL endpoint. |
| Authentication | Keep the API key outside source and tool arguments. |
| Query | Use explicit operation and variables; avoid unnecessary fields. |
| Mutation | Validate identifiers and required inputs before execution. |
| Output | Parse the requested GraphQL data and inspect errors. |
| Verification | Re-query important mutations before reporting completion. |
| Failure modes | GraphQL validation error, authorization failure, rate limit, or stale identifier. |

## Runnable Example

```python
import os, requests

query = "query { viewer { id name } }"
r = requests.post(
    "https://api.linear.app/graphql",
    headers={"Authorization": os.environ["LINEAR_API_KEY"]},
    json={"query": query},
    timeout=20,
)
r.raise_for_status()
body = r.json()
assert not body.get("errors"), body.get("errors")
print(body["data"]["viewer"]["name"])
```

## Failure modes
- Hard-coding API credentials.
- Assuming an issue state or team identifier is stable across workspaces.
- Ignoring the GraphQL errors array when HTTP status is successful.
- Sending large unbounded queries.
- Treating mutation acknowledgement as verified state.

## Evidence
- Linear GraphQL API documentation: https://linear.app/developers/graphql
- Repository schema and validation workflows define local conformance requirements.

## Related
- jira-api
- github-api
- function-calling
- tool-guardrails
