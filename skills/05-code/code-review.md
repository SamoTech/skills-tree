---
title: "Code Review"
category: 05-code
level: intermediate
stability: stable
added: "2026-09"
updated: "2026-10"
version: v2
description: "Review a code change for correctness, security, maintainability, tests, and repository conventions; return evidence-backed findings with severity and file/line anchors. Activate when the task is to review, critique, or assess source code quality—not when the task is only to explain review theory without inspecting code."
tags: [code, review, security, maintainability, pr-review, quality]
related: [security-scanning, code-generation, unit-test-generation, debugging]
---

# Code Review

## Description

Code review inspects a concrete code change (diff, PR, or file set) and reports **evidence-backed findings**: what is wrong or risky, why, where (file/line), and how severe it is. It is not a vague opinion and not a rewrite of the code unless the task explicitly asks for fixes.

Activate this skill when the user asks to **review**, **critique**, **assess**, or **find issues in** source code. Prefer this skill over web search or RAG when the subject is the code itself.

## When to Use

- A pull request, diff, or set of source files must be reviewed for correctness, security, or maintainability.
- The task names acceptance criteria, coding standards, or test expectations to check against.
- The user wants a structured findings list before merge or ship.

**Do not use** when:
- The user only wants an explanation of *how* code review works, with **no code to inspect** (answer conceptually; do not pretend to review).
- The task is pure code generation with no review request (use [Code Generation](code-generation.md)).
- The need is open-web research (use [Web Search](../11-web/web-search.md)) or private-corpus Q&A (use [RAG](../03-memory/rag.md)).

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `diff_or_files` | `str` / `list[File]` | Unified diff, PR patch, or file contents under review |
| `acceptance_criteria` | `list[str]` | Optional explicit requirements or standards |
| `security_policy` | `object` | Optional constraints (no secrets, no privilege escalation, etc.) |
| → `findings` | `list[Finding]` | Ordered by severity |
| → `findings[i].severity` | `critical\|high\|medium\|low\|info` | Impact if unfixed |
| → `findings[i].location` | `str` | `path:line` or range |
| → `findings[i].evidence` | `str` | Quote or concrete observation from the code |
| → `findings[i].recommendation` | `str` | Actionable fix direction |
| → `summary` | `str` | Short overall assessment |
| → `block_merge` | `bool` | True if any critical/high unresolved finding |

## Review Procedure

1. Establish scope: which files/hunks are in the change; ignore unrelated code.
2. Check **correctness** against stated requirements or obvious invariants.
3. Check **security**: injection, authz, secrets, unsafe deserialization, path traversal.
4. Check **tests**: new behavior covered; existing tests not deleted without cause.
5. Check **maintainability**: naming, complexity, dead code, API contracts.
6. Check **repository conventions** and existing gates (lint, types, CI).
7. Emit findings with severity + location + evidence; do not invent issues not grounded in the diff.
8. Set `block_merge` only for critical/high issues or policy violations.

## Runnable Example

```python
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Finding:
    severity: str
    location: str
    evidence: str
    recommendation: str

def review_diff(diff_text: str, acceptance: list[str] | None = None) -> dict:
    """Minimal checklist-style review over a unified diff string."""
    findings: list[Finding] = []
    lines = diff_text.splitlines()

    for i, line in enumerate(lines):
        if line.startswith("+") and not line.startswith("+++"):
            body = line[1:]
            lowered = body.lower()
            if "hardcoded_token" in lowered or ("password" + " = ") in lowered:
                findings.append(Finding(
                    severity="critical",
                    location=f"diff:{i+1}",
                    evidence=body.strip()[:120],
                    recommendation="Remove hardcoded credentials; use env or a secret manager.",
                ))
            if "todo: fix later" in lowered and acceptance:
                findings.append(Finding(
                    severity="medium",
                    location=f"diff:{i+1}",
                    evidence=body.strip()[:120],
                    recommendation="Resolve or ticket TODOs that affect acceptance criteria before merge.",
                ))

    if acceptance and not any("test" in l.lower() for l in lines if l.startswith("+")):
        findings.append(Finding(
            severity="high",
            location="diff:global",
            evidence="No test-related additions detected in diff",
            recommendation="Add or update tests for the new behavior.",
        ))

    severity_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    findings.sort(key=lambda f: severity_rank.get(f.severity, 9))
    block = any(f.severity in ("critical", "high") for f in findings)
    return {
        "findings": findings,
        "summary": f"{len(findings)} finding(s); block_merge={block}",
        "block_merge": block,
    }

if __name__ == "__main__":
    sample = (
        "+++ b/app.py\n+"
        + "hardcoded_" + "token" + " = " + '"placeholder-not-a-real-secret"'
        + "\n+def refund(amount): return True\n"
    )
    out = review_diff(sample, acceptance=["refunds must be tested"])
    print(out["summary"])
    for f in out["findings"]:
        print(f.severity, f.location, f.recommendation)
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Invented bugs | Model guesses without reading the diff | Require every finding to quote evidence from the change |
| Scope creep | Reviewing files not in the PR | Limit to changed hunks unless asked for full-file review |
| Nitpick flood | Style noise hides real issues | Cap low/info; lead with critical/high |
| Missed secrets | Pattern not recognized | Run secret scanning; deny merge on credential literals |
| Rubber-stamp approve | No criteria, shallow pass | Walk correctness → security → tests → conventions explicitly |
| False "review" with no code | User asked how review works, not to review | Do not activate full review procedure; answer conceptually |
| Claiming merge-ready without tests | Tests absent or deleted | High severity finding; `block_merge=true` |

## Security Boundary

- Never recommend disabling security gates to make CI green.
- Flag secrets, unsafe `eval`, unrestricted deserialization, and authz bypasses as critical/high.
- Do not exfiltrate proprietary code beyond the review response channel.

## Related Skills

- [Security Scanning](security-scanning.md) — specialized secret/pattern detection in the code category
- [Secret Scanning](../14-security/secret-scanning.md) — security-category secret detection contract
- [Git Diff Reading](../01-perception/git-diff-reading.md) — parse and scope the change set
- [Unit Test Generation](unit-test-generation.md) — add tests for reviewed behavior
- [Debugging](debugging.md) — investigate failures found in review
- [Code Generation](code-generation.md) — implement fixes after review

## Evidence

Repository-backed guidance aligned with validation and security workflows. No external benchmark score is claimed for this skill version.

## Changelog

| Date | Version | Change |
|---|---|---|
| 2026-09 | v1 | Initial stub-level skill |
| 2026-10 | v2 | Activation-oriented rewrite: when/not-to-use, typed findings, procedure, runnable checklist, failure modes for selection reliability |
