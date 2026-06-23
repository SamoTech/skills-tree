# INITIATIVE-009D — Backfill Plan

**Date:** 2026-06-23  
**Approved edges:** 2  
**Scope:** YAML frontmatter `prerequisites:` additions only. No body edits.

---

## Edge 1: `bug-fixing` → `debugging`

**File:** `skills/05-code/bug-fixing.md`  
**Change:** Add `prerequisites:` block to frontmatter

```yaml
prerequisites:
  - 05-code/debugging
```

**Evidence:** "Don't use when: you don't know what's broken (use Debugging first to localise)"  
**Section:** When to Use  
**Confidence:** HIGH

---

## Edge 2: `code-generation` → `algorithm-design`

**File:** `skills/05-code/code-generation.md`  
**Change:** Add `prerequisites:` block to frontmatter

```yaml
prerequisites:
  - 05-code/algorithm-design
```

**Evidence:** "Don't use when: the user wants you to design the architecture (use Algorithm Design first)"  
**Section:** When to Use  
**Confidence:** HIGH

---

## Implementation

Both files will have `prerequisites:` inserted after existing frontmatter fields,  
before the closing `---`. No other changes to file body.
