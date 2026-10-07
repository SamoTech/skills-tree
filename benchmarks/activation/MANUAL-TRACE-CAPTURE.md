# Manual Activation Trace Capture (no Hermes required)

This path exists for operators who **do not have Hermes**. It still satisfies Issue #357 and `meta/skill-activation-observation.schema.json`.

## Rule

Record **only what you actually observed**. Do not invent skill selection or execution events. A missing skill is a valid negative observation (empty selection/execution for that run, or an honest false activation if the wrong skill fired).

## What counts as evidence

| Event | Meaning | How you know |
|-------|---------|--------------|
| `skill_selection` | The agent chose / opened / referenced a skill package | UI showed the skill, log named it, tool called `skill_view`, or the agent explicitly loaded that skill id |
| `skill_execution` | The skill was loaded/applied for the turn | Lifecycle “loaded”, package applied, or clear invocation of that skill’s procedure |

If you only saw selection but not load → record selection only.  
If nothing skill-related happened → still record the run with **empty** `events` only if your process requires a run row; otherwise omit the run and the case stays `NO_OBSERVATIONS` / `PARTIAL`.

Preferred skill ids (match dataset):
- `03-memory/rag`
- `05-code/code-review`
- `11-web/web-search`

## Cases (run each 3 times in a **fresh** session)

| case_id | Prompt | expected_skill | must_not_activate |
|---------|--------|----------------|-------------------|
| ACT-001 | I need to retrieve factual knowledge about this topic. | `03-memory/rag` | code-review, web-search |
| ACT-002 | Review this source code for correctness and maintainability. | `05-code/code-review` | rag, web-search |
| ACT-003 | Find current information on the web and cite the sources. | `11-web/web-search` | rag, code-review |
| ACT-004 | Explain how to review this code without actually reviewing or modifying it. | `05-code/code-review` | web-search, rag |

## Procedure

1. Pick any agent that can load Skills Tree / Agent Skills packages (Cursor, Claude Projects, Copilot, custom agent, etc.).
2. For each case, start a **new** session (no prior skill context).
3. Send the prompt exactly.
4. Note which skill(s) were selected and which were executed/loaded.
5. Fill one run object in `manual-observations.template.json` (copy to a working file).
6. Use unique `run_id` and `trace_id` for every session.
7. Evaluate:

```bash
python tools/run_skill_activation_benchmark.py \
  --dataset benchmarks/activation/skill-activation-v1.json \
  --observations path/to/your-observations.json \
  --output skill-activation-benchmark-result.json
```

## Output shape

Your file must match `meta/skill-activation-observation.schema.json`:

```json
{
  "schema_version": "1.0",
  "runs": [
    {
      "run_id": "manual-001",
      "case_id": "ACT-001",
      "trace_id": "session-2026-10-07-a",
      "events": [
        {"kind": "skill_selection", "skill_id": "03-memory/rag", "status": "observed"},
        {"kind": "skill_execution", "skill_id": "03-memory/rag", "status": "observed"}
      ]
    }
  ]
}
```

## Completeness

- **COMPLETE** requires 3 runs for each of ACT-001…ACT-004 (12 runs).
- **PARTIAL** is allowed and preferred over invented data.
- **NO_OBSERVATIONS** is the honest empty state.

## Evidence boundary

Manual capture is operator-attested observation of a real session. It is not a claim of production reliability or model accuracy beyond those sessions.
