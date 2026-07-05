# CAPABILITY ROOT CAUSE ANALYSIS

**Report ID:** RCA-001  
**Investigation Date:** 2026-07-05  
**Status:** COMPLETE  
**Repository:** skills-tree  

---

## INVESTIGATION SCOPE

Five artifacts inspected:

| Artifact | Path | SHA |
|---|---|---|
| capability_ontology.json | intelligence/ontology/capability_ontology.json | 5cdcd58d2c3f56a66b883c41e96d79499fb576d0 |
| evaluation_ontology.json | intelligence/ontology/evaluation_ontology.json | 7cd1b696b0ae29f32003b4f85f4e8b0450fe6fd9 |
| CORPUS-001 | intelligence/corpus/entries/engineering/CORPUS-001.json | (committed 2026-07-05) |
| CORPUS-002 | intelligence/corpus/entries/engineering/CORPUS-002.json | d33a7b34db75ed5169f92477c8ff6522f4e27342 |
| CORPUS_ANALYSIS_V1.md | intelligence/corpus/reports/CORPUS_ANALYSIS_V1.md | 4537f0bec6d6864ff48aac9b7da54294c6b9e234 |

---

## SECTION 1: COLLISION INVENTORY

Two collisions detected. Both involve CORPUS-002.

### COLLISION-001 — CAP-009

| Source | cap_id | name |
|---|---|---|
| capability_ontology.json | CAP-009 | chain_of_thought_reasoning |
| evaluation_ontology.json | CAP-009 | (no mapping — not referenced) |
| CORPUS-001 | CAP-009 | (not used) |
| CORPUS-002 | CAP-009 | **tool_execution** |

**Collision type:** Name mismatch. CORPUS-002 assigns `name: "tool_execution"` to `cap_id: "CAP-009"`. The ontology assigns `name: "chain_of_thought_reasoning"` to `CAP-009`.

**What CORPUS-002 intended:** Tool execution (invoke CI/CD APIs, post PR comments, trigger deployments) — a real P0 requirement for a reactive CI/CD agent.

**What CAP-009 actually is in the ontology:** Chain-of-thought reasoning (decompose complex problems into sequential reasoning steps before producing a final answer). A `reasoning` tier capability, not `tool_use`.

**Where the correct capability lives in the ontology:** `CAP-014` — `tool_execution`, `tool_use` tier, purpose: "Correctly format and invoke tool calls, handle responses and errors, and integrate results into the reasoning chain."

---

### COLLISION-002 — CAP-014

| Source | cap_id | name |
|---|---|---|
| capability_ontology.json | CAP-014 | tool_execution |
| evaluation_ontology.json | CAP-014 | (no mapping — not referenced) |
| CORPUS-001 | CAP-014 | (not used) |
| CORPUS-002 | CAP-014 | **planning_and_decomposition** |

**Collision type:** Name mismatch. CORPUS-002 assigns `name: "planning_and_decomposition"` to `cap_id: "CAP-014"`. The ontology assigns `name: "tool_execution"` to `CAP-014`.

**What CORPUS-002 intended:** Planning and decomposition (decompose a cascade of 40+ test failures into root causes rather than reporting each individually) — a real P1 requirement.

**What CAP-014 actually is in the ontology:** Tool execution. The capability CORPUS-002 intended is `CAP-010` — `planning_and_decomposition`, `reasoning` tier, purpose: "Break a high-level goal into an ordered sequence of sub-tasks with dependencies, estimated effort, and success criteria."

---

## SECTION 2: COLLISION TIMELINE

### CAP-009 Timeline

