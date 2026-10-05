---
name: context-compaction
description: Compress long agent context while preserving active task state, user constraints, tool dependencies, and evidence required for correct continuation.
---

# Context Compaction

Before hard context exhaustion, preserve the active objective, user constraints, decisions, unresolved work, dependencies, and authoritative evidence. Collapse redundant tool output and stale narration without inventing missing facts. Prevent self-referential summaries and validate the compacted state before continuation. If critical state cannot be preserved, recover from an authoritative checkpoint or return BLOCKED.
