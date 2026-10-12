---
name: env-file-parsing
description: Parse KEY=VALUE environment files into explicit settings with malformed-line and duplicate-key reporting so misconfiguration surfaces at load time instead of at first use.
metadata:
  source: skills/01-perception/env-file-parsing.md
  category: 01-perception
  version: "v1"
---

# Env File Parsing

Category: Perception | Level: basic | Stability: experimental | Version: v1

## Description

Environment files are a common configuration interface, and they fail quietly: a missing separator, a duplicated key, or an unmatched quote produces a wrong setting long before anyone reads the file back. This skill defines a deterministic parse contract that separates valid settings from reported problems, and it treats quoted values, comments, and blank lines explicitly. It covers parsing only; it does not cover secret storage, rotation, or runtime override precedence.

## When to Use

Use when a service or job loads settings from a dotenv-style file and the failure mode is a misread value discovered late.

Do not use for resolving runtime environment variables or managing secret storage; use the dedicated skills for those boundaries.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `env_text` | `string` | Yes | Raw file contents preserving every line, including comments |
| `required_keys` | `list` | No | Keys that must be present for the load to succeed |
| `value_types` | `object` | No | Per-key coercion such as int or bool applied after parsing |
| `strict` | `boolean` | No | When true, duplicate keys fail the load instead of being reported |

## Procedure

1. Read the file as text and preserve line numbers; do not trim or rewrite the raw input before parsing.
2. Skip blank lines and lines whose first non-space character is a hash; record them as ignored, not as errors.
3. Split each remaining line on the first equals sign; a line without a separator is a malformed entry, not a parse-stopping exception.
4. Validate the key shape and strip one layer of matching surrounding quotes from the value.
5. Detect duplicate keys and record whether the last value wins or the load fails under the declared strictness.
6. Apply the declared per-key type coercion and record coercion failures alongside malformed entries.
7. Return the parsed settings together with the problem list, including line number, kind, and raw line; never return a silent partial result.
8. Fail the load when strict mode is on or when a required key is missing; otherwise surface every problem at load time.

## Outputs

| Output | Type | Description |
|---|---|---|
| `settings` | `object` | Valid key-to-value map after coercion |
| `problems` | `list` | Malformed, duplicate, and coercion failures with line numbers |
| `missing_required` | `list` | Declared required keys absent from the file |
| `ignored_lines` | `list` | Comment and blank line numbers skipped during parsing |

## Runnable Example

```python
def parse_env_file(text):
    """Parse KEY=VALUE lines and report malformed or duplicate entries."""
    settings = {}
    problems = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            problems.append((lineno, "missing '=' separator", line))
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if not key or not key.replace("_", "x").isidentifier():
            problems.append((lineno, "invalid key", key))
            continue
        if key in settings:
            problems.append((lineno, "duplicate key overwritten", key))
        settings[key] = value
    return settings, problems

sample = """HOST=localhost
PORT = 8080
# comment
BROKEN LINE
PORT=9090
"""
settings, problems = parse_env_file(sample)
print(settings)
print(problems)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Missing separator | A line has no equals sign | Record as malformed; never guess a separator |
| Duplicate key | The same key appears twice | Report duplicates and fail the load under strict mode |
| Quote mismatch | An opening quote has no closing partner | Strip only matched pairs and report unmatched quotes |
| Coercion failure | A non-numeric value sits where an integer was declared | Coerce during parsing and record the failure with its line |
| Required key absent | The file parses but is incomplete | Compare against required_keys and fail the load |

## Security and Authority Boundary

Parsing a configuration file grants no execution authority. Values from environment files are untrusted input: they must be validated before use and must never be evaluated as code. Sensitive values parsed from such files flow only into the runtime’s declared secret storage, and the problem report must never echo those values.

## Evidence

This skill is grounded in dated public implementation references:

1. The twelve-factor app guidance on configuration (https://12factor.net/config).
2. Python’s configparser module documentation (https://docs.python.org/3/library/configparser.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Structured Data Reading](structured-data-reading.md) — parses structured inputs into typed records; this skill applies that discipline to KEY=VALUE files.
- [Log Parsing](log-parsing.md) — reports malformed lines with line numbers the same way.
- [Env Vars](../04-action-execution/env-vars.md) — consumes resolved environment variables; this skill only parses the file form.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
