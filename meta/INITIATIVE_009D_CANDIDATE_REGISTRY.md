# INITIATIVE-009D — Candidate Registry

**Date:** 2026-06-23  
**Source:** Priority A files in `skills/05-code/`

All quotes verbatim. No paraphrasing.

---

## CANDIDATE 009D-001

| Field | Value |
|-------|-------|
| **Source** | `skills/05-code/bug-fixing.md` |
| **Target** | `skills/05-code/debugging.md` |
| **Exact Quote** | "**Don't use** when: you don't know what's broken (use [Debugging](debugging.md) first to localise)" |
| **Section** | "When to Use" |
| **Qualifier** | "use X first" — explicit prerequisite ordering |
| **Confidence** | HIGH |

---

## CANDIDATE 009D-002

| Field | Value |
|-------|-------|
| **Source** | `skills/05-code/bug-fixing.md` |
| **Target** | `skills/05-code/debugging.md` |
| **Exact Quote** | "[Debugging](debugging.md) — localise the bug before patching" |
| **Section** | "Related Skills" |
| **Qualifier** | "before" — explicit temporal/sequential ordering |
| **Confidence** | HIGH |

**Note:** 009D-001 and 009D-002 both support the same edge (bug-fixing → debugging). 009D-001 is the primary evidence; 009D-002 corroborates.

---

## CANDIDATE 009D-003

| Field | Value |
|-------|-------|
| **Source** | `skills/05-code/code-generation.md` |
| **Target** | `skills/05-code/algorithm-design.md` |
| **Exact Quote** | "**Don't use** when: the user wants you to design the architecture (use [Algorithm Design](algorithm-design.md) first)" |
| **Section** | "When to Use" |
| **Qualifier** | "use X first" — explicit prerequisite ordering |
| **Confidence** | HIGH |

---

## CANDIDATE 009D-004

| Field | Value |
|-------|-------|
| **Source** | `skills/05-code/code-generation.md` |
| **Target** | `skills/05-code/algorithm-design.md` |
| **Exact Quote** | "[Algorithm Design](algorithm-design.md) — picks the strategy before generation" |
| **Section** | "Related Skills" |
| **Qualifier** | "before" — explicit temporal/sequential ordering |
| **Confidence** | HIGH |

**Note:** 009D-003 and 009D-004 both support the same edge (code-generation → algorithm-design). 009D-003 is the primary evidence; 009D-004 corroborates.

---

## CANDIDATE 009D-005

| Field | Value |
|-------|-------|
| **Source** | `skills/05-code/code-generation.md` |
| **Target** | `skills/05-code/refactoring.md` |
| **Exact Quote** | "**Don't use** when: …you need to modify many files (use [Refactoring](refactoring.md))" |
| **Section** | "When to Use" |
| **Qualifier** | "use X instead" — skill boundary / prerequisite routing |
| **Confidence** | MEDIUM — this is a routing rule ("use Refactoring instead"), not a strict prerequisite. Refactoring does not have to be learned before code-generation. |

---

## CANDIDATE 009D-006

| Field | Value |
|-------|-------|
| **Source** | `skills/05-code/code-generation.md` |
| **Target** | `skills/07-tool-use/function-calling.md` |
| **Exact Quote** | "[Function Calling](../07-tool-use/function-calling.md) — when generation must invoke tools" |
| **Section** | "Related Skills" |
| **Qualifier** | "when generation must invoke tools" — describes a functional dependency on function-calling when tools are needed |
| **Confidence** | MEDIUM — conditional dependency ("when"), not universal prerequisite |

---

## CANDIDATE 009D-007

| Field | Value |
|-------|-------|
| **Source** | `skills/05-code/dependency-auditor.md` |
| **Target** | `skills/05-code/code-execution-sandbox.md` |
| **Exact Quote** | "[`code-execution-sandbox.md`](code-execution-sandbox.md) — Isolated execution environments" |
| **Section** | "Related Skills" |
| **Qualifier** | The pipeline diagram shows: `dependency-auditor` sits at step 2 ("execution proof"). `code-execution-sandbox` describes the isolation environment the auditor **operates within**. |
| **Confidence** | MEDIUM — no explicit "requires" word, but the pipeline position and execution-layer description imply dependency |

---

## CANDIDATE 009D-008

| Field | Value |
|-------|-------|
| **Source** | `skills/05-code/bug-fixing.md` |
| **Target** | `skills/09-agentic-patterns/reflection.md` |
| **Exact Quote** | "[Reflection](../09-agentic-patterns/reflection.md) — generic critique-revise pattern" |
| **Section** | "Related Skills" |
| **Qualifier** | "generic critique-revise pattern" — describes reflection as the conceptual foundation the bug-fixing loop **instantiates** |
| **Confidence** | MEDIUM — no explicit dependency word; "generic pattern" implies conceptual extension |

---

## CANDIDATE 009D-009

| Field | Value |
|-------|-------|
| **Source** | `skills/05-code/code-interpreter-agent.md` |
| **Target** | `skills/09-agentic-patterns/tool-use-loop.md` |
| **Exact Quote** | "Related: `code-execution.md` · `code-review.md` · `tool-use-loop.md` · `agent-as-tool.md`" |
| **Section** | "Related" |
| **Qualifier** | Listed in Related only; no dependency language |
| **Confidence** | LOW — REJECT |
