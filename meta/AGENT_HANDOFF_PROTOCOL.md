# AGENT HANDOFF PROTOCOL

**Initiative:** INITIATIVE-010A  
**Created:** 2026-06-23  
**Status:** ACTIVE

---

## Purpose

Every agent that completes a mission must produce a structured handoff packet. This packet is the only permitted communication channel between agents. It must be written to the repository before the receiving agent begins work.

---

## Standard Handoff Format

```markdown
## HANDOFF PACKET

**MISSION_ID:** <initiative-id>-<phase>-<sequence>
**FROM_AGENT:** <agent name>
**TO_AGENT:** <next agent name>
**TIMESTAMP:** <ISO date>
**STATUS:** COMPLETE | BLOCKED | PARTIAL

---

### INPUTS
- List all files read during this mission
- Include SHAs or last-modified dates where critical

### FILES_READ
- `path/to/file.md` (sha: abc123)
- `data/SKILLS_GRAPH.json` (sha: def456)

### FILES_WRITTEN
- `path/to/output.md` (created | updated)
- `meta/DECISION_LOG.md` (appended entry D-XXX)

### DECISIONS
- D-ID: <decision class> — <brief description> — <APPROVED | PROPOSED | REJECTED>

### RISKS
- Risk 1: <description> — Mitigation: <action>
- Risk 2: <description> — Mitigation: <action>

### NEXT_AGENT
- Agent: <name>
- Mission: <brief description of what they should do>
- Required files: <list>

### SUCCESS_CRITERIA
- [ ] Criterion 1
- [ ] Criterion 2
```

---

## Handoff Examples

### Example 1 — Dependency Auditor → Graph Architect

```markdown
## HANDOFF PACKET

**MISSION_ID:** INITIATIVE-009D-audit-001
**FROM_AGENT:** Dependency Auditor
**TO_AGENT:** Graph Architect
**TIMESTAMP:** 2026-06-20
**STATUS:** COMPLETE

### INPUTS
- Mission charter from Program Director: 009D approved candidates

### FILES_READ
- `meta/INITIATIVE_009D_CANDIDATE_REGISTRY.md` (sha: 3ba9b86)
- `skills/05-code/bug-fixing.md` (sha: read during audit)
- `skills/05-code/code-generation.md` (sha: read during audit)
- `meta/MEMORY_STATE.md` (sha: 7cf959b)

### FILES_WRITTEN
- `meta/INITIATIVE_009D_DECISION_GATE.md` (created)
- `meta/INITIATIVE_009D_QUALITY_GATE.md` (created)

### DECISIONS
- D-009D-001: D3 — Add requires edge bug-fixing→debugging — APPROVED
- D-009D-003: D3 — Add requires edge code-generation→algorithm-design — APPROVED

### RISKS
- Risk: debugging.md is currently a stub (0 prerequisites) — Mitigation: Flagged for INITIATIVE-009E review

### NEXT_AGENT
- Agent: Graph Architect
- Mission: Commit approved edges to skill files and rebuild graph
- Required files: `meta/INITIATIVE_009D_DECISION_GATE.md`, approved candidate specs

### SUCCESS_CRITERIA
- [x] 2 new requires edges added to skill files
- [x] Graph rebuilt successfully
- [x] MEMORY_STATE.md updated to requires_count=15
```

---

### Example 2 — Quality Auditor → Release Manager

```markdown
## HANDOFF PACKET

**MISSION_ID:** INITIATIVE-009D-release-001
**FROM_AGENT:** Quality Auditor
**TO_AGENT:** Release Manager
**TIMESTAMP:** 2026-06-20
**STATUS:** COMPLETE

### INPUTS
- Graph Architect's rebuild output
- Validation workflow results

### FILES_READ
- `.github/workflows/validate-graph.yml`
- `data/SKILLS_GRAPH.json` (post-rebuild)
- `meta/INITIATIVE_009D_QUALITY_GATE.md`

### FILES_WRITTEN
- `meta/INITIATIVE_009D_VALIDATION_REPORT.md` (created)

### DECISIONS
- Quality Gate: PASS — all validators green

### RISKS
- None — clean state

### NEXT_AGENT
- Agent: Release Manager
- Mission: Update MEMORY_STATE.md, append DECISION_LOG entry, update CHANGELOG
- Required files: `meta/MEMORY_STATE.md`, `meta/DECISION_LOG.md`, `meta/CHANGELOG.md`

### SUCCESS_CRITERIA
- [x] MEMORY_STATE.md updated: requires_count=15
- [x] DECISION_LOG.md entry D-009D appended
- [x] CHANGELOG.md updated
```

---

## Handoff Rules

1. A handoff packet MUST be written to the repository before the next agent begins
2. STATUS must accurately reflect the mission outcome — never mark COMPLETE if blockers remain
3. RISKS must be specific, not generic (no "things could go wrong")
4. If NEXT_AGENT is Governance Officer, include the full decision proposal in the packet
5. Handoff packets are permanent record — never delete or overwrite

---

*All agents must use this format. Deviations require Program Director approval.*
