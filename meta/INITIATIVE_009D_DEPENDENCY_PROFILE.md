# INITIATIVE-009D — Dependency Language Profile

**Date:** 2026-06-23  
**Scope:** `skills/05-code/` Priority A files (5 files read in full)

---

## Phase 0.5 — Evidence Hit Ranking

Files scanned for qualifying dependency language before candidate extraction.

| File | Size (bytes) | Evidence Hits | Qualifying Language Found | Priority |
|------|-------------|---------------|--------------------------|----------|
| `bug-fixing.md` | 7,913 | 5 | "agentic loop", "localise the bug before patching" (debugging), "same loop pattern" (code-generation), "critique-revise pattern" (reflection), "Don't use when: you don't know what's broken (use Debugging first)" | **A+** |
| `code-generation.md` | 8,361 | 3 | "use Algorithm Design first", "use Refactoring", "when generation must invoke tools" (function-calling) | **A** |
| `dependency-auditor.md` | 18,380 | 2 | "bridge from existence proof to execution proof", `code-execution-sandbox.md` described as required execution environment | **A** |
| `code-review.md` | 10,174 | 2 | "Find and fix bugs interactively" (debugging), "Verify dependencies execute cleanly" (dependency-auditor) | **A** |
| `code-interpreter-agent.md` | ~2,800 | 2 | `tool-use-loop.md` in Related, `code-execution.md` listed as Related | **B** |

---

## Qualifying Words Found

| Word/Phrase | Occurrences | Files |
|-------------|-------------|-------|
| "Don't use when… use X first" | 2 | bug-fixing, code-generation |
| "agentic loop" | 1 | bug-fixing |
| "prerequisite" / "prerequisites" | 0 | (none in body text) |
| "requires" | 0 | (no dependency-language use) |
| "depends on" | 0 | — |
| "built on" | 0 | — |
| "extends" | 0 | — |
| "foundation" | 0 | — |
| "precedes" | 0 | — |
| "operates on output from" | 0 | — |
| "cannot function without" | 0 | — |
| "localise before" | 1 | bug-fixing |
| "use X first" | 2 | bug-fixing, code-generation |

---

**Top evidence source:** `bug-fixing.md` — explicit sequential dependency on `debugging.md` stated twice in the body.
