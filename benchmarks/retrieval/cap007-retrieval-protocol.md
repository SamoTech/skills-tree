# CAP-007 Retrieval: Human-Labeled Dataset Protocol

**Status: protocol/schema preparation only. No empirical CAP-007 result is claimed.**

CAP-007 evaluates whether the canonical retrieval engine surfaces the correct skill(s) for realistic human support queries. The existing 12-case `cli-search-v1.json` deterministic benchmark is not a substitute for this contract.

## Dataset requirements

Use `cap007-dataset.schema.json` for the versioned human-labeled dataset. It requires at least 100 cases, each with:

- a realistic support query written by or sourced from a human;
- a query type: `exact_match`, `paraphrase`, `multi_hop`, or `no_relevant_document`;
- the expected canonical skill ID(s); `no_relevant_document` cases must list none, and every other query type must list at least one;
- labeler identity, label timestamp, evidence references, and rationale.

The dataset must contain at least one case of each query type. Labels must be assigned by humans from canonical `skills/` content, independently of the retrieval engine output. Do not derive labels by running the search engine and recording what it returned. Do not mark a dataset `human_labeled` until a human has actually labeled it; the schema and its synthetic unit-test examples are not labeled data.

For `no_relevant_document` labels, the labeler must document the search performed across the canonical corpus that supports the conclusion that no skill matches.

## Candidate run record

For every dataset case, retain the raw engine output and record:

- case ID;
- the top-5 returned skill IDs in ranked order;
- per-query latency in milliseconds;
- engine version, index digest, exact commit, and dataset SHA-256.

Report Recall@5, Precision@5, a per-query-type breakdown (exact match, paraphrase, multi-hop, no-relevant-document), and p95 latency. Acceptance thresholds are those defined by the authoritative CAP-007 mapping in `intelligence/ontology/evaluation_ontology.json`: **pass** requires Recall@5 >= 0.85 AND Precision@5 >= 0.75 AND p95 retrieval latency <= 5000ms; **fail** is Recall@5 < 0.80 OR Precision@5 < 0.70 OR retrieval p95 latency > 5000ms; results between those boundaries are NEEDS_INVESTIGATION. Do not invent thresholds or weaken them.

A run with fewer than 100 labeled cases, missing per-case records, an unverifiable dataset digest, or engine-derived labels is **INCOMPLETE / NOT RUN**, never PASS.

## Label acquisition

Use queries from genuine support tickets, user questions, public Q&A, or a controlled experiment, with recorded provenance and consent/licensing boundaries respected. Prefer at least two independent labelers for ambiguous cases and record disagreement resolution. If trustworthy human labels are not available, stop and report the dependency rather than inventing examples.

## Run order

1. Freeze the schema, protocol, sampling plan, and metrics.
2. Collect and independently label at least 100 queries spanning all four query types.
3. Validate the dataset against the schema and compute its SHA-256.
4. Run the canonical retrieval engine without changing the dataset during execution.
5. Score once against the frozen version; retain raw outputs.
6. Report all metrics, per-query-type breakdown, failure cases, and limitations.
7. Any label or protocol change creates a new version and requires rescoring.

## Tooling

Two deterministic tools implement this protocol:

```bash
# Validate a labeled dataset (fail-closed; also computes its SHA-256)
python tools/validate_cap007_dataset.py --dataset path/to/cap007-dataset.json

# Run the empirical evaluation against the canonical search engine
python tools/run_cap007_retrieval_benchmark.py \
  --dataset path/to/cap007-dataset.json \
  --index data/search-index.json \
  --output cap007-result.json
```

The validator enforces the schema, unique case IDs, all-four-query-type coverage, and that every expected skill resolves to a canonical `skills/` file. The runner refuses to run on an unlabeled or invalid dataset (`NOT_RUN`, never PASS), records dataset and index digests, checks deterministic replay, and reports micro-averaged set-based metrics:

- **Recall@5** = total top-5 hits / total expected skills across relevant cases.
- **Precision@5** = total top-5 hits / total predicted IDs (five per case; `no_relevant_document` cases contribute only to precision).
- Per-query-type breakdown for all four types, plus p50/p95 wall-clock latency (environment-dependent; record the measurement environment with the result).
