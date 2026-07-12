# Lessons Learned

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LESSON-ID: LL-001

Date:
2026-07-12

Category:
Memory System

Problem:
Agent claimed files existed without displaying raw verification output.

Root Cause:
Verification relied on internal reasoning instead of filesystem evidence.

Fix Applied:
Added Git verification and physical file validation.

Prevention Rule:
Never claim VERIFIED without:

* directory listing
* file read
* hash verification
* git verification

Status:
RESOLVED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Related Files:
meta/memory/INDEX.md
meta/memory/LESSONS_LEARNED.md
meta/memory/SESSION_START_PROMPT.md

Related Decisions:
[To be filled: DECISION IDs if any]

Evidence References:
[To be filled: EVIDENCE IDs if any]

Status:
RESOLVED