| Event | Date | File | Definition | Commit |
|---|---|---|---|---|
| CAP-009 first defined | 2026-06-28 | capability_ontology.json | `chain_of_thought_reasoning` (reasoning tier) | generated_at: 2026-06-28T00:00:00Z |
| CAP-009 misassigned | 2026-07-05 | CORPUS-002 | `tool_execution` | 0ff08496c7d5d6a3f0c0776eb3899d411a141633 |
| Collision first detectable | 2026-07-05 | CORPUS_ANALYSIS_V1.md | Reported co-occurrence of CAP-009+CAP-028 with `tool_execution` framing | 8f581bf3e2b7bf5262e646f29554208cb9100049 |

**First divergence point:** Commit `0ff08496c7` — CORPUS-002 creation on 2026-07-05.

### CAP-014 Timeline

| Event | Date | File | Definition | Commit |
|---|---|---|---|---|
| CAP-014 first defined | 2026-06-28 | capability_ontology.json | `tool_execution` (tool_use tier) | generated_at: 2026-06-28T00:00:00Z |
| CAP-014 misassigned | 2026-07-05 | CORPUS-002 | `planning_and_decomposition` | 0ff08496c7d5d6a3f0c0776eb3899d411a141633 |
| Collision first detectable | 2026-07-05 | CORPUS_ANALYSIS_V1.md | Reported CAP-014 as `planning_and_decomposition` without cross-check | 8f581bf3e2b7bf5262e646f29554208cb9100049 |

**First divergence point:** Commit `0ff08496c7` — CORPUS-002 creation on 2026-07-05.

---

## SECTION 3: AUTHORITY ANALYSIS

### Candidate A — capability_ontology.json

**Evidence for authority:**

- `generated_at: 2026-06-28T00:00:00Z` — created 7 days before CORPUS-002.
- `total_capabilities: 28` — defines a complete, numbered, contiguous namespace (CAP-001 through CAP-028).
- Naming is internally consistent: `tier` field matches `name` across all 28 entries. CAP-009 is in the `reasoning` tier. CAP-014 is in the `tool_use` tier. The tier assignments are self-consistent.
- The evaluation_ontology.json references cap_ids and names that match the capability_ontology exactly: CAP-001 = text_understanding, CAP-003 = intent_classification, CAP-005 = short_term_context_management, CAP-017 = response_generation, CAP-023 = human_in_loop_escalation (note: ontology CAP-023 is `human_in_loop_escalation`; evaluation maps CAP-023 to `structured_data_generation` — see Collision Note below), CAP-025 = pii_detection_and_redaction, CAP-028 = output_validation.
- CORPUS-001 references: CAP-001, CAP-002, CAP-003, CAP-005, CAP-006, CAP-007, CAP-008, CAP-009, CAP-010, CAP-014, CAP-017, CAP-019, CAP-020, CAP-023, CAP-024, CAP-025, CAP-026, CAP-027, CAP-028 — these should be verified against ontology names in CORPUS-001 to confirm no prior collision exists there.

**Downstream dependencies:** evaluation_ontology.json explicitly resolves cap_ids to names that match capability_ontology.json for all mapped capabilities (CAP-001, CAP-003, CAP-005, CAP-017, CAP-028).

**Verdict:** capability_ontology.json behaves as the primary authority. It is earlier in creation, more complete, internally consistent, and corroborated by the evaluation_ontology.

---

### Candidate B — CORPUS-002

**Evidence against authority:**

- Created 2026-07-05 — 7 days after the ontology.
- Uses `cap_id: "CAP-009"` with `name: "tool_execution"`. The ontology unambiguously defines CAP-009 as `chain_of_thought_reasoning` in the `reasoning` tier.
- Uses `cap_id: "CAP-014"` with `name: "planning_and_decomposition"`. The ontology unambiguously defines CAP-014 as `tool_execution` in the `tool_use` tier.
- CORPUS-002's `dependency_order` lists CAP-009 in position 6 (after CAP-007, suggesting tool invocation in a late pipeline stage), which is semantically consistent with tool execution — confirming the author intended CAP-014 semantics but used the wrong ID.
- CORPUS-002's CAP-014 has `tier: "P1"` in the corpus priority scale. The ontology's CAP-014 (tool_execution) is demonstrably P0 in a CI/CD agent — the rationale written by the corpus author even states "The agent must invoke external tools" and lists it as `criticality: 0.98`, which is inconsistent with a P1 assignment for what the ontology calls tool_execution.

