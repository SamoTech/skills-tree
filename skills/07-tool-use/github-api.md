# GitHub API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Interact with GitHub repositories: create/read issues, pull requests, commits, files, branches, and releases via the GitHub REST or GraphQL API.

### Example

```python
import httpx
headers = {'Authorization': f'token {GITHUB_TOKEN}'}
r = httpx.post(
    f'https://api.github.com/repos/{owner}/{repo}/issues',
    json={'title': 'Bug: skill file missing', 'body': 'The skill file was not created.'},
    headers=headers
)
```

### Frameworks

- GitHub MCP Server
- PyGithub
- Octokit (JavaScript)

### Related Skills

- [Git Operations](../05-code/git-operations.md)
- [MCP Tool](mcp-tool.md)
