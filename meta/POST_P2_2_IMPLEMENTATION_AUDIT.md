

---

## Follow-up audit — Capability↔Adapter linkage symmetry — 2026-09-19

The Capability↔Implementation linkage symmetry correction is now merged. A fresh review of the remaining Capability relationships found that `Capability.adapters` is validated only as a list of existing Adapter IDs. The runtime does not verify that an Adapter listed by a Capability actually realizes an Implementation whose canonical Skill belongs to that Capability.

### Evidence reviewed

- `registry/universal_registry.json` contains `capability/code-quality.adapters = [adapter/code-reviewer-mcp]`.
- `adapter/code-reviewer-mcp` points to `implementation/code-reviewer-system`.
- `implementation/code-reviewer-system` points to canonical Skill `05-code/code-review`.
- `capability/code-quality.skills` contains `05-code/code-review`.
- `registry/runtime.py` currently rejects dangling Capability→Adapter IDs but does not validate this semantic chain.

The current audited record is internally consistent, so this is a missing invariant rather than a correction to production data.

### Selected vertical slice

Implement only Capability↔Adapter semantic linkage symmetry:

1. Runtime: require every Adapter listed by a Capability to resolve through its Implementation to a Skill listed by that Capability.
2. Regression: remove the Implementation's Skill from the Capability and verify registry initialization rejects the Capability→Adapter relationship.
3. Preserve all existing Adapter, Implementation, compatibility, graph, evidence, and MCP behavior.
4. Update `MEMORY_STATE.md` without assigning a numbered P2.3 roadmap item.

This is an audit-derived Phase 2 correctness slice. It adds no entities, providers, model claims, compatibility facts, or ecosystem assertions.
