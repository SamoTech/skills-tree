---
title: "API Version Pinning"
category: 07-tool-use
level: intermediate
stability: experimental
description: "Pin every external API to a specific, recorded version — and upgrade as a deliberate, tested change — so upstream evolution never rewrites behavior silently."
added: "2026-10"
version: v1
related: ["custom-api-wrapper", "openai-api"]
---

# API Version Pinning

Category: Tool Use | Level: intermediate | Stability: experimental | Version: v1

## Description

An unpinned API call is a bet on someone else's release calendar. This skill removes the bet: each external dependency is pinned to a concrete version in configuration, the pin is visible in code review, and upgrades happen as deliberate changes with a diff, a changelog read, and a test pass. Pinning goes further than a version number where the provider allows it — dated pins and versioned endpoints record the wire behavior the tests actually exercised.

## When to Use

Use for every external API integration that reaches production, and pin in configuration rather than in a dependency default.

Do not pin so hard that upgrades never happen; an integration left on an unsupported version is a slower, quieter failure mode.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `dependency` | `string` | Yes | The external API or SDK being integrated |
| `version_pin` | `string` | Yes | The concrete version recorded in configuration |
| `upgrade_policy` | `enum` | Yes | How and when deliberate upgrades are scheduled |

## Procedure

1. Record the pin in configuration, not in a lockfile default or a floating latest, so it appears in review and in audits.
2. Read the provider versioning model — dated pins, endpoint versions, deprecation windows — and record the model beside the pin.
3. Subscribe to change: watch the changelog or deprecation feed for the pinned version, and treat deprecation notices as scheduled work.
4. Upgrade deliberately: new pin, changelog diff read, integration tests run, and the change shipped as its own reviewable commit.
5. Roll back the pin, not the code, when an upgrade misbehaves — the pin is the smallest reversible unit.
6. Audit pins periodically: a pin on an unsupported version is a defect even while everything still works.

## Outputs

| Output | Type | Description |
|---|---|---|
| `pins` | `map` | Dependency to recorded version, with pinning model |
| `upgrade_log` | `list` | Deliberate upgrades with date, diff, and test evidence |

## Runnable Example

```python
CONFIG = {
    "payments_api": "2026-08-27",
    "maps_api": "v3",
}

def assert_pinned(dependency):
    pin = CONFIG.get(dependency)
    if pin is None:
        raise ValueError(f"unpinned dependency in integration: {dependency}")
    return pin

print(assert_pinned("payments_api"))
try:
    print(assert_pinned("ledger_api"))
except ValueError as err:
    print("rejected:", err)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Floating latest | The SDK default changes behavior on its own | Pin every integration in reviewed configuration |
| Missed deprecation | A deprecation window closed unwatched | Watch the changelog feed for the pinned version |
| Surprise upgrades | A dependency bump upgraded the wire behavior | Upgrade the pin in its own reviewed change |
| Unauditable pins | Nobody can list what versions run in production | Keep pins in config and audit them periodically |
| Unreviewable rollback | A bad upgrade reverted by editing code | Move the pin back, the smallest reversible unit |

## Security and Authority Boundary

Version pins interact with trust: upgrading an API client changes what is sent and to whom, so pin changes deserve security review like any dependency change, and a pin must never be loosened to make an unrelated integration problem go away.

## Evidence

This skill is grounded in dated public implementation references:

1. The Stripe documentation on API versioning and upgrades (https://docs.stripe.com/upgrades).
2. The twelve-factor app guidance on configuration (https://12factor.net/config).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Custom API Wrapper](custom-api-wrapper.md) — the adapter where pins and fallbacks live.
- [OpenAI API](openai-api.md) — a concrete provider whose versions get pinned.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
