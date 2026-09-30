---
title: "Jira API"
category: 07-tool-use
level: intermediate
stability: stable
description: "Use Jira REST APIs from agents to inspect and manage issues with explicit authorization, field validation, and outcome verification."
added: "2026-09"
related: [07-tool-use, 04-action-execution]
---

# Jira API

## Description
Use Jira REST APIs as an agent tool for issue retrieval and controlled project operations. Treat issue creation, edits, transitions, and comments as external side effects that require validated inputs and post-action verification.

## When to Use
- Search or retrieve Jira issues needed for an agent workflow.
- Create or update issues when the workflow has authority to modify the project.
- Add structured comments or transitions using documented Jira fields.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Authentication | Use a short-lived or least-privilege credential where supported. |
| Project | Validate the target project key before writing. |
| Issue fields | Validate required fields against the target Jira instance. |
| Query | Bound JQL and pagination; avoid unbounded result sets. |
| Output | Issue key, status, fields, and response metadata required by the workflow. |
| Verification | Re-read the affected issue after mutations. |
| Failure modes | Permission denial, invalid field, transition mismatch, rate limit, or stale issue state. |

## Runnable Example

```python
import os, requests

base = os.environ["JIRA_BASE_URL"].rstrip("/")
auth = (os.environ["JIRA_EMAIL"], os.environ["JIRA_API_TOKEN"])
r = requests.get(
    f"{base}/rest/api/3/myself",
    auth=auth,
    headers={"Accept": "application/json"},
    timeout=20,
)
r.raise_for_status()
print(r.json()["accountId"])
```

## Failure modes
- Assuming custom fields have the same identifiers across Jira instances.
- Mutating an issue without checking current state and permissions.
- Accepting a 2xx response without verifying the resulting issue.
- Logging authorization headers or tokens.
- Using broad JQL when only a bounded issue set is required.

## Evidence
- Atlassian Jira REST API documentation: https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/
- Repository schema and validation workflows define the local skill contract.

## Related
- linear-api
- github-api
- tool-guardrails
- approval-before-destructive-tools
