---
title: Code Review
category: 05-code
level: intermediate
stability: stable
added: "2025-03"
description: "Apply code review in AI agent workflows."
version: v2
tags: [code, review, quality, automation]
updated: 2026-04
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-code-review.json)

# Code Review

## What It Does

Automates code review by analyzing a diff or file for bugs, security issues, style violations, performance problems, and logic errors — returning structured, actionable feedback with severity levels and suggested fixes.

## When to Use

- Automated PR review in CI/CD pipelines
- Pre-commit quality gates
- Onboarding: teaching juniors by example
- Auditing unfamiliar codebases quickly

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `code` | `str` | Code diff or full file content |
| `language` | `str` | Programming language |
| `focus` | `list[str]` | Areas to prioritize: `bugs`, `security`, `performance`, `style` |
| → `issues` | `list[Issue]` | Structured list of findings |
| → `summary` | `str` | Executive summary of overall quality |
| → `score` | `int` | Quality score 0-100 |

## Runnable Example

```python
import anthropic
import json
from dataclasses import dataclass
from typing import List

client = anthropic.Anthropic()

@dataclass
class Issue:
    severity: str  # critical | high | medium | low | info
    category: str  # bug | security | performance | style | logic
    line: str
    description: str
    suggestion: str

def review_code(
    code: str,
    language: str = "python",
    focus: List[str] = None
) -> dict:
    focus_areas = ", ".join(focus or ["bugs", "security", "performance", "style"])

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        system=f"""You are an expert {language} code reviewer.
Analyze the code and return a JSON object with this exact structure:
{{
  "issues": [
    {{
      "severity": "critical|high|medium|low|info",
      "category": "bug|security|performance|style|logic",
      "line": "line number or range, e.g. 12 or 12-15",
      "description": "What is wrong and why it matters",
      "suggestion": "Exact fix or improved code"
    }}
  ],
  "summary": "2-3 sentence executive summary",
  "score": 0-100
}}
Focus on: {focus_areas}
Return ONLY valid JSON, no markdown.""",
        messages=[{"role": "user", "content": f"Review this {language} code:\n\n```{language}\n{code}\n```"}]
    )

    result = json.loads(response.content[0].text)
    return result

# Usage
sample_code = '''
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute(query)
    password = result['password']
    return result
'''

review = review_code(sample_code, language="python", focus=["security", "bugs"])
print(f"Score: {review['score']}/100")
print(f"Summary: {review['summary']}")
for issue in review['issues']:
    print(f"[{issue['severity'].upper()}] Line {issue['line']}: {issue['description']}")
    print(f"  Fix: {issue['suggestion']}\n")
```

## CI/CD Integration

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Get diff
        run: git diff origin/main...HEAD > diff.txt
      - name: AI Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python scripts/review.py diff.txt
```

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| False positives on style | Model too strict | Add `# noqa` annotation support; tune severity threshold |
| Misses context-specific bugs | No project knowledge | Provide `ARCHITECTURE.md` or key files as context |
| JSON parse error | Model adds markdown | Strip ` ```json ` wrappers before parsing; use regex fallback |
| Slow on large files | Full file in context | Send only the diff, not the full file |

## Related Skills

- [`code-generation.md`](code-generation.md) — Write new code
- [`code-debugging.md`](code-debugging.md) — Find and fix bugs interactively
- [`security-scanning.md`](../14-security/security-scanning.md) — Deep security analysis

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-05 | Initial entry |
| v2 | 2026-04 | Structured JSON output, CI/CD example, severity scoring |
