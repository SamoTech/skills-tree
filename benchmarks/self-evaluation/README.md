# CAP-011 Self-Evaluation: Ground-Truth Protocol

**Status: protocol/schema preparation only. No empirical CAP-011 result is claimed.**

CAP-011 evaluates whether an agent's self-assessment confidence tracks independently established task outcomes, and whether low-confidence assessments follow the required review path. The system under test must not generate or adjudicate its own ground truth.

## Dataset requirements

Use `cap011-dataset.schema.json` for the versioned ground-truth dataset. It requires at least 100 cases with:

- a task input and the evidence available to the agent;
- a predeclared expected outcome (`pass` or `fail`);
- reviewer identity, review timestamp, source references, and rationale;
- a documented label protocol and an explicit statement that ground truth is independent of the system under test.

Do not mark a dataset `ground_truth_reviewed` until labels are actually reviewed. The schema and its synthetic unit-test examples are not a substitute for labeled data. Never fill reviewer identities or evidence references with fabricated values.

## Candidate run record

For every dataset case, retain the raw candidate output and record:
- case ID;
- predicted outcome (`pass` or `fail`);
- numeric confidence in `[0,1]`;
- whether the defined review gate was routed when confidence was below 0.90;
- an independently adjudicated hallucination finding, reviewer, timestamp, and evidence references.

Do not accept the model's own hallucination declaration as the adjudication. Reviewers should judge claims against the provided evidence and record unsupported or contradicted claims. Keep raw outputs and adjudication records immutable after scoring; corrections should create a new dataset/result version.

## Metrics and decision

Report:
1. high-confidence correctness for all cases with confidence `>= 0.90` (must be `>= 0.95`);
2. confidence-bin reliability and Expected Calibration Error (ECE) as diagnostic metrics;
3. low-confidence review-gate compliance (every case below 0.90 must route to review);
4. independently adjudicated hallucination rate (must be `<= 0.05` for a pass);
5. case count, missing/duplicate cases, dataset/result SHA-256, system/version, exact commit, and limitations.

A run with fewer than 100 reviewed cases, missing confidence values, missing review-gate evidence, or missing independent hallucination adjudication is **INCOMPLETE / NOT RUN**, never PASS. ECE is diagnostic and must not replace the high-confidence correctness or review-gate criteria.

## Ground-truth acquisition

Use task outcomes that can be independently verified from structured outputs, reproducible tests, authoritative records, or qualified human review. Include both pass and fail cases and document sampling to avoid cherry-picking. Prefer two independent reviewers for safety-sensitive or ambiguous labels and record disagreement resolution. If trustworthy labels are not available, stop and report the dependency rather than inventing examples.

## Run order

1. Freeze the schema, protocol, sampling plan, and decision thresholds.
2. Collect and independently review at least 100 ground-truth cases.
3. Validate the dataset and compute its SHA-256.
4. Run the candidate system without changing the dataset during execution.
5. Independently adjudicate hallucinations and review-gate evidence.
6. Score once against the frozen version; retain raw outputs and report all metrics/failures.
7. Any label or protocol change creates a new version and requires rescoring.

Current ontology acceptance remains authoritative: high-confidence correctness >= 0.95, every low-confidence case follows the review gate, and hallucination rate <= 0.05. No deployment may be triggered solely from self-evaluation output; structured quality-gate state remains authoritative.