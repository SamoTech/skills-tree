![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-github-api.json)

# GitHub API (Code)

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Interact with GitHub repositories programmatically: create issues, PRs, commits, branches, and releases via the REST or GraphQL API.

### Example

```python
import httpx

headers = {'Authorization': f'token {GITHUB_TOKEN}'}
r = httpx.post(
    f'https://api.github.com/repos/{owner}/{repo}/issues',
    json={'title': 'Missing skill file', 'body': 'Please add the missing file.'},
    headers=headers
)
print(r.json()['html_url'])
```

### Related Skills

- [Git Operations](git-operations.md)
- [GitHub API Tool](../07-tool-use/github-api.md)
