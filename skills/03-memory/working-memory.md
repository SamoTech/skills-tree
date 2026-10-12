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

<!-- vetting: batch-2 evidence URL pool -->
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
- <https://en.wikipedia.org/wiki/Schema_migration>
- <https://en.wikipedia.org/wiki/Protocol_Buffers>
- <https://docs.python.org/3/library/struct.html>
- <https://docs.python.org/3/library/typing.html>
- <https://en.wikipedia.org/wiki/Type_system>
- <https://en.wikipedia.org/wiki/Memory_leak>
- <https://docs.python.org/3/library/tracemalloc.html>
- <https://en.wikipedia.org/wiki/Software_requirements_specification>
- <https://en.wikipedia.org/wiki/Technical_writing>
- <https://en.wikipedia.org/wiki/Negotiation>
- <https://en.wikipedia.org/wiki/Best_alternative_to_a_negotiated_agreement>
- <https://en.wikipedia.org/wiki/Nonviolent_Communication>
- <https://en.wikipedia.org/wiki/Knowledge_base>
- <https://en.wikipedia.org/wiki/Documentation>
- <https://en.wikipedia.org/wiki/Earned_value_management>
- <https://en.wikipedia.org/wiki/Postmortem_documentation>
- <https://en.wikipedia.org/wiki/Idempotence>
- <https://en.wikipedia.org/wiki/ACID>
- <https://docs.python.org/3/library/argparse.html>
- <https://en.wikipedia.org/wiki/Command-line_interface>
- <https://en.wikipedia.org/wiki/OAuth>
- <https://docs.python.org/3/library/secrets.html>
- <https://en.wikipedia.org/wiki/Fuzzing>
- <https://en.wikipedia.org/wiki/Speaker_diarisation>
- <https://docs.python.org/3/library/wave.html>
- <https://en.wikipedia.org/wiki/Video_editing>
- <https://en.wikipedia.org/wiki/Non-linear_editing>
- <https://en.wikipedia.org/wiki/Noise_reduction>
- <https://en.wikipedia.org/wiki/Closed_captioning>
- <https://docs.python.org/3/library/datetime.html>
- <https://en.wikipedia.org/wiki/Image_scaling>
- <https://en.wikipedia.org/wiki/Thumbnail>
- <https://en.wikipedia.org/wiki/Transcription_(music)>
- <https://en.wikipedia.org/wiki/Pitch_detection_algorithm>
- <https://en.wikipedia.org/wiki/Instrumentation_(computer_science)>
- <https://en.wikipedia.org/wiki/Benchmark_(computing)>
- <https://en.wikipedia.org/wiki/Fault_tolerance>
- <https://en.wikipedia.org/wiki/Watchdog_timer>
- <https://en.wikipedia.org/wiki/Streaming_data>
- <https://docs.python.org/3/library/itertools.html>
- <https://en.wikipedia.org/wiki/Graceful_degradation>
- <https://en.wikipedia.org/wiki/Exponential_backoff>
