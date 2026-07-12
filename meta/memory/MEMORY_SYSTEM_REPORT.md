# MEMORY_SYSTEM_REPORT.md

# Memory System Report for skills-tree Repository

## Architecture Overview
The investigation memory system is designed to prevent hallucinations, fabricated conclusions, and repeated investigations in the skills-tree repository. It consists of interconnected markdown files that form a structured memory system.

## Memory Design
- **MEMORY.md**: Central repository summary containing current investigation, confirmed facts, open questions, evidence sources, and investigation history
- **FACTS.md**: Evidence-based facts with FACT-ID identifiers, each requiring EVIDENCE-ID references
- **EVIDENCE.md**: Verified evidence with exact quotes, file paths, and line numbers
- **DECISIONS.md**: Locked decisions with confidence levels that cannot be reopened without contradictory evidence
- **STATE.md**: Tracks current investigation phase, progress, and blockers
- **TASK.md**: Defines investigation objectives, scope, success criteria, and stop conditions
- **INVESTIGATION_LOG.md**: Append-only log of investigations with dates, questions, evidence, and next actions
- **READ_VERIFICATION.md**: Proof of file verification with exact quotes and timestamps
- **HERMES_OPERATING_CONTRACT.md**: Mandatory rules that must be followed before every investigation
- **SESSION_START_PROMPT.md**: Standardized procedure for starting investigation sessions
- **MEMORY_SYSTEM_REPORT.md**: This document - documentation of the memory system itself

## Decision Lock Strategy
Decisions are locked in DECISIONS.md with HIGH/MEDIUM/LOW confidence levels. Once LOCKED, decisions cannot be reopened unless contradictory evidence is provided with:
- Exact file path
- Exact line numbers
- Exact quote contradicting the decision

This prevents decision drift and ensures consistency across investigations.

## Evidence Strategy
All conclusions must be backed by evidence in EVIDENCE.md with:
- Exact file paths
- Exact line numbers
- Exact quotes (no paraphrasing)
- VERIFIED status

No conclusions can be drawn without proper evidence citation.

## Hallucination Prevention Strategy
Multiple layers prevent hallucinations:
1. **Evidence Requirement**: No facts without evidence citations
2. **Verification Requirement**: All source files must be verified in READ_VERIFICATION.md
3. **Contract Compliance**: HERMES_OPERATING_CONTRACT.md must be read before every investigation
4. **Decision Reuse**: Existing LOCKED decisions must be reused, not recreated
5. **Missing File Halt**: Investigation stops immediately if any memory file is missing

## Investigation Workflow
1. Session starts with SESSION_START_PROMPT.md procedure
2. Verify all memory files exist
3. Read all memory files in order
4. Update READ_VERIFICATION.md with verification proofs
5. Output CURRENT TASK, KNOWN FACTS, LOCKED DECISIONS, OPEN QUESTIONS
6. Wait for user instructions
7. Conduct investigation following evidence and decision rules
8. Log all findings in INVESTIGATION_LOG.md
9. Update memory files as needed (FACTS.md, DECISIONS.md, etc.)
10. Repeat from step 1 for next session

## Future Maintenance Instructions
1. **File Integrity**: Do not delete or rename any memory files
2. **Format Consistency**: Maintain the exact formats specified in each file
3. **Evidence First**: Always gather evidence before forming conclusions
4. **Decision Review**: Periodically review DECISIONS.md for relevance
5. **Log Maintenance**: Keep INVESTIGATION_LOG.md append-only and chronological
6. **Verification Discipline**: Never skip READ_VERIFICATION.md updates
7. **Contract Adherence**: Always follow HERMES_OPERATING_CONTRACT.md before investigations