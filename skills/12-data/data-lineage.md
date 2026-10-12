---
title: "Data Lineage"
category: 12-data
level: intermediate
stability: experimental
description: "Record where each dataset came from and what it fed — inputs, transformations, outputs — so any result can be traced to its sources and any change traced forward."
added: "2026-10"
version: v1
related: ["etl-pipeline", "data-joining"]
---

# Data Lineage

Category: Data | Level: intermediate | Stability: experimental | Version: v1

## Description

A number without ancestry is a rumor with formatting. This skill records ancestry as a first-class artifact: every dataset declares its inputs, the transformation and code version that produced it, and the outputs that depend on it. Lineage answers two questions the moment they are asked — where did this come from, and what breaks if this changes — and a lineage graph that cannot answer both is decoration, not documentation.

## When to Use

Use for datasets that feed decisions, reports, or models — anywhere a wrong number needs to be traced to its source or an upstream change needs its blast radius known.

Do not hand-maintain lineage for throwaway exploratory scratch data; capture it where outputs persist and matter, and let the pipeline write the graph.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `dataset` | `record` | Yes | The dataset whose ancestry is being recorded |
| `inputs` | `list` | Yes | Upstream datasets and their versions |
| `transform` | `record` | Yes | The code, version, and parameters that produced the dataset |

## Procedure

1. Record inputs precisely: which upstream datasets, at which versions or snapshots, fed the transformation.
2. Record the transformation itself — code version, parameters, and environment — enough to reproduce the output.
3. Write lineage at run time from the pipeline itself, not by hand afterward; hand-maintained lineage is yesterday's graph.
4. Register outputs symmetrically: a dataset knows what it fed, so impact analysis can walk forward as easily as backward.
5. Attach the lineage record to the data — a table property, a manifest, a catalog entry — not to a wiki page.
6. On any upstream change, consult the forward graph before it merges: blast radius is a lineage query, not a guess.

## Outputs

| Output | Type | Description |
|---|---|---|
| `lineage` | `record` | Inputs, transform, and outputs for the dataset |
| `impact` | `list` | Downstream datasets affected by a change to this one |

## Runnable Example

```python
lineage = {}

def register(dataset, inputs, transform):
    lineage[dataset] = {"inputs": inputs, "transform": transform}

def downstream(dataset, found=None):
    found = found if found is not None else set()
    for name, record in lineage.items():
        if dataset in record["inputs"] and name not in found:
            found.add(name)
            downstream(name, found)
    return found

register("daily_revenue", inputs=["orders", "refunds"], transform="agg v4")
register("exec_dashboard", inputs=["daily_revenue"], transform="render v2")
print("affected by orders change:", sorted(downstream("orders")))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Hand-drawn graphs | Lineage edited by hand and drifting from reality | Capture lineage at run time from the pipeline |
| Version-blind inputs | Upstream named but not pinned to a snapshot | Record input versions or snapshots, not just names |
| Half-lineage | Origins recorded but dependents unknown | Register outputs symmetrically for forward walks |
| Orphan manifests | Lineage stored far from the data it describes | Attach lineage to the dataset, not the wiki |
| Unqueried impact | Upstream changes merged without blast-radius checks | Make forward impact a pre-merge step |

## Security and Authority Boundary

Lineage is a map of how sensitive data moves: a complete graph shows exactly where restricted columns flow, so lineage stores must enforce the same access scope as the data they describe, and impact queries must not leak the existence or shape of restricted datasets to callers who cannot read them.

## Evidence

This skill is grounded in dated public implementation references:

1. The OpenLineage open standard for lineage (https://openlineage.io/).
2. Wikipedia's overview of data lineage (https://en.wikipedia.org/wiki/Data_lineage).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [ETL Pipeline](etl-pipeline.md) — the runs whose lineage gets recorded.
- [Data Joining](data-joining.md) — a transformation lineage must document.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