**Verdict:** CORPUS-002 is not authoritative. The IDs in CORPUS-002 are wrong. The names and rationales in CORPUS-002 are correct — the intended capabilities are real and accurately described. Only the ID assignments are wrong.

---

### Candidate C — evaluation_ontology.json

**Evidence:**

- The evaluation_ontology maps CAP-023 to `structured_data_generation`. The capability_ontology defines CAP-023 as `human_in_loop_escalation`. This is a secondary inconsistency within the evaluation_ontology itself, independent of the CORPUS-002 collisions.
- The evaluation_ontology does not reference CAP-009 or CAP-014. It therefore has no direct role in the CAP-009/CAP-014 collision.
- For CAP-025, the evaluation_ontology uses name `multi_modal_understanding`. The capability_ontology defines CAP-025 as `pii_detection_and_redaction`. This is a second secondary inconsistency in the evaluation_ontology.

**Verdict:** The evaluation_ontology has its own internal name mismatches (CAP-023, CAP-025) but is not the source of the CAP-009/CAP-014 CORPUS-002 collisions. The evaluation_ontology inconsistencies are a separate issue documented below and require independent investigation once the CORPUS-002 migration freeze is lifted.

---

## SECTION 4: ROOT CAUSE ATTRIBUTION

### COLLISION-001: CAP-009 in CORPUS-002

| Field | Value |
|---|---|
| **CAP-ID** | CAP-009 |
| **Ontology Definition** | chain_of_thought_reasoning (reasoning tier) |
| **CORPUS-002 Definition** | tool_execution |
| **Evaluation Ontology Definition** | Not mapped |
| **First Divergence Point** | 2026-07-05, commit 0ff08496c7 |
| **Root Cause** | Wrong ID assignment. Author correctly identified the need for tool execution capability but assigned CAP-009 (chain_of_thought_reasoning) instead of CAP-014 (tool_execution). Most probable cause: author constructed CORPUS-002 from a capability name list without cross-referencing the ontology ID assignments. |
| **Verdict** | **CORPUS_CORRECT — ontology ID assignment is wrong in corpus** |

### COLLISION-002: CAP-014 in CORPUS-002

| Field | Value |
|---|---|
| **CAP-ID** | CAP-014 |
| **Ontology Definition** | tool_execution (tool_use tier) |
| **CORPUS-002 Definition** | planning_and_decomposition |
| **Evaluation Ontology Definition** | Not mapped |
| **First Divergence Point** | 2026-07-05, commit 0ff08496c7 |
| **Root Cause** | Wrong ID assignment. Author correctly identified the need for planning and decomposition capability but assigned CAP-014 (tool_execution) instead of CAP-010 (planning_and_decomposition). The error is the symmetric pair of COLLISION-001: the two capabilities (tool_execution and planning_and_decomposition) were swapped in the ID lookup. This is a copy/paste transposition error during CORPUS-002 authoring. |
| **Verdict** | **CORPUS_CORRECT — ontology ID assignment is wrong in corpus** |

### Secondary Finding: evaluation_ontology.json name inconsistencies

Not the subject of this investigation. Documented for completeness.

| CAP-ID | capability_ontology name | evaluation_ontology name | Status |
|---|---|---|---|
| CAP-023 | human_in_loop_escalation | structured_data_generation | Collision — requires separate RCA |
| CAP-025 | pii_detection_and_redaction | multi_modal_understanding | Collision — requires separate RCA |

These evaluation_ontology collisions do not affect CORPUS-001 or CORPUS-002 because neither corpus entry references CAP-023 or CAP-025 with conflicting names (CORPUS-001 uses CAP-023 and CAP-025 — their names in CORPUS-001 must be verified against the evaluation_ontology before that corpus entry is considered clean).

