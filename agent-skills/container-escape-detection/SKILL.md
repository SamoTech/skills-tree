---
name: container-escape-detection
description: Detect container breakout attempts by monitoring privileged operations, namespace and capability anomalies, and kernel interface abuse from inside and around the container runtime.
metadata:
  source: skills/14-security/container-escape-detection.md
  category: 14-security
  version: "v1"
---

# Container Escape Detection

Category: Security | Level: advanced | Stability: experimental | Version: v1

## Description

Container isolation is a soft boundary that attackers probe before they break it. The skill covers baseline of legitimate container behavior, then watching for the escape signatures: unexpected capability use, namespace and cgroup tampering, host filesystem mounts, kernel module loading, and device node access. Detections carry the workload identity so an event can be tied to a specific deployment, not just a host.

## When to Use

Use when containerized workloads, especially those running untrusted or third-party code, must be monitored for breakout attempts toward the host.

Do not assume the container image is trusted because it passed admission control. Escapes frequently come from exploited application code inside an approved image.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `runtime_events` | `table` | Yes | Syscall, capability, and namespace events from the container runtime |
| `container_baseline` | `object` | Yes | Normal behavior profile per workload: allowed syscalls and mounts |
| `scope` | `enum` | No | `per-node` (default) or `fleet` for cross-node correlation |

## Procedure

1. Establish the per-workload baseline: syscalls, capabilities, mounts, and device access in normal operation.
2. Stream runtime events and attribute each to a workload identity and node.
3. Flag privileged deviations: capability escalation, namespace switching, and host path mounts.
4. Correlate across nodes for lateral signatures when fleet scope is enabled.
5. Score detections by proximity to the host boundary: what a successful escape would reach.
6. Emit detections with the event chain, workload identity, and containment recommendation.

## Outputs

| Output | Type | Description |
|---|---|---|
| `detections` | `array` | Escape attempts with event chains and proximity scoring |
| `baseline_violations` | `table` | Per-workload deviations from normal behavior |
| `containment_actions` | `list` | Suggested node and workload isolation steps |

## Runnable Example

```python
def score_escape_chain(events):
    """events: [(capability, target)] observed in one workload"""
    weights = {"cap_sys_admin": 5, "mount_host_path": 4, "load_kernel_module": 5,
               "access_device_node": 4, "namespace_switch": 2}
    score = 0
    for cap, _ in events:
        score += weights.get(cap, 1)
    verdict = "escape-in-progress" if score >= 8 else ("suspicious" if score >= 4 else "normal")
    return {"score": score, "verdict": verdict}

print(score_escape_chain([("cap_sys_admin", "node1"), ("mount_host_path", "node1")]))
print(score_escape_chain([("namespace_switch", "node2")]))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Privileged-legitimate confusion | Sidecar containers legally use high capabilities | Baseline per workload, not per node |
| Kernel-level events missed | Runtime instrumentation too shallow | Instrument at the syscall or eBPF layer |
| Escape already complete | Detection tuned only for attempts | Watch for post-escape signatures such as host process spawning |
| Fleet-wide blind spot | Per-node alerts miss lateral movement | Correlate at fleet scope for shared tactics |
| Alert fatigue | No scoring, every anomaly equal | Score by proximity to the host boundary |

## Security and Authority Boundary

Escape detections imply compromised workloads. Treat them as live incidents: preserve forensic evidence, isolate nodes before investigation, and do not trust container-local logs after an escape is confirmed, because the attacker controls that plane.

## Evidence

This skill is grounded in dated public implementation references:

1. The Falco runtime security project for container and syscall monitoring (https://github.com/falcosecurity/falco).
2. The Trivy vulnerability and misconfiguration scanner for containers (https://github.com/aquasecurity/trivy).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Sandboxed Execution](sandboxed-execution.md) — the isolation layer whose boundary this skill watches.
- [Incident Response](../16-domain-specific/incident-response.md) — the escalation path when an escape is confirmed.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
