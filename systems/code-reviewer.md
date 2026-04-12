# Code Reviewer System

**Category:** systems | **Level:** intermediate | **Stability:** stable | **Version:** v1

## Overview

An automated code review agent that reads pull request diffs, applies reasoning skills to identify bugs, style violations, security risks, and improvement opportunities, then generates structured, actionable review comments — mimicking a senior engineer's review process at scale.

---

## Skills Used

| Skill | Role in System |
|---|---|
| `skills/01-perception/code-reading.md` | Parse and understand the diff |
| `skills/02-reasoning/causal.md` | Trace logic bugs to their root cause |
| `skills/02-reasoning/risk-assessment.md` | Flag security and correctness risks |
| `skills/02-reasoning/abductive.md` | Infer developer intent from context |
| `skills/06-communication/summarize.md` | Produce concise, actionable comments |
| `skills/05-code/debug.md` | Identify runtime and logic errors |
| `skills/14-security/secret-scanning.md` | Detect accidentally committed secrets |

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  Code Reviewer                  │
├─────────────────────────────────────────────────┤
│                                                 │
│  PR Diff ──► Diff Parser ──► Chunk Splitter     │
│                                    │            │
│                                    ▼            │
│                          ┌─────────────────┐    │
│                          │  Review Agent   │    │
│                          │  ┌───────────┐  │    │
│                          │  │ Bug Check │  │    │
│                          │  │ Style     │  │    │
│                          │  │ Security  │  │    │
│                          │  │ Perf      │  │    │
│                          │  └───────────┘  │    │
│                          └────────┬────────┘    │
│                                   │             │
│                          Comment Formatter      │
│                                   │             │
│                          GitHub Review API      │
└─────────────────────────────────────────────────┘
```

---

## Implementation

```python
import anthropic
import httpx
from typing import List

client = anthropic.Anthropic()

SYSTEM_PROMPT = """
You are a senior software engineer conducting a thorough code review.
For each code chunk, identify:
1. BUGS — logic errors, off-by-one, null dereferences, race conditions
2. SECURITY — hardcoded secrets, injection vectors, improper auth
3. STYLE — naming, complexity, dead code, missing docs
4. PERFORMANCE — N+1 queries, missing indexes, inefficient loops

Format each issue as:
**[SEVERITY: critical|major|minor]** `file.py:line` — Description + suggested fix.

If a chunk looks good, say "LGTM" with one sentence of praise.
"""

def get_pr_diff(repo: str, pr_number: int, token: str) -> str:
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3.diff"}
    r = httpx.get(f"https://api.github.com/repos/{repo}/pulls/{pr_number}", headers=headers)
    return r.text

def split_diff_into_chunks(diff: str, max_lines: int = 80) -> List[str]:
    """Split large diffs into reviewable chunks by file boundary."""
    chunks, current = [], []
    for line in diff.splitlines():
        if line.startswith("diff --git") and current:
            chunks.append("\n".join(current))
            current = []
        current.append(line)
        if len(current) >= max_lines:
            chunks.append("\n".join(current))
            current = []
    if current:
        chunks.append("\n".join(current))
    return chunks

def review_chunk(chunk: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Review this diff:\n\n```diff\n{chunk}\n```"}]
    )
    return response.content[0].text

def review_pull_request(repo: str, pr_number: int, github_token: str) -> List[str]:
    diff = get_pr_diff(repo, pr_number, github_token)
    chunks = split_diff_into_chunks(diff)
    reviews = [review_chunk(chunk) for chunk in chunks]
    return reviews

# Usage
if __name__ == "__main__":
    comments = review_pull_request(
        repo="myorg/myrepo",
        pr_number=42,
        github_token="ghp_..."
    )
    for i, comment in enumerate(comments):
        print(f"--- Chunk {i+1} ---\n{comment}\n")
```

---

## Configuration

```python
REVIEW_CONFIG = {
    "model": "claude-opus-4-5",
    "max_chunk_lines": 80,       # Lines per review chunk
    "severity_threshold": "minor",  # Only post comments at or above
    "auto_approve": False,          # Never auto-approve, always human review
    "languages": ["python", "typescript", "go", "rust"],
    "skip_patterns": ["*.lock", "*.min.js", "migrations/"],
}
```

---

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| False positives | Model flags valid patterns | Tune system prompt with repo conventions |
| Context loss | Large diffs exceed window | Chunk by file, pass imports as context |
| Missed secrets | Obfuscated credentials | Add regex pre-pass before LLM |
| Review fatigue | Too many minor comments | Set severity threshold to `major` |

---

## Related

- `systems/coding-agent.md` — Full coding system that can also fix what it reviews
- `blueprints/multi-agent-workflow.md` — Parallelise review across multiple agents
- `skills/05-code/debug.md` · `skills/14-security/secret-scanning.md`

## Changelog

- **v1** (2026-04) — Initial system: diff parsing, chunk review, structured output