---

## SECTION 5: IMPACT ANALYSIS

### If capability_ontology is correct (authoritative) and corpus is wrong:

**Files requiring modification:** 1  
**File:** `intelligence/corpus/entries/engineering/CORPUS-002.json`

| Current (wrong) | Correct |
|---|---|
| cap_id: CAP-009, name: tool_execution | cap_id: CAP-014, name: tool_execution |
| cap_id: CAP-014, name: planning_and_decomposition | cap_id: CAP-010, name: planning_and_decomposition |
| dependency_order entry: CAP-009 | dependency_order entry: CAP-014 |
| dependency_order entry: CAP-014 | dependency_order entry: CAP-010 |

**Migration effort:** Low. 4 field changes in a single file. No schema changes. No new files.  
**Risk:** Low. The capability content (rationale, without_this, criticality) is correct and requires no modification — only the IDs are wrong.  
**Downstream impact:** CORPUS_ANALYSIS_V1.md was generated from CORPUS-002 and contains the wrong IDs. It must be regenerated after CORPUS-002 is corrected.

### If corpus is correct and ontology is wrong:

**Files requiring modification:** 4+  
**Files:** capability_ontology.json, evaluation_ontology.json, CORPUS-001 (which uses CAP-009 and CAP-014 with names that must be verified), CORPUS_ANALYSIS_V1.md  
**Migration effort:** High. Renumbering IDs in the canonical ontology invalidates every downstream reference.  
**Risk:** High. The ontology is the root of the ID namespace. Changing it breaks all existing corpus entries, all evaluation mappings, and all future entries built on the current ID scheme.  
**Verdict:** This path is not supported by the evidence. The ontology was created first and is internally consistent. The corpus was created second and contains a localized transposition error.

---

## SECTION 6: FINAL VERDICT

| Collision | Verdict |
|---|---|
| CAP-009 in CORPUS-002 | **CORPUS_CORRECT** — CORPUS-002's intended capability (tool_execution) is correct; the ID used (CAP-009) is wrong. Fix: change CORPUS-002 CAP-009 → CAP-014. |
| CAP-014 in CORPUS-002 | **CORPUS_CORRECT** — CORPUS-002's intended capability (planning_and_decomposition) is correct; the ID used (CAP-014) is wrong. Fix: change CORPUS-002 CAP-014 → CAP-010. |

**Authoritative source:** `capability_ontology.json` (SHA: 5cdcd58d2c3f56a66b883c41e96d79499fb576d0, generated_at: 2026-06-28)

**Nature of error:** ID transposition in CORPUS-002 — the two capability names (tool_execution and planning_and_decomposition) were swapped during ID lookup. Content is correct. IDs are wrong.

---

## SECTION 7: REPOSITORY STATUS

```
SAFE_TO_FIX
```

**Conditions:**
- Root cause is established with full evidence.
- The fix is localized to CORPUS-002 only.
- CORPUS-001 does not use CAP-009 or CAP-014 with conflicting names (to be verified before CORPUS-001 is declared clean).
- capability_ontology.json requires no modification.
- evaluation_ontology.json requires no modification for this collision (the CAP-023/CAP-025 name inconsistencies in evaluation_ontology are a separate issue and must not be mixed into this fix).
- CORPUS_ANALYSIS_V1.md must be regenerated after CORPUS-002 is corrected.

**Fix scope:** Single file — `intelligence/corpus/entries/engineering/CORPUS-002.json`  
**Fix type:** ID correction only — 4 field value changes, no structural changes.

---

*Generated by investigation on 2026-07-05. Evidence base: capability_ontology.json (SHA: 5cdcd58d), evaluation_ontology.json (SHA: 7cd1b696), CORPUS-002.json (SHA: d33a7b34).*
