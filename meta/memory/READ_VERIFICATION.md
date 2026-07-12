# READ_VERIFICATION.md

# Purpose:
# Proof that files were actually read during investigation sessions.
# Every session must update this file after reading source files.
# Unverified files cannot be trusted as sources of facts or evidence.

# Format for each verification entry:

Timestamp:
[ISO 8601 timestamp, e.g., 2026-07-12T14:30:00Z]

File:
[Absolute or relative path to the file that was read]

Size:
[File size in bytes]

Lines Read:
[Number of lines read, or "FULL FILE" if entire file was read]

First Line:
[Exact first line of the file that was read]

Last Line:
[Exact last line of the file that was read]

Verification:
PASSED

# Rules:
# * Every session must update this file after reading source files.
# * Unverified files cannot be trusted as sources for facts, evidence, or decisions.
# * Each verification entry must contain exact quotes from the first and last lines read.
# * If only part of a file was read, specify the line range and provide first/last lines of that range.
# * Verification fails if any of the above is missing or inaccurate.

# Example entry:
# Timestamp: 2026-07-12T14:30:00Z
# File: skills/advanced-user-memory/SKILL.md
# Size: 3421
# Lines Read: FULL FILE
# First Line: # advanced-user-memory
# Last Line: ## References
# Verification:
# PASSED

# Session start: Initialize with session start verification.