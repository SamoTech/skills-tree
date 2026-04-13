![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-linear-api.json)

# Linear API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Create, update, and query Linear issues, cycles, and projects via the Linear GraphQL API.

### Example

```python
import httpx

query = '''
mutation CreateIssue($title: String!, $teamId: String!) {
  issueCreate(input: { title: $title, teamId: $teamId }) {
    issue { id title url }
  }
}
'''
r = httpx.post(
    'https://api.linear.app/graphql',
    headers={'Authorization': LINEAR_KEY},
    json={'query': query, 'variables': {'title': 'Add missing skill files', 'teamId': TEAM_ID}}
)
```

### Related Skills

- [Jira API](jira-api.md)
- [GitHub API](github-api.md)
