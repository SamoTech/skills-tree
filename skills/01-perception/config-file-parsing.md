---
title: "Config File Parsing"
category: 01-perception
level: basic
stability: experimental
description: "Parse YAML, TOML, and INI configuration files into typed, validated structures with explicit defaults, unknown-key reporting, and provenance of every effective value."
added: "2026-10"
version: v1
related: ["env-file-parsing", "json-schema-validation"]
---

# Config File Parsing

Category: Perception | Level: basic | Stability: experimental | Version: v1

## Description

Configuration is where runtime truth comes from. A loader that silently invents defaults or ignores unknown keys turns typos into behavior, and a system that cannot say which file a setting came from cannot audit its own decisions. This skill treats a configuration file as data with a schema: parse it strictly, validate types, surface unknown keys, and record the provenance of every effective value.

## When to Use

Use whenever an agent or service loads settings from YAML, TOML, or INI files — application settings, tool configuration, pipeline definitions — and later decisions depend on those values.

Do not treat an unparsable file as empty configuration; a missing file and a broken file are different failures and must not collapse into a silent fall-back to defaults.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `file` | `path` | Yes | The configuration file to load |
| `format` | `enum` | Yes | yaml, toml, or ini, detected when not supplied |
| `schema` | `map` | No | Expected keys, types, and ranges for validation |
| `defaults` | `map` | No | Fallback values applied with recorded provenance |

## Procedure

1. Detect the format from the file extension and content before choosing a parser; refuse ambiguous input rather than guessing.
2. Parse with a strict parser that reports line numbers for syntax errors instead of attempting best-effort recovery.
3. Validate parsed values against the schema — required keys, types, ranges — and collect all violations before failing.
4. Report unknown keys rather than silently dropping them; an unknown key is either a typo or a schema that drifted from the config.
5. Merge defaults only for missing values and record, per key, whether it came from file, default, or environment override.
6. Emit the effective configuration together with its provenance map so later decisions can cite their settings.

## Outputs

| Output | Type | Description |
|---|---|---|
| `config` | `map` | The typed, validated effective configuration |
| `provenance` | `map` | The source recorded for each effective value |
| `violations` | `list` | Schema violations and unknown keys found during load |

## Runnable Example

```python
import configparser

def load_ini(path, defaults=None):
    parser = configparser.ConfigParser()
    if not parser.read(path):
        raise FileNotFoundError(f"config not found: {path}")
    config = {s: dict(parser[s]) for s in parser.sections()}
    provenance = {f"{s}.{k}": path for s, values in config.items() for k in values}
    expected = set(defaults or {})
    unknown = expected.symmetric_difference(set(parser.sections()))
    return {"config": config, "provenance": provenance, "unknown_sections": sorted(unknown)}

result = load_ini("app.ini", defaults={"cache", "database"})
print(sorted(result["config"]), result["unknown_sections"])
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Silent defaults | Unparsable file treated as empty config | Fail closed on parse errors |
| Unknown keys dropped | Schema drift or typos stay invisible | Report and list every unknown key |
| Type coercion surprises | Values parsed as strings regardless of intent | Validate against a typed schema |
| Duplicate keys | Last-wins parsing hides conflicts | Surface duplicate definitions at load time |
| Credentials in config | Credential-shaped values committed to files | Keep secrets in the environment or a secret store |

## Security and Authority Boundary

Configuration parsing reads files that often sit next to credentials. Parsed values must not be logged in full, and credential-shaped values found in a config file should be reported as a finding rather than passed through silently.

## Evidence

This skill is grounded in dated public implementation references:

1. The Python standard library configparser reference (https://docs.python.org/3/library/configparser.html).
2. The twelve-factor guidance on keeping config in the environment (https://12factor.net/config).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Env File Parsing](env-file-parsing.md) — the narrow KEY=VALUE loader this skill complements.
- [JSON Schema Validation](json-schema-validation.md) — schema validation applied to structured config formats.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
