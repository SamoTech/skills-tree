---
title: Code Review
category: 05-code
level: intermediate
stability: stable
added: "2025-03"
description: "Automates structured code review — bugs, security, performance, style — returning severity-graded findings, a quality score, and suggested fixes."
version: v3
tags: [code, review, quality, automation, security, diff]
updated: 2026-04
dependencies:
  - package: anthropic
    tested_version: "0.49.0"
    confidence: verified
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-code-review.json)

# Code Review

## Description

Automates code review by analyzing a diff or full file for bugs, security vulnerabilities, style violations, performance problems, and logic errors — returning structured, actionable feedback with severity levels, line references, and suggested fixes. Operates as a drop-in CI/CD step or an interactive agent tool.

## What It Does

Given source code or a unified diff, this skill:

1. Parses the input (full file or `git diff` patch)
2. Sends it to the model with a structured JSON output contract
3. Returns a list of `Issue` objects — each with severity, category, line reference, description, and a concrete fix
4. Computes an overall quality score (0–100) and an executive summary
5. Optionally posts findings as inline GitHub PR review comments

## When to Use

- Automated PR review triggered by `pull_request` events
- Pre-commit quality gates (block on `critical` or `high` findings)
- Onboarding: teaching code standards by example
- Auditing unfamiliar or legacy codebases quickly
- Security triage: focus mode on `security` category only

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `code` | `str` | Code diff (unified format) or full file content |
| `language` | `str` | Programming language (e.g. `python`, `typescript`) |
| `focus` | `list[str]` | Prioritize: `bugs`, `security`, `performance`, `style`, `logic` |
| `context` | `str \| None` | Optional: architecture notes, key conventions |
| → `issues` | `list[Issue]` | Severity-graded findings with line refs and fixes |
| → `summary` | `str` | 2–3 sentence executive summary |
| → `score` | `int` | Quality score 0–100 (100 = no issues) |

### Severity Scale

| Level | Meaning | Block PR? |
|---|---|---|
| `critical` | Data loss, RCE, auth bypass | Always |
| `high` | SQL injection, unhandled exception in hot path | Yes |
| `medium` | Logic error, missing validation | Warn |
| `low` | Style, naming, minor perf | Comment only |
| `info` | Suggestion, best practice | Optional |

## Runnable Example

```python
import anthropic
import json
import re
from dataclasses import dataclass
from typing import Optional

client = anthropic.Anthropic()

@dataclass
class Issue:
    severity: str   # critical | high | medium | low | info
    category: str   # bug | security | performance | style | logic
    line: str       # "12" or "12-15"
    description: str
    suggestion: str

@dataclass
class ReviewResult:
    issues: list[Issue]
    summary: str
    score: int      # 0–100

SYSTEM_PROMPT = """\
You are an expert {language} code reviewer.
Analyze the supplied code and return ONLY a valid JSON object — no markdown, no prose.

JSON schema:
{{
  "issues": [
    {{
      "severity": "critical|high|medium|low|info",
      "category": "bug|security|performance|style|logic",
      "line": "<line or range>",
      "description": "<what is wrong and why it matters>",
      "suggestion": "<exact fix or corrected snippet>"
    }}
  ],
  "summary": "<2-3 sentence executive summary>",
  "score": <integer 0-100>
}}

Focus areas: {focus}
{context_block}
"""

def _strip_json_fence(text: str) -> str:
    """Remove ```json ... ``` wrappers if model adds them despite instructions."""
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return text.strip()

def review_code(
    code: str,
    language: str = "python",
    focus: list[str] | None = None,
    context: Optional[str] = None,
) -> ReviewResult:
    focus_str = ", ".join(focus or ["bugs", "security", "performance", "style"])
    context_block = f"Project context:\n{context}" if context else ""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        system=SYSTEM_PROMPT.format(
            language=language,
            focus=focus_str,
            context_block=context_block,
        ),
        messages=[{
            "role": "user",
            "content": f"Review this {language} code:\n\n```{language}\n{code}\n```"
        }],
    )

    raw = _strip_json_fence(response.content[0].text)
    data = json.loads(raw)

    issues = [Issue(**i) for i in data.get("issues", [])]
    return ReviewResult(
        issues=issues,
        summary=data.get("summary", ""),
        score=data.get("score", 0),
    )

# ── Demo ──────────────────────────────────────────────────────────────────────

SAMPLE_CODE = '''
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute(query)
    password = result["password"]
    print(f"Loaded user {user_id}: {password}")
    return result

def process_upload(filename):
    path = "/uploads/" + filename
    with open(path) as f:
        return f.read()
'''

result = review_code(
    SAMPLE_CODE,
    language="python",
    focus=["security", "bugs"],
)

print(f"Score : {result.score}/100")
print(f"Summary: {result.summary}\n")

SEV_ORDER = ["critical", "high", "medium", "low", "info"]
for sev in SEV_ORDER:
    bucket = [i for i in result.issues if i.severity == sev]
    for issue in bucket:
        print(f"[{issue.severity.upper():8}] ({issue.category}) Line {issue.line}")
        print(f"  ↳ {issue.description}")
        print(f"  ✦ Fix: {issue.suggestion}\n")
```

