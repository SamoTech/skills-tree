# AGENT DECISION FRAMEWORK

**Initiative:** INITIATIVE-010A  
**Created:** 2026-06-23  
**Status:** ACTIVE

---

## Decision Classification

All agent decisions are classified by impact level. The class determines required evidence, approval path, and rollback requirements.

| Class | Name | Definition |
|-------|------|----------|
| **D0** | Observation | Read-only analysis; no repository changes |
| **D1** | Refactor | Structural/cosmetic change; no behavioral impact |
| **D2** | Schema Change | Modification to schema files or field definitions |
| **D3** | Graph Change | Addition, removal, or modification of graph edges or nodes |
| **D4** | Governance Change | Amendment to PROJECT_CONSTITUTION.md or core governance files |
| **D5** | Breaking Change | Any change that invalidates existing data contracts or downstream consumers |

---

## Decision Details by Class

### D0 — Observation

| Field | Value |
|-------|-------|
| **Evidence required** | None — read-only |
| **Approval path** | Self-authorized (any agent) |
| **Rollback** | Not applicable |
| **Examples** | Reading MEMORY_STATE.md; running audit; generating report |

---

### D1 — Refactor

| Field | Value |
|-------|-------|
| **Evidence required** | Before/after diff showing no behavioral change |
| **Approval path** | Specialist Agent → Quality Auditor → Release Manager |
| **Rollback** | Git revert sufficient |
| **Examples** | Renaming a meta file; fixing a broken markdown link; reformatting a table |

---

### D2 — Schema Change

| Field | Value |
|-------|-------|
| **Evidence required** | Migration plan; impact analysis on existing skill files; test run on sample data |
| **Approval path** | Specialist Agent → Governance Officer → Quality Auditor → Release Manager |
| **Rollback** | Schema revert + data migration script required |
| **Examples** | Adding a new required field to skill schema; changing field type; deprecating a field |

---

### D3 — Graph Change

| Field | Value |
|-------|-------|
| **Evidence required** | Minimum 2 independent sources per edge; no speculation; pattern match to existing approved edges |
| **Approval path** | Dependency Auditor → Graph Architect (proposal) → Governance Officer (sign-off) → Release Manager (commit) |
| **Rollback** | Skill file revert + graph rebuild |
| **Examples** | Adding a `requires` prerequisite; removing a dangling edge; merging duplicate nodes |

**D3 Evidence Standards:**
- Source 1: Authoritative curriculum or certification body
- Source 2: Industry consensus (multiple job descriptions, course syllabi, or textbooks)
- Conditional edges ("sometimes requires") are REJECTED — only definitive prerequisites allowed
- "Related" relationships are NOT sufficient — must be demonstrated prerequisite dependency

---

### D4 — Governance Change

| Field | Value |
|-------|-------|
| **Evidence required** | Written rationale; gap analysis showing current constitution is insufficient; community impact assessment |
| **Approval path** | Governance Officer (primary author) → Program Director (co-sign) → Release Manager (commit) |
| **Rollback** | Constitution revert; all agents must re-load on next mission |
| **Examples** | Changing decision class thresholds; adding new governance checkpoints; modifying agent authority boundaries |

---

### D5 — Breaking Change

| Field | Value |
|-------|-------|
| **Evidence required** | Full impact audit of all downstream consumers; migration path for existing data; stakeholder notification plan |
| **Approval path** | Specialist Agent → Graph Architect (impact) → Governance Officer (approval) → Program Director (co-sign) → Release Manager (commit) |
| **Rollback** | Full branch backup required before execution; tested rollback procedure documented |
| **Examples** | Removing a required schema field; renaming node IDs used in the graph; changing the SKILLS_GRAPH.json format |

---

## Decision Log Format

All D1+ decisions must be logged in `meta/DECISION_LOG.md` using this format:

```markdown
## D-<ID>

**Date:** YYYY-MM-DD  
**Class:** D<N> — <Name>  
**Proposed by:** <agent name>  
**Approved by:** <agent name>  
**Initiative:** <initiative ID>  
**Description:** <one sentence>  
**Evidence:** <list evidence sources>  
**Impact:** <what changes>  
**Rollback:** <how to revert>  
```

---

## Quick Reference

| Class | Who can propose | Who approves | Rollback complexity |
|-------|----------------|-------------|--------------------|
| D0 | Any agent | Self | N/A |
| D1 | Any agent | Quality Auditor | Low (git revert) |
| D2 | Specialist Agent | Governance Officer | Medium (migration needed) |
| D3 | Dependency Auditor / Graph Architect | Governance Officer | Medium (file revert + rebuild) |
| D4 | Governance Officer | Program Director | High (constitution revert) |
| D5 | Specialist Agent | Governance Officer + Program Director | Critical (backup required) |

---

*All agents must internalize this framework before making any decision that modifies repository state.*
