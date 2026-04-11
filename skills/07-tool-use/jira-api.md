# Jira API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Create, update, search, and manage Jira issues, projects, and sprints via the Jira REST API.

### Example

```python
import httpx

headers = {'Authorization': f'Basic {AUTH}', 'Content-Type': 'application/json'}
r = httpx.post(
    f'{JIRA_URL}/rest/api/3/issue',
    headers=headers,
    json={
        'fields': {
            'project': {'key': 'SKILL'},
            'summary': 'Add missing skill files',
            'issuetype': {'name': 'Task'}
        }
    }
)
```

### Related Skills

- [Linear API](linear-api.md)
- [GitHub API](github-api.md)
