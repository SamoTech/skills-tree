# CI/CD Pipeline Generation

**Category:** `code`  
**Skill Level:** `advanced`  
**Stability:** `stable`

### Description

Generate CI/CD pipeline configuration files for GitHub Actions, GitLab CI, CircleCI, or other platforms.

### Example

```yaml
# Generated GitHub Actions workflow
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - run: pytest
```

### Related Skills

- [Dockerfile Generation](dockerfile-generation.md)
- [Code Generation](code-generation.md)
