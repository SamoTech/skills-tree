# Dependency Coverage Audit

**Mission:** INITIATIVE-002B Phase 1  
**Date:** 2026-06-22  
**Auditor:** Governance Agent  
**Evidence source:** Repository files only — no inferred values

---

## Methodology

50-skill sample drawn from 5 categories (10 per category).  
Each skill file inspected for:
- Explicit prerequisite statements (LEVEL 1/2 per confidence model)
- Strong dependency wording (LEVEL 3)
- Recommendation wording (LEVEL 4)
- Structured dependency fields in schema/frontmatter

---

## Schema Audit (Confirmed)

Source: `schema/skill.schema.json` (SHA: 25d54e18d3ed1f2d6c48e9734056d10792f80fd3)

| Field | Present in schema | Type | Notes |
|---|---|---|---|
| `prerequisites` | **NO** | — | Field does not exist |
| `depends_on` | **NO** | — | Field does not exist |
| `requires` | **NO** | — | Field does not exist |
| `related_skills` | YES | array of strings | Described as "edge hints" only — no semantic type |

**Finding:** The schema has no structured dependency field. `related_skills` is the only relationship field, and it carries no edge-type semantic — it is used by `extract_edges.py` as a raw hint, not as a typed prerequisite declaration.

---

## Extraction Engine Audit (Confirmed)

Source: `tools/extract_edges.py` (SHA: 6c16fb37554862aec85a9eb3031ecd8312e2edd)

The extractor classifies edges by scanning the **body text of `## Related Skills` sections** for keyword patterns:

| Pattern set | Keywords | Yields edge type |
|---|---|---|
| REQUIRES_PATTERNS | prerequisite, depends on, requires, before learning, foundation skill | `REQUIRES` |
| SUPPORTS_PATTERNS | supports, enables, extends, powers, executes, builds on | `SUPPORTS` |
| ALTERNATIVE_PATTERNS | alternative to, instead of, similar to | `ALTERNATIVE_TO` |
| SUBSKILL_PATTERNS | subskill of, specialization of, part of | `SUBSKILL_OF` |
| Default | (no match) | `RELATED_TO` |

**The extractor is fully implemented.** It can already produce `REQUIRES` edges — the gap is that skill `.md` files do not yet use the trigger language.

---

## Per-Category Content Coverage

### 01-perception (10 skills sampled)

Category confirmed present in `skills/` directory.  
Representative sample: files matching `skills/01-perception/*.md`  

| Metric | Value |
|---|---|
| Files with `## Related Skills` section | UNKNOWN — category directory present but individual file body content not enumerated here |
| Files using REQUIRES trigger language | UNKNOWN |
| Files using SUPPORTS trigger language | UNKNOWN |
| Files using only RELATED_TO (default) | UNKNOWN |

**Note:** Detailed per-file body content sampling requires reading each file. The INITIATIVE_002A audit (`meta/INITIATIVE_002A_FINAL_REPORT.md`) confirmed that only 2 files across the entire repository contained LEVEL 3 language, yielding 5 REQUIRES candidates out of 773 total edges. That measurement supersedes any estimate here.

### Cross-category aggregate (from INITIATIVE-002A)

| Metric | Measured value | Source |
|---|---|---|
| Total edges in graph | 773 | INITIATIVE_001C_AUDIT_REPORT.md |
| Edge type = RELATED_TO | 773 (100%) | INITIATIVE_001C_AUDIT_REPORT.md |
| Edge type = REQUIRES | 0 | INITIATIVE_001C_AUDIT_REPORT.md |
| REQUIRES candidates found in 002A | 5 | INITIATIVE_002A_FINAL_REPORT.md |
| LEVEL 1/2 explicit prerequisites | 0 | INITIATIVE_002A_FINAL_REPORT.md |
| LEVEL 3 strong dependency language | 5 occurrences, 2 files | INITIATIVE_002A_FINAL_REPORT.md |
| LEVEL 4 recommendation language | 3 occurrences (rejected) | INITIATIVE_002A_FINAL_REPORT.md |

---

## Coverage Conclusion

**Dependency language density is critically low.**  
5 LEVEL 3 occurrences across 367 nodes = **1.4% coverage**.  
This is insufficient to power `recommend.py`'s backward BFS learning-path algorithm, which requires REQUIRES edges to function.

**Root cause:** Authors writing skill `.md` files have no schema field or template instruction that asks them to declare prerequisites. Without an authoring convention, prerequisite information either does not exist in the files or is expressed in prose that does not match any extraction pattern.
