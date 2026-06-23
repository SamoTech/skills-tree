# AGENT MEMORY PROTOCOL

**Initiative:** INITIATIVE-010A  
**Created:** 2026-06-23  
**Status:** ACTIVE

---

## Core Rule

**The repository is the ONLY permitted memory store.**

Agents may NOT use:
- Previous chat history
- Unverified claims from any prior session
- Assumed metric values not confirmed in repository files
- Cross-session state not committed to the repository

---

## Authoritative Memory Sources

| File | Contents | Trust level |
|------|----------|------------|
| `meta/MEMORY_STATE.md` | Current graph metrics, active initiatives, REQUIRES count | PRIMARY |
| `meta/DECISION_LOG.md` | All approved decisions with evidence | PRIMARY |
| `data/SKILLS_GRAPH.json` | Actual graph state (nodes, edges, requires) | PRIMARY |
| `schema/` | Schema contracts | SECONDARY |
| `meta/PROJECT_CONSTITUTION.md` | Governance rules | SECONDARY |
| `skills/` | Individual skill definitions | TERTIARY |

---

## State Loading Procedure

Every agent MUST execute this procedure at mission start:

```
STEP 1: Read meta/MEMORY_STATE.md
  - Extract: schema_version, node_count, edge_count, requires_count
  - Extract: LAST_INITIATIVE, NEXT_INITIATIVE, active blockers

STEP 2: Read meta/DECISION_LOG.md
  - Extract: last decision ID
  - Verify: no open D4/D5 decisions blocking current work

STEP 3: Read data/SKILLS_GRAPH.json (or run pipeline)
  - Verify: node count matches MEMORY_STATE.md
  - Verify: edge count matches MEMORY_STATE.md
  - Verify: requires count matches MEMORY_STATE.md
```

---

## State Validation Rules

All three values must match between `MEMORY_STATE.md` and `SKILLS_GRAPH.json`:

| Metric | Must match |
|--------|----------|
| node_count | MEMORY_STATE.md ↔ SKILLS_GRAPH.json |
| edge_count | MEMORY_STATE.md ↔ SKILLS_GRAPH.json |
| requires_count | MEMORY_STATE.md ↔ SKILLS_GRAPH.json |

If any mismatch is found:

```
→ Create meta/STATE_DIVERGENCE_REPORT.md
→ Document: expected value, actual value, source of each
→ STOP — do not proceed
→ Escalate to Program Director
```

---

## Divergence Handling

A divergence is defined as any case where MEMORY_STATE.md reports a metric that does not match the actual value found in `data/SKILLS_GRAPH.json` or in repository files.

**Divergence Report must contain:**

```markdown
## DIVERGENCE DETECTED

Metric: <field name>
Expected (MEMORY_STATE.md): <value>
Actual (source file): <value>
Source file: <path>
Detected by: <agent name>
Timestamp: <ISO date>
Action required: <resolution steps>
```

---

## Recovery Procedure

When a divergence is reported:

1. **Program Director** acknowledges and logs D0 observation in DECISION_LOG.md
2. **Repository Architect** audits affected files
3. **Graph Architect** verifies `data/SKILLS_GRAPH.json` is the ground truth
4. **Release Manager** updates `meta/MEMORY_STATE.md` to match verified ground truth
5. **Governance Officer** approves state correction as D1 (refactor, no behavioral change)
6. All agents re-load state before resuming work

---

## Prohibited Behaviors

| Behavior | Prohibited because |
|---------|-------------------|
| Citing a metric from chat history | Not verified in repository |
| Assuming edge count from prior session | May be stale |
| Claiming an initiative is complete without reading its files | Unverified |
| Writing to MEMORY_STATE.md without Release Manager role | Bypasses governance chain |
| Skipping SKILLS_GRAPH.json verification | Allows divergence to compound |

---

*This protocol is non-negotiable. Any agent that violates it must be reset to STATE_LOAD before proceeding.*
