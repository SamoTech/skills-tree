---
title: "Working Memory"
category: 03-memory
level: intermediate
stability: stable
description: "Maintain bounded active task state, intermediate results, errors, and checkpoints during a multi-step agent workflow."
added: "2025-03"
related: ["03-memory", "input-guardrails", "output-guardrails"]
---

## Description

Maintain bounded active task state, intermediate results, errors, and checkpoints during a multi-step agent workflow.

## When to Use

Use when memory state must persist across steps or sessions and the workflow can define ownership, provenance, retention, and verification rules.

## Inputs / Outputs / Failure Modes

| Area | Contract |
|---|---|
| Inputs | goal, current state, completed steps, tool results, errors, and checkpoint policy. |
| Outputs | validated working state, checkpoint, next action, and failure context. |
| Failure modes | Stale memory, unsupported inference, conflicting records, unauthorized retention, context growth, or acceptance without revalidation. |

## Procedure

1. Define the memory scope, owner, retention rule, and acceptance criteria.
2. Validate incoming memory candidates and preserve their provenance.
3. Apply explicit freshness, confidence, conflict, and size bounds.
4. Retrieve only the memory relevant to the current task.
5. Revalidate memory before treating it as authoritative when material.
6. Record updates, conflicts, and unresolved uncertainty.

## Runnable Example

```python
memory = {"capability": "working-memory", "validated": True, "budget": 4}
assert memory["validated"] and memory["budget"] > 0
print({"status": "bounded_memory_operation", "capability": memory["capability"]})
```

## Failure Modes

- Memory is stale or its provenance cannot be established.
- A model-generated inference is stored as an explicit user fact.
- Conflicting records are silently merged.
- Retention exceeds the declared scope or authorization.
- Memory growth exhausts context or storage budgets.
- A stored procedure or fact is used without required revalidation.

## Safety Boundary

Treat memory as state, not truth. Preserve provenance and scope. Do not store sensitive or personal information unless explicitly authorized by the governing application policy, and honor correction or deletion requirements.

## Evidence

Canonical repository skill: this file. Structural conformance is governed by the repository schema, validation workflows, Agent Skills contract, and security gates. Memory-specific claims require reproducible implementation evidence or authoritative repository evidence; stored memory is not evidence by itself.

## Related

- 03-memory
- input-guardrails
- output-guardrails

<!-- link-check diagnostic: candidate URL scan; this PR is disposable and will be closed unmerged -->

<!-- vetting: batch-2 URL pool bisect round 1 (first half) -->
- <https://en.wikipedia.org/wiki/Apache_Parquet>
- <https://docs.python.org/3/library/statistics.html>
- <https://en.wikipedia.org/wiki/Zip_(file_format)>
- <https://docs.python.org/3/library/zipfile.html>
- <https://en.wikipedia.org/wiki/QR_code>
- <https://en.wikipedia.org/wiki/Barcode>
- <https://en.wikipedia.org/wiki/Curriculum_vitae>
- <https://docs.python.org/3/library/re.html>
- <https://docs.python.org/3/library/sqlite3.html>
- <https://en.wikipedia.org/wiki/Information_schema>
- <https://en.wikipedia.org/wiki/Syllogism>
- <https://en.wikipedia.org/wiki/Venn_diagram>
- <https://en.wikipedia.org/wiki/Game_theory>
- <https://en.wikipedia.org/wiki/Nash_equilibrium>
- <https://en.wikipedia.org/wiki/Cognitive_bias>
- <https://en.wikipedia.org/wiki/Confirmation_bias>
- <https://en.wikipedia.org/wiki/Entropy_(information_theory)>
- <https://en.wikipedia.org/wiki/Decision_tree_learning>
- <https://en.wikipedia.org/wiki/Expected_value>
- <https://en.wikipedia.org/wiki/Memory_consolidation>
- <https://en.wikipedia.org/wiki/Spaced_repetition>
- <https://en.wikipedia.org/wiki/Relevance_(information_retrieval)>
- <https://en.wikipedia.org/wiki/Precision_and_recall>
- <https://en.wikipedia.org/wiki/Conflict_resolution>
- <https://en.wikipedia.org/wiki/Fact-checking>
- <https://en.wikipedia.org/wiki/Knowledge_graph>
- <https://en.wikipedia.org/wiki/Record_linkage>
- <https://en.wikipedia.org/wiki/Context_window>
- <https://en.wikipedia.org/wiki/Lossy_compression>
- <https://en.wikipedia.org/wiki/Rate_limiting>
- <https://docs.python.org/3/library/concurrent.futures.html>
- <https://en.wikipedia.org/wiki/Secure_Shell>
- <https://docs.python.org/3/library/subprocess.html>
- <https://en.wikipedia.org/wiki/Cron>
- <https://docs.python.org/3/library/sched.html>
- <https://en.wikipedia.org/wiki/Chunked_transfer_encoding>
- <https://docs.python.org/3/library/http.client.html>
- <https://docs.python.org/3/library/tarfile.html>
- <https://en.wikipedia.org/wiki/Tar_(computing)>
- <https://docs.python.org/3/library/asyncio.html>
- <https://en.wikipedia.org/wiki/Asynchrony_(computer_science)>
