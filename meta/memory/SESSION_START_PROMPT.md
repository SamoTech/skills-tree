# SESSION_START_PROMPT.md

# Session Start Procedure

At the start of every session investigating the skills-tree repository, follow these steps:

1. **Verify memory system exists**
   - Check that the directory `meta/memory` exists and contains all required files.
   - Required files:
     - MEMORY.md
     - FACTS.md
     - DECISIONS.md
     - STATE.md
     - TASK.md
     - EVIDENCE.md
     - INVESTIGATION_LOG.md
     - READ_VERIFICATION.md
     - HERMES_OPERATING_CONTRACT.md
     - MEMORY_SYSTEM_REPORT.md
     - SESSION_START_PROMPT.md

2. **Read all memory files**
   - Read each of the above files in the order listed above.

3. **Update READ_VERIFICATION.md**
   - For each file read, add an entry to READ_VERIFICATION.md with:
     - Timestamp (ISO 8601)
     - File path
     - File size in bytes
     - Lines read (e.g., "FULL FILE" or line range)
     - First line read (exact quote)
     - Last line read (exact quote)
     - Verification: PASSED

4. **Output the following information**
   - CURRENT TASK (from TASK.md)
   - KNOWN FACTS (from FACTS.md)
   - LOCKED DECISIONS (from DECISIONS.md)
   - OPEN QUESTIONS (from INVESTIGATION_LOG.md or inferred from open questions in the log)

5. **Wait for user instructions**
   - Do not proceed with any investigation until the user provides further instructions.

# Note:
If any required memory file is missing, output:
MEMORY SYSTEM NOT INITIALIZED
Missing Files: [list]
and stop.