## Diff-Mode Example

Feed a `git diff` patch directly — the model only reviews changed lines, reducing noise and token cost.

```python
import subprocess

def get_pr_diff(base: str = "origin/main") -> str:
    return subprocess.check_output(
        ["git", "diff", f"{base}...HEAD"],
        text=True,
    )

diff = get_pr_diff()
result = review_code(diff, language="python", focus=["bugs", "security"])

# Block the pipeline on critical/high
blockers = [i for i in result.issues if i.severity in ("critical", "high")]
if blockers:
    for b in blockers:
        print(f"BLOCKING [{b.severity.upper()}] Line {b.line}: {b.description}")
    raise SystemExit(1)

print(f"✅ Review passed — score {result.score}/100")
```

## Batch Review (Multiple Files)

```python
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def review_file(path: Path) -> tuple[str, ReviewResult]:
    code = path.read_text(encoding="utf-8")
    suffix_map = {".py": "python", ".ts": "typescript", ".js": "javascript"}
    lang = suffix_map.get(path.suffix, "python")
    return str(path), review_code(code, language=lang)

files = list(Path("src").rglob("*.py"))

with ThreadPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(review_file, f): f for f in files}
    for fut in as_completed(futures):
        path, result = fut.result()
        critical_count = sum(1 for i in result.issues if i.severity == "critical")
        print(f"{path}  score={result.score}  critical={critical_count}")
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

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - run: pip install anthropic

      - name: Run AI review on diff
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          git diff origin/main...HEAD > diff.patch
          python scripts/ai_review.py diff.patch

      # Post findings as PR review comments (optional)
      - name: Annotate PR
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            if (!fs.existsSync('review-output.json')) return;
            const findings = JSON.parse(fs.readFileSync('review-output.json'));
            for (const f of findings.filter(x => x.severity === 'critical')) {
              await github.rest.pulls.createReviewComment({
                owner: context.repo.owner, repo: context.repo.repo,
                pull_number: context.payload.pull_request.number,
                body: `**[CRITICAL]** ${f.description}\n\n> Fix: ${f.suggestion}`,
                path: f.file, line: parseInt(f.line),
                commit_id: context.payload.pull_request.head.sha,
              });
            }
```

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| False positives on style | Model too strict | Tune `focus` list; pass `# noqa`-annotated lines in context |
| Misses context-specific bugs | No project knowledge | Pass `ARCHITECTURE.md` snippet as `context` param |
| JSON parse error | Model wraps in markdown | `_strip_json_fence()` handles this; add regex fallback |
| Slow on large files | Full file in context | Use diff-mode: send only changed hunks |
| Duplicate findings | Same issue in multiple related lines | Deduplicate by `(category, line)` tuple before surfacing |
| Severity inflation | Model flags everything critical | Add a post-processing calibration: cap `critical` to genuine exploitability |

## Related Skills

- [`code-generation.md`](code-generation.md) — Write new code
- [`debugging.md`](debugging.md) — Find and fix bugs interactively
- [`security-scanning.md`](security-scanning.md) — Deep CVE and SAST analysis
- [`dependency-auditor.md`](dependency-auditor.md) — Verify dependencies execute cleanly

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-05 | Initial entry |
| v2 | 2026-04 | Structured JSON output, CI/CD example, severity scoring |
| v3 | 2026-04 | Diff-mode, batch review, inline PR comment workflow, fixed broken link to `debugging.md`, added `dependencies` block |
