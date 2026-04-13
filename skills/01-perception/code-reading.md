![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-code-reading.json)

# Code Reading

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Parse, understand, and extract meaning from source code files or snippets. Covers identifying intent, extracting function signatures and docstrings, detecting dependencies, summarizing modules, spotting bugs or anti-patterns, and explaining logic in plain language. Works across all major languages: Python, JavaScript/TypeScript, Go, Rust, Java, C/C++, SQL, and shell scripts.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `source` | `string` | ✅ | Raw source code or file path |
| `language` | `string` | ❌ | Language hint (auto-detected if omitted) |
| `task` | `string` | ❌ | `summarize`, `extract_signatures`, `find_bugs`, `explain` |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `purpose` | `string` | One-sentence description of file intent |
| `functions` | `list` | `[{name, params, return_type, summary}]` |
| `imports` | `list` | External dependencies detected |
| `issues` | `list` | Potential bugs or code smells |

---

## Example

```python
import anthropic
from pathlib import Path

client = anthropic.Anthropic()

def analyze_code_file(file_path: str) -> str:
    """Extract structured metadata from a source code file."""
    source = Path(file_path).read_text(encoding="utf-8")
    language = Path(file_path).suffix.lstrip(".")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": (
                f"Analyze this {language} file and return JSON with:\n"
                "- language\n"
                "- purpose: one-sentence description\n"
                "- functions: [{name, params, return_type, summary}]\n"
                "- classes: [{name, methods, summary}]\n"
                "- imports: list of external dependencies\n"
                "- issues: list of potential bugs or code smells\n"
                "Return ONLY valid JSON.\n\n"
                f"```{language}\n{source[:8000]}\n```"
            )
        }]
    )
    return response.content[0].text

result = analyze_code_file("src/utils.py")
print(result)
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Direct text prompt with fenced code block | 2024-06 |
| GPT-4o | Same pattern via OpenAI SDK | 2024-05 |
| LangChain | `ChatAnthropic` chain | v0.2 |

---

## Notes

- Chunk files larger than ~800 lines before sending; use sliding window for context continuity
- For multi-file analysis, send a directory tree first then individual files
- Combine with [Structured Data Reading](structured-data-reading.md) to process `package.json`, `pyproject.toml`, etc.

---

## Related Skills

- [Text Reading](text-reading.md) — general text extraction
- [Structured Data Reading](structured-data-reading.md) — config file parsing
- [Document Parsing](document-parsing.md) — for code in PDFs or docs
- [File System Reading](file-system-reading.md) — discovering files to read

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, runnable example, notes |
| `2025-03` | Initial stub entry |
