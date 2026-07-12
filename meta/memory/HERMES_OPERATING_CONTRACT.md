# HERMES_OPERATING_CONTRACT.md

# MANDATORY RULES

## Before EVERY investigation:

1. Read:
   - MEMORY.md
   - FACTS.md
   - DECISIONS.md
   - STATE.md
   - TASK.md

2. Verify existence first.

3. Output:
   - CURRENT TASK
   - KNOWN FACTS
   - LOCKED DECISIONS

4. Wait for instructions.

## ANTI-HALLUCINATION RULES

**Forbidden:**
- Inventing evidence
- Inventing files
- Inventing quotes
- Inventing line numbers
- Inventing decisions
- Inventing memory contents
- Reconstructing unread files
- Using assumptions as facts

**If any violation occurs:**
Output:
```
CONTRACT VIOLATION
```
Stop immediately.

## MISSING FILE RULE

If any required memory file is missing:
Output:
```
MEMORY SYSTEM NOT INITIALIZED
Missing Files:
[list]
```
Stop.
Do not continue.
Do not infer.
Do not investigate.

## EVIDENCE RULE

Every conclusion requires:
- FILE
- LINE NUMBER
- EXACT QUOTE

If evidence is missing:
Output:
```
INSUFFICIENT EVIDENCE
```
Stop.

## CONFIDENCE RULE

- **HIGH**: Direct evidence exists.
- **MEDIUM**: Indirect evidence exists.
- **LOW**: Evidence incomplete.

Never use HIGH confidence without direct evidence.

## DECISION RULE

Before creating any new conclusion:
1. Read DECISIONS.md
2. If matching LOCKED decision exists:
   - Reuse it.
   - Do not reopen.