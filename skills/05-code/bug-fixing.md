---
title: "Bug Fixing"
category: 05-code
level: intermediate
stability: stable
added: "2025-03"
updated: "2026-04"
version: v3
description: "Take a failing test or stack trace and produce a minimal patch that makes the test pass. Loops on test execution until green or budget exhausted, with each retry conditioned on the new failure output."
tags: [code, debugging, repair, testing, agentic-loop]
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
code_blocks:
  - id: "example-bug-fixing"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-bug-fixing.json)

# Bug Fixing

## Description

Bug fixing is **an agentic loop**, not a one-shot prompt. Given a repo, a failing test (or a stack trace + reproducer), the agent: (1) reads the failing code + relevant context, (2) proposes a minimal patch, (3) applies it, (4) re-runs the test, (5) repeats until green or the iteration budget is exhausted.

The naive "ask for a fix" prompt fails on three things: it doesn't see the *actual* failure output, it patches sites that aren't the bug, and it gives up after one wrong attempt. This skill encodes the loop with hard guardrails — read-only test runner, max iterations, minimal-diff bias — that get you from broken to green without burning the repo down.

## When to Use

- You have a **deterministic reproducer**: a failing test, a script that crashes, a CI log with a stack trace.
- You can run the reproducer in a **sandbox** (subprocess, container) — never on production.
- The fix is **localised** (a few files at most). For "the architecture is wrong", the loop will spin.
- **Don't use** when: you don't know what's broken (use [Debugging](debugging.md) first to localise), the bug is environmental (config, infra, deps), or the test itself is wrong.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `repo_root` | `str` | Path to the working directory |
| `failing_command` | `str` | Shell command that exits non-zero on the bug (e.g. `pytest tests/test_foo.py::test_bar`) |
| `relevant_files` | `list[str]` | Paths to read into context (None → agent picks) |
| `max_iterations` | `int` | Loop budget (default 4) |
| → `success` | `bool` | Did the failing command exit 0? |
| → `patches` | `list[str]` | Diffs applied per iteration |
| → `final_output` | `str` | stdout/stderr of the last run |

## Runnable Example

```python
# pip install anthropic
from __future__ import annotations
import subprocess
from dataclasses import dataclass
from pathlib import Path
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

@dataclass
class FixResult:
    success: bool
    patches: list[str]
    final_output: str

SYSTEM = (
    "You are a senior engineer fixing a failing test. Output ONLY a unified "
    "diff (one or more `--- a/path\\n+++ b/path` blocks). No prose, no "
    "explanation. Make the smallest change that fixes the failure. Do NOT "
    "modify the test file unless the test is provably wrong."
)

def _run(cmd: str, cwd: str) -> tuple[int, str]:
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=120)
    return p.returncode, (p.stdout + p.stderr)[-4000:]  # tail to fit in context

def _read_file(repo: Path, rel: str) -> str:
    return (repo / rel).read_text(encoding="utf-8")

def _apply_patch(repo: Path, diff: str) -> None:
    # Trust the unified-diff format and let `patch` do the work in --batch mode.
    subprocess.run(
        ["patch", "-p1", "--batch", "--silent"],
        input=diff, text=True, cwd=str(repo), check=True,
    )

def fix_bug(
    repo_root: str,
    failing_command: str,
    *,
    relevant_files: list[str] | None = None,
    max_iterations: int = 4,
) -> FixResult:
    repo = Path(repo_root).resolve()
    relevant_files = relevant_files or []
    patches: list[str] = []

    rc, output = _run(failing_command, str(repo))
    if rc == 0:
        return FixResult(True, patches, output)

    for _ in range(max_iterations):
        ctx = "\n".join(
            f"--- {f} ---\n{_read_file(repo, f)}" for f in relevant_files
        )
        prompt = (
            f"Failing command: {failing_command}\n\n"
            f"Output (tail):\n{output}\n\n"
            f"Files:\n{ctx}\n\n"
            "Return a unified diff that fixes the failure."
        )
        r = client.messages.create(
            model=MODEL, max_tokens=2048, temperature=0.0,
            system=SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        diff = r.content[0].text.strip()
        try:
            _apply_patch(repo, diff)
        except subprocess.CalledProcessError as exc:
            output = f"patch failed to apply: {exc}\n{output}"
            continue
        patches.append(diff)
        rc, output = _run(failing_command, str(repo))
        if rc == 0:
            return FixResult(True, patches, output)

    return FixResult(False, patches, output)

if __name__ == "__main__":
    # Toy demo: write a buggy file + a failing test, then fix it.
    repo = Path("/tmp/bugfix-demo")
    repo.mkdir(exist_ok=True)
    (repo / "calc.py").write_text("def add(a, b):\n    return a - b  # bug\n")
    (repo / "test_calc.py").write_text(
        "from calc import add\ndef test_add(): assert add(2, 3) == 5\n"
    )
    out = fix_bug(
        str(repo), "python3 -m pytest test_calc.py -q",
        relevant_files=["calc.py"], max_iterations=2,
    )
    print("success:", out.success)
    print("patches:", len(out.patches))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Patch applies, test still fails | Wrong file edited, or partial fix | Loop again with new failure output; cap iterations |
| Patch fails to apply | Non-existent line numbers, model hallucinated context | Validate diff hunks against current file; reject malformed |
| Agent edits the test to pass | "Make test pass" interpreted literally | System prompt forbids test edits; diff-allow-list for paths |
| Spinning on flaky test | Test is non-deterministic, not a bug | Run failing command N times before declaring green; flag flakes |
| Catastrophic regression | Fix broke other tests | Run full suite at the end; rollback patches if regression |
| Timeout | Failing command hangs | Hard subprocess timeout (120s above); kill on exceed |

## Variants

| Variant | When |
|---|---|
| **Diff/patch loop** (above) | Default; smallest blast radius |
| **Whole-file rewrite** | Single file; simpler than diff parsing |
| **SWE-Agent style** | Multi-file repos; agent navigates, edits, runs |
| **Verifier-guided** | A second model reviews each candidate diff before apply |
| **Retrieval-augmented** | Pull similar past bugs/fixes from a corpus to ground the agent |

## Frameworks & Models

| Framework | Notes |
|---|---|
| Direct API loop (above) | Maximum control |
| Aider | Repo-aware, git-integrated |
| OpenHands / SWE-Agent | Production agentic IDE for repo work |
| Claude Code / Cursor | Editor-integrated single-file repair |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | claude-haiku-4-5 |
|---|---|---|---|
| Localising the bug | 5 | 4 | 4 |
| Minimal-diff discipline | 5 | 4 | 4 |
| Multi-file fixes | 5 | 4 | 3 |
| Cost-per-iteration | 2 | 3 | 5 |

## Related Skills

- [Debugging](debugging.md) — localise the bug before patching
- [Code Generation](code-generation.md) — same loop pattern, different goal
- [Code Review](code-review.md) — verifier-guided variant
- [Reflection](../09-agentic-patterns/reflection.md) — generic critique-revise pattern

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Stub |
| 2026-04 | v3 | Battle-tested: diff-patch loop, sandboxed test runner, iteration cap, failure modes, model comparison |
