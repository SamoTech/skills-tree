---
title: "Code Generation"
category: 05-code
level: intermediate
stability: stable
added: "2025-03"
updated: "2026-04"
version: v3
description: "Generate runnable code from a natural-language spec, optional context (existing files), and optional tests. Validate with a quick AST + import check before returning so the caller never receives obviously broken code."
tags: [code, generation, llm, validation]
dependencies:
  - package: anthropic
    min_version: "0.39.0"
    tested_version: "0.39.0"
    confidence: verified
code_blocks:
  - id: "example-code-generation"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-code-generation.json)

# Code Generation

## Description

Code generation takes a **natural-language specification** plus optional context (existing files, type signatures, failing tests) and returns runnable source code. It's the most-used LLM capability outside chat.

The naive prompt — "write a function that does X" — works for trivial scripts but loses on three things at scale: (1) it produces code that doesn't compile or import; (2) it loses pre-existing project conventions; (3) it can't tell when it's *wrong*. This skill is the production-grade version: structured spec → grounded prompt with relevant context → AST/import validation → optional self-repair before returning.

## When to Use

- You have a clear, **scoped** spec (a single function, an endpoint, a CLI flag) — not "build me an app".
- You can supply **context**: type signatures, docstrings, a few neighbouring files, or failing tests.
- You want the result to **compile**: rejecting obviously-broken output is cheaper than letting the agent run it.
- **Don't use** when: the user wants you to design the architecture (use [Algorithm Design](algorithm-design.md) first), or when you need to modify many files (use [Refactoring](refactoring.md)).

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `spec` | `str` | Natural-language description of what to write |
| `language` | `str` | `"python"`, `"typescript"`, etc. |
| `context_files` | `list[str]` | Paths whose contents to inline as grounding |
| `target_path` | `str` | Where the generated file would live (informs imports) |
| `max_repair_attempts` | `int` | Retries on syntax/import failure (default 2) |
| → `code` | `str` | Validated source |
| → `path` | `str` | Same as `target_path` |
| → `validations` | `list[str]` | Checks that passed (`"syntax"`, `"imports"`) |

## Runnable Example

```python
# pip install anthropic
from __future__ import annotations
import ast
import importlib
from dataclasses import dataclass
from pathlib import Path
import anthropic

client = anthropic.Anthropic()
MODEL = "claude-opus-4-5"

@dataclass
class GenResult:
    code: str
    path: str
    validations: list[str]

SYSTEM = (
    "You are a senior {language} engineer. Output ONLY the file contents — "
    "no markdown fences, no commentary, no leading/trailing prose. The code "
    "must be syntactically valid and import-clean."
)

def _build_prompt(spec: str, context_files: list[str], target_path: str) -> str:
    parts = [f"Target file: `{target_path}`", "", "Spec:", spec]
    for path in context_files:
        text = Path(path).read_text(encoding="utf-8")
        parts += ["", f"--- {path} ---", text]
    return "\n".join(parts)

def _strip_fences(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        # Remove leading ```language\n and trailing ```
        s = s.split("\n", 1)[1] if "\n" in s else ""
        if s.endswith("```"):
            s = s[: -3]
    return s.rstrip() + "\n"

def _validate_python(code: str) -> list[str]:
    """Quick local validation. Returns checks passed; raises on failure."""
    ok: list[str] = []
    ast.parse(code)  # SyntaxError on failure
    ok.append("syntax")
    # Top-level imports must resolve. We DON'T execute the module — only check
    # that the imported package names are importable in the current env.
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                importlib.import_module(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            importlib.import_module(node.module.split(".")[0])
    ok.append("imports")
    return ok

def generate_code(
    spec: str,
    *,
    language: str = "python",
    context_files: list[str] | None = None,
    target_path: str = "out.py",
    max_repair_attempts: int = 2,
) -> GenResult:
    context_files = context_files or []
    prompt = _build_prompt(spec, context_files, target_path)
    last_err: Exception | None = None
    for attempt in range(max_repair_attempts + 1):
        r = client.messages.create(
            model=MODEL, max_tokens=2048, temperature=0.0,
            system=SYSTEM.format(language=language),
            messages=[{"role": "user", "content": prompt}],
        )
        code = _strip_fences(r.content[0].text)
        try:
            checks = _validate_python(code) if language == "python" else ["syntax-skipped"]
            return GenResult(code=code, path=target_path, validations=checks)
        except (SyntaxError, ModuleNotFoundError) as exc:
            last_err = exc
            prompt = (
                f"{prompt}\n\n--- previous attempt failed validation ---\n"
                f"Error: {exc}\nReturn corrected file contents only."
            )
    raise RuntimeError(f"code-generation failed after {max_repair_attempts + 1} attempts: {last_err}")

if __name__ == "__main__":
    out = generate_code(
        spec="A pure function `slugify(s: str) -> str` that lowercases, strips, "
             "and replaces non-alphanumeric runs with single hyphens.",
        target_path="slugify.py",
    )
    print(out.code)
    print("validations:", out.validations)
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Markdown fences leak into the file | Model wrapped output in ```` ```python ... ``` ```` | Strip fences (above); add to system prompt: "no markdown" |
| Import of a missing package | Hallucinated dependency | Validate imports; reject + repair; pin dependency list in prompt |
| Generates a NEW file when caller expected an EDIT | Spec didn't say "edit" | Pass the existing file as context AND say "modify in place; return full file" |
| Drops existing functions | Free-form rewrite | Use diff/patch protocol or explicit "preserve all unchanged code" rule |
| Indentation mixes tabs + spaces | Non-determinism at temp>0 | `temperature=0.0` for code; lint after generation |
| Loops on repair (same error each time) | Spec is genuinely ambiguous | Cap retries; surface failure to caller; ask the user |

## Variants

| Variant | When |
|---|---|
| **Spec → file** (above) | New file from scratch |
| **Spec → edit** | Modify existing file; pass it as context; ask for full file back |
| **Tests → impl (TDD)** | Tests are the spec; loop until they pass |
| **Type-driven** | Pass type signatures only; let the model fill bodies |
| **Diff/patch protocol** | For multi-file edits; return unified diffs |

## Frameworks & Models

| Framework | Notes |
|---|---|
| Direct API (above) | Maximum control; ~80 lines |
| Aider | Repo-aware diff/patch protocol with git integration |
| Claude Code / Cursor | IDE-integrated; context-aware via the editor |
| GitHub Copilot Workspaces | PR-level codegen with task spec |

## Model Comparison

| Capability | claude-opus-4-5 | gpt-4o | claude-haiku-4-5 |
|---|---|---|---|
| Single-function correctness | 5 | 5 | 4 |
| Multi-file edits | 5 | 4 | 3 |
| Following project conventions | 5 | 4 | 4 |
| Strict format adherence | 5 | 4 | 5 |
| Cost-per-task | 2 | 3 | 5 |

## Related Skills

- [Bug Fixing](bug-fixing.md) — repair generated or human code
- [Code Review](code-review.md) — automated critique of the result
- [Algorithm Design](algorithm-design.md) — picks the strategy before generation
- [Function Calling](../07-tool-use/function-calling.md) — when generation must invoke tools

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Stub |
| 2026-04 | v3 | Battle-tested: validated AST + imports, self-repair loop, fence stripping, model comparison |
