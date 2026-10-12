---
title: "Meeting Notes"
category: 06-communication
level: basic
stability: experimental
description: "Turn live meeting transcripts into structured notes with attributed decisions, owner-assigned action items, and open questions so follow-up work is trackable instead of relying on memory."
added: "2026-10"
version: v1
related: ["summarization", "report-writing", "clarification-seeking"]
---

# Meeting Notes

Category: Communication | Level: basic | Stability: experimental | Version: v1

## Description

Meeting value leaks through unrecorded decisions and ownerless actions. This skill defines a note contract for live meetings: capture decisions with attribution and verbatim wording where it matters, convert actions into owner-task-date triplets, and keep open questions visible with a follow-up owner. The notes are the record; the transcript is only the input.

## When to Use

Use when a live or asynchronous meeting produces decisions or actions that anyone must act on later.

Do not use for verbatim transcripts or archival records; capture and summarization skills fit those goals.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `transcript` | `list` | Yes | Timestamped contributions keyed by speaker |
| `known_participants` | `list` | Yes | Names and roles used for attribution |
| `action_marker` | `string` | No | Line prefix that marks action items |
| `due_format` | `string` | No | Expected date format for action deadlines |

## Procedure

1. Record every participant and role before discussion starts; unattributable statements are flagged, not guessed.
2. Capture decisions with their speaker, the exact phrasing, and the point in the agenda where they were made.
3. Extract actions as owner, task, and due date; a missing owner is recorded as UNASSIGNED, never silently filled.
4. Keep open questions in their own list with a named follow-up owner and a next checkpoint.
5. Quote verbatim where wording matters; paraphrase only when the meaning is unambiguous.
6. Publish the structured notes in the same channel as the meeting so latecomers see the same record.
7. Reconcile actions against the previous meeting’s notes; uncompleted actions carry forward visibly.
8. Retain the notes under the organization’s retention policy; notes are records, not scratch space.

## Outputs

| Output | Type | Description |
|---|---|---|
| `decisions` | `list` | Attributed decision entries with verbatim wording |
| `actions` | `list` | Owner-task-date triplets including UNASSIGNED flags |
| `open_questions` | `list` | Unresolved items with follow-up owners |
| `carried_over` | `list` | Actions reopened from the previous notes |

## Runnable Example

```python
def extract_action_items(lines):
    """Pull owner, task, and due date from structured note lines."""
    actions = []
    for line in lines:
        if not line.startswith("ACTION:"):
            continue
        parts = [p.strip() for p in line[len("ACTION:"):].split("|")]
        if len(parts) != 3:
            continue
        owner, task, due = parts
        actions.append({"owner": owner or "UNASSIGNED", "task": task, "due": due})
    return actions

transcript = [
    "DECISION: staging deploys move to Thursdays",
    "ACTION: Sara | update the deploy runbook | 2026-10-15",
    "ACTION:  | schedule the load test | 2026-10-18",
    "OPEN: which region hosts the failover instance",
]
print(extract_action_items(transcript))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Ghost actions | A task is recorded without an owner | Record UNASSIGNED and surface it at review |
| Decision drift | A paraphrase replaces the agreed wording | Quote verbatim where the wording matters |
| Lost question | An open issue drops out of the notes | Keep a dedicated open-questions list |
| Attribution guess | The speaker is inferred from context | Attribute only from known participants, or flag |
| Phantom closure | Actions are never revisited | Reconcile against the previous notes every meeting |

## Security and Authority Boundary

Taking notes grants no authority to speak for participants. Attributed statements must match what the participant actually said, and notes shared beyond the meeting must respect the organization’s information-handling rules. Commitments belong to whoever made them; personal observations belong to their author.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia’s article on minutes of meetings (https://en.wikipedia.org/wiki/Minutes).
2. Wikipedia’s article on the Cornell note-taking system (https://en.wikipedia.org/wiki/Cornell_notes).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Summarization](summarization.md) — condenses content; this skill structures it into a trackable record.
- [Report Writing](report-writing.md) — produces polished documents; these notes are the raw, attributed record.
- [Clarification Seeking](clarification-seeking.md) — resolves ambiguity live, before it hardens into a vague note.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
