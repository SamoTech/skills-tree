---
title: Code Reviewer
category: systems
version: v1
stability: stable
skills: [code-reading, reasoning, comment-generation, diff-analysis, security-scanning]
---

# Code Reviewer

> Automated pull-request review agent that reads diffs, reasons about correctness, flags bugs, security issues, and style violations, then posts structured inline comments.

## Skills Used

| Skill | Role |
|---|---|
| `skills/01-perception/code-reading.md` | Parse diff hunks, understand context |
| `skills/02-reasoning/causal.md` | Trace impact of changes through call graph |
| `skills/02-reasoning/risk-assessment.md` | Rate severity of each finding |
| `skills/14-security/secret-scanning.md` | Catch leaked keys / tokens in diffs |
| `skills/06-communication/comment-generation.md` | Draft clear, actionable review comments |

## Architecture

```
GitHub Webhook (PR opened/updated)
        │
        ▼
┌──────────────────┐
│  Diff Fetcher    │  ← pulls unified diff via GitHub API
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────┐
│          Chunk Router                │
│  splits diff into per-file hunks     │
│  skips generated / vendor files      │
└──────┬──────────┬──────────┬─────────┘
       │          │          │
       ▼          ▼          ▼
  Bug Check  Security    Style / DX
  (causal)   (secret +   (comment
              vuln scan)  generation)
       │          │          │
       └──────────┴──────────┘
                  │
                  ▼
         Severity Ranker
      (risk-assessment.md)
                  │
                  ▼
        GitHub Review API
     (inline + summary post)
```

## Implementation

```python
import anthropic
import httpx

client = anthropic.Anthropic()

SYSTEM = """
You are a senior code reviewer. Given a unified diff, you:
1. Identify bugs, logic errors, and edge-case failures
2. Flag security issues (injection, secrets, auth bypass, SSRF)
3. Note performance problems (N+1 queries, unbounded loops)
4. Suggest clarity / DX improvements
5. Skip cosmetic nitpicks unless they harm readability

For every finding output JSON:
{"file": "path", "line": N, "severity": "critical|high|medium|low",
 "category": "bug|security|perf|style", "comment": "...", "suggestion": "..."}
"""

def review_pr(repo: str, pr_number: int, gh_token: str) -> list[dict]:
    headers = {"Authorization": f"Bearer {gh_token}", "Accept": "application/vnd.github.v3.diff"}
    diff = httpx.get(f"https://api.github.com/repos/{repo}/pulls/{pr_number}", headers=headers).text

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Review this diff:\n\n{diff[:12000]}"}]
    )

    import json, re
    findings = []
    for m in re.finditer(r'\{[^{}]+\}', response.content[0].text, re.DOTALL):
        try:
            findings.append(json.loads(m.group()))
        except json.JSONDecodeError:
            pass
    return sorted(findings, key=lambda f: ["critical","high","medium","low"].index(f["severity"]))

def post_review(repo: str, pr_number: int, findings: list[dict], gh_token: str, commit_sha: str):
    headers = {"Authorization": f"Bearer {gh_token}", "Content-Type": "application/json"}
    comments = [
        {"path": f["file"], "line": f["line"], "body": f"**[{f['severity'].upper()}] {f['category']}**\n{f['comment']}\n\n```suggestion\n{f.get('suggestion','')}\n```"}
        for f in findings if f["severity"] in ("critical", "high")
    ]
    summary = f"Found {len(findings)} issues: " + ", ".join(f"{f['severity']}: {f['category']}" for f in findings[:5])
    httpx.post(
        f"https://api.github.com/repos/{repo}/pulls/{pr_number}/reviews",
        headers=headers,
        json={"commit_id": commit_sha, "body": summary, "event": "COMMENT", "comments": comments}
    )
```

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| False positives on generated code | Vendored / auto-generated files | Add `.codereviewignore` skip list |
| Diff truncation on large PRs | Token limits | Chunk by file, review independently |
| Stale line numbers | Force-push rebases PR | Re-fetch commit SHA before posting |
| Review spam on draft PRs | Webhook fires on all events | Filter `draft: true` in webhook handler |

## Related

- `systems/coding-agent.md`
- `benchmarks/reasoning/react-vs-lats.md`
- `skills/14-security/secret-scanning.md`

## Changelog

- `v1` (2026-04) — Initial system with diff parsing, severity ranking, inline comment posting
