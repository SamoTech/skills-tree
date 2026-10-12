---
title: "Health Check Endpoints"
category: 17-infrastructure
level: intermediate
stability: experimental
description: "Expose separate liveness and readiness endpoints with dependency-aware checks so orchestrators restart dead processes while temporarily unready ones simply receive no traffic."
added: "2026-10"
version: v1
related: ["kubernetes-deployment", "dependency-auditor"]
---

# Health Check Endpoints

Category: Infrastructure | Level: intermediate | Stability: experimental | Version: v1

## Description

Liveness answers "is this process broken"; readiness answers "can it serve right now". Conflating them produces the two classic outages: restarts during a dependency blip (the process is fine, the database is not) and traffic routed to instances that cannot serve. This skill splits the endpoints, makes readiness check real dependencies with real timeouts, and degrades to unready instead of dead — because a restart loop solves nothing a moment of patience would.

## When to Use

Use for any long-running service an orchestrator manages — web services, workers, agents behind a scheduler or platform that probes health.

Do not run side effects in probes; a health check that writes, rotates, or caches changes system state on a timer nobody scheduled.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `dependencies` | `map[name -> check]` | Yes | Dependency probes with timeouts for readiness |
| `probe_interval` | `duration` | Yes | How often the orchestrator checks |
| `failure_threshold` | `number` | Yes | Consecutive failures before action |
| `actions` | `map[state -> response]` | Yes | What liveness failure and unreadiness each do |

## Procedure

1. Implement two endpoints: liveness reports process health from in-process state only; readiness reports the ability to serve.
2. Make readiness walk the real dependencies with short timeouts; a dependency down means unready, not a restart.
3. Keep checks cheap and side-effect free — probing sits on the request path of every scheduling decision.
4. Tune probe intervals and thresholds above the noise floor; flapping thresholds convert blips into restart storms.
5. Degrade to unready under partial dependency failure, and report which dependency held the gate.
6. Log state transitions with the reason; restart and no-traffic events are only debuggable with that record.

## Outputs

| Output | Type | Description |
|---|---|---|
| `liveness` | `healthy | dead` | Process state from in-process evidence |
| `readiness` | `ready | unready` | Ability to serve, per dependency |
| `gate_reason` | `dependency | null` | Which dependency made the instance unready |

## Runnable Example

```python
def readiness(dependencies):
    """Unready on dependency failure; never dead for it."""
    gates = {}
    for name, check in dependencies.items():
        gates[name] = "ok" if check() else "down"
    unready = [name for name, state in gates.items() if state == "down"]
    return ("unready" if unready else "ready"), gates

deps = {"db": lambda: True, "cache": lambda: False, "queue": lambda: True}
state, gates = readiness(deps)
print(state)
print(gates)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| One endpoint for both states | Restart policy and traffic policy share one signal | Split liveness from readiness |
| Dependency blip restarts | Readiness failures routed to liveness | Degrade to unready, never to dead |
| Heavy probe checks | Health checks loading dependencies | Keep checks cheap, cached, and side-effect free |
| Restart storms | Thresholds tuned under the noise floor | Set thresholds above transient error rates |
| Silent unreadiness | Unready with no recorded reason | Log the gating dependency with every transition |

## Security and Authority Boundary

Health endpoints report process state; they do not validate data quality, security posture, or business correctness. Those belong to monitoring, security scanning, and SLOs — separate signals with separate owners.

## Evidence

This skill is grounded in dated public implementation references:

1. The Kubernetes documentation on liveness, readiness, and startup probes (https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).
2. Wikipedia's overview of heartbeat signals in computing (https://en.wikipedia.org/wiki/Heartbeat_%28computing%29).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Kubernetes Deployment](kubernetes-deployment.md) — the orchestrator side that consumes these probes.
- [Dependency Auditor](dependency-auditor.md) — dependency-level evidence beyond process state.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
