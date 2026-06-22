# Dependency Schema Specification

**Mission:** INITIATIVE-003 Phase 1  
**Date:** 2026-06-22  
**Status:** APPROVED — implemented in `schema/skill.schema.json` v3.1

---

## Problem Statement

From `meta/INITIATIVE_002B_AUTHORING_MODEL_AUDIT.md`:

- `schema/skill.schema.json` uses `additionalProperties: false`
- No `prerequisites` field existed prior to this initiative
- `extract_edges.py` docstring references a `dependencies` frontmatter field that never existed
- Any author attempting to declare prerequisites would fail schema validation

---

## Field Design

### Field name: `prerequisites`

| Property | Value | Rationale |
|---|---|---|
| Field name | `prerequisites` | Matches natural language; aligns with `extract_edges.py` REQUIRES_PATTERNS keyword |
| Type | `array` of `string` | Supports multiple prerequisites per skill |
| Required | **No** (optional) | Non-breaking — all 367 existing skills omit it without error |
| Item type | `string` | Canonical skill ID format |
| Item pattern | `^[0-9]{2}-[a-z][a-z0-9-]*/[a-z][a-z0-9-]*$` | Enforces canonical `category/slug` format |
| Item minLength | `1` | Rejects empty strings |
| uniqueItems | `true` | No duplicate prerequisites |
| minItems | `1` | If the field is present, it must contain at least one entry |
| additionalProperties | N/A | Field added to existing `additionalProperties: false` object |

### Semantic meaning

A `prerequisites` entry declares: *"This skill cannot be effectively learned without first understanding the referenced skill."*

This maps to edge type `REQUIRES` in `schema/edge.schema.json`.

---

## Frontmatter Example

```yaml
---
id: 09-agentic-patterns/plan-and-execute
title: Plan-and-Execute Pattern
category: 09-agentic-patterns
level: advanced
stability: stable
version: v2
prerequisites:
  - 02-reasoning/planning-decomposition
  - 09-agentic-patterns/goal-decomposition
---
```

This declares two REQUIRES edges:
- `09-agentic-patterns/plan-and-execute` → REQUIRES → `02-reasoning/planning-decomposition`
- `09-agentic-patterns/plan-and-execute` → REQUIRES → `09-agentic-patterns/goal-decomposition`

---

## Compatibility

| Check | Result |
|---|---|
| Existing 367 skills without `prerequisites` field | ✅ PASS — field is optional |
| New skills with `prerequisites: []` | ❌ FAIL — `minItems: 1` rejects empty array; omit field instead |
| New skills with duplicate entries | ❌ FAIL — `uniqueItems: true` |
| New skills with malformed ID (e.g. `causal`) | ❌ FAIL — pattern requires `category/slug` format |
| New skills with valid prerequisites | ✅ PASS |

---

## Schema Version

Prior: `3.0` (in `build_graph.py` `SCHEMA_VERSION` constant)  
After: **`3.1`** — minor version bump (additive, non-breaking change)  

Note: `SCHEMA_VERSION = "3.0"` in `tools/build_graph.py` must be updated to `"3.1"` in INITIATIVE-004 when `build_graph.py` is updated to consume the `prerequisites` field.
